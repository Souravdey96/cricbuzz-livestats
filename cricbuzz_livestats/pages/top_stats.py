import streamlit as st
import sqlite3
import pandas as pd
from config.settings import DB_PATH

def main():
    st.markdown("""
    <style>
    .top-player-card {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        color: black;
        font-weight: bold;
    }
    .tab-content {
        background: #1A1F2E;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("📊 Top Player Stats")

    queries = {
        "Most Runs": "SELECT player_name, SUM(runs) as total_runs FROM batsman_stats GROUP BY player_name ORDER BY total_runs DESC LIMIT 10",
        "Highest Score": "SELECT player_name, MAX(runs) as highest_score FROM batsman_stats GROUP BY player_name ORDER BY highest_score DESC LIMIT 10",
        "Best Strike Rate": "SELECT player_name, ROUND(AVG(strike_rate), 2) as avg_strike_rate FROM batsman_stats WHERE balls >= 10 GROUP BY player_name ORDER BY avg_strike_rate DESC LIMIT 10",
        "Most Wickets": "SELECT player_name, SUM(wickets) as total_wickets FROM bowler_stats GROUP BY player_name ORDER BY total_wickets DESC LIMIT 10",
        "Best Economy": "SELECT player_name, ROUND(AVG(economy), 2) as avg_economy FROM bowler_stats WHERE overs >= 5 GROUP BY player_name ORDER BY avg_economy ASC LIMIT 10",
        "Most Matches Played": "SELECT player_name, COUNT(DISTINCT match_id) as matches_played FROM batsman_stats GROUP BY player_name ORDER BY matches_played DESC LIMIT 10"
    }

    tabs = st.tabs(list(queries.keys()))

    for i, (tab_name, query) in enumerate(queries.items()):
        with tabs[i]:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            try:
                conn = sqlite3.connect(DB_PATH)
                df = pd.read_sql(query, conn)
                conn.close()
                
                if not df.empty:
                    # Top player highlight
                    top_player = df.iloc[0]
                    st.markdown(f"""
                    <div class="top-player-card">
                        <h3>🥇 {top_player['player_name']}</h3>
                        <h2>{top_player[df.columns[1]]}</h2>
                        <p>{df.columns[1].replace('_', ' ').title()}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Table with alternating colors
                    st.dataframe(df.style.set_table_styles([
                        {'selector': 'tr:nth-child(even)', 'props': [('background-color', '#1A1F2E')]},
                        {'selector': 'tr:nth-child(odd)', 'props': [('background-color', '#0E1117')]}
                    ]))
                    
                    # Bar chart
                    chart_col = df.columns[1]
                    st.bar_chart(df.set_index('player_name')[chart_col], color="#FF4B4B")
                else:
                    st.write("No data available for this category.")
            except Exception as e:
                st.error(f"Error loading data: {e}")
            st.markdown('</div>', unsafe_allow_html=True)

    st.info("Showing data from local database")