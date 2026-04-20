import streamlit as st
import sqlite3
from config.settings import DB_PATH

def main():
    # Styled HTML banner
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FF4B4B, #1A1F2E); 
    padding: 40px; border-radius: 15px; text-align: center; margin-bottom: 20px;">
        <h1 style="color: white; font-size: 3em; margin: 0;">🏏 CricBuzz LiveStats</h1>
        <p style="color: #FFD700; font-size: 1.2em;">Real-time Cricket Analytics Platform</p>
    </div>
    """, unsafe_allow_html=True)

    # Metric cards with styled HTML
    col1, col2, col3 = st.columns(3)
    
    try:
        conn = sqlite3.connect(DB_PATH)
        total_matches = conn.execute("SELECT COUNT(*) FROM matches").fetchone()[0]
        total_players = conn.execute("SELECT COUNT(*) FROM players").fetchone()[0]
        total_series = conn.execute("SELECT COUNT(*) FROM series").fetchone()[0]
        conn.close()
    except Exception as e:
        total_matches = 0
        total_players = 0
        total_series = 0
        st.error(f"Failed to load metrics: {e}")
    
    with col1:
        st.markdown(f"""
        <div style="background:#1A1F2E; border-left: 4px solid #FF4B4B; 
        padding:20px; border-radius:10px; text-align:center;">
            <h2 style="color:#FF4B4B; margin:0;">{total_matches}</h2>
            <p style="color:white; margin:0;">Total Matches</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background:#1A1F2E; border-left: 4px solid #4B9EFF; 
        padding:20px; border-radius:10px; text-align:center;">
            <h2 style="color:#4B9EFF; margin:0;">{total_players}</h2>
            <p style="color:white; margin:0;">Total Players</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background:#1A1F2E; border-left: 4px solid #4BFF91; 
        padding:20px; border-radius:10px; text-align:center;">
            <h2 style="color:#4BFF91; margin:0;">{total_series}</h2>
            <p style="color:white; margin:0;">Total Series</p>
        </div>
        """, unsafe_allow_html=True)

    # Tools Used
    st.header("🛠️ Tools Used")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown("**Python**")
    with col2:
        st.markdown("**Streamlit**")
    with col3:
        st.markdown("**SQLite**")
    with col4:
        st.markdown("**RapidAPI**")
    with col5:
        st.markdown("**Pandas**")

    # Navigate (same tab — query_params + rerun, not markdown links)
    st.header("📌 Navigate")
    st.caption("Use the top bar, or jump from here:")
    h1, h2, h3, h4 = st.columns(4)
    with h1:
        if st.button("🏏 Live Matches", key="home_go_live", use_container_width=True):
            st.query_params["page"] = "live"
            st.rerun()
    with h2:
        if st.button("📊 Top Stats", key="home_go_stats", use_container_width=True):
            st.query_params["page"] = "stats"
            st.rerun()
    with h3:
        if st.button("🔍 SQL Analytics", key="home_go_sql", use_container_width=True):
            st.query_params["page"] = "sql"
            st.rerun()
    with h4:
        if st.button("🛠️ CRUD", key="home_go_crud", use_container_width=True):
            st.query_params["page"] = "crud"
            st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("Built with ❤️ using Python & Streamlit")