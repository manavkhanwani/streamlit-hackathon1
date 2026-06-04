"""
_pages/dashboard.py — Government dashboard page.

Renders KPI metrics, complaint heatmap, filterable complaint list,
and per-complaint status update controls.

Spec compliance:
  - PRD §6.2 (Government Dashboard features)
  - UX_FLOWS §3 (Flow 2 — Government Dashboard)
  - DATA_SPEC §3 (get_stats, load_complaints, update_status APIs)
  - AI_SPEC §4 (build_heatmap_html usage)
"""

import streamlit as st
import streamlit.components.v1 as components

from utils import data_store, maps_helper

# Priority icons per UX_FLOWS §3 (Priority and Status Color Codes)
PRIORITY_ICONS = {
    "Critical": "🔴",
    "High": "🟠",
    "Medium": "🟡",
    "Low": "🟢",
}

# Status icons per UX_FLOWS §3 (Priority and Status Color Codes)
STATUS_ICONS = {
    "Open": "🔵",
    "In Progress": "🟡",
    "Resolved": "✅",
}

# Filter options — enums from DATA_SPEC §2
CATEGORIES = ["All", "Roads", "Water Supply", "Electricity", "Sanitation", "Encroachment", "Parks", "Other"]
PRIORITIES = ["All", "Critical", "High", "Medium", "Low"]
STATUSES = ["All", "Open", "In Progress", "Resolved"]


def show() -> None:
    """Renders the government dashboard page."""
    st.header("📊 Government Dashboard")
    st.write("Manage and respond to citizen complaints across Hyderabad.")

    # --- KPI Metrics Row (PRD §6.2, UX_FLOWS §3 — 4 columns) ---
    stats = data_store.get_stats()
    by_status = stats["by_status"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Complaints", stats["total"])
    col2.metric("Open", by_status.get("Open", 0))
    col3.metric("In Progress", by_status.get("In Progress", 0))
    col4.metric("Resolved", by_status.get("Resolved", 0))

    # --- Complaint Heatmap (PRD §6.2, AI_SPEC §4) ---
    with st.expander("🗺️ Complaint Heatmap", expanded=True):
        complaints_all = data_store.load_complaints()
        heatmap_html = maps_helper.build_heatmap_html(complaints_all)
        components.html(heatmap_html, height=440)

    # --- Filterable Complaint List (PRD §6.2, UX_FLOWS §3) ---
    st.subheader("📋 All Complaints")

    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        filter_category = st.selectbox("Filter by Category", CATEGORIES)
    with f_col2:
        filter_priority = st.selectbox("Filter by Priority", PRIORITIES)
    with f_col3:
        filter_status = st.selectbox("Filter by Status", STATUSES)

    # Client-side filtering (UX_FLOWS §3 — Filter Behaviour)
    complaints = data_store.load_complaints()
    filtered = [
        c for c in complaints
        if (filter_category == "All" or c.get("category") == filter_category)
        and (filter_priority == "All" or c.get("priority") == filter_priority)
        and (filter_status == "All" or c.get("status") == filter_status)
    ]

    st.caption(f"Showing **{len(filtered)}** complaint(s)")

    # --- Complaint Cards (UX_FLOWS §3 — Complaint Cards) ---
    for c in filtered:
        priority_icon = PRIORITY_ICONS.get(c.get("priority", "Medium"), "")
        summary_preview = c.get("summary", "")[:80]
        expander_label = f"{priority_icon} {c['id']} · {c.get('category', 'Other')} — {summary_preview}"

        with st.expander(expander_label):
            left, right = st.columns([2, 1])

            with left:
                st.markdown(f"**Description:** {c.get('description', '')}")
                st.markdown(f"**Location:** {c.get('location', {}).get('address', 'N/A')}")
                st.markdown(f"**Department:** {c.get('department', 'N/A')}")
                # Display first 16 chars of ISO timestamp: YYYY-MM-DDTHH:MM → YYYY-MM-DD HH:MM
                submitted_at = c.get("submitted_at", "")[:16].replace("T", " ")
                st.markdown(f"**Submitted:** {submitted_at}")

            with right:
                current_status = c.get("status", "Open")
                status_icon = STATUS_ICONS.get(current_status, "")
                st.markdown(f"**Status:** {status_icon} {current_status}")

                new_status = st.selectbox(
                    "Update Status",
                    ["Open", "In Progress", "Resolved"],
                    index=["Open", "In Progress", "Resolved"].index(current_status),
                    key=f"status_select_{c['id']}",
                )

                # Save button — status does NOT change until Save is clicked (UX_FLOWS §3)
                if st.button("💾 Save", key=f"save_{c['id']}"):
                    data_store.update_status(c["id"], new_status)
                    st.success("Status updated!")
                    st.rerun()
