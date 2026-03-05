# Vercel Deployment Guide — Attractiveness Rater (AURA)

## Pre-Deployment Checklist

| Item | Status |
|------|--------|
| Type | Static HTML (single file) |
| Build step | None required |
| Framework | None (vanilla HTML/JS) |
| Dependencies | CDN-loaded (Tailwind, Chart.js, Inter font) |

## Vercel Dashboard Environment Variables

> **None required.** The Gemini API key is provided by the user at runtime via the UI input field and sent directly to the Gemini API from the client browser.

## Deployment Steps

### Option 1: Vercel CLI
```bash
cd "Attractiveness Rater"

# Rename to index.html for Vercel auto-detection
copy App.html index.html

# Deploy
npx vercel --prod
```

### Option 2: Drag & Drop
1. Go to [vercel.com/new](https://vercel.com/new)
2. Drag the `Attractiveness Rater` folder onto the page
3. Vercel will auto-detect it as a static site

## Architecture

```
Browser → [AURA UI (Vercel CDN)] → [Gemini API (Google Cloud)]
                                        ↑
                                  User-provided API key
```

**No backend needed.** All inference happens via direct client-side calls to `generativelanguage.googleapis.com`.

## Free Tier Limits

| Resource | Vercel Free Tier | This Project |
|----------|-----------------|--------------|
| Bandwidth | 100 GB/month | ~40 KB/visit (HTML only) |
| Build | N/A | Static file, no build |
| Functions | N/A | No serverless functions |

## Security Note

⚠️ The user's Gemini API key is transmitted directly from the browser to Google's API. It is **not** stored server-side. Users should be advised to use a key with appropriate quotas and restrictions.
