from datetime import datetime
import uuid
import pandas as pd

# ==========================================
# GENERATE MATCH ID
# ==========================================

def generate_match_id():

    timestamp = datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )

    return f"MATCH_{timestamp}"

# ==========================================
# GENERATE PLAYER ID
# ==========================================

def generate_player_id():

    short_uuid = str(
        uuid.uuid4()
    )[:8].upper()

    return f"PLY_{short_uuid}"

# ==========================================
# GENERATE TOURNAMENT ID
# ==========================================

def generate_tournament_id():

    timestamp = datetime.now().strftime(
        "%Y%m%d"
    )

    short_uuid = str(
        uuid.uuid4()
    )[:5].upper()

    return (

        f"TOUR_{timestamp}_"

        f"{short_uuid}"
    )

# ==========================================
# CURRENT TIMESTAMP
# ==========================================

def current_timestamp():

    return str(
        datetime.now()
    )

# ==========================================
# FORMAT OVERS
# ==========================================

def format_overs(
    legal_balls
):

    overs = legal_balls // 6

    balls = legal_balls % 6

    return f"{overs}.{balls}"

# ==========================================
# OVERS TO BALLS
# ==========================================

def overs_to_balls(
    overs
):

    try:

        over, balls = str(
            overs
        ).split(".")

        return (
            int(over) * 6
            +
            int(balls)
        )

    except:
        return 0

# ==========================================
# BALLS TO OVERS
# ==========================================

def balls_to_overs(
    balls
):

    overs = balls // 6

    rem = balls % 6

    return f"{overs}.{rem}"

# ==========================================
# SAFE INTEGER
# ==========================================

def safe_int(
    value,
    default=0
):

    try:
        return int(value)

    except:
        return default

# ==========================================
# SAFE FLOAT
# ==========================================

def safe_float(
    value,
    default=0.0
):

    try:
        return float(value)

    except:
        return default

# ==========================================
# DATAFRAME EMPTY
# ==========================================

def empty_dataframe():

    return pd.DataFrame()

# ==========================================
# RUNS DISPLAY
# ==========================================

def format_score(
    runs,
    wickets
):

    return f"{runs}/{wickets}"

# ==========================================
# MATCH DISPLAY
# ==========================================

def match_title(
    team1,
    team2
):

    return f"{team1} vs {team2}"

# ==========================================
# WIN %
# ==========================================

def calculate_win_percentage(
    wins,
    played
):

    if played <= 0:
        return 0

    return round(
        (wins / played) * 100,
        2
    )

# ==========================================
# NET RUN RATE
# ==========================================

def calculate_nrr(

    runs_scored,

    overs_faced,

    runs_conceded,

    overs_bowled
):

    if overs_faced <= 0:
        return 0

    if overs_bowled <= 0:
        return 0

    scored_rr = (
        runs_scored
        / overs_faced
    )

    conceded_rr = (
        runs_conceded
        / overs_bowled
    )

    return round(
        scored_rr - conceded_rr,
        3
    )

# ==========================================
# RESULT TEXT
# ==========================================

def result_text(

    winner,

    margin,

    result_type
):

    if result_type == "runs":

        return (

            f"{winner} won by "

            f"{margin} runs"
        )

    if result_type == "wickets":

        return (

            f"{winner} won by "

            f"{margin} wickets"
        )

    return "Match Tied"

# ==========================================
# IS WICKET
# ==========================================

def is_wicket(
    wicket_value
):

    return str(
        wicket_value
    ).lower() == "yes"

# ==========================================
# IS LEGAL DELIVERY
# ==========================================

def is_legal_delivery(
    extra_type
):

    illegal = [

        "wide",

        "no_ball"
    ]

    return extra_type not in illegal

# ==========================================
# LAST BALL EVENT
# ==========================================

def last_ball_event(
    ball_df
):

    if ball_df.empty:
        return None

    return ball_df.iloc[-1].to_dict()

# ==========================================
# RECENT OVERS
# ==========================================

def recent_overs(
    ball_df,
    balls=12
):

    if ball_df.empty:
        return []

    recent = ball_df.tail(
        balls
    )

    outputs = []

    for _, row in recent.iterrows():

        if row["wicket"] == "Yes":

            outputs.append("W")

        elif row["extra_type"] == "wide":

            outputs.append("WD")

        elif row["extra_type"] == "no_ball":

            outputs.append("NB")

        else:

            outputs.append(
                str(row["total_runs"])
            )

    return outputs

# ==========================================
# UNIQUE TEAMS
# ==========================================

def unique_teams(
    matches_df
):

    if matches_df.empty:
        return []

    teams = pd.concat([

        matches_df["team1"],

        matches_df["team2"]

    ]).dropna().unique()

    return sorted(
        list(teams)
    )

# ==========================================
# UNIQUE PLAYERS
# ==========================================

def unique_players(
    ball_df
):

    if ball_df.empty:
        return []

    players = pd.concat([

        ball_df["striker"],

        ball_df["non_striker"],

        ball_df["bowler"]

    ]).dropna().unique()

    return sorted(
        list(players)
    )

# ==========================================
# EXPORT CSV
# ==========================================

def dataframe_to_csv(
    df
):

    if df.empty:
        return ""

    return df.to_csv(
        index=False
    )

# ==========================================
# DATE FORMAT
# ==========================================

def format_date(
    date_string
):

    try:

        date_obj = datetime.fromisoformat(
            str(date_string)
        )

        return date_obj.strftime(
            "%d %b %Y"
        )

    except:
        return str(date_string)