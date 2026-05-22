from database.queries import (

    fetch_match,

    fetch_match_state,

    update_match_state,

    update_match_target
)

from utils.score_engine import (

    first_innings_score,

    innings_completed,

    chase_completed,

    process_match_result
)

# ==========================================
# START SECOND INNINGS
# ==========================================

def start_second_innings(

    match_id,

    striker,

    non_striker,

    bowler
):

    match = fetch_match(
        match_id
    )

    state = fetch_match_state(
        match_id
    )

    if not match or not state:
        return False

    innings1_score = (
        first_innings_score(
            match_id
        )
    )

    target = innings1_score + 1

    update_match_target(
        match_id,
        target
    )

    batting_team = (
        match["batting_second"]
    )

    bowling_team = (
        match["batting_first"]
    )

    update_match_state(

        match_id=match_id,

        innings=2,

        striker=striker,

        non_striker=non_striker,

        bowler=bowler,

        batting_team=batting_team,

        bowling_team=bowling_team,

        current_over=0,

        current_ball=1,

        legal_balls=0,

        current_score=0,

        wickets=0,

        target=target,

        last_event="Second innings started",

        free_hit=0,

        match_completed=0
    )

    return True

# ==========================================
# CHECK OVER COMPLETE
# ==========================================

def is_over_complete(
    current_ball
):

    return current_ball > 6

# ==========================================
# NEXT OVER
# ==========================================

def move_to_next_over(

    current_over
):

    return current_over + 1

# ==========================================
# ROTATE STRIKE
# ==========================================

def rotate_batters(

    striker,

    non_striker
):

    return (

        non_striker,

        striker
    )

# ==========================================
# SHOULD ROTATE
# ==========================================

def should_rotate_strike(
    runs
):

    return runs % 2 == 1

# ==========================================
# HANDLE END OF OVER
# ==========================================

def process_end_of_over(

    striker,

    non_striker,

    current_over
):

    striker, non_striker = (
        rotate_batters(
            striker,
            non_striker
        )
    )

    next_over = move_to_next_over(
        current_over
    )

    return {

        "striker": striker,

        "non_striker": non_striker,

        "next_over": next_over
    }

# ==========================================
# CHECK FIRST INNINGS END
# ==========================================

def first_innings_finished(

    legal_balls,

    max_overs,

    wickets
):

    return innings_completed(

        legal_balls,

        max_overs,

        wickets
    )

# ==========================================
# CHECK SECOND INNINGS END
# ==========================================

def second_innings_finished(

    current_score,

    target,

    legal_balls,

    max_overs,

    wickets
):

    if chase_completed(
        current_score,
        target
    ):

        return True

    return innings_completed(

        legal_balls,

        max_overs,

        wickets
    )

# ==========================================
# COMPLETE MATCH
# ==========================================

def complete_match(
    match_id
):

    result = process_match_result(
        match_id
    )

    state = fetch_match_state(
        match_id
    )

    if state:

        update_match_state(

            match_id=match_id,

            innings=state["innings"],

            striker=state["striker"],

            non_striker=state["non_striker"],

            bowler=state["bowler"],

            batting_team=state["batting_team"],

            bowling_team=state["bowling_team"],

            current_over=state["current_over"],

            current_ball=state["current_ball"],

            legal_balls=state["legal_balls"],

            current_score=state["current_score"],

            wickets=state["wickets"],

            target=state["target"],

            last_event="Match completed",

            free_hit=0,

            match_completed=1
        )

    return result

# ==========================================
# NEW BATTER ENTRY
# ==========================================

def add_new_batter(

    current_striker,

    dismissed_player,

    new_batter
):

    if current_striker == dismissed_player:

        return {

            "striker": new_batter
        }

    return {

        "non_striker": new_batter
    }

# ==========================================
# FREE HIT RESET
# ==========================================

def reset_free_hit():

    return 0

# ==========================================
# ENABLE FREE HIT
# ==========================================

def activate_free_hit():

    return 1

# ==========================================
# VALIDATE INNINGS TRANSITION
# ==========================================

def can_start_second_innings(
    match_id
):

    match = fetch_match(
        match_id
    )

    state = fetch_match_state(
        match_id
    )

    if not match or not state:
        return False

    return int(
        state["innings"]
    ) == 1

# ==========================================
# SUPER OVER ELIGIBILITY
# ==========================================

def super_over_required(
    innings1_score,
    innings2_score
):

    return (
        innings1_score
        ==
        innings2_score
    )

# ==========================================
# CALCULATE CURRENT OVER
# ==========================================

def current_over_display(
    legal_balls
):

    overs = legal_balls // 6

    balls = legal_balls % 6

    return f"{overs}.{balls}"

# ==========================================
# OVER BALL RESET
# ==========================================

def reset_ball_counter():

    return 1

# ==========================================
# NEXT BALL NUMBER
# ==========================================

def next_ball(
    current_ball
):

    return current_ball + 1