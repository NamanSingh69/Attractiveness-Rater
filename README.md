# Attractiveness Rater (AURA) — Technical Report

## Architecture Overview

| Component | Technology |
|-----------|-----------|
| Frontend | Vanilla HTML + JavaScript |
| Styling | Tailwind CSS (CDN) |
| Charts | Chart.js (CDN) |
| AI | Google Generative AI (Gemini API, client-side) |
| Font | Google Fonts (Inter) |
| Deployment | Vercel (static) |

### Architecture
```
[User Browser] → [AURA UI (Single HTML File)]
                       ↓ (Client-side JS)
              [Gemini API (generativelanguage.googleapis.com)]
                       ↓
              [Facial Analysis Results + Chart.js Visualization]
```

## Study Findings

- **Type**: Single-file web application (`App.html` — 742 lines)
- **Functionality**: Uploads a face photo, sends to Gemini API for analysis, displays attractiveness scores with radar chart
- **Zero Backend**: All API calls happen in the user's browser — no server needed
- **API Key**: User provides their own Gemini API key at runtime
- **Deployment**: ✅ Deployable as a static site on Vercel (see `DEPLOY.md`)

## Local Setup Guide

```bash
# No setup needed — just open the file in a browser
cd "Attractiveness Rater"
start App.html          # Windows
# open App.html         # macOS
# xdg-open App.html    # Linux
```

## 🔑 Getting Your Free Gemini API Key

1. Visit **[Google AI Studio](https://aistudio.google.com/app/apikey)**
2. Sign in with your Google account — **completely free**, no credit card
3. Click **"Create API Key"** → Copy the key
4. Paste into the app's API key input field

### Model Fallback
The app currently calls Gemini directly from JavaScript. For resilience, you can implement client-side fallback:
```javascript
const MODEL_CASCADE = [
gemini-3.1-pro-preview` → `gemini-3-flash-preview` → `gemini-3.1-flash-lite-preview`
];
```
