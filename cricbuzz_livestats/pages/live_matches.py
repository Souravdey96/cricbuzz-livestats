import html
import pandas as pd
import streamlit as st

from services.match_service import get_recent_matches, get_scorecard


def _bat_name(row):
    if isinstance(row, dict):
        return row.get("batsmanName") or row.get("name") or row.get("nickname") or ""
    return ""


def _bat_sr(row):
    if isinstance(row, dict):
        return row.get("strikeRate") or row.get("strkrate") or row.get("strike_rate") or ""
    return ""


def _bowl_name(row):
    if isinstance(row, dict):
        return row.get("bowlerName") or row.get("name") or row.get("nickname") or ""
    return ""


def _format_innings_line(inn):
    team = inn.get("team") or "—"
    r, w, o = inn.get("runs"), inn.get("wickets"), inn.get("overs")
    if r is None and w is None and o is None:
        return team
    return f"{team}  {r or 0}/{w or 0} ({o} ov)"


def _build_batting_df(rows):
    out = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        out.append(
            {
                "BATTER": _bat_name(row),
                "R": row.get("runs", 0),
                "B": row.get("balls", 0),
                "4s": row.get("fours", 0),
                "6s": row.get("sixes", 0),
                "SR": _bat_sr(row),
            }
        )
    return pd.DataFrame(out)


def _build_bowling_df(rows):
    out = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        out.append(
            {
                "BOWLER": _bowl_name(row),
                "O": row.get("overs", ""),
                "R": row.get("runs", 0),
                "W": row.get("wickets", 0),
                "ECO": row.get("economy", ""),
            }
        )
    return pd.DataFrame(out)


def _top_batting_cards(rows, team1, team2, limit=6):
    enriched = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        try:
            runs = int(row.get("runs") or 0)
        except (TypeError, ValueError):
            runs = 0
        sr_raw = _bat_sr(row)
        try:
            sr = float(sr_raw) if sr_raw not in (None, "") else 0.0
        except (TypeError, ValueError):
            sr = 0.0
        team = row.get("batTeamName") or ""
        if not team:
            if team1 and team2:
                team = f"{team1} / {team2}"
            else:
                team = "—"
        enriched.append(
            {
                "name": _bat_name(row),
                "team": team,
                "runs": runs,
                "sr": sr,
            }
        )
    enriched.sort(key=lambda x: (x["runs"], x["sr"]), reverse=True)
    return enriched[:limit]


def _html_batting_table(df):
    if df.empty:
        return '<p style="color:#2d2747;">No batting data.</p>'
    rows_html = []
    for _, r in df.iterrows():
        rows_html.append(
            f"<tr><td>{html.escape(str(r['BATTER']))}</td><td>{r['R']}</td><td>{r['B']}</td>"
            f"<td>{r['4s']}</td><td>{r['6s']}</td><td>{html.escape(str(r['SR']))}</td></tr>"
        )
    return f"""
<table class="mock-bat-table">
<thead><tr><th>BATTER</th><th>R</th><th>B</th><th>4s</th><th>6s</th><th>SR</th></tr></thead>
<tbody>{"".join(rows_html)}</tbody>
</table>
"""


def _html_bowling_table(df):
    if df.empty:
        return '<p style="color:#2d2747;">No bowling data.</p>'
    rows_html = []
    for _, r in df.iterrows():
        rows_html.append(
            f"<tr><td>{html.escape(str(r['BOWLER']))}</td><td>{html.escape(str(r['O']))}</td>"
            f"<td>{r['R']}</td><td>{r['W']}</td><td>{html.escape(str(r['ECO']))}</td></tr>"
        )
    return f"""
<table class="mock-bat-table mock-bowl-table">
<thead><tr><th>BOWLER</th><th>O</th><th>R</th><th>W</th><th>ECO</th></tr></thead>
<tbody>{"".join(rows_html)}</tbody>
</table>
"""


