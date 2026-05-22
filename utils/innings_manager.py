from database.queries import (

    fetch_match,

    fetch_match_state,

    update_match_state,

    update_match_target
)

from utils.score_engine import (

    first_innings_score,

    second_innings_score
)

from utils.result_engine import (
    complete_match
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

    target = (
        first_innings_score(
            match_id
        )
        + 1
    )

    update_match_target(
        match_id,
        target
    )

    update_match_state(

        match_id=match_id,

        innings=2,

        striker=striker,

        non_striker=non_striker,

        bowler=bowler,

        batting_team=match[
            "batting_second"
        ],

        bowling_team=match[
            "batting_first"
        ],

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
# CHECK FIRST INNINGS END
# ==========================================

def first_innings_completed(

    wickets,

    legal_balls,

    max_overs
):

    if wickets >= 10:
        return True

    max_balls = (
        int(max_overs) * 6
    )

    return legal_balls >= max_balls

# ==========================================
# CHECK SECOND INNINGS END
# ==========================================

def second_innings_completed(

    current_score,

    target,

    wickets,

    legal_balls,

    max_overs
):

    if current_score >= target:
        return True

    if wickets >= 10:
        return True

    max_balls = (
        int(max_overs) * 6
    )

    return legal_balls >= max_balls

# ==========================================
# NEXT INNINGS DECISION
# ==========================================

def process_innings_transition(
    match_id
):

    match = fetch_match(
        match_id
    )

    state = fetch_match_state(
        match_id
    )

    if not match or not state:
        return None

    innings = int(
        state["innings"]
    )

    wickets = int(
        state["wickets"]
    )

    legal_balls = int(
        state["legal_balls"]
    )

    max_overs = int(
        match["overs"]
    )

    current_score = int(
        state["current_score"]
    )

    target = int(
        state["target"]
    )

    # ======================================
    # FIRST INNINGS
    # ======================================

    if innings == 1:

        if first_innings_completed(

            wickets,

            legal_balls,

            max_overs
        ):

            return {

                "action":
                "start_second_innings"
            }

    # ======================================
    # SECOND INNINGS
    # ======================================

    if innings == 2:

        if second_innings_completed(

            current_score,

            target,

            wickets,

            legal_balls,

            max_overs
        ):

            return {

                "action":
                "complete_match"
            }

    return {

        "action": "continue"
    }

# ==========================================
# COMPLETE CURRENT MATCH
# ==========================================

def finish_match(
    match_id
):

    return complete_match(
        match_id
    )

# ==========================================
# MATCH TARGET
# ==========================================

def current_target(
    match_id
):

    match = fetch_match(
        match_id
    )

    if not match:
        return 0

    return int(
        match.get("target", 0)
    )

# ==========================================
# RUNS REQUIRED
# ==========================================

def runs_required(
    match_id
):

    target = current_target(
        match_id
    )

    current = (
        second_innings_score(
            match_id
        )
    )

    remaining = (
        target - current
    )

    return max(remaining, 0)

# ==========================================
# BALLS REMAINING
# ==========================================

def balls_remaining(
    match_id
):

    match = fetch_match(
        match_id
    )

    state = fetch_match_state(
        match_id
    )

    if not match or not state:
        return 0

    total_balls = (
        int(match["overs"]) * 6
    )

    used = int(
        state["legal_balls"]
    )

    remaining = (
        total_balls - used
    )

    return max(remaining, 0)

# ==========================================
# REQUIRED RUN RATE
# ==========================================

def required_run_rate(
    match_id
):

    required = runs_required(
        match_id
    )

    remaining_balls = (
        balls_remaining(
            match_id
        )
    )

    if remaining_balls <= 0:
        return 0

    overs_remaining = (
        remaining_balls / 6
    )

    return round(
        required / overs_remaining,
        2
    )

# ==========================================
# MATCH STATUS
# ==========================================

def innings_status(
    match_id
):

    state = fetch_match_state(
        match_id
    )

    if not state:
        return None

    innings = int(
        state["innings"]
    )

    if innings == 1:

        return "First Innings"

    return "Second Innings"

# ==========================================
# CURRENT SCORE DISPLAY
# ==========================================

def live_score(
    match_id
):

    state = fetch_match_state(
        match_id
    )

    if not state:
        return "0/0"

    score = int(
        state["current_score"]
    )

    wickets = int(
        state["wickets"]
    )

    return f"{score}/{wickets}"

# ==========================================
# CURRENT OVER DISPLAY
# ==========================================

def live_overs(
    match_id
):

    state = fetch_match_state(
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