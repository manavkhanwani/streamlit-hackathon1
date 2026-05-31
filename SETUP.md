# 🚀 SETUP.md — Running CivicLens Locally

## Prerequisites

- Python 3.9 or higher
- A Google Cloud account with billing enabled
- Git

---

## Step 1 — Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/civiclens.git
cd civiclens
```

---

## Step 2 — Create a Virtual Environment

```bash
python -m venv venv

# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

---

## Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4 — Set Up API Keys

### Get your API keys:

**Google Gemini API:**
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Click **Get API key** → Create API key
3. Copy the key

**Google Maps API:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable **Maps JavaScript API** and **Geocoding API**
3. Create credentials → API Key
4. Copy the key

### Configure your environment:

```bash
# Copy the example env file
cp .env.example .env
```

Open `.env` and fill in your keys:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

---

## Step 5 — Run the App

```bash
streamlit run app.py
```

The app will open at **http://localhost:8501**

---

## Pages

| Page | URL | Description |
|------|-----|-------------|
| Citizen Portal | `/?page=citizen` | Submit a new complaint |
| Government Dashboard | `/?page=dashboard` | View & manage all complaints |
| Track Complaint | `/?page=track` | Check status of a complaint |

---

## Troubleshooting

**`ModuleNotFoundError`** — Make sure your virtual environment is activated and you ran `pip install -r requirements.txt`

**`GEMINI_API_KEY not set`** — Ensure your `.env` file exists and has the correct key. Restart the terminal after editing.

**Map not loading** — Check that **Maps JavaScript API** is enabled in Google Cloud Console and your API key has no domain restrictions set for local development.

**Port already in use** — Run on a different port: `streamlit run app.py --server.port 8502`

---

## Demo Mode

If you don't have API keys yet, the app loads sample data from `assets/sample_data.json` and shows a placeholder map. Gemini features will be disabled but the UI is fully browsable.
