import os
import requests
import json
import time
import datetime
from config.settings import RAPIDAPI_KEY

HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}

CACHE_DIR = "raw_cache"
LOG_FILE = os.path.join(CACHE_DIR, "api_call_log.json")

os.makedirs(CACHE_DIR, exist_ok=True)

def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            return json.load(f)
    return {"total_calls_made": 0, "last_call_timestamp": "", "calls_this_month": 0}

def save_log(log):
    with open(LOG_FILE, 'w') as f:
        json.dump(log, f)

def check_and_update_log():
    log = load_log()
    now = datetime.datetime.now()
    current_month = now.strftime("%Y-%m")
    if log["last_call_timestamp"]:
        last_month = datetime.datetime.fromisoformat(log["last_call_timestamp"]).strftime("%Y-%m")
        if last_month != current_month:
            log["calls_this_month"] = 0
    if log["calls_this_month"] >= 450:
        print("Warning: API call limit reached for this month.")
        return False
    log["calls_this_month"] += 1
    log["total_calls_made"] += 1
    log["last_call_timestamp"] = now.isoformat()
    save_log(log)
    return True

def make_api_call(url, cache_key):
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    if not RAPIDAPI_KEY:
        print("RAPIDAPI_KEY is missing. Returning cached/empty data.")
        return None
    if not check_and_update_log():
        return None
    try:
        time.sleep(1)
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        with open(cache_file, 'w') as f:
            json.dump(data, f)
        return data
    except Exception as e:
        print(f"API call failed: {e}")
        return None

def get_recent_matches():
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent"
    data = make_api_call(url, "recent_matches")
    if data is None:
        return {'data': [], 'warning': 'API call limit reached for this month.'}
    try:
        matches_list = []
        for type_match in data.get("typeMatches", []):
            for series in type_match.get("seriesMatches", []):
                for match in series.get("seriesAdWrapper", {}).get("matches", []):
                    match_info = match.get("matchInfo", {})
                    venue_info = match_info.get("venueInfo", {})
                    team1 = match_info.get("team1", {}).get("teamName", "")
                    team2 = match_info.get("team2", {}).get("teamName", "")
                    venue = venue_info.get("ground", "")
                    city = venue_info.get("city", "")
                    match_date = match_info.get("startDate", "")
                    status = match_info.get("status", "")
                    match_desc = match_info.get("matchDesc", "")
                    match_id = match_info.get("matchId", "")
                    matches_list.append({
                        "match_id": match_id,
                        "match_desc": match_desc,
                        "team1": team1,
                        "team2": team2,
                        "venue": venue,
                        "city": city,
                        "match_date": match_date,
                        "status": status
                    })
        return {'data': matches_list, 'warning': None}
    except Exception as e:
        print(f"Error parsing recent matches: {e}")
        return {'data': [], 'warning': None}

def get_scorecard(match_id):
    url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{match_id}/hscard"
    data = make_api_call(url, f"scorecard_{match_id}")
    if data is None:
        return {
            "data": {"batsmen": [], "bowlers": [], "innings": []},
            "warning": "API call limit reached for this month.",
        }
    try:
        innings_raw = data.get("scoreCard") or data.get("scorecard") or []
        batsmen = []
        bowlers = []
        innings = []

        for inning in innings_raw:
            team = inning.get("batteamname") or inning.get("batTeamName") or ""
            overs = inning.get("overs")
            score = inning.get("score")
            wickets = inning.get("wickets")
            innings.append(
                {
                    "team": team,
                    "runs": score,
                    "wickets": wickets,
                    "overs": overs,
                }
            )

            bat_detail = inning.get("batTeamDetails", {}).get("batsmenData") or {}
            if isinstance(bat_detail, dict) and bat_detail:
                for batsman in bat_detail.values():
                    if isinstance(batsman, dict):
                        batsmen.append({**batsman, "batTeamName": team or batsman.get("batTeamName", "")})
            else:
                for batsman in inning.get("batsman") or []:
                    if isinstance(batsman, dict):
                        batsmen.append({**batsman, "batTeamName": team or batsman.get("batTeamName", "")})

            bowl_detail = inning.get("bowlTeamDetails", {}).get("bowlersData") or {}
            if isinstance(bowl_detail, dict) and bowl_detail:
                for bowler in bowl_detail.values():
                    if isinstance(bowler, dict):
                        bowlers.append({**bowler, "bowlTeamName": team or bowler.get("bowlTeamName", "")})
            else:
                for bowler in inning.get("bowler") or []:
                    if isinstance(bowler, dict):
                        bowlers.append({**bowler, "bowlTeamName": team or bowler.get("bowlTeamName", "")})

        return {"data": {"batsmen": batsmen, "bowlers": bowlers, "innings": innings}, "warning": None}
    except Exception as e:
        print(f"Error parsing scorecard: {e}")
        return {"data": {"batsmen": [], "bowlers": [], "innings": []}, "warning": None}