"""
_pages/track.py — Complaint tracking page.

Citizens enter their CL-XXXXXX ID to view status and full complaint details.

Spec compliance:
  - PRD §6.3 (Complaint Tracking features)
  - UX_FLOWS §4 (Flow 3 — Complaint Tracking)
  - DATA_SPEC §3 (get_complaint_by_id API)
"""

import streamlit as st

from utils import data_store

# Priority icons per UX_FLOWS §3 (Priority and Status Color Codes)
PRIORITY_ICONS = {
    "Critical": "🔴",
    "High": "🟠",
    "Medium": "🟡",
    "Low": "🟢",
}

# Step order for the progress indicator (UX_FLOWS §4 — Progress Indicator Logic)
STATUS_STEPS = ["Open", "In Progress", "Resolved"]


def _render_progress(status: str) -> None:
    """
    Renders a three-column step progress indicator.

    Logic per UX_FLOWS §4:
      - Past steps:    ✅ **{step}**
      - Current step:  🔵 **{step}** ← *Current*
      - Future steps:  ⬜ {step}
    """
    try:
        current_step = STATUS_STEPS.index(status)
    except ValueError:
        current_step = 0  # Fallback: treat unknown status as Open (UX_FLOWS §4 — Edge Cases)

    cols = st.columns(3)
    for i, (col, step) in enumerate(zip(cols, STATUS_STEPS)):
        with col:
            if i < current_step:
                st.markdown(f"✅ **{step}**")
            elif i == current_step:
                st.markdown(f"🔵 **{step}** ← *Current*")
            else:
                st.markdown(f"⬜ {step}")


def show() -> None:
    """Renders the complaint tracking page."""
    st.header("🔍 Track Your Complaint")
    st.write("Enter your complaint ID to check its current status.")

    complaint_id_input = st.text_input(
        "Complaint ID",
        placeholder="e.g. CL-001 or CL-A1B2C3",
    )

    tracked = st.button("Track", use_container_width=True, type="primary")

    if tracked:
        # Normalize: strip whitespace + uppercase for case-insensitive lookup (UX_FLOWS §4)
        normalized_id = complaint_id_input.strip().upper()

        if not normalized_id:
            st.error("Please enter a complaint ID.")
            return

        # DATA_SPEC §3 — get_complaint_by_id (exact match; caller normalizes with .upper())
        complaint = data_store.get_complaint_by_id(normalized_id)

        if complaint is None:
            st.error(
                f"No complaint found with ID **{normalized_id}**. "
                "Please check your ID and try again."
            )
            return

        st.success(f"Found complaint **{complaint['id']}**")

        # --- Progress Indicator (UX_FLOWS §4 — Progress Indicator Logic) ---
        _render_progress(complaint.get("status", "Open"))

        st.markdown("---")

        # --- Detail Columns (UX_FLOWS §4 — Detail columns — 2 columns, 1:1) ---
        left, right = st.columns(2)
        with left:
            st.markdown(f"**Category:** {complaint.get('category', 'N/A')}")
            priority = complaint.get("priority", "Medium")
            priority_icon = PRIORITY_ICONS.get(priority, "")
            st.markdown(f"**Priority:** {priority_icon} {priority}")
            st.markdown(f"**Department:** {complaint.get('department', 'N/A')}")
        with right:
            st.markdown(f"**Location:** {complaint.get('location', {}).get('address', 'N/A')}")
            submitted_at = complaint.get("submitted_at", "")[:16].replace("T", " ")
            st.markdown(f"**Submitted:** {submitted_at}")

        st.markdown(f"**AI Summary:** {complaint.get('summary', '')}")

        # Original description rendered in a disabled text area (UX_FLOWS §4 — 100px height)
        st.text_area(
            "Original Description",
            value=complaint.get("description", ""),
            height=100,
            disabled=True,
        )
