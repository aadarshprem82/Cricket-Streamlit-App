-- =========================================
-- MATCHES
-- =========================================

CREATE TABLE IF NOT EXISTS matches (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    match_id TEXT UNIQUE NOT NULL,

    team1 TEXT NOT NULL,

    team2 TEXT NOT NULL,

    overs INTEGER NOT NULL,

    toss_winner TEXT,

    elected TEXT,

    batting_first TEXT,

    batting_second TEXT,

    status TEXT DEFAULT 'LIVE',

    innings INTEGER DEFAULT 1,

    target INTEGER DEFAULT 0,

    current_score INTEGER DEFAULT 0,

    wickets INTEGER DEFAULT 0,

    overs_completed TEXT DEFAULT '0.0',

    winner TEXT,

    result TEXT,

    man_of_match TEXT,

    created_at TEXT,

    updated_at TEXT
);

-- =========================================
-- BALL BY BALL
-- =========================================

CREATE TABLE IF NOT EXISTS ball_by_ball (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    match_id TEXT NOT NULL,

    innings INTEGER NOT NULL,

    batting_team TEXT NOT NULL,

    bowling_team TEXT NOT NULL,

    over_num INTEGER NOT NULL,

    ball_num INTEGER NOT NULL,

    striker TEXT,

    non_striker TEXT,

    bowler TEXT,

    runs_off_bat INTEGER DEFAULT 0,

    extras INTEGER DEFAULT 0,

    extra_type TEXT DEFAULT '',

    total_runs INTEGER DEFAULT 0,

    wicket TEXT DEFAULT 'No',

    wicket_type TEXT DEFAULT '',

    player_out TEXT DEFAULT '',

    commentary TEXT DEFAULT '',

    created_at TEXT
);

-- =========================================
-- PLAYERS
-- =========================================

CREATE TABLE IF NOT EXISTS players (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    player_id TEXT UNIQUE NOT NULL,

    player_name TEXT NOT NULL,

    team TEXT NOT NULL,

    role TEXT,

    batting_style TEXT,

    bowling_style TEXT,

    matches INTEGER DEFAULT 0,

    runs INTEGER DEFAULT 0,

    wickets INTEGER DEFAULT 0,

    is_active INTEGER DEFAULT 1,

    created_at TEXT
);

-- =========================================
-- TEAMS
-- =========================================

CREATE TABLE IF NOT EXISTS teams (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    team_name TEXT UNIQUE NOT NULL,

    matches_played INTEGER DEFAULT 0,

    matches_won INTEGER DEFAULT 0,

    matches_lost INTEGER DEFAULT 0,

    points INTEGER DEFAULT 0,

    net_run_rate REAL DEFAULT 0,

    created_at TEXT
);

-- =========================================
-- MATCH STATE
-- =========================================

CREATE TABLE IF NOT EXISTS match_state (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    match_id TEXT UNIQUE NOT NULL,

    innings INTEGER DEFAULT 1,

    striker TEXT,

    non_striker TEXT,

    bowler TEXT,

    batting_team TEXT,

    bowling_team TEXT,

    current_over INTEGER DEFAULT 0,

    current_ball INTEGER DEFAULT 1,

    legal_balls INTEGER DEFAULT 0,

    current_score INTEGER DEFAULT 0,

    wickets INTEGER DEFAULT 0,

    target INTEGER DEFAULT 0,

    last_event TEXT,

    free_hit INTEGER DEFAULT 0,

    match_completed INTEGER DEFAULT 0,

    updated_at TEXT
);

-- =========================================
-- TOURNAMENTS
-- =========================================

CREATE TABLE IF NOT EXISTS tournaments (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    tournament_id TEXT UNIQUE NOT NULL,

    tournament_name TEXT NOT NULL,

    format_type TEXT,

    total_teams INTEGER DEFAULT 0,

    total_matches INTEGER DEFAULT 0,

    status TEXT DEFAULT 'UPCOMING',

    winner TEXT,

    created_at TEXT
);

-- =========================================
-- TOURNAMENT MATCHES
-- =========================================

CREATE TABLE IF NOT EXISTS tournament_matches (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    tournament_id TEXT NOT NULL,

    match_id TEXT NOT NULL
);

-- =========================================
-- POINTS TABLE
-- =========================================

CREATE TABLE IF NOT EXISTS points_table (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    tournament_id TEXT NOT NULL,

    team_name TEXT NOT NULL,

    played INTEGER DEFAULT 0,

    won INTEGER DEFAULT 0,

    lost INTEGER DEFAULT 0,

    tied INTEGER DEFAULT 0,

    no_result INTEGER DEFAULT 0,

    points INTEGER DEFAULT 0,

    net_run_rate REAL DEFAULT 0
);

-- =========================================
-- PLAYER CAREER STATS
-- =========================================

CREATE TABLE IF NOT EXISTS player_career_stats (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    player_name TEXT UNIQUE NOT NULL,

    matches INTEGER DEFAULT 0,

    innings INTEGER DEFAULT 0,

    runs INTEGER DEFAULT 0,

    balls INTEGER DEFAULT 0,

    highest_score INTEGER DEFAULT 0,

    average REAL DEFAULT 0,

    strike_rate REAL DEFAULT 0,

    wickets INTEGER DEFAULT 0,

    overs REAL DEFAULT 0,

    economy REAL DEFAULT 0,

    best_bowling TEXT DEFAULT '0/0',

    fifties INTEGER DEFAULT 0,

    hundreds INTEGER DEFAULT 0,

    fours INTEGER DEFAULT 0,

    sixes INTEGER DEFAULT 0,

    created_at TEXT,

    updated_at TEXT
);

-- =========================================
-- TEAM CAREER STATS
-- =========================================

CREATE TABLE IF NOT EXISTS team_career_stats (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    team_name TEXT UNIQUE NOT NULL,

    matches INTEGER DEFAULT 0,

    wins INTEGER DEFAULT 0,

    losses INTEGER DEFAULT 0,

    ties INTEGER DEFAULT 0,

    runs_scored INTEGER DEFAULT 0,

    wickets_lost INTEGER DEFAULT 0,

    highest_score INTEGER DEFAULT 0,

    lowest_score INTEGER DEFAULT 0,

    run_rate REAL DEFAULT 0,

    created_at TEXT,

    updated_at TEXT
);

-- =========================================
-- USERS
-- =========================================

CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE NOT NULL,

    password_hash TEXT NOT NULL,

    role TEXT DEFAULT 'viewer',

    is_active INTEGER DEFAULT 1,

    created_at TEXT
);

-- =========================================
-- INDEXES
-- =========================================

CREATE INDEX IF NOT EXISTS idx_match_id
ON ball_by_ball(match_id);

CREATE INDEX IF NOT EXISTS idx_player_name
ON players(player_name);

CREATE INDEX IF NOT EXISTS idx_team_name
ON teams(team_name);

CREATE INDEX IF NOT EXISTS idx_match_state
ON match_state(match_id);

CREATE INDEX IF NOT EXISTS idx_tournament
ON tournament_matches(tournament_id);

-- =========================================
-- DEFAULT TEAMS
-- =========================================

INSERT OR IGNORE INTO teams (
    team_name
)
VALUES
('Warriors'),
('Titans'),
('Royals'),
('Strikers');

-- =========================================
-- DEFAULT ADMIN USER
-- =========================================

INSERT OR IGNORE INTO users (

    username,
    password_hash,
    role

)
VALUES (

    'admin',

    'admin123',

    'admin'
);