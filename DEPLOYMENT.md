# Streamlit Cloud Deployment

## App Location

- **Repository**: `Souravdey96/cricbuzz-livestats`
- **Main file path**: `cricbuzz_livestats/app.py`

## Required Secrets

Set these in Streamlit Cloud at **App Settings -> Secrets**:

```toml
RAPIDAPI_KEY = "your-rapidapi-key"
DB_PATH = "cricket.db"
```

## Notes

- The app auto-creates and seeds SQLite tables on first run.
- `cricket.db` is intentionally ignored by Git and generated at runtime.
- If `RAPIDAPI_KEY` is not set, live endpoints return cached or empty data.

## Local Run

From repository root:

```bash
pip install -r requirements.txt
streamlit run cricbuzz_livestats/app.py
```
