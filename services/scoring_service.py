import pandas as pd

from database.queries import (
    fetch_ball_data,
    fetch_match_state
)

from utils.scoring import (

    score_runs,

    score_dot_ball,

    score_wide,

    score_no_ball,

    score_byes,

    score_leg_byes,

    score_wicket
)

from utils.match_state import (

    update_score,

    increment_ball,

    rotate_strike,

    add_new_batter,

    set_free_hit
)

from utils.innings_manager import (
    process_innings_transition
)

# ==========================================
# MATCH STATE
# ==========================================

def current_state(
    match_id
):

    return fetch_match_state(
        match_id
    )

# ==========================================
# BALL DATAFRAME
# ==========================================

def ball_dataframe(
    match_id
):

    balls = fetch_ball_data(
        match_id
    )

    return pd.DataFrame(balls)

# ==========================================
# NORMAL RUNS
# ==========================================

def add_runs(

    match_id,

    runs
):

    state = current_state(
        match_id
    )

    if not state:
        return

    score_runs(

        match_id=match_id,

        innings=state["innings"],

        batting_team=state[
            "batting_team"
        ],

        bowling_team=state[
            "bowling_team"
        ],

        over_num=state[
            "current_over"
        ],

        ball_num=state[
            "current_ball"
        ],

        striker=state[
            "striker"
        ],

        non_striker=state[
            "non_striker"
        ],

        bowler=state[
            "bowler"
        ],

        runs=runs
    )

    update_score(
        match_id,
        runs
    )

    increment_ball(
        match_id
    )

    if runs % 2 == 1:

        rotate_strike(
            match_id
        )

# ==========================================
# DOT BALL
# ==========================================

def add_dot_ball(
    match_id
):

    state = current_state(
        match_id
    )

    if not state:
        return

    score_dot_ball(

        match_id=match_id,

        innings=state["innings"],

        batting_team=state[
            "batting_team"
        ],

        bowling_team=state[
            "bowling_team"
        ],

        over_num=state[
            "current_over"
        ],

        ball_num=state[
            "current_ball"
        ],

        striker=state[
            "striker"
        ],

        non_striker=state[
            "non_striker"
        ],

        bowler=state[
            "bowler"
        ]
    )

    increment_ball(
        match_id
    )

# ==========================================
# WIDE
# ==========================================

def add_wide(
    match_id,
    runs=1
):

    state = current_state(
        match_id
    )

    if not state:
        return

    score_wide(

        match_id=match_id,

        innings=state["innings"],

        batting_team=state[
            "batting_team"
        ],

        bowling_team=state[
            "bowling_team"
        ],

        over_num=state[
            "current_over"
        ],

        ball_num=state[
            "current_ball"
        ],

        striker=state[
            "striker"
        ],

        non_striker=state[
            "non_striker"
        ],

        bowler=state[
            "bowler"
        ],

        extra_runs=runs
    )

    update_score(
        match_id,
        runs
    )

# ==========================================
# NO BALL
# ==========================================

def add_no_ball(

    match_id,

    bat_runs=0
):

    state = current_state(
        match_id
    )

    if not state:
        return

    total = 1 + bat_runs

    score_no_ball(

        match_id=match_id,

        innings=state["innings"],

        batting_team=state[
            "batting_team"
        ],

        bowling_team=state[
            "bowling_team"
        ],

        over_num=state[
            "current_over"
        ],

        ball_num=state[
            "current_ball"
        ],

        striker=state[
            "striker"
        ],

        non_striker=state[
            "non_striker"
        ],

        bowler=state[
            "bowler"
        ],

        bat_runs=bat_runs
    )

    update_score(
        match_id,
        total
    )

    set_free_hit(
        match_id,
        True
    )

# ==========================================
# BYES
# ==========================================

def add_byes(

    match_id,

    runs
):

    state = current_state(
        match_id
    )

    if not state:
        return

    score_byes(

        match_id=match_id,

        innings=state["innings"],

        batting_team=state[
            "batting_team"
        ],

        bowling_team=state[
            "bowling_team"
        ],

        over_num=state[
            "current_over"
        ],

        ball_num=state[
            "current_ball"
        ],

        striker=state[
            "striker"
        ],

        non_striker=state[
            "non_striker"
        ],

        bowler=state[
            "bowler"
        ],

        byes=runs
    )

    update_score(
        match_id,
        runs
    )

    increment_ball(
        match_id
    )

    if runs % 2 == 1:

        rotate_strike(
            match_id
        )

# ==========================================
# LEG BYES
# ==========================================

def add_leg_byes(

    match_id,

    runs
):

    state = current_state(
        match_id
    )

    if not state:
        return

    score_leg_byes(

        match_id=match_id,

        innings=state["innings"],

        batting_team=state[
            "batting_team"
        ],

        bowling_team=state[
            "bowling_team"
        ],

        over_num=state[
            "current_over"
        ],

        ball_num=state[
            "current_ball"
        ],

        striker=state[
            "striker"
        ],

        non_striker=state[
            "non_striker"
        ],

        bowler=state[
            "bowler"
        ],

        leg_byes=runs
    )

    update_score(
        match_id,
        runs
    )

    increment_ball(
        match_id
    )

# ==========================================
# WICKET
# ==========================================

def add_wicket(

    match_id,

    wicket_type,

    new_batter
):

    state = current_state(
        match_id
    )

    if not state:
        return

    striker = state["striker"]

    score_wicket(

        match_id=match_id,

        innings=state["innings"],

        batting_team=state[
            "batting_team"
        ],

        bowling_team=state[
            "bowling_team"
        ],

        over_num=state[
            "current_over"
        ],

        ball_num=state[
            "current_ball"
        ],

        striker=state[
            "striker"
        ],

        non_striker=state[
            "non_striker"
        ],

        bowler=state[
            "bowler"
        ],

        player_out=striker,

        wicket_type=wicket_type,

        runs=0
    )

    update_score(

        match_id,

        0,

        wicket=True
    )

    increment_ball(
        match_id
    )

    add_new_batter(

        match_id,

        striker,

        new_batter
    )

# ==========================================
# INNINGS CHECK
# ==========================================

def innings_transition_check(
    match_id
):

    return process_innings_transition(
        match_id
    )

# ==========================================
# MATCH SCORE
# ==========================================

def live_score(
    match_id
):

    state = current_state(
        match_id
    )

    if not state:
        return "0/0"

    return (

        f'{state["current_score"]}/'

        f'{state["wickets"]}'
    )

# ==========================================
# LIVE OVERS
# ==========================================

def live_overs(
    match_id
):

    state = current_state(
        match_id
    )

    if not state:
        return "0.0"

    legal_balls = int(
        state["legal_balls"]
    )

    overs = legal_balls // 6

    balls = legal_balls % 6

    return f"{overs}.{balls}"

# ==========================================
# CURRENT BATTERS
# ==========================================

def current_batters(
    match_id
):

    state = current_state(
        match_id
    )

    if not state:
        return {}

    return {

        "striker":
        state["striker"],

        "non_striker":
        state["non_striker"]
    }

# ==========================================
# CURRENT BOWLER
# ==========================================

def current_bowler(
    match_id
):

    state = current_state(
        match_id
    )

    if not state:
        return None

    return state["bowler"]