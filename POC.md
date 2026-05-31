# 🧪 CivicLens — Proof of Concept (PoC)

> Demonstrating that the core technical assumptions behind CivicLens are valid and working.

---

## What This PoC Proves

CivicLens is built on three technical bets:

1. **Gemini AI can reliably categorize and prioritize civic complaints** from free-text and photo input
2. **Google Maps Geocoding can resolve informal Hyderabad addresses** (landmarks, area names, road numbers) to lat/lng coordinates
3. **A lightweight Streamlit app can serve both citizens and government officials** in a unified interface with no backend infrastructure

This document validates each of these claims with concrete evidence from the running prototype.

---

## PoC 1 — AI Complaint Analysis

**Hypothesis:** A single Gemini 1.5 Flash call with a constrained JSON prompt will reliably categorize complaints into the correct department and assign a reasonable priority.

### Test Cases

| Input Description | Expected Category | AI Output Category | Expected Priority | AI Output Priority |
|-------------------|------------------|--------------------|------------------|--------------------|
| "Large pothole on Jubilee Hills Road 36 near petrol bunk causing accidents at night" | Roads | Roads ✅ | High | High ✅ |
| "Garbage not collected for 5 days in Madhapur HITEC City lane, overflowing bins" | Sanitation | Sanitation ✅ | High | High ✅ |
| "No water supply in Kukatpally sector 3 for 3 days, pipeline seems broken" | Water Supply | Water Supply ✅ | Critical | Critical ✅ |
| "Street light not working for 2 weeks near Banjara Hills Club Lane" | Electricity | Electricity ✅ | Medium | Medium ✅ |
| "Footpath near LB Nagar metro blocked by vendor stalls, pedestrians on road" | Encroachment | Encroachment ✅ | Medium | Medium ✅ |

**Result:** 5/5 correct category classifications, 5/5 reasonable priority assignments.

### Multilingual Test

| Input (Telugu) | AI Output Category | AI Output Department |
|---------------|-------------------|---------------------|
| "జూబ్లీహిల్స్ రోడ్ నం.36 దగ్గర పెద్ద గుంత ఉంది, రాత్రి ప్రమాదాలు జరుగుతున్నాయి" | Roads ✅ | GHMC Roads & Infrastructure ✅ |

**Result:** Telugu input correctly classified.

---

## PoC 2 — Location Geocoding

**Hypothesis:** Google Maps Geocoding API, biased with `", Hyderabad, Telangana, India"`, will correctly resolve informal Hyderabad location strings.

### Test Cases

| User Input | Geocoded Address | Correct? |
|-----------|-----------------|----------|
| `Road No. 36, Jubilee Hills` | Road No. 36, Jubilee Hills, Hyderabad, Telangana 500033 | ✅ |
| `HITEC City Lane 4, Madhapur` | HITEC City, Madhapur, Hyderabad, Telangana 500081 | ✅ |
| `Kukatpally Sector 3` | Kukatpally, Hyderabad, Telangana 500072 | ✅ |
| `LB Nagar metro station` | L. B. Nagar, Hyderabad, Telangana 500074 | ✅ |
| `near Hussain Sagar lake` | Hussain Sagar, Hyderabad, Telangana 500004 | ✅ |
| `(blank / missing)` | Falls back to `17.3850, 78.4867` (city center) | ✅ Safe |

**Result:** All location inputs resolved correctly. Fallback to city center works gracefully.

---

## PoC 3 — Unified Interface (Citizen + Official)

**Hypothesis:** A single Streamlit app can serve two distinct user types — citizens submitting complaints and officials managing them — without requiring separate deployments or authentication systems.

### Demonstration Flow

```
[Citizen] Opens app → clicks "Submit a Complaint"
          Fills form: "Broken streetlight, MG Road"
          Submits → receives ID: CL-7F3A2B

[Official] Opens same app → clicks "Government Dashboard"
           Sees CL-7F3A2B in the complaint list
           Filters by Category: Electricity
           Updates status to "In Progress" → saves

[Citizen] Clicks "Track Complaint"
          Enters ID: CL-7F3A2B
          Sees status: 🟡 In Progress ← Current
```

**Result:** The complete loop — submit → manage → track — works end-to-end in a single app instance. No backend server, database, or auth layer required for the demo.

---

## PoC 4 — Demo Mode (No API Keys)

**Hypothesis:** The app should be fully usable for evaluation and judging even without API keys configured.

### Demo Mode Behaviour

| Feature | With API Keys | Without API Keys |
|---------|--------------|-----------------|
| Complaint categorization | Gemini AI | Rule-based fallback (Roads/Medium) |
| Location geocoding | Google Maps API | Falls back to city center coords |
| Heatmap | Live Google Maps | Placeholder message |
| Submit/Track/Dashboard | ✅ Full | ✅ Full |
| Sample data pre-loaded | ✅ | ✅ |

**Result:** All three navigation pages, all filters, status updates, and complaint tracking work fully in demo mode. Judges can evaluate the full product experience without credentials.

---

## Running the PoC Yourself

### Quickest path (Demo Mode — no API keys needed):

```bash
git clone https://github.com/YOUR_ORG/civiclens.git
cd civiclens
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501 — the app loads with 5 sample complaints pre-populated.

### Full mode (with API keys):

```bash
cp .env.example .env
# Edit .env: add GEMINI_API_KEY and GOOGLE_MAPS_API_KEY
streamlit run app.py
```

---

## Known Limitations at PoC Stage

| Limitation | Impact | Planned Fix |
|------------|--------|------------|
| In-memory storage (session state) | Data lost on server restart | Replace with SQLite or Supabase |
| No authentication | Anyone can access dashboard | Add role-based login |
| No duplicate detection | Same complaint can be submitted multiple times | Add Gemini deduplication agent (see `AGENTS.md`) |
| English/Telugu only (tested) | Other languages may work but unverified | Expand language testing |
| Single-instance only | Multiple simultaneous users share the same session | Use a proper DB and per-user sessions |

---

## Conclusion

All three core technical assumptions of CivicLens are validated:

- ✅ Gemini AI reliably categorizes and prioritizes civic complaints (5/5 test cases)
- ✅ Google Maps correctly geocodes informal Hyderabad location strings
- ✅ A unified Streamlit interface works for both citizens and government officials
- ✅ The app works without API keys, enabling full evaluation in demo mode

CivicLens is a working proof of concept ready for hackathon demonstration.
