import streamlit as st
import sqlite3
from config.settings import DB_PATH

def main():
    st.markdown("""
    <style>
    .form-card {
        background: #1A1F2E;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid #FF4B4B;
    }
    .success-banner {
        background: #4BFF9E;
        color: black;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-weight: bold;
    }
    .error-banner {
        background: #FF4B4B;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-weight: bold;
    }
    .stButton>button {
        background: #FF4B4B !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 0.5rem 2rem !important;
        font-weight: bold !important;
    }
    .stButton>button:hover {
        background: #E63946 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("🛠️ CRUD Operations")

    tab1, tab2, tab3, tab4 = st.tabs(["➕ Add Player", "➕ Add Match", "✏️ Update", "🗑️ Delete"])

    # Add Player Tab
    with tab1:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        st.header("Add New Player")
        
        with st.form("add_player_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Player Name")
                country = st.text_input("Country")
                role = st.selectbox("Role", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
            with col2:
                batting_style = st.selectbox("Batting Style", ["Right-handed", "Left-handed"])
                bowling_style = st.selectbox("Bowling Style", ["Right-arm fast", "Right-arm medium", "Left-arm fast", "Left-arm orthodox", "Off-break", "Leg-break", "None"])
            
            submitted = st.form_submit_button("Add Player")
            if submitted:
                if name and country:
                    try:
                        conn = sqlite3.connect(DB_PATH)
                        conn.execute("INSERT INTO players (name, country, role, batting_style, bowling_style) VALUES (?, ?, ?, ?, ?)",
                                   (name, country, role, batting_style, bowling_style))
                        conn.commit()
                        conn.close()
                        st.markdown('<div class="success-banner">✅ Player added successfully!</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f'<div class="error-banner">❌ Error adding player: {e}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-banner">❌ Please fill in all required fields.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Add Match Tab
    with tab2:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        st.header("Add New Match")
        
        with st.form("add_match_form"):
            col1, col2 = st.columns(2)
            with col1:
                match_desc = st.text_input("Match Description (e.g., ODI, Test)")
                team1 = st.text_input("Team 1")
                team2 = st.text_input("Team 2")
                venue = st.text_input("Venue")
            with col2:
                city = st.text_input("City")
                match_date = st.date_input("Match Date")
                winner = st.text_input("Winner (optional)")
                victory_margin = st.number_input("Victory Margin", min_value=0, step=1)
            
            victory_type = st.selectbox("Victory Type", ["runs", "wickets", "tie", "no result"])
            
            submitted = st.form_submit_button("Add Match")
            if submitted:
                if match_desc and team1 and team2 and venue and city:
                    try:
                        conn = sqlite3.connect(DB_PATH)
                        conn.execute("""INSERT INTO matches (match_desc, team1, team2, venue, city, match_date, winner, victory_margin, victory_type) 
                                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                   (match_desc, team1, team2, venue, city, match_date, winner or None, victory_margin, victory_type))
                        conn.commit()
                        conn.close()
                        st.markdown('<div class="success-banner">✅ Match added successfully!</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f'<div class="error-banner">❌ Error adding match: {e}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-banner">❌ Please fill in all required fields.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Update Tab
    with tab3:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        st.header("Update Records")
        
        update_type = st.selectbox("What to update?", ["Player", "Match"])
        
        if update_type == "Player":
            try:
                conn = sqlite3.connect(DB_PATH)
                players = conn.execute("SELECT player_id, name FROM players").fetchall()
                conn.close()
                
                player_options = {f"{p[1]} (ID: {p[0]})": p[0] for p in players}
                selected_player = st.selectbox("Select Player", list(player_options.keys()))
                
                if selected_player:
                    player_id = player_options[selected_player]
                    
                    with st.form("update_player_form"):
                        col1, col2 = st.columns(2)
                        with col1:
                            name = st.text_input("Player Name")
                            country = st.text_input("Country")
                            role = st.selectbox("Role", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
                        with col2:
                            batting_style = st.selectbox("Batting Style", ["Right-handed", "Left-handed"])
                            bowling_style = st.selectbox("Bowling Style", ["Right-arm fast", "Right-arm medium", "Left-arm fast", "Left-arm orthodox", "Off-break", "Leg-break", "None"])
                        
                        submitted = st.form_submit_button("Update Player")
                        if submitted:
                            try:
                                conn = sqlite3.connect(DB_PATH)
                                conn.execute("UPDATE players SET name=?, country=?, role=?, batting_style=?, bowling_style=? WHERE player_id=?",
                                           (name, country, role, batting_style, bowling_style, player_id))
                                conn.commit()
                                conn.close()
                                st.markdown('<div class="success-banner">✅ Player updated successfully!</div>', unsafe_allow_html=True)
                            except Exception as e:
                                st.markdown(f'<div class="error-banner">❌ Error updating player: {e}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error loading players: {e}")
        
        elif update_type == "Match":
            try:
                conn = sqlite3.connect(DB_PATH)
                matches = conn.execute("SELECT match_id, match_desc, team1, team2 FROM matches").fetchall()
                conn.close()
                
                match_options = {f"{m[1]}: {m[2]} vs {m[3]} (ID: {m[0]})": m[0] for m in matches}
                selected_match = st.selectbox("Select Match", list(match_options.keys()))
                
                if selected_match:
                    match_id = match_options[selected_match]
                    
                    with st.form("update_match_form"):
                        col1, col2 = st.columns(2)
                        with col1:
                            winner = st.text_input("Winner")
                            victory_margin = st.number_input("Victory Margin", min_value=0, step=1)
                        with col2:
                            victory_type = st.selectbox("Victory Type", ["runs", "wickets", "tie", "no result"])
                        
                        submitted = st.form_submit_button("Update Match")
                        if submitted:
                            try:
                                conn = sqlite3.connect(DB_PATH)
                                conn.execute("UPDATE matches SET winner=?, victory_margin=?, victory_type=? WHERE match_id=?",
                                           (winner, victory_margin, victory_type, match_id))
                                conn.commit()
                                conn.close()
                                st.markdown('<div class="success-banner">✅ Match updated successfully!</div>', unsafe_allow_html=True)
                            except Exception as e:
                                st.markdown(f'<div class="error-banner">❌ Error updating match: {e}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error loading matches: {e}")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Delete Tab
    with tab4:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        st.header("Delete Records")
        
        delete_type = st.selectbox("What to delete?", ["Player", "Match"])
        
        if delete_type == "Player":
            try:
                conn = sqlite3.connect(DB_PATH)
                players = conn.execute("SELECT player_id, name FROM players").fetchall()
                conn.close()
                
                player_options = {f"{p[1]} (ID: {p[0]})": p[0] for p in players}
                selected_player = st.selectbox("Select Player to Delete", list(player_options.keys()))
                
                if selected_player and st.button("🗑️ Delete Player"):
                    player_id = player_options[selected_player]
                    try:
                        conn = sqlite3.connect(DB_PATH)
                        conn.execute("DELETE FROM players WHERE player_id=?", (player_id,))
                        conn.commit()
                        conn.close()
                        st.markdown('<div class="success-banner">✅ Player deleted successfully!</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f'<div class="error-banner">❌ Error deleting player: {e}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error loading players: {e}")
        
        elif delete_type == "Match":
            try:
                conn = sqlite3.connect(DB_PATH)
                matches = conn.execute("SELECT match_id, match_desc, team1, team2 FROM matches").fetchall()
                conn.close()
                
                match_options = {f"{m[1]}: {m[2]} vs {m[3]} (ID: {m[0]})": m[0] for m in matches}
                selected_match = st.selectbox("Select Match to Delete", list(match_options.keys()))
                
                if selected_match and st.button("🗑️ Delete Match"):
                    match_id = match_options[selected_match]
                    try:
                        conn = sqlite3.connect(DB_PATH)
                        conn.execute("DELETE FROM matches WHERE match_id=?", (match_id,))
                        conn.commit()
                        conn.close()
                        st.markdown('<div class="success-banner">✅ Match deleted successfully!</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f'<div class="error-banner">❌ Error deleting match: {e}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error loading matches: {e}")
        
        st.markdown('</div>', unsafe_allow_html=True)