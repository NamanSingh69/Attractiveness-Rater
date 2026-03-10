# Attractiveness Rater — Complete Standalone Agent Prompt

## Project Identity

| Field | Value |
|-------|-------|
| **Project Folder** | `C:\Users\namsi\Desktop\Projects\Attractiveness Rater` |
| **Tech Stack** | Vanilla HTML/CSS/JS frontend + Python backend (Vercel Serverless Functions) |
| **Vercel URL** | https://attractiveness-rater.vercel.app/ |
| **GitHub Repo** | `NamanSingh69/Attractiveness-Rater` (create if not exists) |
| **Vercel Env Vars** | `GEMINI_API_KEY` is set |

### Key Files
- `index.html` — Main HTML page ("AURA v1.0 — Biometric Evaluation"), cyberpunk/neon theme
- `gemini-client.js` — Should be v2 (28KB). This is the shared Gemini client that provides Pro/Fast toggle, rate limit counter, and model cascade. If the file is missing or under 28KB, copy it from the reference implementation (see Shared Infrastructure below)
- `api/` — Vercel Serverless Functions directory for proxying Gemini API calls
- `vercel.json` — Route configuration

---

## Shared Infrastructure Context (CRITICAL — Read Before Making Changes)

This project is part of a 16-project portfolio. Previous work sessions established shared patterns you MUST follow:

### Design System — The "UX Mandate"
All projects must implement **4 core UI states**:
1. **Loading** → Animated skeleton screen placeholders (shimmer effect, NOT static "Loading..." text)
2. **Success** → Toast notifications (CSS-animated, green, auto-dismiss after 4s)
3. **Empty** → Beautiful null states with friendly messaging and SVG/icon graphics
4. **Error** → Red toast notifications with actionable recovery messages (e.g., "Try again" button)

**NEVER use native `alert()`, `confirm()`, or `prompt()` dialogs. Replace ALL of them with toast notifications.**

### Gemini Client (for Python/Vanilla JS projects)
The standard client is `gemini-client.js` v2 (28KB file). It provides:
- **Pro/Fast Toggle**: A floating `⚡ PRO / 🚀 FAST` pill button (bottom-right corner) that persists selection in `localStorage` key `gemini_mode` (value: `"pro"` or `"fast"`)
- **Rate Limit Counter**: Visual `Requests: X/15 remaining` badge that decrements on each API call and resets after 60 seconds
- **Model Cascade**: Automatic fallback chain on 429/503 errors (Pro → Flash)
- **Auto-inject**: Call `window.gemini.injectUI()` or it auto-injects on load

### Smart Model Cascade (March 2026)
**Primary (Free Preview):** `gemini-3.1-pro-preview` → `gemini-3-flash-preview` → `gemini-3.1-flash-lite-preview`
**Fallback (Free Stable):** `gemini-2.5-pro` → `gemini-2.5-flash` → `gemini-2.5-flash-lite`

**Note:** `gemini-2.0-flash` and `gemini-2.0-flash-lite` were **deprecated March 3, 2026** — do NOT use.
Pro/Fast toggle maps to: Pro → first model in cascade, Fast → second model.
For grounding/Google Search tasks (live data): use `gemini-2.5-pro` or `gemini-2.5-flash` (5K free grounded queries/month).

### Security Rules
- **NEVER** hardcode API keys in client-side JavaScript
- Use Vercel Serverless Functions (`api/` directory) to proxy Gemini API calls using `process.env.GEMINI_API_KEY`
- `.gitignore` MUST cover: `.env*`, `node_modules/`, `.vercel/`, `dist/`, `__pycache__/`

### Mobile Responsiveness (NEW — Required for ALL projects)
- `<meta name="viewport" content="width=device-width, initial-scale=1.0">` must be in `<head>`
- All layouts must work at 375px width (iPhone SE) through 1920px (desktop)
- Use CSS flexbox/grid with `flex-wrap`, percentage widths, `max-width`, and `@media` queries
- Touch targets must be at least 44×44px
- Font sizes must be readable on mobile (minimum 14px body text)
- No horizontal scrolling on any viewport size

### Accessibility
- ARIA labels on all interactive elements
- Keyboard navigability (Tab order, Enter/Space activation)
- WCAG AA contrast ratios (4.5:1 for normal text, 3:1 for large text)

---

## Current Live State (Verified March 10, 2026)

| Feature | Status | Details |
|---------|--------|---------|
| Site loads | ✅ 200 OK | Cyberpunk "AURA v1.0" themed UI |
| Login wall | ✅ None | No login required |
| Pro/Fast Toggle | ❌ NOT VISIBLE | Despite `gemini-client.js` existing in project, the toggle is not rendering in the live deployment |
| Rate Limit Counter | ❌ NOT VISIBLE | Same issue — client may not be injecting |
| Empty State | ✅ Present | "Upload Subject Images" area with drag-drop zone |
| Skeleton Loaders | ⚠️ Partially | Has `id="loader"` with "PROCESSING BIOMETRICS..." text but needs animated shimmer |
| Toasts | ❌ Missing | Uses `alert()` for errors like "Please upload at least one image" |
| Mobile Responsive | ✅ Yes | Layout stacks correctly at 375px width |
| Console Errors | ⚠️ Check | favicon.ico 404 warning |

