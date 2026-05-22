import pandas as pd

from database.queries import (

    create_match,

    fetch_match,

    fetch_all_matches,

    update_match_status,

    fetch_ball_data
)

from utils.helpers import (
    generate_match_id
)

from utils.match_summary import (
    generate_match_summary
)

# ==========================================
# CREATE NEW MATCH
# ==========================================

def create_new_match(

    team1,

    team2,

    overs,

    toss_winner,

    elected
):

    match_id = generate_match_id()

    if elected == "Bat":

        batting_first = toss_winner

        batting_second = (

            team2

            if toss_winner == team1

            else team1
        )

    else:

        batting_second = toss_winner

        batting_first = (

            team2

            if toss_winner == team1

            else team1
        )

    create_match(

        match_id=match_id,

        team1=team1,

        team2=team2,

        overs=overs,

        toss_winner=toss_winner,

        elected=elected,

        batting_first=batting_first,

        batting_second=batting_second
    )

    return match_id

# ==========================================
# GET MATCH
# ==========================================

def get_match(
    match_id
):

    return fetch_match(
        match_id
    )

# ==========================================
# GET ALL MATCHES
# ==========================================

def get_all_matches():

    matches = fetch_all_matches()

    return pd.DataFrame(matches)

# ==========================================
# LIVE MATCHES
# ==========================================

def get_live_matches():

    matches_df = get_all_matches()

    if matches_df.empty:
        return matches_df

    return matches_df[

        matches_df["status"]
        == "LIVE"
    ]

# ==========================================
# COMPLETED MATCHES
# ==========================================

def get_completed_matches():

    matches_df = get_all_matches()

    if matches_df.empty:
        return matches_df

    return matches_df[

        matches_df["status"]
        == "COMPLETED"
    ]

# ==========================================
# UPCOMING MATCHES
# ==========================================

def get_upcoming_matches():

    matches_df = get_all_matches()

    if matches_df.empty:
        return matches_df

    return matches_df[

        matches_df["status"]
        == "UPCOMING"
    ]

# ==========================================
# START MATCH
# ==========================================

def start_match(
    match_id
):

    update_match_status(
        match_id,
        "LIVE"
    )

# ==========================================
# COMPLETE MATCH
# ==========================================

def complete_match(
    match_id
):

    update_match_status(
        match_id,
        "COMPLETED"
    )

# ==========================================
# MATCH SCORECARD
# ==========================================

def match_scorecard(
    match_id
):

    balls = fetch_ball_data(
        match_id
    )

    if not balls:
        return {}

    ball_df = pd.DataFrame(
        balls
    )

    return generate_match_summary(
        ball_df
    )

# ==========================================
# MATCH EXISTS
# ==========================================

def match_exists(
    match_id
):

    match = fetch_match(
        match_id
    )

    return match is not None

# ==========================================
# TOTAL MATCHES
# ==========================================

def total_matches():

    matches_df = get_all_matches()

    return int(
        matches_df.shape[0]
    )

# ==========================================
# LIVE MATCH COUNT
# ==========================================

def live_match_count():

    matches_df = get_live_matches()

    return int(
        matches_df.shape[0]
    )

# ==========================================
# RECENT MATCHES
# ==========================================

def recent_matches(
    limit=5
):

    matches_df = get_all_matches()

    if matches_df.empty:
        return matches_df

    return matches_df.head(
        limit
    )

# ==========================================
# TEAM MATCHES
# ==========================================

def team_matches(
    team_name
):

    matches_df = get_all_matches()

    if matches_df.empty:
        return matches_df

    return matches_df[

        (matches_df["team1"]
         == team_name)

        |

        (matches_df["team2"]
         == team_name)
    ]

# ==========================================
# TEAM WINS
# ==========================================

def team_wins(
    team_name
):

    matches_df = get_all_matches()

    if matches_df.empty:
        return 0

    wins = matches_df[

        matches_df["winner"]
        == team_name
    ]

    return int(
        wins.shape[0]
    )

# ==========================================
# MATCH RESULT
# ==========================================

def match_result(
    match_id
):

    match = fetch_match(
        match_id
    )

    if not match:
        return None

    return {

        "winner":
        match.get("winner"),

        "result":
        match.get("result")
    }

# ==========================================
# MATCH HEADER
# ==========================================

def match_header(
    match_id
):

    match = fetch_match(
        match_id
    )

    if not match:
        return None

    return (

        f'{match["team1"]} '

        f'vs '

        f'{match["team2"]}'
    )

# ==========================================
# DELETE MATCH
# ==========================================

def delete_match(
    match_id
):

    from database.db import (
        execute_query
    )

    queries = [

        (
            "DELETE FROM "
            "ball_by_ball "
            "WHERE match_id=?"
        ),

        (
            "DELETE FROM "
            "match_state "
            "WHERE match_id=?"
        ),

        (
            "DELETE FROM "
            "matches "
            "WHERE match_id=?"
        )
    ]

    for query in queries:

        execute_query(
            query,
            (match_id,)
        )