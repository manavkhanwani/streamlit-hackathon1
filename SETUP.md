# CivicLens — Setup Guide

## Prerequisites

| Requirement | Version | Notes |
|------------|---------|-------|
| Python | 3.9+ | 3.10+ recommended |
| pip | Latest | For installing dependencies |
| Git | Any recent | For cloning the repository |
| Google Cloud account | — | Required for full mode (API keys) |

---

## Local Setup (Step-by-Step)

### Step 1 — Clone and Enter Directory

```bash
git clone https://github.com/YOUR_ORG/civiclens.git
cd civiclens
```

### Step 2 — Create and Activate Virtual Environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Configure API Keys (Full Mode Only)

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

**Skip this step to run in Demo Mode.**

### Step 5 — Run the App

```bash
streamlit run app.py
```

The app opens at **http://localhost:8501**

If port 8501 is in use:

```bash
streamlit run app.py --server.port 8502
```

---

## Getting API Keys

### Google Gemini API

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Click **Get API key** → **Create API key**
3. Copy the key and add it to `.env` as `GEMINI_API_KEY`

### Google Maps API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable:
   - **Maps JavaScript API**
   - **Geocoding API**
3. Create credentials → **API Key**
4. Add it to `.env` as `GOOGLE_MAPS_API_KEY`

---

## Streamlit Cloud Deployment

1. Push repository to GitHub
2. Log in to [Streamlit Cloud](https://streamlit.io/cloud) → **New app**
3. Connect your repository; set **Main file path:** `app.py`
4. In **Advanced settings → Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your_key_here"
   GOOGLE_MAPS_API_KEY = "your_key_here"
   ```
5. Click **Deploy**

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError` | Activate venv and run `pip install -r requirements.txt` |
| Map not loading | Enable Maps JavaScript API in GCP; remove domain restrictions for localhost |
| `Port 8501 already in use` | Use `--server.port 8502` or kill the existing process |
| Heatmap shows placeholder | Set `GOOGLE_MAPS_API_KEY` in `.env` |
| Data lost after restart | Expected in v1.0 — session state is ephemeral |
| Geocoding returns city center | Address too vague, or Maps key not set |
| `json.JSONDecodeError` from Gemini | App catches this and uses fallback — no action needed |
