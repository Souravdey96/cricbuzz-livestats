from sqlalchemy import Column, Integer, String, Date, Float, create_engine, MetaData, Table, insert, text
from config.settings import DB_URL
from datetime import date

metadata = MetaData()

players = Table('players', metadata,
    Column('player_id', Integer, primary_key=True),
    Column('name', String),
    Column('country', String),
    Column('role', String),
    Column('batting_style', String),
    Column('bowling_style', String)
)

matches = Table('matches', metadata,
    Column('match_id', Integer, primary_key=True),
    Column('match_desc', String),
    Column('team1', String),
    Column('team2', String),
    Column('venue', String),
    Column('city', String),
    Column('match_date', Date),
    Column('winner', String),
    Column('victory_margin', String),
    Column('victory_type', String),
    Column('toss_winner', String),
    Column('toss_decision', String)
)

series = Table('series', metadata,
    Column('series_id', Integer, primary_key=True),
    Column('series_name', String),
    Column('match_type', String),
    Column('start_date', Date),
    Column('total_matches', Integer)
)

batsman_stats = Table('batsman_stats', metadata,
    Column('inning_id', Integer, primary_key=True),
    Column('match_id', Integer),
    Column('player_name', String),
    Column('runs', Integer),
    Column('balls', Integer),
    Column('fours', Integer),
    Column('sixes', Integer),
    Column('strike_rate', Float),
    Column('dismissed_by', String)
)

bowler_stats = Table('bowler_stats', metadata,
    Column('inning_id', Integer, primary_key=True),
    Column('match_id', Integer),
    Column('player_name', String),
    Column('overs', Float),
    Column('runs_given', Integer),
    Column('wickets', Integer),
    Column('economy', Float),
    Column('maidens', Integer)
)

venues = Table('venues', metadata,
    Column('venue_id', Integer, primary_key=True),
    Column('name', String),
    Column('city', String),
    Column('country', String),
    Column('capacity', Integer)
)

def get_engine():
    return create_engine(DB_URL)

def create_all_tables():
    engine = get_engine()
    metadata.create_all(engine)

    # Sample data
    with engine.connect() as conn:
        # Players
        conn.execute(text("INSERT INTO players VALUES (1, 'Virat Kohli', 'India', 'Batsman', 'Right-hand bat', 'Right-arm medium')"))
        conn.execute(text("INSERT INTO players VALUES (2, 'Rohit Sharma', 'India', 'Batsman', 'Right-hand bat', 'Right-arm off-break')"))
        conn.execute(text("INSERT INTO players VALUES (3, 'Jasprit Bumrah', 'India', 'Bowler', 'Right-hand bat', 'Right-arm fast')"))
        conn.execute(text("INSERT INTO players VALUES (4, 'Ben Stokes', 'England', 'All-rounder', 'Left-hand bat', 'Right-arm fast-medium')"))
        conn.execute(text("INSERT INTO players VALUES (5, 'Steve Smith', 'Australia', 'Batsman', 'Right-hand bat', 'Right-arm leg-break')"))

        # Matches
        conn.execute(text("INSERT INTO matches VALUES (1, 'India vs Australia 1st ODI', 'India', 'Australia', 'Wankhede Stadium', 'Mumbai', '2024-01-15', 'India', '26', 'runs', 'India', 'bat')"))
        conn.execute(text("INSERT INTO matches VALUES (2, 'England vs Australia 1st Test', 'England', 'Australia', 'Lords', 'London', '2024-02-10', 'Australia', '5', 'wickets', 'Australia', 'bowl')"))
        conn.execute(text("INSERT INTO matches VALUES (3, 'India vs England 1st T20', 'India', 'England', 'Eden Gardens', 'Kolkata', '2024-03-20', 'India', '7', 'wickets', 'India', 'bat')"))

        # batsman_stats
        conn.execute(text("INSERT INTO batsman_stats VALUES (1, 1, 'Virat Kohli', 82, 90, 8, 2, 91.1, 'bowled')"))
        conn.execute(text("INSERT INTO batsman_stats VALUES (2, 1, 'Rohit Sharma', 65, 70, 7, 1, 92.8, 'caught')"))
        conn.execute(text("INSERT INTO batsman_stats VALUES (3, 1, 'Steve Smith', 45, 55, 4, 0, 81.8, 'lbw')"))
        conn.execute(text("INSERT INTO batsman_stats VALUES (4, 2, 'Ben Stokes', 120, 150, 12, 3, 80.0, 'not out')"))
        conn.execute(text("INSERT INTO batsman_stats VALUES (5, 2, 'Steve Smith', 95, 110, 9, 1, 86.3, 'caught')"))
        conn.execute(text("INSERT INTO batsman_stats VALUES (6, 3, 'Virat Kohli', 55, 40, 5, 3, 137.5, 'not out')"))
        conn.execute(text("INSERT INTO batsman_stats VALUES (7, 3, 'Rohit Sharma', 72, 48, 6, 4, 150.0, 'caught')"))

        # bowler_stats
        conn.execute(text("INSERT INTO bowler_stats VALUES (1, 1, 'Jasprit Bumrah', 10.0, 35, 3, 3.5, 1)"))
        conn.execute(text("INSERT INTO bowler_stats VALUES (2, 2, 'Jasprit Bumrah', 20.0, 65, 4, 3.25, 2)"))
        conn.execute(text("INSERT INTO bowler_stats VALUES (3, 3, 'Jasprit Bumrah', 4.0, 28, 2, 7.0, 0)"))
        conn.execute(text("INSERT INTO bowler_stats VALUES (4, 2, 'Ben Stokes', 15.0, 55, 2, 3.67, 1)"))

        # venues
        conn.execute(text("INSERT INTO venues VALUES (1, 'Wankhede Stadium', 'Mumbai', 'India', 33000)"))
        conn.execute(text("INSERT INTO venues VALUES (2, 'Lords', 'London', 'England', 28000)"))
        conn.execute(text("INSERT INTO venues VALUES (3, 'Eden Gardens', 'Kolkata', 'India', 66000)"))
        conn.execute(text("INSERT INTO venues VALUES (4, 'MCG', 'Melbourne', 'Australia', 100024)"))
        conn.execute(text("INSERT INTO venues VALUES (5, 'The Oval', 'London', 'England', 25000)"))

        # series
        conn.execute(text("INSERT INTO series VALUES (1, 'India tour of Australia 2024', 'ODI', '2024-01-15', 5)"))
        conn.execute(text("INSERT INTO series VALUES (2, 'The Ashes 2024', 'Test', '2024-02-10', 5)"))
        conn.execute(text("INSERT INTO series VALUES (3, 'India vs England T20 2024', 'T20', '2024-03-20', 3)"))

        conn.commit()

if __name__ == "__main__":
    create_all_tables()