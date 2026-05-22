from datetime import datetime

from database.db import (
    execute_query
)

# ==========================================
# DEFAULT TEAMS
# ==========================================

DEFAULT_TEAMS = [

    "Warriors",

    "Titans",

    "Royals",

    "Strikers"
]

# ==========================================
# DEFAULT PLAYERS
# ==========================================

DEFAULT_PLAYERS = [

    (
        "P001",
        "Virat",
        "Warriors",
        "Batter",
        "Right Hand Bat",
        "None"
    ),

    (
        "P002",
        "Rohit",
        "Warriors",
        "Batter",
        "Right Hand Bat",
        "None"
    ),

    (
        "P003",
        "Hardik",
        "Titans",
        "All Rounder",
        "Right Hand Bat",
        "Right Arm Fast"
    ),

    (
        "P004",
        "Bumrah",
        "Titans",
        "Bowler",
        "Right Hand Bat",
        "Right Arm Fast"
    ),

    (
        "P005",
        "Dhoni",
        "Royals",
        "Wicket Keeper",
        "Right Hand Bat",
        "None"
    ),

    (
        "P006",
        "Rashid",
        "Strikers",
        "Bowler",
        "Right Hand Bat",
        "Right Arm Spin"
    )
]

# ==========================================
# SEED TEAMS
# ==========================================

def seed_teams():

    query = """

    INSERT OR IGNORE INTO teams (

        team_name,
        created_at

    )

    VALUES (?, ?)

    """

    data = [

        (
            team,
            str(datetime.now())
        )

        for team in DEFAULT_TEAMS
    ]

    for row in data:

        execute_query(
            query,
            row
        )

# ==========================================
# SEED PLAYERS
# ==========================================

def seed_players():

    query = """

    INSERT OR IGNORE INTO players (

        player_id,
        player_name,
        team,
        role,
        batting_style,
        bowling_style,
        created_at

    )

    VALUES (?, ?, ?, ?, ?, ?, ?)

    """

    data = []

    for player in DEFAULT_PLAYERS:

        row = (

            player[0],

            player[1],

            player[2],

            player[3],

            player[4],

            player[5],

            str(datetime.now())
        )

        data.append(row)

    for row in data:

        execute_query(
            query,
            row
        )

# ==========================================
# SEED ADMIN USER
# ==========================================

def seed_admin_user():

    query = """

    INSERT OR IGNORE INTO users (

        username,
        password_hash,
        role,
        created_at

    )

    VALUES (?, ?, ?, ?)

    """

    execute_query(

        query,

        (

            "admin",

            "admin123",

            "admin",

            str(datetime.now())
        )
    )

# ==========================================
# FULL DATABASE SEED
# ==========================================

def seed_database():

    seed_teams()

    seed_players()

    seed_admin_user()

# ==========================================
# CLEAR DEMO DATA
# ==========================================

def clear_demo_data():

    tables = [

        "ball_by_ball",

        "matches",

        "match_state"
    ]

    for table in tables:

        query = (
            f"DELETE FROM {table}"
        )

        execute_query(query)

# ==========================================
# RESET DATABASE
# ==========================================

def reset_database():

    tables = [

        "ball_by_ball",

        "matches",

        "match_state",

        "players",

        "teams",

        "users"
    ]

    for table in tables:

        query = (
            f"DELETE FROM {table}"
        )

        execute_query(query)

    seed_database()

# ==========================================
# SAMPLE MATCH
# ==========================================

def seed_sample_match():

    query = """

    INSERT OR IGNORE INTO matches (

        match_id,
        team1,
        team2,
        overs,
        toss_winner,
        elected,
        batting_first,
        batting_second,
        status,
        created_at,
        updated_at

    )

    VALUES (

        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?

    )

    """

    now = str(datetime.now())

    execute_query(

        query,

        (

            "MATCH001",

            "Warriors",

            "Titans",

            20,

            "Warriors",

            "Bat",

            "Warriors",

            "Titans",

            "LIVE",

            now,

            now
        )
    )

# ==========================================
# FULL DEVELOPMENT SETUP
# ==========================================

def setup_development_database():

    seed_database()

    seed_sample_match()

# ==========================================
# AUTO RUN
# ==========================================

if __name__ == "__main__":

    setup_development_database()

    print(
        "Database seeded successfully."
    )