# CivicLens

> **"See the City Clearly"** — AI-powered civic complaint platform for Hyderabad & Telangana

---

## What is CivicLens?

CivicLens is a unified, AI-powered civic complaint platform where citizens of Hyderabad can report issues in text or photo format and government officials can view and act on them from a single dashboard.

**Team:** BogControls (Manav · Aniket · Aryan)  
**Hackathon:** CivicTech Hackathon — Hyderabad City / Telangana State  
**Stack:** Python · Streamlit · Google Gemini 1.5 Flash · Google Maps API

---

## Quick Start

```bash
# Clone and enter the directory
git clone https://github.com/YOUR_ORG/civiclens.git
cd civiclens

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Run (Demo Mode — no API keys needed)
streamlit run app.py
```

The app opens at **http://localhost:8501**

---

## Features

- **Submit complaints** in English or Telugu — text, with optional photo
- **AI categorization** (Gemini 1.5 Flash) — auto-assigns category, priority, department, and one-line summary
- **Geo-tagging** — plain-text location is geocoded to lat/lng via Google Maps
- **Government Dashboard** — KPI metrics, complaint heatmap, filterable list, status update
- **Complaint Tracking** — citizens track their `CL-XXXXXX` ID through Open → In Progress → Resolved
- **Demo Mode** — works fully without any API keys (5 seed complaints pre-loaded)

---

## Project Structure

```
civiclens/
├── app.py                      # Entry point: page config + sidebar routing
├── _pages/
│   ├── __init__.py
│   ├── citizen_portal.py       # Complaint submission page
│   ├── dashboard.py            # Government dashboard page
│   └── track.py                # Complaint tracking page
├── utils/
│   ├── __init__.py
│   ├── gemini_helper.py        # Gemini API client + analyze_complaint()
│   ├── maps_helper.py          # Maps client + geocode_address() + build_heatmap_html()
│   └── data_store.py           # Session-state CRUD + stats
├── assets/
│   └── sample_data.json        # 5 seed complaints for demo mode
├── requirements.txt
├── .env.example
├── README.md
├── SETUP.md
├── AGENTS.md
├── POC.md
├── CONTRIBUTING.md
└── USER_MANUAL.md
```

---

## Configuration

Copy `.env.example` to `.env` and fill in your keys:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

Leave empty or as placeholders to run in **Demo Mode**.

---

## Demo Mode

When no API keys are set:
- AI analysis falls back to rule-based categorization (`Roads / Medium`)
- Geocoding falls back to Hyderabad city center coordinates (17.3850, 78.4867)
- Heatmap shows a placeholder message
- All 5 sample complaints are pre-loaded and fully interactive

---

## Supported Languages

- English ✅
- Telugu ✅ (Gemini handles Telugu input natively)

---

## Known Limitations (v1.0)

- Data is stored in-memory (`st.session_state`) — lost on server restart
- No user authentication
- Shared state across all browser sessions on the same server
- No duplicate complaint detection
- No persistent notifications to citizens

See `TECH_SPEC.md` and `DEPLOY_SPEC.md` in the spec kit for full technical details.
