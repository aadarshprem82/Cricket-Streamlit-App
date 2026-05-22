from database.queries import (

    create_match_state,

    fetch_match_state,

    update_match_state,

    fetch_match
)

# ==========================================
# INITIALIZE MATCH STATE
# ==========================================

def initialize_match_state(
    match_id
):

    existing = fetch_match_state(
        match_id
    )

    if existing:
        return existing

    create_match_state(
        match_id
    )

    return fetch_match_state(
        match_id
    )

# ==========================================
# START MATCH
# ==========================================

def start_match(

    match_id,

    striker,

    non_striker,

    bowler
):

    match = fetch_match(
        match_id
    )

    if not match:
        return False

    batting_team = (
        match["batting_first"]
    )

    bowling_team = (
        match["batting_second"]
    )

    update_match_state(

        match_id=match_id,

        innings=1,

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

        target=0,

        last_event="Match started",

        free_hit=0,

        match_completed=0
    )

    return True

# ==========================================
# GET STATE
# ==========================================

def get_match_state(
    match_id
):

    return fetch_match_state(
        match_id
    )

# ==========================================
# UPDATE SCORE
# ==========================================

def update_score(

    match_id,

    runs,

    wicket=False
):

    state = fetch_match_state(
        match_id
    )

    if not state:
        return

    current_score = (
        int(state["current_score"])
        + runs
    )

    wickets = int(
        state["wickets"]
    )

    if wicket:
        wickets += 1

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

        current_score=current_score,

        wickets=wickets,

        target=state["target"],

        last_event=f"{runs} run(s)",

        free_hit=state["free_hit"],

        match_completed=state["match_completed"]
    )

# ==========================================
# UPDATE BALL COUNT
# ==========================================

def increment_ball(
    match_id
):

    state = fetch_match_state(
        match_id
    )

    if not state:
        return

    current_ball = (
        int(state["current_ball"])
        + 1
    )

    current_over = int(
        state["current_over"]
    )

    legal_balls = int(
        state["legal_balls"]
    ) + 1

    # ======================================
    # OVER COMPLETE
    # ======================================

    if current_ball > 6:

        current_ball = 1

        current_over += 1

        striker = (
            state["non_striker"]
        )

        non_striker = (
            state["striker"]
        )

    else:

        striker = state["striker"]

        non_striker = (
            state["non_striker"]
        )

    update_match_state(

        match_id=match_id,

        innings=state["innings"],

        striker=striker,

        non_striker=non_striker,

        bowler=state["bowler"],

        batting_team=state["batting_team"],

        bowling_team=state["bowling_team"],

        current_over=current_over,

        current_ball=current_ball,

        legal_balls=legal_balls,

        current_score=state["current_score"],

        wickets=state["wickets"],

        target=state["target"],

        last_event=state["last_event"],

        free_hit=state["free_hit"],

        match_completed=state["match_completed"]
    )

# ==========================================
# ROTATE STRIKE
# ==========================================

def rotate_strike(
    match_id
):

    state = fetch_match_state(
        match_id
    )

    if not state:
        return

    update_match_state(

        match_id=match_id,

        innings=state["innings"],

        striker=state["non_striker"],

        non_striker=state["striker"],

        bowler=state["bowler"],

        batting_team=state["batting_team"],

        bowling_team=state["bowling_team"],

        current_over=state["current_over"],

        current_ball=state["current_ball"],

        legal_balls=state["legal_balls"],

        current_score=state["current_score"],

        wickets=state["wickets"],

        target=state["target"],

        last_event="Strike rotated",

        free_hit=state["free_hit"],

        match_completed=state["match_completed"]
    )

# ==========================================
# CHANGE BOWLER
# ==========================================

def change_bowler(

    match_id,

    bowler
):

    state = fetch_match_state(
        match_id
    )

    if not state:
        return

    update_match_state(

        match_id=match_id,

        innings=state["innings"],

        striker=state["striker"],

        non_striker=state["non_striker"],

        bowler=bowler,

        batting_team=state["batting_team"],

        bowling_team=state["bowling_team"],

        current_over=state["current_over"],

        current_ball=state["current_ball"],

        legal_balls=state["legal_balls"],

        current_score=state["current_score"],

        wickets=state["wickets"],

        target=state["target"],

        last_event=f"{bowler} starts bowling",

        free_hit=state["free_hit"],

        match_completed=state["match_completed"]
    )

# ==========================================
# NEW BATTER
# ==========================================

def add_new_batter(

    match_id,

    out_player,

    new_batter
):

    state = fetch_match_state(
        match_id
    )

    if not state:
        return

    striker = state["striker"]

    non_striker = (
        state["non_striker"]
    )

    if striker == out_player:

        striker = new_batter

    else:

        non_striker = (
            new_batter
        )

    update_match_state(

        match_id=match_id,

        innings=state["innings"],

        striker=striker,

        non_striker=non_striker,

        bowler=state["bowler"],

        batting_team=state["batting_team"],

        bowling_team=state["bowling_team"],

        current_over=state["current_over"],

        current_ball=state["current_ball"],

        legal_balls=state["legal_balls"],

        current_score=state["current_score"],

        wickets=state["wickets"],

        target=state["target"],

        last_event=f"{new_batter} came in",

        free_hit=state["free_hit"],

        match_completed=state["match_completed"]
    )

# ==========================================
# FREE HIT
# ==========================================

def set_free_hit(

    match_id,

    enabled
):

    state = fetch_match_state(
        match_id
    )

    if not state:
        return

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

        last_event="Free hit updated",

        free_hit=int(enabled),

        match_completed=state["match_completed"]
    )

# ==========================================
# COMPLETE MATCH
# ==========================================

def mark_match_complete(
    match_id
):

    state = fetch_match_state(
        match_id
    )

    if not state:
        return

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

        free_hit=state["free_hit"],

        match_completed=1
    )