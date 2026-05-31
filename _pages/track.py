import streamlit as st
from utils.data_store import get_complaint_by_id

STATUS_STEPS = ["Open", "In Progress", "Resolved"]
PRIORITY_COLOR = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}


def show():
    st.title("🔍 Track Your Complaint")
    st.markdown("Enter your complaint ID to check its current status.")
    st.divider()

    complaint_id = st.text_input("Complaint ID", placeholder="e.g. CL-001 or CL-A1B2C3").strip().upper()

    if st.button("Track", type="primary", use_container_width=True):
        if not complaint_id:
            st.error("Please enter a complaint ID.")
            return

        complaint = get_complaint_by_id(complaint_id)

        if not complaint:
            st.error(f"No complaint found with ID **{complaint_id}**. Please check and try again.")
            return

        status = complaint.get("status", "Open")
        current_step = STATUS_STEPS.index(status) if status in STATUS_STEPS else 0

        st.success(f"Found complaint **{complaint_id}**")

        # Progress indicator
        cols = st.columns(3)
        for i, step in enumerate(STATUS_STEPS):
            with cols[i]:
                if i < current_step:
                    st.markdown(f"✅ **{step}**")
                elif i == current_step:
                    st.markdown(f"🔵 **{step}** ← *Current*")
                else:
                    st.markdown(f"⬜ {step}")

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**🏷️ Category:** {complaint.get('category', 'N/A')}")
            st.markdown(f"**⚡ Priority:** {PRIORITY_COLOR.get(complaint.get('priority','Medium'),'')} {complaint.get('priority', 'N/A')}")
            st.markdown(f"**🏢 Department:** {complaint.get('department', 'N/A')}")
        with col2:
            st.markdown(f"**📍 Location:** {complaint.get('location', {}).get('address', 'N/A')}")
            st.markdown(f"**📅 Submitted:** {complaint.get('submitted_at', 'N/A')[:16]}")

        st.markdown(f"**📝 AI Summary:** {complaint.get('summary', 'N/A')}")
        st.text_area("Original Description", complaint.get("description", ""), height=100, disabled=True)
