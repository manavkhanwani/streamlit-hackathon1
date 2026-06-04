# CivicLens — User Manual

**Version:** 1.0 | **Team:** BogControls

---

## For Citizens

### Submitting a Complaint

1. Open CivicLens and select **🗣️ Submit a Complaint** from the sidebar
2. **Describe the issue** — type a clear description in English or Telugu
3. **Enter your location** — use plain English (e.g., "Road No. 36, Jubilee Hills")
4. **Attach a photo** (optional) — JPG or PNG format
5. Click **🚀 Submit Complaint**

After submission you will see:
- Your unique **Complaint ID** (e.g., `CL-A1B2C3`) — save this!
- The AI-assigned **Category**, **Priority**, and **Department**
- A one-line **AI Summary** of your complaint
- The **resolved address** from geocoding

### Tracking Your Complaint

1. Select **🔍 Track Complaint** from the sidebar
2. Enter your **Complaint ID** (e.g., `CL-001` or `CL-A1B2C3`)
3. Click **Track**

You will see a progress indicator showing your complaint's current stage:

```
✅ Open  →  🔵 In Progress ← Current  →  ⬜ Resolved
```

---

## For Government Officials

### Dashboard Overview

Select **📊 Government Dashboard** from the sidebar.

**KPI Metrics** at the top show:
- Total complaints across all statuses
- Count of Open, In Progress, and Resolved complaints

**Complaint Heatmap** shows geographic concentration of complaints across Hyderabad (requires Google Maps API key).

### Filtering Complaints

Use the three dropdowns to filter:
- **Category:** Roads, Water Supply, Electricity, Sanitation, Encroachment, Parks, Other
- **Priority:** Critical 🔴, High 🟠, Medium 🟡, Low 🟢
- **Status:** Open 🔵, In Progress 🟡, Resolved ✅

### Updating a Complaint Status

1. Click on a complaint card to expand it
2. Select the new status from the **Update Status** dropdown
3. Click **💾 Save** to confirm

The KPI counters refresh automatically after saving.

---

## Priority Guide

| Priority | Meaning | Response Target |
|----------|---------|----------------|
| 🔴 Critical | Immediate safety risk or large-scale disruption | Immediate |
| 🟠 High | Significant impact — needs attention within 24 hours | Same day |
| 🟡 Medium | Moderate issue — normal processing queue | Within a week |
| 🟢 Low | Minor inconvenience — schedule when available | Routine |

---

## Demo Mode

When no API keys are configured, CivicLens runs in **Demo Mode**:
- 5 pre-loaded sample complaints covering Hyderabad locations
- All UI features (filtering, tracking, status updates) work normally
- AI analysis uses rule-based fallbacks instead of Gemini
- Map heatmap is replaced by a placeholder message
