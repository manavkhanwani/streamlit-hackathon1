"""
app.py — CivicLens entry point.
Configures page, renders sidebar navigation, and routes to page modules.

Uses _pages/ (underscore prefix) to prevent Streamlit MPA auto-discovery,
giving full control over the sidebar UI. (TECH_SPEC §3.1)
"""

import streamlit as st

st.set_page_config(
    page_title="CivicLens",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from _pages import citizen_portal, dashboard, track  # noqa: E402

with st.sidebar:
    st.title("🏛️ CivicLens")
    st.caption("See the City Clearly")
    st.markdown("---")
    page = st.radio(
        "Navigation",
        ["🗣️ Submit a Complaint", "📊 Government Dashboard", "🔍 Track Complaint"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("Built for CivicTech Hackathon\nHyderabad · Telangana")

if page == "🗣️ Submit a Complaint":
    citizen_portal.show()
elif page == "📊 Government Dashboard":
    dashboard.show()
elif page == "🔍 Track Complaint":
    track.show()
