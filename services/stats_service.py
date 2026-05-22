import pandas as pd

from database.queries import (

    fetch_ball_data,

    fetch_matches
)

from utils.batting_scorecard import (
    generate_batting_scorecard
)

from utils.bowling_scorecard import (
    generate_bowling_scorecard
)

from utils.player_stats import (

    batting_career_stats,

    bowling_career_stats
)

from utils.team_stats import (
    team_career_stats
)

from utils.match_summary import (
    generate_match_summary
)

# ==========================================
# BALL DATAFRAME
# ==========================================

def load_ball_df(
    match_id
):

    balls = fetch_ball_data(
        match_id
    )

    return pd.DataFrame(balls)

# ==========================================
# MATCH SUMMARY
# ==========================================

def get_match_summary_service(
    match_id
):

    ball_df = load_ball_df(
        match_id
    )

    if ball_df.empty:
        return {}

    return generate_match_summary(
        ball_df
    )

# ==========================================
# BATTING SCORECARD
# ==========================================

def batting_scorecard_service(
    match_id
):

    ball_df = load_ball_df(
        match_id
    )

    return generate_batting_scorecard(
        ball_df
    )

# ==========================================
# BOWLING SCORECARD
# ==========================================

def bowling_scorecard_service(
    match_id
):

    ball_df = load_ball_df(
        match_id
    )

    return generate_bowling_scorecard(
        ball_df
    )

# ==========================================
# PLAYER BATTING STATS
# ==========================================

def player_batting_stats():

    matches = fetch_matches()

    if not matches:
        return pd.DataFrame()

    all_balls = []

    for match in matches:

        balls = fetch_ball_data(
            match["match_id"]
        )

        all_balls.extend(balls)

    ball_df = pd.DataFrame(
        all_balls
    )

    if ball_df.empty:
        return ball_df

    return batting_career_stats(
        ball_df
    )

# ==========================================
# PLAYER BOWLING STATS
# ==========================================

def player_bowling_stats():

    matches = fetch_matches()

    if not matches:
        return pd.DataFrame()

    all_balls = []

    for match in matches:

        balls = fetch_ball_data(
            match["match_id"]
        )

        all_balls.extend(balls)

    ball_df = pd.DataFrame(
        all_balls
    )

    if ball_df.empty:
        return ball_df

    return bowling_career_stats(
        ball_df
    )

# ==========================================
# TEAM STATS
# ==========================================

def team_stats_service():

    matches = fetch_matches()

    matches_df = pd.DataFrame(
        matches
    )

    if matches_df.empty:
        return matches_df

    all_balls = []

    for match in matches:

        balls = fetch_ball_data(
            match["match_id"]
        )

        all_balls.extend(balls)

    ball_df = pd.DataFrame(
        all_balls
    )

    if ball_df.empty:
        return pd.DataFrame()

    return team_career_stats(

        matches_df,

        ball_df
    )

# ==========================================
# ORANGE CAP
# ==========================================

def orange_cap_holder():

    batting_df = (
        player_batting_stats()
    )

    if batting_df.empty:
        return None

    return batting_df.iloc[0]

# ==========================================
# PURPLE CAP
# ==========================================

def purple_cap_holder():

    bowling_df = (
        player_bowling_stats()
    )

    if bowling_df.empty:
        return None

    return bowling_df.iloc[0]

# ==========================================
# TOP TEAM
# ==========================================

def top_team():

    team_df = team_stats_service()

    if team_df.empty:
        return None

    return team_df.iloc[0]

# ==========================================
# MATCH ANALYTICS
# ==========================================

def match_analytics(
    match_id
):

    summary = (
        get_match_summary_service(
            match_id
        )
    )

    batting = (
        batting_scorecard_service(
            match_id
        )
    )

    bowling = (
        bowling_scorecard_service(
            match_id
        )
    )

    return {

        "summary": summary,

        "batting": batting,

        "bowling": bowling
    }

# ==========================================
# PLAYER PROFILE
# ==========================================

def player_profile(
    player_name
):

    batting_df = (
        player_batting_stats()
    )

    bowling_df = (
        player_bowling_stats()
    )

    batting = batting_df[

        batting_df["Player"]
        == player_name
    ]

    bowling = bowling_df[

        bowling_df["Bowler"]
        == player_name
    ]

    return {

        "batting":

        batting.iloc[0].to_dict()

        if not batting.empty

        else None,

        "bowling":

        bowling.iloc[0].to_dict()

        if not bowling.empty

        else None
    }

# ==========================================
# TEAM PROFILE
# ==========================================

def team_profile(
    team_name
):

    teams_df = (
        team_stats_service()
    )

    if teams_df.empty:
        return None

    team = teams_df[
        teams_df["Team"]
        == team_name
    ]

    if team.empty:
        return None

    return team.iloc[0].to_dict()

# ==========================================
# TOTAL DATABASE BALLS
# ==========================================

def total_balls_recorded():

    matches = fetch_matches()

    total = 0

    for match in matches:

        balls = fetch_ball_data(
            match["match_id"]
        )

        total += len(balls)

    return total