def _score_boxes_html(innings, team1, team2):
    """Alternating navy / coral boxes like the mockup."""
    boxes = []
    for i, inn in enumerate(innings[:2]):
        team = html.escape(str(inn.get("team") or (team1 if i == 0 else team2) or "—"))
        r = inn.get("runs")
        w = inn.get("wickets")
        o = inn.get("overs")
        score_txt = f"{r or 0}-{w or 0}" if r is not None or w is not None else "—"
        sub = f"{o} ov" if o is not None else ""
        if i % 2 == 0:
            boxes.append(
                f"""
<div class="score-box score-box-navy">
  <div class="score-box-inner">
    <span class="sb-team sb-coral">{team}</span>
    <span class="sb-runs sb-coral">{html.escape(str(score_txt))}</span>
  </div>
  <div class="sb-sub">{html.escape(sub)}</div>
</div>"""
            )
        else:
            boxes.append(
                f"""
<div class="score-box score-box-coral">
  <div class="score-box-inner">
    <span class="sb-team sb-navy">{team}</span>
    <span class="sb-runs sb-navy">{html.escape(str(score_txt))}</span>
  </div>
  <div class="sb-sub sb-sub-navy">{html.escape(sub)}</div>
</div>"""
            )
    if not boxes:
        return f"""
<div class="score-box score-box-navy">
  <div class="score-box-inner">
    <span class="sb-team sb-coral">{html.escape(team1 or "Team 1")}</span>
    <span class="sb-runs sb-coral">—</span>
  </div>
</div>
<div class="score-box score-box-coral">
  <div class="score-box-inner">
    <span class="sb-team sb-navy">{html.escape(team2 or "Team 2")}</span>
    <span class="sb-runs sb-navy">—</span>
  </div>
</div>"""
    if len(boxes) == 1:
        other_team = team2 if (innings[0].get("team") or "") == team1 else team1
        boxes.append(
            f"""
<div class="score-box score-box-coral">
  <div class="score-box-inner">
    <span class="sb-team sb-navy">{html.escape(other_team or "—")}</span>
    <span class="sb-runs sb-navy">—</span>
  </div>
</div>"""
        )
    return "\n".join(boxes)


