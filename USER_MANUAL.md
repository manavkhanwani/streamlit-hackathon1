# 📖 CivicLens — User Manual

> **"See the City Clearly"** — An AI-powered civic complaint platform for Hyderabad & Telangana

---

## Table of Contents

1. [Getting Started](#1-getting-started)
2. [Navigating the App](#2-navigating-the-app)
3. [Submitting a Complaint](#3-submitting-a-complaint) *(Citizens)*
4. [Tracking Your Complaint](#4-tracking-your-complaint) *(Citizens)*
5. [Government Dashboard](#5-government-dashboard) *(Officials)*
6. [Understanding Complaint Data](#6-understanding-complaint-data)
7. [Demo Mode (No API Keys)](#7-demo-mode-no-api-keys)
8. [FAQ](#8-faq)

---

## 1. Getting Started

### Launching the App

After completing the setup steps in `SETUP.md`, run:

```bash
streamlit run app.py
```

Open your browser to **http://localhost:8501**. You will see the CivicLens homepage with the sidebar navigation on the left.

---

## 2. Navigating the App

CivicLens has three sections, accessible from the **sidebar** on the left:

| Section | Icon | Who Uses It |
|---------|------|-------------|
| Submit a Complaint | 🗣️ | Citizens |
| Government Dashboard | 📊 | Government Officials |
| Track Complaint | 🔍 | Citizens |

Click any option in the sidebar to navigate to that section.

---

## 3. Submitting a Complaint

**Section:** 🗣️ Submit a Complaint

This is where citizens report civic issues — potholes, broken streetlights, garbage overflow, water supply failures, and more.

### Step-by-Step

**Step 1 — Describe the issue**

In the "Describe the issue" text box, type a clear description of the problem. Be as specific as possible.

> *Example: "There is a large pothole (~2ft wide) on Road No. 36, Jubilee Hills near the petrol bunk. Cars swerving to avoid it — dangerous at night."*

**Step 2 — Enter the location**

Type the area or street where the issue is located. The AI will resolve this to a precise address.

> *Example: "Road No. 36, Jubilee Hills, Hyderabad"*

**Step 3 — Attach a photo (optional)**

Click "Browse files" to upload a JPG or PNG photo of the issue. A photo helps the AI give a more accurate category and priority.

**Step 4 — Submit**

Click **🚀 Submit Complaint**. The AI will analyze your complaint in a few seconds.

### After Submission

You will see:
- A **Complaint ID** (e.g., `CL-A1B2C3`) — save this to track your complaint later
- **Category** — the type of civic issue (Roads, Water Supply, Electricity, etc.)
- **Priority** — how urgently the AI flagged it (Critical, High, Medium, Low)
- **Department** — which government body has been notified
- **AI Summary** — a concise one-line summary of your complaint
- **Resolved location** — the address the system mapped your input to

---

## 4. Tracking Your Complaint

**Section:** 🔍 Track Complaint

Use this section to check the current status of a complaint you submitted.

### How to Track

1. Enter your **Complaint ID** in the text box (e.g., `CL-A1B2C3`). IDs are case-insensitive.
2. Click **Track**.

### What You'll See

- A **progress bar** showing the three stages: `Open → In Progress → Resolved`
- Your complaint's **category, priority, and department**
- The **resolved location address**
- The **date and time** your complaint was submitted
- The **AI-generated summary** and your original description

### Status Meanings

| Status | Meaning |
|--------|---------|
| 🔵 Open | Complaint received, awaiting action |
| 🟡 In Progress | A department official is handling the issue |
| ✅ Resolved | The issue has been addressed and closed |

---

## 5. Government Dashboard

**Section:** 📊 Government Dashboard

This section is for government officials to view, filter, and act on complaints.

### Overview Metrics

At the top of the dashboard you will see four counters:
- **Total Complaints** — all complaints in the system
- **Open** — complaints awaiting action
- **In Progress** — complaints being actively handled
- **Resolved** — closed complaints

### Heatmap

The **Complaint Heatmap** shows a live Google Maps view with a heat overlay indicating where complaints are concentrated across Hyderabad. Bright/dense areas = more complaints.

> Requires a valid `GOOGLE_MAPS_API_KEY` in your `.env` file. Without it, a placeholder message appears.

### Filtering Complaints

Use the three dropdown filters to narrow the list:

| Filter | Options |
|--------|---------|
| Category | Roads, Water Supply, Electricity, Sanitation, Encroachment, Parks, Other |
| Priority | Critical, High, Medium, Low |
| Status | Open, In Progress, Resolved |

Select "All" in any filter to see all complaints for that field.

### Viewing a Complaint

Click any complaint row to expand it. You will see:
- Full description
- Location, department, submission timestamp
- Current status
- AI summary

### Updating a Complaint's Status

Inside the expanded complaint card:
1. Use the **"Update Status"** dropdown to select a new status
2. Click **💾 Save**

The page will refresh and the counter at the top will update accordingly.

---

## 6. Understanding Complaint Data

### Categories

| Category | Covers |
|----------|--------|
| Roads | Potholes, road damage, dividers, signage |
| Water Supply | Supply disruptions, pipeline bursts, contamination |
| Electricity | Streetlights, power cuts, exposed wiring |
| Sanitation | Garbage overflow, drainage, open defecation |
| Encroachment | Footpath blockages, illegal construction |
| Parks | Broken equipment, maintenance issues |
| Other | Anything that doesn't fit above |

### Priority Levels

| Priority | Icon | Meaning |
|----------|------|---------|
| Critical | 🔴 | Immediate safety risk or large-scale disruption |
| High | 🟠 | Significant impact, needs attention within 24 hours |
| Medium | 🟡 | Moderate issue, normal queue |
| Low | 🟢 | Minor inconvenience, can be scheduled |

---

## 7. Demo Mode (No API Keys)

If you haven't set up API keys, CivicLens still works in **Demo Mode**:

- The app loads **5 pre-loaded sample complaints** from `assets/sample_data.json`
- Submitted complaints use a **fallback AI response** (category: Roads, priority: Medium)
- The map shows a **placeholder message** instead of the live heatmap
- All navigation, filtering, tracking, and status-update features work normally

This lets you explore the full UI without requiring API credentials.

---

## 8. FAQ

**Q: I submitted a complaint but lost my ID. How do I find it?**
Complaint IDs are shown on screen immediately after submission. If you missed it, there is currently no account-based lookup — note your ID at time of submission.

**Q: Why does my location show as "Hyderabad, Telangana" instead of my street?**
This happens when the Google Maps API key is not configured, or the address string was too vague to geocode precisely. Try adding a landmark or PIN code.

**Q: The AI gave my complaint the wrong category. Can I change it?**
Currently, categories are set by the AI at submission time. Government officials can filter and act on complaints by department regardless of category. Manual override is a planned feature.

**Q: Why isn't the heatmap loading?**
Check that your `GOOGLE_MAPS_API_KEY` is set in `.env`, the Maps JavaScript API and Visualization library are enabled in Google Cloud Console, and there are no domain restrictions on your API key for localhost.

**Q: Does CivicLens store my data permanently?**
No. CivicLens uses Streamlit's session state for storage. Data is lost when the server restarts. This is a hackathon demo — a production version would use a persistent database.

**Q: Can I submit complaints in Telugu?**
Yes. Type your complaint in Telugu in the description field. Gemini AI understands Telugu and will process it correctly.
