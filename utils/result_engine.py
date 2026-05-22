from database.queries import (

    fetch_match,

    update_match_result,

    update_match_status
)

from utils.score_engine import (

    first_innings_score,

    second_innings_score
)

# ==========================================
# MATCH RESULT
# ==========================================

def generate_match_result(
    match_id
):

    match = fetch_match(
        match_id
    )

    if not match:
        return None

    innings1 = (
        first_innings_score(
            match_id
        )
    )

    innings2 = (
        second_innings_score(
            match_id
        )
    )

    batting_first = (
        match["batting_first"]
    )

    batting_second = (
        match["batting_second"]
    )

    # ======================================
    # CHASING TEAM WON
    # ======================================

    if innings2 > innings1:

        margin = (
            10
            -
            match.get("wickets", 0)
        )

        return {

            "winner": batting_second,

            "result": (

                f"{batting_second} "

                f"won by {margin} wickets"
            )
        }

    # ======================================
    # DEFENDING TEAM WON
    # ======================================

    if innings1 > innings2:

        margin = (
            innings1 - innings2
        )

        return {

            "winner": batting_first,

            "result": (

                f"{batting_first} "

                f"won by {margin} runs"
            )
        }

    # ======================================
    # TIE
    # ======================================

    return {

        "winner": "Tie",

        "result": "Match Tied"
    }

# ==========================================
# COMPLETE MATCH
# ==========================================

def complete_match(
    match_id
):

    result_data = (
        generate_match_result(
            match_id
        )
    )

    if not result_data:
        return None

    update_match_result(

        match_id,

        result_data["winner"],

        result_data["result"]
    )

    update_match_status(
        match_id,
        "COMPLETED"
    )

    return result_data

# ==========================================
# MATCH TIED
# ==========================================

def is_match_tied(
    match_id
):

    innings1 = (
        first_innings_score(
            match_id
        )
    )

    innings2 = (
        second_innings_score(
            match_id
        )
    )

    return innings1 == innings2

# ==========================================
# MATCH WON BY CHASE
# ==========================================

def won_by_wickets(
    match_id
):

    innings1 = (
        first_innings_score(
            match_id
        )
    )

    innings2 = (
        second_innings_score(
            match_id
        )
    )

    return innings2 > innings1

# ==========================================
# MATCH WON BY DEFENCE
# ==========================================

def won_by_runs(
    match_id
):

    innings1 = (
        first_innings_score(
            match_id
        )
    )

    innings2 = (
        second_innings_score(
            match_id
        )
    )

    return innings1 > innings2

# ==========================================
# WIN MARGIN
# ==========================================

def winning_margin(
    match_id
):

    match = fetch_match(
        match_id
    )

    if not match:
        return None

    innings1 = (
        first_innings_score(
            match_id
        )
    )

    innings2 = (
        second_innings_score(
            match_id
        )
    )

    if innings2 > innings1:

        wickets_remaining = (
            10
            -
            match.get("wickets", 0)
        )

        return {

            "type": "wickets",

            "value": wickets_remaining
        }

    if innings1 > innings2:

        margin = (
            innings1 - innings2
        )

        return {

            "type": "runs",

            "value": margin
        }

    return {

        "type": "tie",

        "value": 0
    }

# ==========================================
# MAN OF THE MATCH
# ==========================================

def assign_man_of_match(

    match_id,

    player_name
):

    query = """

    UPDATE matches

    SET man_of_match=?

    WHERE match_id=?

    """

    from database.db import (
        execute_query
    )

    execute_query(

        query,

        (
            player_name,
            match_id
        )
    )

# ==========================================
# RESULT SUMMARY
# ==========================================

def result_summary(
    match_id
):

    match = fetch_match(
        match_id
    )

    if not match:
        return None

    innings1 = (
        first_innings_score(
            match_id
        )
    )

    innings2 = (
        second_innings_score(
            match_id
        )
    )

    result = (
        generate_match_result(
            match_id
        )
    )

    return {

        "match_id": match_id,

        "team1": match["team1"],

        "team2": match["team2"],

        "innings1_score": innings1,

        "innings2_score": innings2,

        "winner": result["winner"],

        "result": result["result"]
    }

# ==========================================
# CHECK MATCH COMPLETION
# ==========================================

def is_completed(
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
# SUPER OVER NEEDED
# ==========================================

def super_over_needed(
    match_id
):

    return is_match_tied(
        match_id
    )