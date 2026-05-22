import pandas as pd

from database.queries import (

    fetch_ball_data,

    fetch_match,

    update_match_result,

    update_match_target
)

from utils.calculations import (

    get_match_summary,

    calculate_balls_remaining,

    calculate_required_rr
)

# ==========================================
# LOAD MATCH BALL DATA
# ==========================================

def load_match_dataframe(
    match_id
):

    balls = fetch_ball_data(
        match_id
    )

    return pd.DataFrame(balls)

# ==========================================
# CURRENT SCORE
# ==========================================

def current_score(
    match_id
):

    ball_df = load_match_dataframe(
        match_id
    )

    return get_match_summary(
        ball_df
    )

# ==========================================
# FIRST INNINGS SCORE
# ==========================================

def first_innings_score(
    match_id
):

    ball_df = load_match_dataframe(
        match_id
    )

    if ball_df.empty:
        return 0

    innings1 = ball_df[
        ball_df["innings"] == 1
    ]

    if innings1.empty:
        return 0

    return int(
        innings1["total_runs"]
        .sum()
    )

# ==========================================
# SECOND INNINGS SCORE
# ==========================================

def second_innings_score(
    match_id
):

    ball_df = load_match_dataframe(
        match_id
    )

    if ball_df.empty:
        return 0

    innings2 = ball_df[
        ball_df["innings"] == 2
    ]

    if innings2.empty:
        return 0

    return int(
        innings2["total_runs"]
        .sum()
    )

# ==========================================
# SET FIRST INNINGS TARGET
# ==========================================

def finalize_first_innings(
    match_id
):

    score = (
        first_innings_score(
            match_id
        )
    )

    target = score + 1

    update_match_target(
        match_id,
        target
    )

    return target

# ==========================================
# CHECK INNINGS COMPLETE
# ==========================================

def innings_completed(

    legal_balls,

    max_overs,

    wickets
):

    if wickets >= 10:
        return True

    max_balls = (
        int(max_overs) * 6
    )

    return legal_balls >= max_balls

# ==========================================
# CHECK CHASE WON
# ==========================================

def chase_completed(

    current_score,

    target
):

    if target <= 0:
        return False

    return current_score >= target

# ==========================================
# RESULT ENGINE
# ==========================================

def process_match_result(
    match_id
):

    match = fetch_match(
        match_id
    )

    if not match:
        return None

    target = int(
        match.get("target", 0)
    )

    if target <= 0:
        return None

    team1 = match["team1"]

    team2 = match["team2"]

    batting_first = (
        match["batting_first"]
    )

    batting_second = (
        match["batting_second"]
    )

    innings1_score = (
        first_innings_score(
            match_id
        )
    )

    innings2_score = (
        second_innings_score(
            match_id
        )
    )

    # ======================================
    # CHASE WON
    # ======================================

    if innings2_score >= target:

        winner = batting_second

        wickets_remaining = (
            10
            -
            current_score(
                match_id
            )["wickets"]
        )

        result = (

            f"{winner} won by "

            f"{wickets_remaining} wickets"
        )

    # ======================================
    # DEFENDING TEAM WON
    # ======================================

    elif innings1_score > innings2_score:

        winner = batting_first

        margin = (
            innings1_score
            -
            innings2_score
        )

        result = (

            f"{winner} won by "

            f"{margin} runs"
        )

    # ======================================
    # TIE
    # ======================================

    else:

        winner = "Tie"

        result = "Match Tied"

    update_match_result(

        match_id,

        winner,

        result
    )

    return {

        "winner": winner,

        "result": result
    }

# ==========================================
# REQUIRED RUNS
# ==========================================

def runs_required(
    current_score,
    target
):

    remaining = (
        target - current_score
    )

    return max(remaining, 0)

# ==========================================
# CHASE METRICS
# ==========================================

def chase_metrics(
    match_id
):

    match = fetch_match(
        match_id
    )

    if not match:
        return None

    target = int(
        match.get("target", 0)
    )

    if target <= 0:
        return None

    summary = current_score(
        match_id
    )

    balls_remaining = (
        calculate_balls_remaining(

            match["overs"],

            summary["legal_balls"]
        )
    )

    required_rr = (
        calculate_required_rr(

            summary["runs"],

            target,

            balls_remaining
        )
    )

    required_runs = (
        runs_required(

            summary["runs"],

            target
        )
    )

    return {

        "target": target,

        "required_runs": required_runs,

        "balls_remaining": balls_remaining,

        "required_rr": required_rr
    }

# ==========================================
# MATCH COMPLETED CHECK
# ==========================================

def is_match_completed(
    match_id
):

    match = fetch_match(
        match_id
    )

    if not match:
        return False

    return (
        match["status"]
        ==
        "COMPLETED"
    )

# ==========================================
# GET CURRENT INNINGS
# ==========================================

def current_innings(
    match_id
):

    match = fetch_match(
        match_id
    )

    if not match:
        return 1

    return int(
        match.get("innings", 1)
    )

# ==========================================
# TOTAL BOUNDARIES
# ==========================================

def total_boundaries(
    match_id
):

    ball_df = load_match_dataframe(
        match_id
    )

    if ball_df.empty:

        return {

            "fours": 0,

            "sixes": 0
        }

    fours = int(

        ball_df[
            ball_df["runs_off_bat"]
            == 4
        ].shape[0]
    )

    sixes = int(

        ball_df[
            ball_df["runs_off_bat"]
            == 6
        ].shape[0]
    )

    return {

        "fours": fours,

        "sixes": sixes
    }