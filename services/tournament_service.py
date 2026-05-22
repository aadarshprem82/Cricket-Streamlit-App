import pandas as pd

from utils.tournament_engine import (

    create_tournament,

    fetch_tournaments,

    fetch_tournament,

    add_match_to_tournament,

    fetch_tournament_matches,

    initialize_points_table,

    update_points_table,

    fetch_points_table,

    declare_tournament_winner,

    start_tournament,

    qualified_teams
)

from utils.helpers import (
    generate_tournament_id
)

# ==========================================
# CREATE TOURNAMENT
# ==========================================

def create_new_tournament(

    tournament_name,

    format_type,

    teams
):

    tournament_id = (
        generate_tournament_id()
    )

    create_tournament(

        tournament_id=tournament_id,

        tournament_name=tournament_name,

        format_type=format_type,

        total_teams=len(teams)
    )

    initialize_points_table(

        tournament_id,

        teams
    )

    return tournament_id

# ==========================================
# ALL TOURNAMENTS
# ==========================================

def all_tournaments():

    tournaments = fetch_tournaments()

    return pd.DataFrame(
        tournaments
    )

# ==========================================
# TOURNAMENT DETAILS
# ==========================================

def tournament_details(
    tournament_id
):

    return fetch_tournament(
        tournament_id
    )

# ==========================================
# ADD MATCH
# ==========================================

def add_match(

    tournament_id,

    match_id
):

    add_match_to_tournament(

        tournament_id,

        match_id
    )

# ==========================================
# TOURNAMENT MATCHES
# ==========================================

def tournament_matches(
    tournament_id
):

    matches = (
        fetch_tournament_matches(
            tournament_id
        )
    )

    return pd.DataFrame(matches)

# ==========================================
# START TOURNAMENT
# ==========================================

def begin_tournament(
    tournament_id
):

    start_tournament(
        tournament_id
    )

# ==========================================
# UPDATE RESULT
# ==========================================

def update_result(

    tournament_id,

    winner,

    loser=None,

    tie=False
):

    update_points_table(

        tournament_id,

        winner,

        loser,

        tie
    )

# ==========================================
# POINTS TABLE
# ==========================================

def points_table(
    tournament_id
):

    return fetch_points_table(
        tournament_id
    )

# ==========================================
# LEADER
# ==========================================

def tournament_leader(
    tournament_id
):

    table = points_table(
        tournament_id
    )

    if table.empty:
        return None

    return table.iloc[0]

# ==========================================
# QUALIFIERS
# ==========================================

def qualifiers(

    tournament_id,

    limit=4
):

    return qualified_teams(

        tournament_id,

        qualification_count=limit
    )

# ==========================================
# DECLARE WINNER
# ==========================================

def finish_tournament(

    tournament_id,

    winner
):

    declare_tournament_winner(

        tournament_id,

        winner
    )

# ==========================================
# TOURNAMENT SUMMARY
# ==========================================

def tournament_summary(
    tournament_id
):

    tournament = (
        tournament_details(
            tournament_id
        )
    )

    if not tournament:
        return None

    matches_df = (
        tournament_matches(
            tournament_id
        )
    )

    points_df = points_table(
        tournament_id
    )

    return {

        "Tournament":
        tournament[
            "tournament_name"
        ],

        "Format":
        tournament[
            "format_type"
        ],

        "Status":
        tournament[
            "status"
        ],

        "Teams":
        tournament[
            "total_teams"
        ],

        "Matches":
        int(
            matches_df.shape[0]
        ),

        "Leader":

        points_df.iloc[0][
            "team_name"
        ]

        if not points_df.empty

        else None
    }

# ==========================================
# ACTIVE TOURNAMENTS
# ==========================================

def active_tournaments():

    tournaments_df = (
        all_tournaments()
    )

    if tournaments_df.empty:
        return tournaments_df

    return tournaments_df[

        tournaments_df["status"]
        == "LIVE"
    ]

# ==========================================
# COMPLETED TOURNAMENTS
# ==========================================

def completed_tournaments():

    tournaments_df = (
        all_tournaments()
    )

    if tournaments_df.empty:
        return tournaments_df

    return tournaments_df[

        tournaments_df["status"]
        == "COMPLETED"
    ]

# ==========================================
# UPCOMING TOURNAMENTS
# ==========================================

def upcoming_tournaments():

    tournaments_df = (
        all_tournaments()
    )

    if tournaments_df.empty:
        return tournaments_df

    return tournaments_df[

        tournaments_df["status"]
        == "UPCOMING"
    ]

# ==========================================
# TOURNAMENT COUNT
# ==========================================

def tournament_count():

    tournaments_df = (
        all_tournaments()
    )

    return int(
        tournaments_df.shape[0]
    )

# ==========================================
# LIVE TOURNAMENT COUNT
# ==========================================

def live_tournament_count():

    tournaments_df = (
        active_tournaments()
    )

    return int(
        tournaments_df.shape[0]
    )