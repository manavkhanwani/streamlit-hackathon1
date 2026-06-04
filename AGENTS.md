# CivicLens — Agents Documentation

## Current Agents (v1.0)

### Agent 1 — Complaint Analysis Agent

**File:** `utils/gemini_helper.py`  
**Function:** `analyze_complaint(description, image_bytes=None)`  
**Model:** `gemini-1.5-flash`

Receives a free-text civic complaint (and optionally a photo) and returns:

```json
{
  "category":   "Roads | Water Supply | Electricity | Sanitation | Encroachment | Parks | Other",
  "priority":   "Low | Medium | High | Critical",
  "summary":    "One concise sentence summarizing the issue",
  "department": "Name of the most relevant government department"
}
```

**Prompt engineering:**
- Enum injection prevents hallucination outside allowed values
- `ONLY with a valid JSON object` prevents markdown/explanation wrappers
- `one concise sentence` prevents verbose summaries breaking the dashboard layout

**Multi-modal:** When a photo is attached, image bytes are sent as a second content part — Gemini can factor visual context into priority and category.

**Fallback:**
- No API key → `Roads / Medium` defaults
- API error / malformed JSON → `Other / Medium` defaults

---

### Agent 2 — Location Resolution Agent

**File:** `utils/maps_helper.py`  
**Function:** `geocode_address(address)`  
**Service:** Google Maps Geocoding API

Converts a plain-text location (e.g., "Jubilee Hills Road 36") to `{lat, lng, formatted_address}`.
Appends `", Hyderabad, Telangana, India"` to anchor results to the city.

**Fallback:** Returns Hyderabad city center (`17.3850, 78.4867`) when Maps API is unavailable.

---

### Agent 3 — Heatmap Visualization Agent

**File:** `utils/maps_helper.py`  
**Function:** `build_heatmap_html(complaints)`  
**Service:** Google Maps JavaScript API + Visualization Library

Converts the complaint list into a self-contained HTML heatmap rendered via `st.components.v1.html()` at height=440px.

**Fallback:** Returns a placeholder `<p>` element when Maps API key is not configured.

---

## Planned Future Agents (Post-Hackathon)

### Agent 4 — Deduplication Agent

**Function:** `deduplicate_complaint(new_description, existing_complaints) -> dict`  
**Output:** `{"is_duplicate": bool, "similar_id": str | null}`

Uses Gemini to check if an incoming complaint is semantically similar to an existing open one. Prevents duplicate accumulation in the dashboard.

---

### Agent 5 — Translation / Normalization Agent

**Function:** `normalize_to_english(description) -> str`

Normalizes complaint descriptions to English for consistent downstream processing, while preserving the original language for citizen-facing display.

---

### Agent 6 — Escalation Agent

**Trigger:** Scheduled daily job  
**Output:** List of complaint IDs exceeding SLA thresholds with recommended escalation actions.

Monitors open complaints that have not been updated within a defined time window and flags them for management review.