def main():
    st.markdown(
        """
<style>
    .live-dashboard-inner {
        font-family: "Source Sans Pro", sans-serif;
    }
    .live-title-block {
        text-align: center;
        margin-bottom: 18px;
    }
    .live-title-block h2 {
        color: #2d2747;
        font-size: 1.75rem;
        font-weight: 900;
        letter-spacing: 0.04em;
        margin: 0;
    }
    .live-subtitle {
        color: #5a5270;
        font-size: 0.95rem;
        margin-top: 6px;
    }
    .score-box {
        border-radius: 22px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }
    .score-box-navy {
        background: #2d2747;
    }
    .score-box-coral {
        background: #ff8c69;
    }
    .score-box-inner {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .sb-team { font-size: 1.35rem; font-weight: 800; }
    .sb-runs { font-size: 1.55rem; font-weight: 900; }
    .sb-coral { color: #ff8c69; }
    .sb-navy { color: #2d2747; }
    .sb-sub { color: #a89fc9; font-size: 0.85rem; margin-top: 6px; }
    .sb-sub-navy { color: #5a3d52 !important; }
    table.mock-bat-table {
        width: 100%;
        border-collapse: collapse;
        border-radius: 16px;
        overflow: hidden;
        margin-bottom: 12px;
        font-size: 0.92rem;
    }
    table.mock-bat-table thead tr {
        background: #2d2747;
        color: #fff;
    }
    table.mock-bat-table th {
        padding: 10px 8px;
        text-align: left;
        font-weight: 700;
    }
    table.mock-bat-table tbody tr:nth-child(odd) {
        background: rgba(255, 255, 255, 0.55);
    }
    table.mock-bat-table tbody tr:nth-child(even) {
        background: rgba(255, 180, 150, 0.45);
    }
    table.mock-bat-table td {
        padding: 10px 8px;
        color: #2d2747;
        font-weight: 600;
    }
    .section-label {
        color: #2d2747;
        font-weight: 800;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin: 14px 0 8px 0;
    }
    .analytics-header {
        background: #2d2747;
        color: #fff;
        text-align: center;
        font-weight: 800;
        padding: 12px;
        border-radius: 16px 16px 0 0;
        letter-spacing: 0.06em;
        font-size: 0.95rem;
    }
    .analytics-body {
        background: rgba(255, 255, 255, 0.35);
        border-radius: 0 0 16px 16px;
        padding: 12px;
        border: 2px solid #2d2747;
        border-top: none;
    }
    .analytics-field {
        background: #ffcba8;
        border-radius: 14px;
        padding: 10px 14px;
        margin-bottom: 10px;
        color: #2d2747;
        font-weight: 700;
        font-size: 0.88rem;
    }
    .analytics-field span.label { color: #5a5270; font-size: 0.72rem; text-transform: uppercase; display:block; margin-bottom:4px;}
    .player-card-mock {
        border: 2px solid #2d2747;
        border-radius: 16px;
        padding: 10px;
        margin-bottom: 12px;
        background: rgba(255, 255, 255, 0.25);
    }
    .spark-wrap {
        background: #2d2747;
        border-radius: 18px;
        padding: 14px;
        margin-top: 12px;
        min-height: 70px;
    }
    .spark-title {
        color: #fff;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 8px;
        opacity: 0.85;
    }
    .action-btns {
        display: flex;
        gap: 10px;
        justify-content: center;
        margin-top: 14px;
    }
    .mini-btn-pink {
        background: #ff4d8d !important;
        border-radius: 12px !important;
        min-height: 42px;
    }
    .mini-btn-coral {
        background: #ff8c69 !important;
        border-radius: 12px !important;
        min-height: 42px;
    }
    .mini-btn-navy {
        background: #2d2747 !important;
        color: #fff !important;
        border-radius: 12px !important;
        min-height: 42px;
    }
</style>
""",
        unsafe_allow_html=True,
    )

    st.markdown("### 🏏 Live Matches")

    with st.spinner("Loading matches..."):
        result = get_recent_matches()

    if result["warning"]:
        st.warning(result["warning"])

    matches = result["data"]

    if not matches:
        st.warning("No live matches found. Showing cached data when available.")
        return

    match_labels = [f"{m['match_desc'] or 'Match'} — {m['team1']} vs {m['team2']}" for m in matches]
    match_ids = [m["match_id"] for m in matches]

    choice = st.selectbox("Select match", options=list(range(len(matches))), format_func=lambda i: match_labels[i])
    match = matches[choice]
    mid = match_ids[choice]

    title = match.get("match_desc") or f"{match['team1']} vs {match['team2']}"
    team1, team2 = match.get("team1") or "", match.get("team2") or ""

    scorecard_result = get_scorecard(mid)
    if scorecard_result["warning"]:
        st.warning(scorecard_result["warning"])

    sc = scorecard_result["data"]
    innings = sc.get("innings") or []
    score_lines = [_format_innings_line(inn) for inn in innings if inn.get("team") or inn.get("runs") is not None]
    score_fallback = "  ·  ".join(score_lines) if score_lines else match.get("status", "—")

    bat_rows = sc.get("batsmen") or []
    bowl_rows = sc.get("bowlers") or []
    df_bat = _build_batting_df(bat_rows)
    df_bowl = _build_bowling_df(bowl_rows)
    top_players = _top_batting_cards(bat_rows, team1, team2)

    left, right = st.columns([7, 3])

    with left:
        st.markdown('<div class="live-dashboard-inner">', unsafe_allow_html=True)
        st.markdown(
            f"""
<div class="live-title-block">
  <h2>LIVE SCORECARD</h2>
  <div class="live-subtitle">{html.escape(title)}</div>
  <div class="live-subtitle">{html.escape(score_fallback)}</div>
</div>
{_score_boxes_html(innings, team1, team2)}
""",
            unsafe_allow_html=True,
        )
        st.markdown('<div class="section-label">Batting</div>', unsafe_allow_html=True)
        st.markdown(_html_batting_table(df_bat), unsafe_allow_html=True)
        st.markdown('<div class="section-label">Bowling</div>', unsafe_allow_html=True)
        st.markdown(_html_bowling_table(df_bowl), unsafe_allow_html=True)

        st.markdown(
            f'<div class="live-subtitle" style="text-align:center;margin-top:10px;">'
            f"{html.escape(match.get('status', '—'))} · {html.escape(match.get('venue', ''))}, {html.escape(match.get('city', ''))}"
            f"</div>",
            unsafe_allow_html=True,
        )

        # Sparkline-style block (mockup trend strip)
        if not df_bat.empty and "R" in df_bat.columns:
            chart_data = df_bat.head(8)["R"].astype(float).tolist()
            spark_df = pd.DataFrame({"runs": chart_data})
            st.markdown('<div class="spark-wrap">', unsafe_allow_html=True)
            st.markdown('<div class="spark-title">Run spread (top order)</div>', unsafe_allow_html=True)
            st.line_chart(spark_df, height=100, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown(
            '<div class="analytics-header">PLAYER ANALYTICS</div><div class="analytics-body">',
            unsafe_allow_html=True,
        )
        if not top_players:
            st.markdown(
                '<div class="player-card-mock">'
                '<div class="analytics-field"><span class="label">Info</span>No scorecard batters yet.</div>'
                "</div>",
                unsafe_allow_html=True,
            )
        for p in top_players:
            nm = html.escape(p["name"] or "—")
            tm = html.escape(p["team"] or "—")
            st.markdown(
                f"""
<div class="player-card-mock">
  <div class="analytics-field"><span class="label">Name</span>{nm}</div>
  <div class="analytics-field"><span class="label">Team</span>{tm}</div>
  <div class="analytics-field"><span class="label">Matches</span>1 <span style="opacity:.75;font-weight:600;">(this fixture)</span></div>
  <div class="analytics-field"><span class="label">Runs</span>{p["runs"]}</div>
  <div class="analytics-field"><span class="label">Strike rate</span>{p["sr"]:.2f}</div>
</div>
""",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

        b1, b2, b3 = st.columns(3)
        with b1:
            st.button("✏️", key="mock_edit", help="Placeholder")
        with b2:
            st.button("➕", key="mock_add1", help="Placeholder")
        with b3:
            st.button("➕", key="mock_add2", help="Placeholder")
