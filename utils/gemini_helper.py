import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

CATEGORIES = ["Roads", "Water Supply", "Electricity", "Sanitation", "Encroachment", "Parks", "Other"]
PRIORITIES = ["Low", "Medium", "High", "Critical"]

_model = None

def get_model():
    global _model
    if _model is None:
        api_key = os.getenv("GEMINI_API_KEY", "")
        if not api_key or api_key == "your_gemini_api_key_here":
            return None
        genai.configure(api_key=api_key)
        _model = genai.GenerativeModel("gemini-1.5-flash")
    return _model


def analyze_complaint(description: str, image_bytes: bytes = None) -> dict:
    """
    Sends a complaint to Gemini and returns category, priority, and summary.
    Falls back to defaults if API key is not configured.
    """
    model = get_model()

    if model is None:
        # Demo fallback — no API key set
        return {
            "category": "Roads",
            "priority": "Medium",
            "summary": description[:120] + ("..." if len(description) > 120 else ""),
            "department": "GHMC Roads & Infrastructure",
        }

    prompt = f"""
You are an AI assistant for CivicLens, a civic complaint platform for Hyderabad, India.

Analyze the following civic complaint and respond ONLY with a valid JSON object (no markdown, no explanation):
{{
  "category": "<one of: {', '.join(CATEGORIES)}>",
  "priority": "<one of: {', '.join(PRIORITIES)}>",
  "summary": "<one concise sentence summarizing the issue>",
  "department": "<the most relevant government department to handle this>"
}}

Complaint: {description}
"""

    try:
        parts = [prompt]
        if image_bytes:
            parts.append({"mime_type": "image/jpeg", "data": image_bytes})

        response = model.generate_content(parts)
        text = response.text.strip().replace("```json", "").replace("```", "").strip()
        result = json.loads(text)
        return result
    except Exception:
        return {
            "category": "Other",
            "priority": "Medium",
            "summary": description[:120],
            "department": "GHMC General",
        }
