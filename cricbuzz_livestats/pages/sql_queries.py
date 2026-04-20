import sqlite3

import pandas as pd
import streamlit as st

from config.settings import DB_PATH


def main():
    st.markdown(
        """
    <style>
    .sidebar-panel {
        background: #1A1F2E;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .question-item {
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-radius: 5px;
        cursor: pointer;
        transition: background 0.3s;
    }
    .question-item:hover { background: #2A2F3E; }
    .question-selected { background: #FF4B4B !important; color: white; }
    .sql-code {
        background: #0E1117;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #FF4B4B;
        font-family: monospace;
    }
    .results-table {
        background: #1A1F2E;
        border-radius: 10px;
        padding: 1rem;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.title("🔍 SQL Queries & Analytics")

    queries = {
        "Q1": "SELECT name, role, batting_style, bowling_style FROM players WHERE country = 'India'",
        "Q2": "SELECT match_desc, team1, team2, venue, city, match_date FROM matches WHERE match_date >= DATE('now', '-30 days') ORDER BY match_date DESC",
        "Q3": "SELECT player_name, SUM(runs) as total_runs, ROUND(AVG(runs),2) as avg, COUNT(CASE WHEN runs >= 100 THEN 1 END) as centuries FROM batsman_stats JOIN matches ON batsman_stats.match_id = matches.match_id WHERE matches.match_desc LIKE '%ODI%' GROUP BY player_name ORDER BY total_runs DESC LIMIT 10",
        "Q4": "SELECT name, city, country, capacity FROM venues WHERE capacity > 50000 ORDER BY capacity DESC",
        "Q5": "SELECT winner, COUNT(*) as total_wins FROM matches WHERE winner IS NOT NULL GROUP BY winner ORDER BY total_wins DESC",
        "Q6": "SELECT role, COUNT(*) as total_players FROM players GROUP BY role ORDER BY total_players DESC",
        "Q7": "SELECT match_desc as format, MAX(runs) as highest_score FROM batsman_stats JOIN matches ON batsman_stats.match_id = matches.match_id GROUP BY match_desc",
        "Q8": "SELECT series_name, match_type, start_date, total_matches FROM series WHERE strftime('%Y', start_date) = '2024'",
        "Q9": "SELECT p.name, SUM(b.runs) as total_runs, SUM(bw.wickets) as total_wickets FROM players p JOIN batsman_stats b ON p.name = b.player_name JOIN bowler_stats bw ON p.name = bw.player_name WHERE p.role = 'All-rounder' GROUP BY p.name HAVING total_runs > 1000 AND total_wickets > 50",
        "Q10": "SELECT match_desc, team1, team2, winner, victory_margin, victory_type, venue FROM matches WHERE winner IS NOT NULL ORDER BY match_date DESC LIMIT 20",
        "Q11": "SELECT player_name, SUM(CASE WHEN match_desc LIKE '%Test%' THEN runs ELSE 0 END) as test_runs, SUM(CASE WHEN match_desc LIKE '%ODI%' THEN runs ELSE 0 END) as odi_runs, SUM(CASE WHEN match_desc LIKE '%T20%' THEN runs ELSE 0 END) as t20_runs, ROUND(AVG(runs), 2) as overall_avg FROM batsman_stats JOIN matches ON batsman_stats.match_id = matches.match_id GROUP BY player_name HAVING COUNT(DISTINCT match_desc) >= 2",
        "Q12": "SELECT m.team1 as team, SUM(CASE WHEN m.winner = m.team1 THEN 1 ELSE 0 END) as home_wins, SUM(CASE WHEN m.winner = m.team2 THEN 1 ELSE 0 END) as away_wins FROM matches m GROUP BY m.team1",
        "Q13": "WITH partnerships AS (SELECT b1.inning_id, b1.player_name as batsman1, b2.player_name as batsman2, b1.runs + b2.runs as partnership_runs FROM batsman_stats b1 JOIN batsman_stats b2 ON b1.inning_id = b2.inning_id AND b1.rowid + 1 = b2.rowid) SELECT batsman1, batsman2, partnership_runs, inning_id FROM partnerships WHERE partnership_runs >= 100",
        "Q14": "SELECT bw.player_name, m.venue, ROUND(AVG(bw.economy), 2) as avg_economy, SUM(bw.wickets) as total_wickets, COUNT(*) as matches_played FROM bowler_stats bw JOIN matches m ON bw.match_id = m.match_id WHERE bw.overs >= 4 GROUP BY bw.player_name, m.venue HAVING matches_played >= 3",
        "Q15": "SELECT b.player_name, ROUND(AVG(b.runs), 2) as avg_runs_close, COUNT(*) as close_matches FROM batsman_stats b JOIN matches m ON b.match_id = m.match_id WHERE (m.victory_type = 'runs' AND CAST(m.victory_margin AS INT) < 50) OR (m.victory_type = 'wickets' AND CAST(m.victory_margin AS INT) < 5) GROUP BY b.player_name",
        "Q16": "SELECT player_name, strftime('%Y', match_date) as year, ROUND(AVG(runs), 2) as avg_runs, ROUND(AVG(strike_rate), 2) as avg_strike_rate, COUNT(*) as matches FROM batsman_stats JOIN matches ON batsman_stats.match_id = matches.match_id WHERE strftime('%Y', match_date) >= '2020' GROUP BY player_name, year HAVING matches >= 5",
        "Q17": "SELECT toss_decision, COUNT(*) as total_matches, SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) as toss_wins, ROUND(100.0 * SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) / COUNT(*), 2) as win_percentage FROM matches GROUP BY toss_decision",
        "Q18": "SELECT player_name, ROUND(AVG(economy), 2) as avg_economy, SUM(wickets) as total_wickets, COUNT(*) as matches FROM bowler_stats JOIN matches ON bowler_stats.match_id = matches.match_id WHERE match_desc LIKE '%ODI%' OR match_desc LIKE '%T20%' GROUP BY player_name HAVING matches >= 10 AND AVG(overs) >= 2",
        "Q19": "SELECT player_name, ROUND(AVG(runs), 2) as avg_runs, ROUND(SQRT(AVG(runs * runs) - AVG(runs) * AVG(runs)), 2) as std_dev, COUNT(*) as innings FROM batsman_stats JOIN matches ON batsman_stats.match_id = matches.match_id WHERE balls >= 10 AND match_date >= '2022-01-01' GROUP BY player_name HAVING innings >= 5 ORDER BY std_dev ASC",
        "Q20": "SELECT player_name, COUNT(CASE WHEN match_desc LIKE '%Test%' THEN 1 END) as test_matches, COUNT(CASE WHEN match_desc LIKE '%ODI%' THEN 1 END) as odi_matches, COUNT(CASE WHEN match_desc LIKE '%T20%' THEN 1 END) as t20_matches, ROUND(AVG(CASE WHEN match_desc LIKE '%Test%' THEN runs END), 2) as test_avg, ROUND(AVG(CASE WHEN match_desc LIKE '%ODI%' THEN runs END), 2) as odi_avg, ROUND(AVG(CASE WHEN match_desc LIKE '%T20%' THEN runs END), 2) as t20_avg FROM batsman_stats JOIN matches ON batsman_stats.match_id = matches.match_id GROUP BY player_name HAVING (test_matches + odi_matches + t20_matches) >= 20",
        "Q21": "SELECT p.name, ROUND((COALESCE(SUM(b.runs),0) * 0.01) + (COALESCE(AVG(b.runs),0) * 0.5) + (COALESCE(AVG(b.strike_rate),0) * 0.3) + (COALESCE(SUM(bw.wickets),0) * 2) + ((50 - COALESCE(AVG(bw.economy),0)) * 0.5) + ((6 - COALESCE(AVG(bw.economy),0)) * 2), 2) as performance_score, m.match_desc as format FROM players p LEFT JOIN batsman_stats b ON p.name = b.player_name LEFT JOIN bowler_stats bw ON p.name = bw.player_name LEFT JOIN matches m ON b.match_id = m.match_id GROUP BY p.name, format ORDER BY performance_score DESC",
        "Q22": "SELECT team1, team2, COUNT(*) as total_matches, SUM(CASE WHEN winner = team1 THEN 1 ELSE 0 END) as team1_wins, SUM(CASE WHEN winner = team2 THEN 1 ELSE 0 END) as team2_wins, ROUND(100.0 * SUM(CASE WHEN winner = team1 THEN 1 ELSE 0 END) / COUNT(*), 2) as team1_win_pct FROM matches WHERE match_date >= DATE('now', '-3 years') GROUP BY team1, team2 HAVING total_matches >= 3",
        "Q23": "WITH recent AS (SELECT player_name, runs, strike_rate, match_date, ROW_NUMBER() OVER (PARTITION BY player_name ORDER BY match_date DESC) as rn FROM batsman_stats JOIN matches ON batsman_stats.match_id = matches.match_id) SELECT player_name, ROUND(AVG(CASE WHEN rn <= 5 THEN runs END), 2) as last_5_avg, ROUND(AVG(CASE WHEN rn <= 10 THEN runs END), 2) as last_10_avg, COUNT(CASE WHEN rn <= 10 AND runs >= 50 THEN 1 END) as fifties_last_10, CASE WHEN AVG(CASE WHEN rn <= 5 THEN runs END) >= 50 THEN 'Excellent Form' WHEN AVG(CASE WHEN rn <= 5 THEN runs END) >= 35 THEN 'Good Form' WHEN AVG(CASE WHEN rn <= 5 THEN runs END) >= 20 THEN 'Average Form' ELSE 'Poor Form' END as form_category FROM recent GROUP BY player_name",
        "Q24": "WITH pairs AS (SELECT b1.player_name as p1, b2.player_name as p2, b1.runs + b2.runs as partnership_runs FROM batsman_stats b1 JOIN batsman_stats b2 ON b1.inning_id = b2.inning_id AND b1.rowid + 1 = b2.rowid) SELECT p1, p2, COUNT(*) as total_partnerships, ROUND(AVG(partnership_runs), 2) as avg_partnership, MAX(partnership_runs) as highest_partnership, COUNT(CASE WHEN partnership_runs >= 50 THEN 1 END) as good_partnerships, ROUND(100.0 * COUNT(CASE WHEN partnership_runs >= 50 THEN 1 END) / COUNT(*), 2) as success_rate FROM pairs GROUP BY p1, p2 HAVING total_partnerships >= 3 ORDER BY avg_partnership DESC",
        "Q25": "WITH quarterly AS (SELECT player_name, strftime('%Y', match_date) || '-Q' || CAST((CAST(strftime('%m', match_date) AS INT) + 2) / 3 AS TEXT) as quarter, AVG(runs) as avg_runs, AVG(strike_rate) as avg_sr, COUNT(*) as matches FROM batsman_stats JOIN matches ON batsman_stats.match_id = matches.match_id GROUP BY player_name, quarter HAVING matches >= 1), trajectory AS (SELECT player_name, quarter, avg_runs, LAG(avg_runs) OVER (PARTITION BY player_name ORDER BY quarter) as prev_avg, COUNT(*) OVER (PARTITION BY player_name) as total_quarters FROM quarterly) SELECT player_name, quarter, ROUND(avg_runs, 2) as avg_runs, CASE WHEN avg_runs > COALESCE(prev_avg,0) * 1.1 THEN 'Improving' WHEN avg_runs < COALESCE(prev_avg,0) * 0.9 THEN 'Declining' ELSE 'Stable' END as trend, CASE WHEN AVG(avg_runs) OVER (PARTITION BY player_name) > 40 THEN 'Career Ascending' WHEN AVG(avg_runs) OVER (PARTITION BY player_name) < 25 THEN 'Career Declining' ELSE 'Career Stable' END as career_phase FROM trajectory WHERE total_quarters >= 1",
    }

    descriptions = {
        "Q1": "List all Indian players with their roles and batting/bowling styles.",
        "Q2": "Show matches from the last 30 days with details.",
        "Q3": "Top 10 ODI batsmen by total runs and centuries.",
        "Q4": "Venues with capacity over 50,000.",
        "Q5": "Teams ranked by total wins.",
        "Q6": "Count of players by role.",
        "Q7": "Highest individual scores by match format.",
        "Q8": "Series starting in 2024.",
        "Q9": "All-rounders with over 1000 runs and 50 wickets.",
        "Q10": "Recent match results with winners.",
        "Q11": "Players who played in multiple formats with runs breakdown.",
        "Q12": "Home and away win counts for teams.",
        "Q13": "Partnerships of 100+ runs.",
        "Q14": "Bowlers' performance at specific venues.",
        "Q15": "Batting averages in close matches.",
        "Q16": "Yearly batting averages since 2020.",
        "Q17": "Impact of toss decisions on match outcomes.",
        "Q18": "Top bowlers in limited-overs cricket.",
        "Q19": "Most consistent batsmen by standard deviation.",
        "Q20": "Multi-format players' statistics.",
        "Q21": "Player performance scores across formats.",
        "Q22": "Head-to-head records between teams.",
        "Q23": "Recent form analysis of batsmen.",
        "Q24": "Partnership statistics between player pairs.",
        "Q25": "Quarterly performance trends and career phases.",
    }

    st.markdown('<div class="sidebar-panel">', unsafe_allow_html=True)
    st.subheader("📋 Questions")

    def _label_q(qid):
        return f"{qid} — {descriptions[qid]}"

    selected_q = st.selectbox(
        "Select a predefined query",
        list(queries.keys()),
        format_func=_label_q,
        key="sql_predefined_select",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.info(descriptions[selected_q])
    st.markdown(f'<div class="sql-code"><pre>{queries[selected_q]}</pre></div>', unsafe_allow_html=True)

    if st.button("▶ Run Query"):
        try:
            conn = sqlite3.connect(DB_PATH)
            df = pd.read_sql(queries[selected_q], conn)
            conn.close()
            st.markdown('<div class="results-table">', unsafe_allow_html=True)
            st.dataframe(
                df.style.set_table_styles(
                    [
                        {"selector": "tr:nth-child(even)", "props": [("background-color", "#1A1F2E")]},
                        {"selector": "tr:nth-child(odd)", "props": [("background-color", "#0E1117")]},
                    ]
                )
            )
            st.markdown("</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Query failed: {e}")

    st.header("✏️ Write Your Own Query")
    custom_query = st.text_area("Enter your SQL query:")
    if st.button("▶ Run Custom Query"):
        if custom_query.strip():
            try:
                conn = sqlite3.connect(DB_PATH)
                df = pd.read_sql(custom_query, conn)
                conn.close()
                st.markdown('<div class="results-table">', unsafe_allow_html=True)
                st.dataframe(
                    df.style.set_table_styles(
                        [
                            {"selector": "tr:nth-child(even)", "props": [("background-color", "#1A1F2E")]},
                            {"selector": "tr:nth-child(odd)", "props": [("background-color", "#0E1117")]},
                        ]
                    )
                )
                st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Query failed: {e}")
        else:
            st.warning("Please enter a query.")
