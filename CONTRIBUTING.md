# CivicLens — Contributing Guide

**Team:** BogControls

---

## Development Setup

```bash
git clone https://github.com/YOUR_ORG/civiclens.git
cd civiclens
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # Add your API keys
streamlit run app.py
```

---

## Project Structure

```
civiclens/
├── app.py                  # Entry point — do not add business logic here
├── _pages/                 # One module per page; each exports show()
├── utils/                  # AI, Maps, data store — stateless helpers
└── assets/                 # Static files (sample_data.json)
```

---

## Code Style

- Python 3.9+ compatible
- Type hints on all public functions
- Docstrings on every module and public function
- All external API calls wrapped in try/except with fallback returns
- No secrets in source code — use `.env` only

---

## Adding a New Page

1. Create `_pages/your_page.py` with a `show()` function
2. Import it in `app.py`
3. Add a radio option in the sidebar
4. Add a routing `elif` block

---

## Testing

Run the app in demo mode to verify:
- Complaint submission flow (no API keys required)
- Dashboard filtering and status updates
- Complaint tracking with IDs from `assets/sample_data.json`

---

## Submitting Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes with descriptive messages
4. Open a pull request against `main`
