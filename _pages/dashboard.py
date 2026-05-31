import streamlit as st
import pandas as pd
from utils.data_store import load_complaints, update_status, get_stats
from utils.maps_helper import build_heatmap_html

STATUS_OPTIONS = ["Open", "In Progress", "Resolved"]
PRIORITY_COLOR = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}
STATUS_COLOR = {"Open": "🔵", "In Progress": "🟡", "Resolved": "✅"}


def show():
    st.title("📊 Government Dashboard")
    st.markdown("Manage and respond to citizen complaints across Hyderabad.")
    st.divider()

    stats = get_stats()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Complaints", stats["total"])
    col2.metric("Open", stats["by_status"].get("Open", 0))
    col3.metric("In Progress", stats["by_status"].get("In Progress", 0))
    col4.metric("Resolved", stats["by_status"].get("Resolved", 0))

    st.divider()

    # Heatmap
    with st.expander("🗺️ Complaint Heatmap", expanded=True):
        complaints = load_complaints()
        heatmap_html = build_heatmap_html(complaints)
        st.components.v1.html(heatmap_html, height=440)

    st.divider()

    # Filters
    st.subheader("📋 All Complaints")
    col_f1, col_f2, col_f3 = st.columns(3)

    all_cats = sorted({c.get("category", "Other") for c in load_complaints()})
    selected_cat = col_f1.selectbox("Filter by Category", ["All"] + all_cats)
    selected_priority = col_f2.selectbox("Filter by Priority", ["All", "Critical", "High", "Medium", "Low"])
    selected_status = col_f3.selectbox("Filter by Status", ["All"] + STATUS_OPTIONS)

    complaints = load_complaints()
    filtered = [
        c for c in complaints
        if (selected_cat == "All" or c.get("category") == selected_cat)
        and (selected_priority == "All" or c.get("priority") == selected_priority)
        and (selected_status == "All" or c.get("status") == selected_status)
    ]

    st.caption(f"Showing {len(filtered)} complaint(s)")

    for c in filtered:
        priority_icon = PRIORITY_COLOR.get(c.get("priority", "Medium"), "🟡")
        status_icon = STATUS_COLOR.get(c.get("status", "Open"), "🔵")

        with st.expander(f"{priority_icon} [{c['id']}] {c.get('category', 'Other')} — {c.get('summary', '')[:80]}"):
            col_l, col_r = st.columns([2, 1])

            with col_l:
                st.markdown(f"**Description:** {c.get('description', 'N/A')}")
                st.markdown(f"**📍 Location:** {c.get('location', {}).get('address', 'N/A')}")
                st.markdown(f"**🏢 Department:** {c.get('department', 'N/A')}")
                st.caption(f"Submitted: {c.get('submitted_at', 'N/A')[:16]}")

            with col_r:
                st.markdown(f"**Status:** {status_icon} {c.get('status', 'Open')}")
                new_status = st.selectbox(
                    "Update Status",
                    STATUS_OPTIONS,
                    index=STATUS_OPTIONS.index(c.get("status", "Open")),
                    key=f"status_{c['id']}",
                )
                if st.button("💾 Save", key=f"save_{c['id']}"):
                    update_status(c["id"], new_status)
                    st.success("Status updated!")
                    st.rerun()