---

## Required Changes

### 1. Fix gemini-client.js Integration (HIGH PRIORITY)
The `gemini-client.js` file should be v2 (28KB). Verify:
```bash
# Check file size — must be >= 28000 bytes
Get-Item "gemini-client.js" | Select-Object Name, Length
```
- If the file is missing or smaller than 28KB, it needs to be the full v2 version with Pro/Fast toggle, rate limit counter, and model cascade built in.
- Ensure `index.html` has `<script src="gemini-client.js"></script>` before the closing `</body>` tag.
- Add `window.GEMINI_CONFIG = { needsRealTimeData: false }` before the script tag.
- Verify `window.gemini.injectUI()` is called at page load (or the script auto-injects).
- After fixing, the ⚡ PRO / 🚀 FAST floating toggle and rate limit badge should appear automatically.

### 2. Replace ALL alert() with Toast Notifications
Search the entire codebase for `alert(`:
```bash
Select-String -Path "*.js","*.html" -Pattern "alert\(" -Recurse
```
Replace every instance with a toast notification system:
- Create a `showToast(message, type)` function where type is `'success'`, `'error'`, or `'info'`
- Toast CSS: Fixed position bottom-right, slides-in from right, auto-dismisses after 4 seconds
- Toast colors: Success = `#10b981` (green), Error = `#ef4444` (red), Info = `#3b82f6` (blue)
- Apply to: "Please upload at least one image", API errors, successful analysis completion

### 3. Upgrade Skeleton Loaders
The existing `id="loader"` with "PROCESSING BIOMETRICS..." static text needs upgrading:
- Replace static text with animated shimmer skeleton placeholders
- Skeleton should mimic the shape of the results output (score bars, text lines)
- Use CSS keyframe animation for the shimmer effect:
```css
@keyframes shimmer {
  0% { background-position: -200px 0; }
  100% { background-position: calc(200px + 100%) 0; }
}
.skeleton {
  background: linear-gradient(90deg, #1a1a2e 25%, #16213e 50%, #1a1a2e 75%);
  background-size: 200px 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
}
```
- Colors should match the cyberpunk/neon dark theme

### 4. Server-Side API Key Proxy
- Verify the `api/` directory contains a serverless function that reads `process.env.GEMINI_API_KEY`
- The client-side JS must call `/api/analyze` (or similar), NOT directly call `generativelanguage.googleapis.com`
- If the API route doesn't exist, create `api/analyze.js`:
```javascript
export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) return res.status(500).json({ error: 'API key not configured' });
  // Proxy the request to Gemini API
  const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${req.body.model || 'gemini-3.1-flash-lite-preview'}:generateContent?key=${apiKey}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(req.body.payload)
  });
  const data = await response.json();
  res.status(response.status).json(data);
}
```

### 5. Mobile Responsiveness Hardening
While the site already stacks at mobile widths, verify:
- The image upload zone is usable on touch devices (file input triggers correctly)
- Results cards don't overflow horizontally
- The Pro/Fast toggle and rate limit badge don't overlap on small screens
- Touch targets are at least 44×44px (especially the "Initiate Analysis" button)

### 6. GitHub & Deployment
- Create GitHub repo `Attractiveness-Rater` under `NamanSingh69` if not exists
- Ensure `.gitignore` covers `.env*`, `node_modules/`, `.vercel/`, `dist/`, `__pycache__/`
- Push all code: `git add -A && git commit -m "feat: gemini client v2, toast system, skeleton loaders, mobile hardening" && git push`
- Redeploy: `npx vercel --prod --yes`
- Verify at https://attractiveness-rater.vercel.app/

---

## Verification Checklist
1. ✅ Open https://attractiveness-rater.vercel.app/ — page loads without errors
2. ✅ The ⚡ PRO / 🚀 FAST floating toggle is visible (bottom-right corner)
3. ✅ Click the toggle — confirm it switches modes and `localStorage.gemini_mode` updates
4. ✅ Rate limit counter is visible (e.g., `Requests: 15/15 remaining`)
5. ✅ Upload an image → click "Initiate Analysis" → animated skeleton loader appears (shimmer, not static text)
6. ✅ Analysis completes → success toast slides in (green, auto-dismisses)
7. ✅ Trigger an error (e.g., submit without image) → error toast appears (red) — NO native `alert()`
8. ✅ Resize browser to 375px width → layout is fully usable, no horizontal scroll
9. ✅ Open DevTools console → zero JavaScript errors
10. ✅ Check Network tab → no API calls go directly to `generativelanguage.googleapis.com` (all proxied through `/api/`)
