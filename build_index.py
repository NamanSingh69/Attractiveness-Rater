import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('<script src="gemini-client.js"></script>\n', '')
content = content.replace('<script src="gemini-client.js"></script>\r\n', '')
content = content.replace('    <script src="gemini-client.js"></script>', '')

content = content.replace('py-2 text-sm font-bold text-cyan-400', 'py-3 text-sm font-bold text-cyan-400 min-h-[44px]')
content = content.replace('py-2 text-sm font-bold text-gray-500', 'py-3 text-sm font-bold text-gray-500 min-h-[44px]')
content = content.replace('px-4 py-2 bg-gray-800', 'px-4 py-2 bg-gray-800 min-h-[44px]')
content = content.replace('px-6 py-2 bg-cyan-600', 'px-6 py-2 bg-cyan-600 min-h-[44px]')

loader_orig_regex = re.compile(r'<div id=\"loader\"[^>]*>\s*<div class=\"text-center z-10\">.*?<div class=\"scanner-line absolute top-0\"></div>\s*</div>', re.DOTALL)

loader_new = '''<div id="loader" class="hidden-anim w-full glass-panel rounded-xl p-6 sm:p-8 flex flex-col md:flex-row gap-8 relative overflow-hidden">
            <div class="w-full md:w-1/3 flex flex-col items-center gap-4">
                <div class="skeleton w-full aspect-square rounded-xl"></div>
            </div>
            <div class="flex-1 flex flex-col gap-6 w-full">
                <div class="flex justify-between items-start">
                    <div>
                        <div class="skeleton w-48 h-6 mb-2"></div>
                        <div class="skeleton w-32 h-4"></div>
                    </div>
                    <div class="skeleton w-20 h-20 rounded-full"></div>
                </div>
                <div class="skeleton w-full h-4"></div>
                <div class="skeleton w-full h-32"></div>
                <div class="skeleton w-full h-12 rounded-lg"></div>
            </div>
            <div class="scanner-line absolute top-0 left-0 w-full hidden"></div>
        </div>'''

content = loader_orig_regex.sub(loader_new, content)

content = content.replace('alert("Camera access denied or unavailable.");', 'showToast("Camera access denied or unavailable.", "error");')
content = content.replace('alert("Please enter a Google Gemini API Key in the settings panel (bottom right).");', 'showToast("Please enter a Google Gemini API Key in the settings panel.", "error");')
content = content.replace('alert("Please upload at least one image.");', 'showToast("Please upload at least one image.", "error");')
content = content.replace('alert("Analysis failed: " + error.message);', 'showToast("Analysis failed: " + error.message, "error");')

content = content.replace('displayResults(result);', 'displayResults(result);\n                showToast("Biometric analysis completed successfully.", "success");')

css = '''        /* Skeleton Shimmer */
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

        /* Toast Notifications */
        .toast {
            position: fixed;
            bottom: 80px;
            right: -100%;
            transition: right 0.4s ease-in-out;
            padding: 16px 24px;
            border-radius: 8px;
            color: white;
            font-family: 'JetBrains Mono', monospace;
            font-size: 14px;
            z-index: 10000;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
            max-width: 90vw;
        }
        .toast.show {
            right: 20px;
        }
        .toast-success { border-left: 4px solid #10b981; background: rgba(16, 185, 129, 0.1); backdrop-filter: blur(12px); border-top: 1px solid rgba(16,185,129,0.2); border-right: 1px solid rgba(16,185,129,0.2); border-bottom: 1px solid rgba(16,185,129,0.2); }
        .toast-error { border-left: 4px solid #ef4444; background: rgba(239, 68, 68, 0.1); backdrop-filter: blur(12px); border-top: 1px solid rgba(239,68,68,0.2); border-right: 1px solid rgba(239,68,68,0.2); border-bottom: 1px solid rgba(239,68,68,0.2); }
        .toast-info { border-left: 4px solid #3b82f6; background: rgba(59, 130, 246, 0.1); backdrop-filter: blur(12px); border-top: 1px solid rgba(59,130,246,0.2); border-right: 1px solid rgba(59,130,246,0.2); border-bottom: 1px solid rgba(59,130,246,0.2); }
    </style>'''

content = content.replace('    </style>', css)

js_end = '''        }

        // --- Toast System ---
        function showToast(message, type = 'info') {
            const toast = document.createElement('div');
            toast.className = `toast toast-${type}`;
            toast.innerText = message;
            document.body.appendChild(toast);
            
            // Trigger reflow
            void toast.offsetWidth;
            
            toast.classList.add('show');
            
            setTimeout(() => {
                toast.classList.remove('show');
                setTimeout(() => toast.remove(), 400);
            }, 4000);
        }
    </script>
    <script>window.GEMINI_CONFIG = { needsRealTimeData: false };</script>
    <script src="gemini-client.js"></script>
</body>'''

content = re.sub(r'        }\s*</script>\s*</body>', js_end, content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
