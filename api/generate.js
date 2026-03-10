let g_cascadeCache = null;
let g_cacheTime = 0;

function scoreModel(name) {
    name = name.toLowerCase().replace("models/", "");
    let score = 0;
    if (name.includes("flash-lite")) score = 25;
    else if (name.includes("pro")) score = 100;
    else if (name.includes("lite")) score = 25;
    else if (name.includes("flash")) score = 50;
    else score = 10;

    let versionScore = 1.0;
    const vMatch = name.match(/(\d+)\.(\d+)/);
    if (vMatch) {
        versionScore = parseInt(vMatch[1]) + (parseInt(vMatch[2]) * 0.1);
    } else {
        const genMatch = name.match(/gemini-(\d+)-/);
        if (genMatch) versionScore = parseFloat(genMatch[1]);
        else if (name.includes("latest")) versionScore = 2.5;
    }
    score *= versionScore;
    if (name.includes("preview")) score *= 1.05;
    if (name.includes("exp")) score *= 0.85;
    return score;
}

async function getModelCascade(apiKey) {
    if (g_cascadeCache && (Date.now() - g_cacheTime < 3600000)) {
        return g_cascadeCache;
    }
    try {
        const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models?key=${apiKey}`);
        if (!res.ok) throw new Error("Fetch failed");
        const data = await res.json();
        const models = data.models
            .filter(m => m.supportedGenerationMethods?.includes("generateContent"))
            .map(m => m.name.replace("models/", ""));

        const sorted = models.sort((a, b) => scoreModel(b) - scoreModel(a));
        const pros = sorted.filter(m => m.includes("pro"));
        const flashLites = sorted.filter(m => m.includes("flash-lite"));
        const flashes = sorted.filter(m => m.includes("flash") && !m.includes("lite"));

        // Static generation project → 3.1 first
        const bestPro = pros[0] || 'gemini-3.1-pro-preview';
        const bestFlashLite = flashLites[0] || 'gemini-3.1-flash-lite-preview';
        const fallbackPro = pros.length > 1 ? pros[1] : 'gemini-2.5-pro';
        const fallbackFlash = flashes[0] || 'gemini-2.5-flash';

        g_cascadeCache = [bestPro, bestFlashLite, fallbackPro, fallbackFlash];
        g_cacheTime = Date.now();
        return g_cascadeCache;
    } catch (e) {
        console.error(e);
        return ['gemini-3.1-pro-preview', 'gemini-3.1-flash-lite-preview', 'gemini-2.5-pro', 'gemini-2.5-flash'];
    }
}

export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    const { model = 'gemini-3.1-pro-preview', contents, systemInstruction, generationConfig, safetySettings } = req.body;

    const userApiKey = req.headers['x-gemini-api-key'];
    const apiKey = userApiKey || process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY;

    if (!apiKey) {
        return res.status(500).json({ error: 'Server configuration error: Missing API Key' });
    }

    const MODEL_CASCADE = await getModelCascade(apiKey);

    let currentModelIndex = MODEL_CASCADE.indexOf(model);
    if (currentModelIndex === -1) currentModelIndex = 0;

    let lastError = null;

    for (let i = currentModelIndex; i < MODEL_CASCADE.length; i++) {
        const currentModel = MODEL_CASCADE[i];
        try {
            const url = `https://generativelanguage.googleapis.com/v1beta/models/${currentModel}:generateContent?key=${apiKey}`;

            const payload = { contents };
            if (systemInstruction) payload.systemInstruction = systemInstruction;
            if (generationConfig) payload.generationConfig = generationConfig;
            if (safetySettings) payload.safetySettings = safetySettings;

            // Enable search grounding for 2.5 models
            if (currentModel.startsWith('gemini-2.5')) {
                payload.tools = [{ google_search: {} }];
            }

            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                lastError = { status: response.status, data: errorData };

                if (response.status === 429 || response.status === 503 || response.status === 500) {
                    console.warn(`Model ${currentModel} failed with ${response.status}. Falling back...`);
                    continue;
                }
                return res.status(response.status).json(errorData);
            }

            const data = await response.json();
            data._model_used = currentModel;
            return res.status(200).json(data);
        } catch (error) {
            console.error(`Fetch error with ${currentModel}:`, error);
            lastError = { status: 500, error: error.message };
            continue;
        }
    }

    return res.status(lastError?.status || 500).json(lastError?.data || { error: 'All models in cascade failed.', retryAfterSeconds: 60 });
}
