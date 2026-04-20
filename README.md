# 🏏 CricBuzz LiveStats Dashboard

A comprehensive cricket analytics dashboard built with Python and Streamlit, integrating live data from the Cricbuzz API with a SQLite database.

---

## 📌 Project Overview

CricBuzz LiveStats is a multi-page web application that delivers:
- ⚡ Real-time match updates via RapidAPI
- 📊 Detailed player statistics from local database
- 🔍 25 SQL-driven analytics queries (Beginner to Advanced)
- 🛠️ Full CRUD operations for data management

---

## 🗂️ Project Structure

```
cricbuzz_livestats/
├── config/
│   └── settings.py          # API keys, DB path, constants
├── services/
│   ├── match_service.py     # API calls + caching logic
│   └── player_service.py    # Player data service
├── pages/
│   ├── home.py              # Dashboard home page
│   ├── live_matches.py      # Live match scorecards
│   ├── top_stats.py         # Top batting/bowling stats
│   ├── sql_queries.py       # 25 SQL analytics queries
│   └── crud_operations.py   # CRUD operations UI
├── utils/
│   ├── db_connection.py     # SQLite schema + sample data
│   └── cache.py             # JSON caching utilities
├── raw_cache/               # Cached API responses (auto-created)
├── app.py                   # Main Streamlit entry point
├── .env                     # API key + DB path (never commit)
├── requirements.txt         # Python dependencies
└── cricket.db               # SQLite database (auto-created)
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Souravdey96/cricbuzz-livestats.git
cd cricbuzz-livestats/cricbuzz_livestats
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the project root:
```
RAPIDAPI_KEY=your_rapidapi_key_here
DB_PATH=cricket.db
```

Get your free API key from: https://rapidapi.com - Search "Cricbuzz Cricket" and subscribe to the free tier.

### 4. Initialize the Database
```bash
python utils/db_connection.py
```

### 5. Run the App
```bash
streamlit run app.py
```

Open your browser at: http://localhost:8501

---

## 📦 Requirements

```
streamlit
requests
pandas
sqlalchemy
python-dotenv
```

---

## 🌐 API Configuration

This project uses the Cricbuzz Cricket API from RapidAPI.

| Setting | Value |
|---------|-------|
| Host | cricbuzz-cricket.p.rapidapi.com |
| Endpoint | GET /matches/v1/recent |
| Scorecard | GET /mcenter/v1/{matchId}/hscard |
| Free Tier | 500 calls/month |

The app automatically caches every API response, skips calls if cached data exists, blocks calls at 450/500 usage, and resets the counter each month.

---

## 📄 Pages

### Home
Live metrics showing Total Matches, Players, and Series from the database, along with tools overview and navigation guide.

### Live Matches
Fetches real-time matches from Cricbuzz API. Shows expandable match cards with team, venue, and status. Full scorecard with batting and bowling tables per innings.

### Top Stats
Six stat categories: Most Runs, Highest Score, Best Strike Rate, Most Wickets, Best Economy, Most Matches. Interactive bar chart visualization from local SQLite database.

### SQL Analytics
25 complete SQL queries across 3 difficulty levels. Beginner (Q1-Q8) covers SELECT, WHERE, GROUP BY. Intermediate (Q9-Q16) covers JOINs and aggregations. Advanced (Q17-Q25) covers window functions, CTEs, and statistical analysis. Includes a custom SQL editor.

### CRUD Operations
Add Player, View/Edit Players, Delete Player with confirmation, and Add Match — all with form-based UI.

---

## 🗄️ Database Schema

| Table | Description |
|-------|-------------|
| players | Player profiles: name, country, role, batting/bowling style |
| matches | Match details: teams, venue, result, toss info |
| series | Series info: name, format, dates |
| batsman_stats | Per-innings batting: runs, balls, 4s, 6s, strike rate |
| bowler_stats | Per-innings bowling: overs, wickets, economy, maidens |
| venues | Venue details: name, city, country, capacity |

---

## 🔒 Security Notes

- Never commit your .env file to GitHub
- Add .env and raw_cache/ to .gitignore
- Regenerate your RapidAPI key if accidentally exposed

---

## 🚀 Deployment on Streamlit Cloud

1. Push code to GitHub (without .env)
2. Go to share.streamlit.io
3. Connect your GitHub repo
4. Add secrets in Streamlit Cloud dashboard:
   RAPIDAPI_KEY = "your_key_here"
5. Deploy

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core language |
| Streamlit | Web dashboard framework |
| SQLite | Local database |
| RapidAPI Cricbuzz | Live cricket data |
| Pandas | Data manipulation |
| python-dotenv | Environment variables |

---

## 👨‍💻 Author

Sourav Dey
- LinkedIn: linkedin.com/in/souravdey1996
- GitHub: github.com/Souravdey96
- Email: jobsforsourav831@gmail.com
