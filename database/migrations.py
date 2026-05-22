from database.db import (

    execute_query,

    fetch_all,

    table_exists
)

# ==========================================
# GET ALL TABLES
# ==========================================

def get_all_tables():

    query = """

    SELECT name

    FROM sqlite_master

    WHERE type='table'

    ORDER BY name

    """

    tables = fetch_all(query)

    return [
        table["name"]
        for table in tables
    ]

# ==========================================
# ADD COLUMN
# ==========================================

def add_column(

    table_name,

    column_name,

    column_definition
):

    query = f"""

    ALTER TABLE {table_name}

    ADD COLUMN {column_name}

    {column_definition}

    """

    execute_query(query)

# ==========================================
# SAFE ADD COLUMN
# ==========================================

def safe_add_column(

    table_name,

    column_name,

    column_definition
):

    query = f"""

    PRAGMA table_info({table_name})

    """

    columns = fetch_all(query)

    existing_columns = [

        column["name"]

        for column in columns
    ]

    if column_name in existing_columns:

        return False

    add_column(

        table_name,

        column_name,

        column_definition
    )

    return True

# ==========================================
# CREATE INDEX
# ==========================================

def create_index(

    index_name,

    table_name,

    column_name
):

    query = f"""

    CREATE INDEX IF NOT EXISTS

    {index_name}

    ON {table_name}({column_name})

    """

    execute_query(query)

# ==========================================
# DROP TABLE
# ==========================================

def drop_table(
    table_name
):

    query = f"""

    DROP TABLE IF EXISTS
    {table_name}

    """

    execute_query(query)

# ==========================================
# RENAME TABLE
# ==========================================

def rename_table(

    old_name,

    new_name
):

    query = f"""

    ALTER TABLE {old_name}

    RENAME TO {new_name}

    """

    execute_query(query)

# ==========================================
# CREATE TOURNAMENT TABLES
# ==========================================

def create_tournament_tables():

    tournament_query = """

    CREATE TABLE IF NOT EXISTS tournaments (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        tournament_id TEXT UNIQUE,

        tournament_name TEXT,

        format_type TEXT,

        total_teams INTEGER,

        total_matches INTEGER,

        status TEXT,

        winner TEXT,

        created_at TEXT
    )

    """

    execute_query(
        tournament_query
    )

    tournament_match_query = """

    CREATE TABLE IF NOT EXISTS tournament_matches (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        tournament_id TEXT,

        match_id TEXT
    )

    """

    execute_query(
        tournament_match_query
    )

# ==========================================
# CREATE USER TABLES
# ==========================================

def create_user_tables():

    query = """

    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE,

        password_hash TEXT,

        role TEXT,

        is_active INTEGER DEFAULT 1,

        created_at TEXT
    )

    """

    execute_query(query)

# ==========================================
# CREATE POINTS TABLE
# ==========================================

def create_points_table():

    query = """

    CREATE TABLE IF NOT EXISTS points_table (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        tournament_id TEXT,

        team_name TEXT,

        played INTEGER DEFAULT 0,

        won INTEGER DEFAULT 0,

        lost INTEGER DEFAULT 0,

        tied INTEGER DEFAULT 0,

        no_result INTEGER DEFAULT 0,

        points INTEGER DEFAULT 0,

        net_run_rate REAL DEFAULT 0
    )

    """

    execute_query(query)

# ==========================================
# APPLY FUTURE MIGRATIONS
# ==========================================

def run_future_migrations():

    # ======================================
    # MATCHES TABLE UPDATES
    # ======================================

    safe_add_column(

        "matches",

        "venue",

        "TEXT"
    )

    safe_add_column(

        "matches",

        "umpire",

        "TEXT"
    )

    safe_add_column(

        "matches",

        "season",

        "TEXT"
    )

    # ======================================
    # PLAYERS TABLE UPDATES
    # ======================================

    safe_add_column(

        "players",

        "player_image",

        "TEXT"
    )

    safe_add_column(

        "players",

        "jersey_number",

        "INTEGER"
    )

    # ======================================
    # BALL DATA COMMENTARY
    # ======================================

    safe_add_column(

        "ball_by_ball",

        "wagon_zone",

        "TEXT"
    )

    # ======================================
    # TOURNAMENT TABLES
    # ======================================

    create_tournament_tables()

    # ======================================
    # USER TABLES
    # ======================================

    create_user_tables()

    # ======================================
    # POINTS TABLE
    # ======================================

    create_points_table()

# ==========================================
# DATABASE STRUCTURE REPORT
# ==========================================

def database_structure_report():

    report = {}

    tables = get_all_tables()

    for table in tables:

        query = f"""

        PRAGMA table_info({table})

        """

        columns = fetch_all(query)

        report[table] = [

            column["name"]

            for column in columns
        ]

    return report

# ==========================================
# VERIFY REQUIRED TABLES
# ==========================================

def verify_required_tables():

    required_tables = [

        "matches",

        "ball_by_ball",

        "players",

        "teams",

        "match_state"
    ]

    missing_tables = []

    for table in required_tables:

        if not table_exists(table):

            missing_tables.append(
                table
            )

    return {

        "success": (
            len(missing_tables) == 0
        ),

        "missing_tables": missing_tables
    }

# ==========================================
# CREATE PERFORMANCE INDEXES
# ==========================================

def create_performance_indexes():

    indexes = [

        (
            "idx_ball_match",
            "ball_by_ball",
            "match_id"
        ),

        (
            "idx_ball_batter",
            "ball_by_ball",
            "striker"
        ),

        (
            "idx_ball_bowler",
            "ball_by_ball",
            "bowler"
        ),

        (
            "idx_matches_status",
            "matches",
            "status"
        )
    ]

    for index_name, table, column in indexes:

        create_index(

            index_name,

            table,

            column
        )