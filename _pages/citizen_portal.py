import streamlit as st
from utils.gemini_helper import analyze_complaint
from utils.maps_helper import geocode_address
from utils.data_store import add_complaint


PRIORITY_COLOR = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}


def show():
    st.title("🏛️ Submit a Complaint")
    st.markdown("Report any civic issue in Hyderabad. Our AI will categorize and route it to the right department.")
    st.divider()

    with st.form("complaint_form", clear_on_submit=True):
        description = st.text_area(
            "Describe the issue *",
            placeholder="e.g. There is a large pothole on Road No. 36, Jubilee Hills near the petrol bunk...",
            height=150,
        )

        location_input = st.text_input(
            "Location / Area *",
            placeholder="e.g. Road No. 36, Jubilee Hills, Hyderabad",
        )

        image_file = st.file_uploader(
            "Attach a photo (optional)",
            type=["jpg", "jpeg", "png"],
        )

        submitted = st.form_submit_button("🚀 Submit Complaint", use_container_width=True, type="primary")

    if submitted:
        if not description.strip():
            st.error("Please describe the issue.")
            return
        if not location_input.strip():
            st.error("Please enter a location.")
            return

        with st.spinner("🤖 Analyzing your complaint with AI..."):
            image_bytes = image_file.read() if image_file else None
            analysis = analyze_complaint(description, image_bytes)
            location = geocode_address(location_input)
            complaint = add_complaint(description, location, analysis, image_bytes)

        st.success(f"✅ Complaint submitted! Your ID: **{complaint['id']}**")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Category", complaint["category"])
        with col2:
            icon = PRIORITY_COLOR.get(complaint["priority"], "🟡")
            st.metric("Priority", f"{icon} {complaint['priority']}")
        with col3:
            st.metric("Department", complaint["department"])

        st.info(f"📝 **AI Summary:** {complaint['summary']}")
        st.caption(f"📍 Location resolved to: {location['address']}")
        st.caption("Track your complaint status using your ID in the **Track Complaint** page.")
