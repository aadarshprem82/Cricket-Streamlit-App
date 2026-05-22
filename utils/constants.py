# ==========================================
# APPLICATION
# ==========================================

APP_NAME = (
    "Cricket Scoring App"
)

APP_VERSION = "1.0.0"

DEFAULT_OVERS = 20

# ==========================================
# MATCH STATUS
# ==========================================

MATCH_STATUS_UPCOMING = (
    "UPCOMING"
)

MATCH_STATUS_LIVE = (
    "LIVE"
)

MATCH_STATUS_COMPLETED = (
    "COMPLETED"
)

MATCH_STATUSES = [

    MATCH_STATUS_UPCOMING,

    MATCH_STATUS_LIVE,

    MATCH_STATUS_COMPLETED
]

# ==========================================
# INNINGS
# ==========================================

FIRST_INNINGS = 1

SECOND_INNINGS = 2

MAX_WICKETS = 10

BALLS_PER_OVER = 6

# ==========================================
# EXTRA TYPES
# ==========================================

EXTRA_NONE = ""

EXTRA_WIDE = "wide"

EXTRA_NO_BALL = "no_ball"

EXTRA_BYES = "byes"

EXTRA_LEG_BYES = "leg_byes"

EXTRA_TYPES = [

    EXTRA_NONE,

    EXTRA_WIDE,

    EXTRA_NO_BALL,

    EXTRA_BYES,

    EXTRA_LEG_BYES
]

# ==========================================
# WICKET TYPES
# ==========================================

WICKET_BOWLED = "Bowled"

WICKET_CAUGHT = "Caught"

WICKET_LBW = "LBW"

WICKET_RUN_OUT = "Run Out"

WICKET_STUMPED = "Stumped"

WICKET_HIT_WICKET = (
    "Hit Wicket"
)

WICKET_RETIRED_OUT = (
    "Retired Out"
)

WICKET_TYPES = [

    WICKET_BOWLED,

    WICKET_CAUGHT,

    WICKET_LBW,

    WICKET_RUN_OUT,

    WICKET_STUMPED,

    WICKET_HIT_WICKET,

    WICKET_RETIRED_OUT
]

# ==========================================
# PLAYER ROLES
# ==========================================

ROLE_BATTER = "Batter"

ROLE_BOWLER = "Bowler"

ROLE_ALL_ROUNDER = (
    "All Rounder"
)

ROLE_WICKET_KEEPER = (
    "Wicket Keeper"
)

PLAYER_ROLES = [

    ROLE_BATTER,

    ROLE_BOWLER,

    ROLE_ALL_ROUNDER,

    ROLE_WICKET_KEEPER
]

# ==========================================
# BATTING STYLES
# ==========================================

RIGHT_HAND_BAT = (
    "Right Hand Bat"
)

LEFT_HAND_BAT = (
    "Left Hand Bat"
)

BATTING_STYLES = [

    RIGHT_HAND_BAT,

    LEFT_HAND_BAT
]

# ==========================================
# BOWLING STYLES
# ==========================================

BOWLING_NONE = "None"

RIGHT_ARM_FAST = (
    "Right Arm Fast"
)

LEFT_ARM_FAST = (
    "Left Arm Fast"
)

RIGHT_ARM_SPIN = (
    "Right Arm Spin"
)

LEFT_ARM_SPIN = (
    "Left Arm Spin"
)

BOWLING_STYLES = [

    BOWLING_NONE,

    RIGHT_ARM_FAST,

    LEFT_ARM_FAST,

    RIGHT_ARM_SPIN,

    LEFT_ARM_SPIN
]

# ==========================================
# TOURNAMENT FORMAT
# ==========================================

FORMAT_LEAGUE = "League"

FORMAT_KNOCKOUT = (
    "Knockout"
)

FORMAT_ROUND_ROBIN = (
    "Round Robin"
)

TOURNAMENT_FORMATS = [

    FORMAT_LEAGUE,

    FORMAT_KNOCKOUT,

    FORMAT_ROUND_ROBIN
]

# ==========================================
# USER ROLES
# ==========================================

ROLE_ADMIN = "admin"

ROLE_SCORER = "scorer"

ROLE_VIEWER = "viewer"

USER_ROLES = [

    ROLE_ADMIN,

    ROLE_SCORER,

    ROLE_VIEWER
]

# ==========================================
# CACHE
# ==========================================

CACHE_MATCH = "match_cache"

CACHE_PLAYER = (
    "player_cache"
)

CACHE_SCORECARD = (
    "scorecard_cache"
)

CACHE_STATS = "stats_cache"

CACHE_POINTS = (
    "points_table_cache"
)

# ==========================================
# CHART TYPES
# ==========================================

CHART_MANHATTAN = (
    "Manhattan"
)

CHART_WORM = "Worm"

CHART_RUN_RATE = (
    "Run Rate"
)

CHART_PHASES = (
    "Phase Analysis"
)

CHART_WICKETS = (
    "Wicket Timeline"
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
# FILE PATHS
# ==========================================

DATABASE_PATH = (
    "database/cricket.db"
)

EXPORTS_PATH = (
    "data/exports"
)

BACKUPS_PATH = (
    "data/backups"
)

REPORTS_PATH = (
    "data/reports"
)

# ==========================================
# COLORS
# ==========================================

PRIMARY_COLOR = "#FF4B4B"

SECONDARY_COLOR = (
    "#0E1117"
)

SUCCESS_COLOR = "#00C853"

WARNING_COLOR = "#FFD600"

ERROR_COLOR = "#D50000"

# ==========================================
# SESSION KEYS
# ==========================================

SESSION_MATCH_ID = (
    "current_match_id"
)

SESSION_LOGGED_IN = (
    "logged_in"
)

SESSION_USERNAME = (
    "username"
)

SESSION_ROLE = "role"

# ==========================================
# POINTS SYSTEM
# ==========================================

WIN_POINTS = 2

TIE_POINTS = 1

LOSS_POINTS = 0

# ==========================================
# PAGE TITLES
# ==========================================

PAGE_CREATE_MATCH = (
    "Create Match"
)

PAGE_LIVE_SCORING = (
    "Live Scoring"
)

PAGE_SCOREBOARD = (
    "Scoreboard"
)

PAGE_POINTS_TABLE = (
    "Points Table"
)

PAGE_CAREER_STATS = (
    "Career Stats"
)

PAGE_ADMIN_PANEL = (
    "Admin Panel"
)