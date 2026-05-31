# 🤝 Contributing — CivicLens

## Team

CivicLens was built by a three-member team for the CivicTech Hackathon. All members contributed equally to the project.

---

## 👥 Team Members & Contributions

### Aniket
**Role:** AI/ML Integration & Backend Logic

- Designed and implemented the **Gemini AI pipeline** (`utils/gemini_helper.py`) — prompt engineering, complaint categorization, priority scoring, and AI summary generation
- Built the **data store layer** (`utils/data_store.py`) — session-state management, complaint CRUD operations, and statistics aggregation
- Integrated **image analysis** support: multi-modal complaint submission using Gemini Vision
- Authored `SETUP.md` and the troubleshooting guide
- Contributed to `assets/sample_data.json` (complaint schemas and demo data)

---

### Manav
**Role:** Maps Integration & Citizen Portal

- Built the **Google Maps integration** (`utils/maps_helper.py`) — geocoding, reverse geocoding, and heatmap HTML generation
- Developed the **Citizen Portal** (`pages/citizen_portal.py`) — complaint submission form, AI-result display, and location resolution flow
- Integrated the **live heatmap** into the Government Dashboard using Maps JavaScript API with Visualization library
- Designed the overall **app routing and sidebar navigation** (`app.py`)
- Contributed to the project architecture diagram in `README.md`

---

### Aryan
**Role:** Dashboard, Tracking & Product Design

- Built the **Government Dashboard** (`pages/dashboard.py`) — complaint listing, filters (category/priority/status), status update controls, and KPI metrics
- Built the **Complaint Tracking page** (`pages/track.py`) — complaint ID lookup and step-by-step progress indicator
- Drove overall **UI/UX decisions**: layout, color-coded priority/status icons, and responsive column structure
- Authored the main `README.md` (problem statement, solution overview, feature list, tech stack table)
- Managed `requirements.txt`, environment config, and demo mode fallbacks

---

## Contribution Summary

| Area | Aniket | Manav | Aryan |
|------|--------|-------|-------|
| Gemini AI integration | ✅ Lead | | Support |
| Google Maps integration | | ✅ Lead | |
| Citizen Portal UI | | ✅ Lead | Support |
| Government Dashboard | Support | | ✅ Lead |
| Complaint Tracking | | | ✅ Lead |
| Data store & state management | ✅ Lead | | |
| App routing & config | | ✅ Lead | |
| UI/UX design | | Support | ✅ Lead |
| Documentation (README, SETUP) | Support | Support | ✅ Lead |
| Sample data & demo mode | ✅ Lead | | Support |

> All members participated in ideation, system design, testing, and the final presentation.

---

## How to Contribute (Post-Hackathon)

We welcome contributions! To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes with clear messages
4. Open a Pull Request with a description of what you changed and why

Please ensure your code follows the existing style and that new features include a brief update to the relevant docs.

---

## Code of Conduct

Be respectful, constructive, and collaborative. This project was built in a hackathon spirit — keep it fun and inclusive.
