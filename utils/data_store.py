import json
import uuid
import streamlit as st
from datetime import datetime
from typing import Optional

SAMPLE_DATA_PATH = "assets/sample_data.json"


def load_complaints() -> list:
    """Load complaints from session state, seeding with sample data on first run."""
    if "complaints" not in st.session_state:
        try:
            with open(SAMPLE_DATA_PATH) as f:
                st.session_state.complaints = json.load(f)
        except FileNotFoundError:
            st.session_state.complaints = []
    return st.session_state.complaints


def add_complaint(description: str, location: dict, analysis: dict, image_bytes: bytes = None) -> dict:
    """Create and store a new complaint. Returns the created complaint dict."""
    complaints = load_complaints()
    complaint_id = f"CL-{str(uuid.uuid4())[:6].upper()}"
    complaint = {
        "id": complaint_id,
        "category": analysis.get("category", "Other"),
        "priority": analysis.get("priority", "Medium"),
        "summary": analysis.get("summary", description[:100]),
        "department": analysis.get("department", "GHMC General"),
        "description": description,
        "location": location,
        "status": "Open",
        "submitted_at": datetime.now().isoformat(),
        "has_image": image_bytes is not None,
    }
    complaints.insert(0, complaint)
    st.session_state.complaints = complaints
    return complaint


def update_status(complaint_id: str, new_status: str):
    """Update the status of a complaint by ID."""
    complaints = load_complaints()
    for c in complaints:
        if c["id"] == complaint_id:
            c["status"] = new_status
            break
    st.session_state.complaints = complaints


def get_complaint_by_id(complaint_id: str) -> Optional[dict]:
    """Fetch a single complaint by its ID."""
    for c in load_complaints():
        if c["id"] == complaint_id:
            return c
    return None


def get_stats() -> dict:
    complaints = load_complaints()
    total = len(complaints)
    by_status = {"Open": 0, "In Progress": 0, "Resolved": 0}
    by_category = {}
    by_priority = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}

    for c in complaints:
        by_status[c.get("status", "Open")] = by_status.get(c.get("status", "Open"), 0) + 1
        cat = c.get("category", "Other")
        by_category[cat] = by_category.get(cat, 0) + 1
        pri = c.get("priority", "Medium")
        by_priority[pri] = by_priority.get(pri, 0) + 1

    return {
        "total": total,
        "by_status": by_status,
        "by_category": by_category,
        "by_priority": by_priority,
    }
