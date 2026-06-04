"""
utils/gemini_helper.py — Google Gemini AI integration.

Implements the Complaint Analysis Agent (AI_SPEC §2).
Uses lazy initialization (TECH_SPEC §7.1) and graceful degradation (TECH_SPEC §7.2).

Spec compliance:
  - AI_SPEC §2.1–2.8 (Complaint Analysis Agent — full specification)
  - TECH_SPEC §7.1 (Lazy Initialization Pattern)
  - TECH_SPEC §7.2 (Graceful Degradation)
"""

import json
import os

from dotenv import load_dotenv

load_dotenv()

# Module-level singleton — lazy initialized (TECH_SPEC §7.1)
_model = None


def _get_model():
    """
    Lazy-initialize Gemini 1.5 Flash model.
    Returns None if GEMINI_API_KEY is absent or a placeholder (AI_SPEC §2.7).
    """
    global _model
    if _model is not None:
        return _model

    api_key = os.getenv("GEMINI_API_KEY", "")
    # Sentinel check: placeholder strings are treated as missing (TECH_SPEC §6)
    if not api_key or "your_" in api_key:
        return None

    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        # AI_SPEC §5 — Model: gemini-1.5-flash
        _model = genai.GenerativeModel("gemini-1.5-flash")
        return _model
    except Exception:
        return None


def analyze_complaint(description: str, image_bytes: bytes = None) -> dict:
    """
    Analyzes a civic complaint using Gemini 1.5 Flash (AI_SPEC §2).

    Args:
        description: Free-text complaint description. Supports English and Telugu (AI_SPEC §2.8).
        image_bytes: Optional JPEG image bytes. Enables multi-modal analysis (AI_SPEC §2.5).

    Returns:
        dict with keys: category, priority, summary, department.
        Output schema per AI_SPEC §2.2.

    Fallback behaviour per AI_SPEC §2.7:
        - No API key:           Roads / Medium / first 120 chars / GHMC Roads & Infrastructure
        - API error:            Other / Medium / first 120 chars / GHMC General
        - Malformed JSON:       Other / Medium / first 120 chars / GHMC General
    """
    # AI_SPEC §2.7 — Fallback: no API key configured
    fallback_roads = {
        "category": "Roads",
        "priority": "Medium",
        "summary": description[:120],
        "department": "GHMC Roads & Infrastructure",
    }
    # AI_SPEC §2.7 — Fallback: API error or malformed JSON
    fallback_other = {
        "category": "Other",
        "priority": "Medium",
        "summary": description[:120],
        "department": "GHMC General",
    }

    model = _get_model()
    if model is None:
        return fallback_roads

    # AI_SPEC §2.4 — Prompt Design: inject category/priority enums to prevent hallucination
    prompt = (
        "You are an AI assistant for CivicLens, a civic complaint platform for Hyderabad, India.\n\n"
        "Analyze the following civic complaint and respond ONLY with a valid JSON object "
        "(no markdown, no explanation):\n"
        "{\n"
        '  "category": "<one of: Roads, Water Supply, Electricity, Sanitation, Encroachment, Parks, Other>",\n'
        '  "priority": "<one of: Low, Medium, High, Critical>",\n'
        '  "summary": "<one concise sentence summarizing the issue>",\n'
        '  "department": "<the most relevant government department to handle this>"\n'
        "}\n\n"
        f"Complaint: {description}"
    )

    try:
        # AI_SPEC §2.5 — Multi-modal: append image bytes as second content part if present
        parts = [prompt]
        if image_bytes:
            parts.append({"mime_type": "image/jpeg", "data": image_bytes})

        response = model.generate_content(parts)

        # AI_SPEC §2.6 — Response Parsing: strip code fences defensively
        text = response.text.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        result = json.loads(text)

        # Validate all required keys are present (AI_SPEC §2.2 — Output Schema)
        required_keys = {"category", "priority", "summary", "department"}
        if not required_keys.issubset(result.keys()):
            return fallback_other

        return result

    except json.JSONDecodeError:
        # AI_SPEC §2.7 — Malformed JSON fallback
        return fallback_other
    except Exception:
        # AI_SPEC §2.7 — API error / network failure fallback
        return fallback_other
