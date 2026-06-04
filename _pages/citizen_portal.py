"""
_pages/citizen_portal.py — Complaint submission page.

Orchestrates AI analysis, geocoding, and data store on form submit.

Spec compliance:
  - PRD §6.1 (Citizen Portal features)
  - UX_FLOWS §2 (Flow 1 — Complaint Submission)
  - DATA_SPEC §3 (add_complaint API contract)
  - AI_SPEC §2 (analyze_complaint usage)
"""

import streamlit as st

from utils import data_store, gemini_helper, maps_helper

# Priority icons per UX_FLOWS §3 (color codes table)
PRIORITY_ICONS = {
    "Critical": "🔴",
    "High": "🟠",
    "Medium": "🟡",
    "Low": "🟢",
}


def show() -> None:
    """Renders the citizen complaint submission page."""
    st.header("🗣️ Submit a Complaint")
    st.write(
        "Report any civic issue in Hyderabad. Our AI will categorize "
        "and route it to the right department."
    )

    # --- Form Inputs (UX_FLOWS §2 — Happy Path) ---
    description = st.text_area(
        "Describe the issue *",
        height=150,
        placeholder=(
            "e.g. There is a large pothole on Road No. 36, Jubilee Hills near the petrol bunk. "
            "Vehicles are swerving dangerously at night."
        ),
    )

    location_input = st.text_input(
        "Location / Area *",
        placeholder="e.g. Road No. 36, Jubilee Hills, Hyderabad",
    )

    uploaded_file = st.file_uploader(
        "Attach a photo (optional)",
        type=["jpg", "jpeg", "png"],
    )

    submitted = st.button("🚀 Submit Complaint", use_container_width=True, type="primary")

    if submitted:
        # --- Validation (UX_FLOWS §2 — Validation Errors) ---
        if not description.strip():
            st.error("Please describe the issue.")
            return
        if not location_input.strip():
            st.error("Please enter a location.")
            return

        # --- AI Analysis + Geocoding + Data Store ---
        with st.spinner("🤖 Analyzing your complaint with AI..."):
            image_bytes = None
            if uploaded_file is not None:
                image_bytes = uploaded_file.read()

            # AI_SPEC §2 — analyze_complaint(description, image_bytes)
            analysis = gemini_helper.analyze_complaint(description.strip(), image_bytes)

            # AI_SPEC §3 — geocode_address(address)
            location = maps_helper.geocode_address(location_input.strip())

            # DATA_SPEC §3 — add_complaint(...)
            complaint = data_store.add_complaint(
                description=description.strip(),
                location=location,
                analysis=analysis,
                image_bytes=image_bytes,
            )

        # --- Success Display (UX_FLOWS §2 — Happy Path) ---
        st.success(f"✅ Complaint submitted! Your ID: **{complaint['id']}**")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Category", complaint["category"])
        with col2:
            priority_icon = PRIORITY_ICONS.get(complaint["priority"], "")
            st.metric("Priority", f"{priority_icon} {complaint['priority']}")
        with col3:
            st.metric("Department", complaint["department"])

        st.info(f"📝 **AI Summary:** {complaint['summary']}")
        st.caption(f"📍 Location resolved to: {complaint['location']['address']}")
        st.caption(
            "Track your complaint status using your ID in the **Track Complaint** page."
        )
