import pandas as pd

from database.queries import (

    fetch_matches,

    fetch_ball_data
)

from utils.charts import (

    generate_manhattan_chart,

    generate_worm_chart,

    generate_run_rate_chart,

    generate_phase_runs_chart,

    generate_wicket_timeline
)

from utils.match_summary import (
    generate_match_summary
)

from utils.player_stats import (

    batting_career_stats,

    bowling_career_stats
)

from utils.team_stats import (
    team_career_stats
)

# ==========================================
# LOAD BALL DATA
# ==========================================

def load_ball_data(
    match_id
):

    balls = fetch_ball_data(
        match_id
    )

    return pd.DataFrame(balls)

# ==========================================
# MATCH ANALYTICS
# ==========================================

def match_analytics(
    match_id
):

    ball_df = load_ball_data(
        match_id
    )

    if ball_df.empty:
        return {}

    summary = generate_match_summary(
        ball_df
    )

    return {

        "summary": summary,

        "manhattan_chart":

        generate_manhattan_chart(
            ball_df
        ),

        "worm_chart":

        generate_worm_chart(
            ball_df
        ),

        "run_rate_chart":

        generate_run_rate_chart(
            ball_df
        ),

        "phase_chart":

        generate_phase_runs_chart(
            ball_df
        ),

        "wicket_chart":

        generate_wicket_timeline(
            ball_df
        )
    }

# ==========================================
# PLAYER ANALYTICS
# ==========================================

def player_analytics():

    matches = fetch_matches()

    if not matches:
        return {}

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
        return {}

    batting = batting_career_stats(
        ball_df
    )

    bowling = bowling_career_stats(
        ball_df
    )

    return {

        "batting": batting,

        "bowling": bowling
    }

# ==========================================
# TEAM ANALYTICS
# ==========================================

def team_analytics():

    matches = fetch_matches()

    matches_df = pd.DataFrame(
        matches
    )

    if matches_df.empty:
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
        return pd.DataFrame()

    return team_career_stats(

        matches_df,

        ball_df
    )

# ==========================================
# MOST RUNS
# ==========================================

def most_runs_player():

    analytics = player_analytics()

    batting = analytics.get(
        "batting",
        pd.DataFrame()
    )

    if batting.empty:
        return None

    return batting.iloc[0]

# ==========================================
# MOST WICKETS
# ==========================================

def most_wickets_player():

    analytics = player_analytics()

    bowling = analytics.get(
        "bowling",
        pd.DataFrame()
    )

    if bowling.empty:
        return None

    return bowling.iloc[0]

# ==========================================
# BEST TEAM
# ==========================================

def best_team():

    teams = team_analytics()

    if teams.empty:
        return None

    return teams.iloc[0]

# ==========================================
# MATCH COUNT
# ==========================================

def total_matches():

    matches = fetch_matches()

    return len(matches)

# ==========================================
# TOTAL BALLS
# ==========================================

def total_balls():

    matches = fetch_matches()

    total = 0

    for match in matches:

        balls = fetch_ball_data(
            match["match_id"]
        )

        total += len(balls)

    return total

# ==========================================
# TOTAL RUNS
# ==========================================

def total_runs():

    matches = fetch_matches()

    total = 0

    for match in matches:

        balls = fetch_ball_data(
            match["match_id"]
        )

        ball_df = pd.DataFrame(
            balls
        )

        if not ball_df.empty:

            total += int(

                ball_df[
                    "total_runs"
                ].sum()
            )

    return total

# ==========================================
# TOTAL WICKETS
# ==========================================

def total_wickets():

    matches = fetch_matches()

    total = 0

    for match in matches:

        balls = fetch_ball_data(
            match["match_id"]
        )

        ball_df = pd.DataFrame(
            balls
        )

        if not ball_df.empty:

            total += int(

                ball_df[

                    ball_df[
                        "wicket"
                    ] == "Yes"

                ].shape[0]
            )

    return total

# ==========================================
# PLATFORM SUMMARY
# ==========================================

def platform_summary():

    return {

        "matches":
        total_matches(),

        "balls":
        total_balls(),

        "runs":
        total_runs(),

        "wickets":
        total_wickets()
    }

# ==========================================
# MATCH CHARTS
# ==========================================

def match_charts(
    match_id
):

    analytics = match_analytics(
        match_id
    )

    return {

        "manhattan":
        analytics.get(
            "manhattan_chart"
        ),

        "worm":
        analytics.get(
            "worm_chart"
        ),

        "run_rate":
        analytics.get(
            "run_rate_chart"
        ),

        "phase":
        analytics.get(
            "phase_chart"
        ),

        "wickets":
        analytics.get(
            "wicket_chart"
        )
    }