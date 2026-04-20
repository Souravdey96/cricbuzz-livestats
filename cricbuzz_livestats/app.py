import streamlit as st

from pages import crud_operations, home, live_matches, sql_queries, top_stats
from config.settings import RAPIDAPI_KEY
from utils.db_connection import ensure_database_ready

st.set_page_config(
    page_title="CricBuzz LiveStats",
    page_icon="🏏",
    layout="wide",
)

ensure_database_ready()

if not RAPIDAPI_KEY:
    st.info("`RAPIDAPI_KEY` is not configured. Live API features may show cached data only.")

st.markdown(
    """
<style>
    /* App shell: pink → purple gradient (mockup) */
    [data-testid="stAppViewContainer"],
    .stApp {
        background: linear-gradient(to right, #ff4d8d, #7e30e1) !important;
    }
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    [data-testid="stSidebarNav"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    .main > div { padding-top: 0rem !important; }
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* Coral “dashboard” panel behind main content */
    .main .block-container {
        background: rgba(255, 140, 105, 0.97);
        border-radius: 28px;
        padding: 1.5rem 1.75rem 2rem 1.75rem !important;
        margin-top: 0.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 12px 40px rgba(45, 39, 71, 0.25);
        max-width: 1180px;
    }

    /* Top nav row (first horizontal block in main content) */
    .main .block-container [data-testid="stHorizontalBlock"]:first-of-type {
        background: #2d2747;
        border-radius: 20px;
        padding: 10px 16px 14px 16px;
        margin-bottom: 8px;
        align-items: center;
        gap: 4px;
        flex-wrap: wrap !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    }
    .main .block-container [data-testid="stHorizontalBlock"]:first-of-type button {
        background: transparent !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: none !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
    }
    .main .block-container [data-testid="stHorizontalBlock"]:first-of-type button:hover {
        color: #ffb3d4 !important;
    }
    /* Brand = home link (first column) */
    .main .block-container [data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:first-child button {
        color: #000000 !important;
        font-size: 1.35rem !important;
        font-weight: 800 !important;
        text-align: left !important;
        padding: 4px 8px 0 4px !important;
    }
    .main .block-container [data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:first-child button:hover {
        color: #1a1a1a !important;
        text-decoration: underline !important;
    }
    .nav-profile-emoji {
        font-size: 1.35rem;
        text-align: center;
        padding-top: 6px;
    }
</style>
""",
    unsafe_allow_html=True,
)

page = st.query_params.get("page", "home")
if isinstance(page, list):
    page = page[0] if page else "home"

# Same-tab navigation: st.query_params + st.rerun (avoids <a href> opening a new tab)
n1, n2, n3, n4, n5, n6 = st.columns([2.4, 1.15, 1.15, 1.15, 1.15, 0.55])
with n1:
    if st.button("🏏 CricBuzz", key="nav_brand_home", type="tertiary", help="Back to home"):
        st.query_params["page"] = "home"
        st.rerun()
with n2:
    if st.button("🏏 Live", key="nav_live", type="tertiary"):
        st.query_params["page"] = "live"
        st.rerun()
with n3:
    if st.button("📊 Stats", key="nav_stats", type="tertiary"):
        st.query_params["page"] = "stats"
        st.rerun()
with n4:
    if st.button("🔍 SQL", key="nav_sql", type="tertiary"):
        st.query_params["page"] = "sql"
        st.rerun()
with n5:
    if st.button("🛠️ CRUD", key="nav_crud", type="tertiary"):
        st.query_params["page"] = "crud"
        st.rerun()
with n6:
    st.markdown('<p class="nav-profile-emoji" title="Profile">👤</p>', unsafe_allow_html=True)

if page == "home":
    home.main()
elif page == "live":
    live_matches.main()
elif page == "stats":
    top_stats.main()
elif page == "sql":
    sql_queries.main()
elif page == "crud":
    crud_operations.main()
else:
    home.main()
