# 🏛️ CivicLens — Unified Civic Complaint Platform

> **"See the City Clearly"** — An AI-powered civic complaint platform for Hyderabad & Telangana

---

## 📋 Hackathon Submission

| Field | Details |
|-------|---------|
| **Hackathon** | CivicTech Hackathon |
| **Focus Area** | Hyderabad City / Telangana State |
| **Team Size** | 3 Members |
| **Tech Stack** | Google Gemini API · Google Maps API · Streamlit |

---

## 🚨 Problem Statement

Citizens of Hyderabad and Telangana face a **fragmented system** when reporting civic issues — potholes, garbage overflow, broken streetlights, water supply failures, encroachments, and more.

- Complaints are scattered across GHMC portals, Twitter, WhatsApp groups, and helpline numbers
- There is **no unified view**, no intelligent categorization, and no accountability loop
- Government departments receive unstructured data that is hard to act on

---

## 💡 Solution Overview

**CivicLens** (meaning *See the City Clearly*) is a unified, AI-powered civic complaint platform where:

- 🗣️ Citizens submit complaints in **text, voice, or photo**
- 🤖 **Google Gemini** auto-categorizes, prioritizes, and summarizes complaints
- 🗺️ **Google Maps** geo-tags each complaint and renders a live heatmap of civic issues
- 📊 A **Government Dashboard** provides a structured, filterable view for officials to act on

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                    CivicLens                       │
├──────────────────┬──────────────────────────────────┤
│  Citizen Portal  │       Government Dashboard        │
│  ─────────────  │  ──────────────────────────────  │
│  · Text input   │  · Filter by category/area        │
│  · Voice input  │  · Priority queue                 │
│  · Photo upload │  · Complaint heatmap              │
│  · Location tag │  · Status update controls         │
└────────┬─────────┴──────────────┬────────────────────┘
         │                        │
         ▼                        ▼
  ┌─────────────┐        ┌──────────────┐
  │ Gemini API  │        │ Maps API     │
  │ · Category  │        │ · Geo-tag    │
  │ · Priority  │        │ · Heatmap    │
  │ · Summary   │        │ · Clustering │
  └─────────────┘        └──────────────┘
```

---

## ✨ Key Features

### For Citizens
- **Multi-modal complaint submission** — type, speak, or photograph the issue
- **Auto-categorization** — Gemini AI classifies into Roads, Water, Electricity, Sanitation, Encroachment, etc.
- **Real-time status tracking** — know when your complaint is acknowledged and resolved
- **Multilingual support** — submit complaints in Telugu or English

### For Government Officials
- **Unified dashboard** — all complaints in one place, no more fragmented channels
- **AI-generated summaries** — structured, actionable complaint data
- **Priority scoring** — AI flags urgent/high-impact issues automatically
- **Heatmap visualization** — identify civic hotspots across Hyderabad zones
- **One-click status updates** — close the accountability loop with citizens

---

## 📁 Project Structure

```
civiclens/
├── app.py                  # Main Streamlit application entry point
├── pages/
│   ├── citizen_portal.py   # Citizen complaint submission page
│   ├── dashboard.py        # Government officials dashboard
│   └── track.py            # Complaint tracking page
├── components/
│   ├── complaint_form.py   # Complaint submission form component
│   ├── heatmap.py          # Google Maps heatmap component
│   └── complaint_card.py   # Individual complaint display card
├── utils/
│   ├── gemini_helper.py    # Google Gemini API integration
│   ├── maps_helper.py      # Google Maps API integration
│   └── data_store.py       # In-memory data management
├── assets/
│   └── sample_data.json    # Sample complaints for demo
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── README.md               # This file (submission overview)
└── SETUP.md                # Setup & running instructions
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Streamlit | Rapid UI for citizen portal & dashboard |
| **AI/ML** | Google Gemini 1.5 Flash | Complaint categorization, prioritization, summarization |
| **Maps** | Google Maps API | Geo-tagging, heatmap rendering, location search |
| **Data** | Session State + JSON | Lightweight in-memory store (demo) |
| **Language** | Python 3.10+ | Core application logic |

---

## 🎯 Impact

- **Reduces response time** by routing complaints to the right department instantly
- **Eliminates duplicate complaints** through AI deduplication
- **Creates accountability** with a closed feedback loop between citizens and officials
- **Data-driven governance** — heatmaps reveal infrastructure patterns city-wide

---

## 👥 Team

Built for Hyderabad by BogControls


- Manav → AI & Backend (Gemini, categorization, data)
- Aniket → Frontend & UX (all Streamlit pages, navigation)
- Aryan → Maps & Infrastructure (Google Maps, geo-tagging, setup)