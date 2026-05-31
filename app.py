import streamlit as st

st.set_page_config(
    page_title="CivicLens — Unified Civic Complaints",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import from _pages (not pages/) so Streamlit does NOT auto-discover these
# files as MPA pages and add unwanted nav links to the sidebar.
from _pages import citizen_portal, dashboard, track

# ── Sidebar navigation ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏛️ CivicLens")
    st.caption("*See the City Clearly*")
    st.divider()

    page = st.radio(
        "Navigate",
        ["🗣️ Submit a Complaint", "📊 Government Dashboard", "🔍 Track Complaint"],
        label_visibility="collapsed",
    )

    st.divider()
    st.caption("Built for CivicTech Hackathon")
    st.caption("Hyderabad · Telangana")

# ── Route to the selected page ───────────────────────────────────────────────
if page == "🗣️ Submit a Complaint":
    citizen_portal.show()
elif page == "📊 Government Dashboard":
    dashboard.show()
elif page == "🔍 Track Complaint":
    track.show()
