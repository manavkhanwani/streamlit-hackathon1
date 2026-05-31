# 🤖 CivicLens — Agents & AI Intelligence Layer

This document describes the AI-powered agents and intelligence components used in CivicLens.

---

## Overview

CivicLens uses **Google Gemini 1.5 Flash** as its underlying AI model. The intelligence layer is implemented as a set of focused, stateless functions in `utils/gemini_helper.py`. Each function acts as a specialized agent with a narrow, well-defined task.

```
┌────────────────────────────────────────────────┐
│              CivicLens AI Layer                │
│                                                │
│  ┌──────────────────────────────────────────┐  │
│  │         Complaint Analysis Agent         │  │
│  │  (Categorizer · Prioritizer · Summarizer)│  │
│  └──────────────────┬───────────────────────┘  │
│                     │                          │
│       ┌─────────────┴─────────────┐            │
│       ▼                           ▼            │
│  Text Analysis             Image Analysis      │
│  (description string)      (JPEG bytes)        │
└────────────────────────────────────────────────┘
```

---

## Agent 1 — Complaint Analysis Agent

**File:** `utils/gemini_helper.py`  
**Function:** `analyze_complaint(description, image_bytes=None)`  
**Model:** `gemini-1.5-flash`

### What It Does

This is the core agent. When a citizen submits a complaint, this agent receives the free-text description (and optionally a photo) and returns four structured fields:

| Output Field | Type | Example |
|-------------|------|---------|
| `category` | string (enum) | `"Roads"` |
| `priority` | string (enum) | `"High"` |
| `summary` | string | `"Deep pothole near petrol bunk causing safety risk"` |
| `department` | string | `"GHMC Roads & Infrastructure"` |

### How It Works

1. A system prompt is constructed that constrains Gemini to act as a Hyderabad civic complaint classifier
2. The allowed categories and priorities are injected into the prompt as enums to prevent hallucination
3. The model is instructed to return **only valid JSON** with no markdown or explanation
4. If an image is attached, it is passed as a second part in a multi-modal request
5. The raw response is stripped of any code fences and parsed with `json.loads()`
6. On any failure (API error, malformed JSON), a safe fallback dict is returned so the app never crashes

### Prompt Design

```
You are an AI assistant for CivicLens, a civic complaint platform for Hyderabad, India.

Analyze the following civic complaint and respond ONLY with a valid JSON object:
{
  "category": "<one of: Roads, Water Supply, Electricity, Sanitation, Encroachment, Parks, Other>",
  "priority": "<one of: Low, Medium, High, Critical>",
  "summary": "<one concise sentence summarizing the issue>",
  "department": "<the most relevant government department to handle this>"
}

Complaint: {user_description}
```

### Multi-modal Support

When a photo is attached, the image bytes are appended as a second content part:

```python
parts = [prompt]
if image_bytes:
    parts.append({"mime_type": "image/jpeg", "data": image_bytes})
response = model.generate_content(parts)
```

This allows Gemini to visually inspect the complaint image and factor it into the priority and category decision. For example, a photo of a deep pothole may cause the agent to escalate priority from `Medium` to `High`.

### Fallback Behaviour

| Condition | Fallback Response |
|-----------|------------------|
| No API key configured | `category: Roads, priority: Medium, summary: first 120 chars of description` |
| API error / network failure | `category: Other, priority: Medium, department: GHMC General` |
| Malformed JSON from model | Same as API error fallback |

---

## Agent 2 — Location Resolution Agent (Maps)

**File:** `utils/maps_helper.py`  
**Function:** `geocode_address(address)`  
**Service:** Google Maps Geocoding API

### What It Does

Converts a free-text location string into precise lat/lng coordinates and a formatted address, anchored to Hyderabad, Telangana.

### How It Works

1. Appends `", Hyderabad, Telangana, India"` to the user's input to bias results to the city
2. Calls the Google Maps Geocoding API via the `googlemaps` Python client
3. Extracts `lat`, `lng`, and `formatted_address` from the first result
4. Falls back to Hyderabad city center (`17.3850, 78.4867`) if geocoding fails

### Output Schema

```json
{
  "lat": 17.4239,
  "lng": 78.4071,
  "address": "Road No. 36, Jubilee Hills, Hyderabad, Telangana 500033, India"
}
```

---

## Agent 3 — Heatmap Visualization Agent

**File:** `utils/maps_helper.py`  
**Function:** `build_heatmap_html(complaints)`  
**Service:** Google Maps JavaScript API + Visualization Library

### What It Does

Takes the full list of complaints and generates a self-contained HTML snippet that renders a live Google Maps heatmap. The density of the heatmap reflects the geographic concentration of civic issues.

### How It Works

1. Extracts `lat/lng` from every complaint that has a `location` field
2. Generates a JavaScript array of `{lat, lng}` objects
3. Injects these points into a Maps JavaScript API `HeatmapLayer`
4. Returns the entire `<div>` + `<script>` block as a string for embedding via `st.components.v1.html()`

---

## Configuration & Environment

All AI agents read their credentials from environment variables (via `python-dotenv`):

```env
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

Both agents lazy-initialize their client objects on first call and cache them as module-level singletons. If a key is missing or is the placeholder string, the agent returns a safe demo fallback instead of raising an exception.

---

## Extending the AI Layer

To add a new agent (e.g., a deduplication agent or a multilingual translation agent):

1. Add a new function to `utils/gemini_helper.py`
2. Follow the pattern: construct a constrained prompt → call `model.generate_content()` → parse JSON response → handle exceptions with a safe fallback
3. Call the function from the relevant page in `pages/`

Example skeleton:

```python
def deduplicate_complaint(new_description: str, existing_complaints: list) -> dict:
    """Checks if a new complaint is a duplicate of an existing one."""
    model = get_model()
    if model is None:
        return {"is_duplicate": False, "similar_id": None}

    existing_summaries = [f"{c['id']}: {c['summary']}" for c in existing_complaints[:20]]
    prompt = f"""
    You are a deduplication agent for CivicLens.
    New complaint: {new_description}
    Existing complaints:
    {chr(10).join(existing_summaries)}
    
    Respond ONLY with JSON: {{"is_duplicate": true/false, "similar_id": "<id or null>"}}
    """
    try:
        response = model.generate_content(prompt)
        text = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(text)
    except Exception:
        return {"is_duplicate": False, "similar_id": None}
```

---

## Limitations (Hackathon Scope)

- **No memory between calls** — each `analyze_complaint()` call is stateless; there is no conversation history
- **No fine-tuning** — Gemini 1.5 Flash is used out-of-the-box with prompt engineering only
- **English/Telugu only** — tested for these two languages; other languages may work but are untested
- **Single model** — all tasks use the same `gemini-1.5-flash` model; a production system might route different tasks to different models
