"""
utils/data_store.py — In-memory data layer backed by st.session_state.

All complaints are stored in st.session_state.complaints as list[dict],
ordered newest-first. (TECH_SPEC §5 — State Management)

Spec compliance:
  - DATA_SPEC §1 (Data Layer Overview)
  - DATA_SPEC §2 (Complaint Schema — all field types, enums, defaults)
  - DATA_SPEC §3 (full Data Store API: load_complaints, add_complaint,
                  update_status, get_complaint_by_id, get_stats)
"""

import json
import os
import uuid
from datetime import datetime

import streamlit as st

# Path to the seed data file (DATA_SPEC §4 — Sample Data)
SAMPLE_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "sample_data.json")


def load_complaints() -> list:
    """
    Returns the full complaints list ordered newest-first.

    On first call in a session, seeds from assets/sample_data.json.
    On subsequent calls within the same session, returns cached session state.
    Falls back to an empty list if the file is missing or malformed.
    (DATA_SPEC §3 — load_complaints behaviour)
    """
    if "complaints" not in st.session_state:
        try:
            with open(SAMPLE_DATA_PATH, "r", encoding="utf-8") as f:
                st.session_state.complaints = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            st.session_state.complaints = []
    return st.session_state.complaints


def add_complaint(
    description: str,
    location: dict,
    analysis: dict,
    image_bytes: bytes = None,
) -> dict:
    """
    Creates a new complaint and inserts it at index 0 (newest first).
    Returns the created complaint dict.

    ID format: CL- + 6-character uppercase UUID prefix (DATA_SPEC §2 — id field).
    All schema fields are populated per DATA_SPEC §2.
    image_bytes are NOT stored in the complaint dict — only has_image flag (DATA_SPEC §6).
    """
    load_complaints()  # Ensure session state is initialized

    # DATA_SPEC §2 — id: CL- + 6-char uppercase UUID prefix
    complaint_id = f"CL-{str(uuid.uuid4())[:6].upper()}"

    complaint = {
        "id": complaint_id,
        # DATA_SPEC §2 — category: from Gemini analysis, default "Other"
        "category": analysis.get("category", "Other"),
        # DATA_SPEC §2 — priority: from Gemini analysis, default "Medium"
        "priority": analysis.get("priority", "Medium"),
        # DATA_SPEC §2 — status: defaults to "Open" on creation
        "status": "Open",
        # DATA_SPEC §2 — summary: AI-generated one-sentence summary
        "summary": analysis.get("summary", description[:120]),
        # DATA_SPEC §2 — department: from Gemini analysis
        "department": analysis.get("department", "GHMC General"),
        # DATA_SPEC §2 — description: original citizen input
        "description": description,
        # DATA_SPEC §2 — location: nested {lat, lng, address} with city-center fallback
        "location": {
            "lat": location.get("lat", HYD_LAT),
            "lng": location.get("lng", HYD_LNG),
            "address": location.get("address", "Hyderabad, Telangana, India"),
        },
        # DATA_SPEC §2 — submitted_at: UTC ISO 8601 datetime string
        "submitted_at": datetime.now().isoformat(),
        # DATA_SPEC §2 — has_image: True if citizen attached a photo; bytes NOT stored
        "has_image": image_bytes is not None,
    }

    # Insert at index 0 to maintain newest-first ordering
    st.session_state.complaints.insert(0, complaint)
    return complaint


# Hyderabad city center fallback — matches maps_helper constants (DATA_SPEC §2)
HYD_LAT = 17.3850
HYD_LNG = 78.4867


def update_status(complaint_id: str, new_status: str) -> None:
    """
    Updates the status field of a complaint in-place.
    Silent no-op if the ID is not found. (DATA_SPEC §3 — update_status behaviour)

    Args:
        complaint_id: Exact complaint ID (e.g., "CL-A1B2C3").
        new_status: One of "Open", "In Progress", "Resolved" (DATA_SPEC §2 — status enum).
    """
    load_complaints()
    for c in st.session_state.complaints:
        if c["id"] == complaint_id:
            c["status"] = new_status
            break


def get_complaint_by_id(complaint_id: str):
    """
    Returns the complaint dict for the given ID, or None if not found.

    Matching is exact (case-sensitive). Callers should normalize with .upper()
    to achieve case-insensitive lookup from the user's perspective.
    (DATA_SPEC §3 — get_complaint_by_id, UX_FLOWS §4 — Edge Cases)
    """
    for c in load_complaints():
        if c["id"] == complaint_id:
            return c
    return None


def get_stats() -> dict:
    """
    Returns aggregated statistics across all complaints.

    Output schema per DATA_SPEC §3 — get_stats:
    {
        "total": int,
        "by_status": {"Open": int, "In Progress": int, "Resolved": int},
        "by_category": {category_name: int, ...},
        "by_priority": {"Critical": int, "High": int, "Medium": int, "Low": int}
    }
    """
    complaints = load_complaints()

    by_status = {"Open": 0, "In Progress": 0, "Resolved": 0}
    by_category: dict = {}
    by_priority = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}

    for c in complaints:
        status = c.get("status", "Open")
        if status in by_status:
            by_status[status] += 1
        else:
            by_status[status] = 1

        cat = c.get("category", "Other")
        by_category[cat] = by_category.get(cat, 0) + 1

        pri = c.get("priority", "Medium")
        if pri in by_priority:
            by_priority[pri] += 1
        else:
            by_priority[pri] = 1

    return {
        "total": len(complaints),
        "by_status": by_status,
        "by_category": by_category,
        "by_priority": by_priority,
    }
