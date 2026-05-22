from datetime import datetime
import pandas as pd

from database.db import (

    execute_query,

    fetch_all,

    fetch_one
)

# ==========================================
# CREATE TOURNAMENT
# ==========================================

def create_tournament(

    tournament_id,

    tournament_name,

    format_type,

    total_teams
):

    query = """

    INSERT INTO tournaments (

        tournament_id,
        tournament_name,
        format_type,
        total_teams,
        status,
        created_at

    )

    VALUES (?, ?, ?, ?, ?, ?)

    """

    execute_query(

        query,

        (

            tournament_id,

            tournament_name,

            format_type,

            total_teams,

            "UPCOMING",

            str(datetime.now())
        )
    )

# ==========================================
# FETCH TOURNAMENTS
# ==========================================

def fetch_tournaments():

    query = """

    SELECT *

    FROM tournaments

    ORDER BY id DESC

    """

    return fetch_all(query)

# ==========================================
# FETCH TOURNAMENT
# ==========================================

def fetch_tournament(
    tournament_id
):

    query = """

    SELECT *

    FROM tournaments

    WHERE tournament_id=?

    """

    return fetch_one(
        query,
        (tournament_id,)
    )

# ==========================================
# ADD MATCH TO TOURNAMENT
# ==========================================

def add_match_to_tournament(

    tournament_id,

    match_id
):

    query = """

    INSERT INTO tournament_matches (

        tournament_id,
        match_id

    )

    VALUES (?, ?)

    """

    execute_query(

        query,

        (
            tournament_id,
            match_id
        )
    )

# ==========================================
# FETCH TOURNAMENT MATCHES
# ==========================================

def fetch_tournament_matches(
    tournament_id
):

    query = """

    SELECT *

    FROM tournament_matches

    WHERE tournament_id=?

    """

    return fetch_all(
        query,
        (tournament_id,)
    )

# ==========================================
# INITIALIZE POINTS TABLE
# ==========================================

def initialize_points_table(

    tournament_id,

    teams
):

    query = """

    INSERT INTO points_table (

        tournament_id,
        team_name

    )

    VALUES (?, ?)

    """

    for team in teams:

        execute_query(

            query,

            (
                tournament_id,
                team
            )
        )

# ==========================================
# UPDATE POINTS
# ==========================================

def update_points_table(

    tournament_id,

    winner,

    loser=None,

    tie=False
):

    if tie:

        tie_query = """

        UPDATE points_table

        SET played = played + 1,
            tied = tied + 1,
            points = points + 1

        WHERE tournament_id=?
        AND team_name=?

        """

        execute_query(

            tie_query,

            (
                tournament_id,
                winner
            )
        )

        execute_query(

            tie_query,

            (
                tournament_id,
                loser
            )
        )

        return

    # ======================================
    # WINNER
    # ======================================

    winner_query = """

    UPDATE points_table

    SET played = played + 1,
        won = won + 1,
        points = points + 2

    WHERE tournament_id=?
    AND team_name=?

    """

    execute_query(

        winner_query,

        (
            tournament_id,
            winner
        )
    )

    # ======================================
    # LOSER
    # ======================================

    if loser:

        loser_query = """

        UPDATE points_table

        SET played = played + 1,
            lost = lost + 1

        WHERE tournament_id=?
        AND team_name=?

        """

        execute_query(

            loser_query,

            (
                tournament_id,
                loser
            )
        )

# ==========================================
# FETCH POINTS TABLE
# ==========================================

def fetch_points_table(
    tournament_id
):

    query = """

    SELECT *

    FROM points_table

    WHERE tournament_id=?

    ORDER BY points DESC,
             net_run_rate DESC

    """

    table = fetch_all(
        query,
        (tournament_id,)
    )

    return pd.DataFrame(table)

# ==========================================
# UPDATE NRR
# ==========================================

def update_net_run_rate(

    tournament_id,

    team_name,

    net_run_rate
):

    query = """

    UPDATE points_table

    SET net_run_rate=?

    WHERE tournament_id=?
    AND team_name=?

    """

    execute_query(

        query,

        (
            net_run_rate,
            tournament_id,
            team_name
        )
    )

# ==========================================
# TOP TEAMS
# ==========================================

def top_teams(

    tournament_id,

    limit=4
):

    table = fetch_points_table(
        tournament_id
    )

    if table.empty:
        return table

    return table.head(limit)

# ==========================================
# TOURNAMENT WINNER
# ==========================================

def declare_tournament_winner(

    tournament_id,

    winner
):

    query = """

    UPDATE tournaments

    SET winner=?,
        status='COMPLETED'

    WHERE tournament_id=?

    """

    execute_query(

        query,

        (
            winner,
            tournament_id
        )
    )

# ==========================================
# START TOURNAMENT
# ==========================================

def start_tournament(
    tournament_id
):

    query = """

    UPDATE tournaments

    SET status='LIVE'

    WHERE tournament_id=?

    """

    execute_query(
        query,
        (tournament_id,)
    )

# ==========================================
# TOURNAMENT SUMMARY
# ==========================================

def tournament_summary(
    tournament_id
):

    tournament = fetch_tournament(
        tournament_id
    )

    if not tournament:
        return None

    matches = (
        fetch_tournament_matches(
            tournament_id
        )
    )

    points = fetch_points_table(
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

        "Matches":
        len(matches),

        "Teams":
        tournament[
            "total_teams"
        ],

        "Leader":

        points.iloc[0][
            "team_name"
        ]

        if not points.empty

        else None
    }

# ==========================================
# QUALIFIED TEAMS
# ==========================================

def qualified_teams(
    tournament_id,
    qualification_count=4
):

    points = fetch_points_table(
        tournament_id
    )

    if points.empty:
        return pd.DataFrame()

    return points.head(
        qualification_count
    )

# ==========================================
# TOURNAMENT MATCH COUNT
# ==========================================

def total_matches_in_tournament(
    tournament_id
):

    matches = (
        fetch_tournament_matches(
            tournament_id
        )
    )

    return len(matches)