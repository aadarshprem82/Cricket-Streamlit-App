from datetime import datetime

from database.db import (

    execute_query,

    execute_many,

    fetch_all,

    fetch_one
)

# ==========================================
# MATCH QUERIES
# ==========================================

def create_match(

    match_id,

    team1,

    team2,

    overs,

    toss_winner,

    elected,

    batting_first,

    batting_second
):

    query = """

    INSERT INTO matches (

        match_id,
        team1,
        team2,
        overs,
        toss_winner,
        elected,
        batting_first,
        batting_second,
        created_at,
        updated_at

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """

    now = str(datetime.now())

    execute_query(

        query,

        (

            match_id,

            team1,

            team2,

            overs,

            toss_winner,

            elected,

            batting_first,

            batting_second,

            now,

            now
        )
    )

# ==========================================
# FETCH MATCHES
# ==========================================

def fetch_all_matches():

    query = """

    SELECT *

    FROM matches

    ORDER BY id DESC

    """

    return fetch_all(query)

# ==========================================
# FETCH LIVE MATCHES
# ==========================================

def fetch_live_matches():

    query = """

    SELECT *

    FROM matches

    WHERE status='LIVE'

    ORDER BY id DESC

    """

    return fetch_all(query)

# ==========================================
# FETCH MATCH
# ==========================================

def fetch_match(
    match_id
):

    query = """

    SELECT *

    FROM matches

    WHERE match_id=?

    """

    return fetch_one(
        query,
        (match_id,)
    )

# ==========================================
# UPDATE MATCH STATUS
# ==========================================

def update_match_status(

    match_id,
    status
):

    query = """

    UPDATE matches

    SET status=?,
        updated_at=?

    WHERE match_id=?

    """

    execute_query(

        query,

        (
            status,
            str(datetime.now()),
            match_id
        )
    )

# ==========================================
# UPDATE MATCH RESULT
# ==========================================

def update_match_result(

    match_id,

    winner,

    result,

    man_of_match=None
):

    query = """

    UPDATE matches

    SET winner=?,
        result=?,
        man_of_match=?,
        status='COMPLETED',
        updated_at=?

    WHERE match_id=?

    """

    execute_query(

        query,

        (

            winner,

            result,

            man_of_match,

            str(datetime.now()),

            match_id
        )
    )

# ==========================================
# UPDATE TARGET
# ==========================================

def update_match_target(

    match_id,
    target
):

    query = """

    UPDATE matches

    SET target=?,
        updated_at=?

    WHERE match_id=?

    """

    execute_query(

        query,

        (
            target,
            str(datetime.now()),
            match_id
        )
    )

# ==========================================
# BALL EVENTS
# ==========================================

def insert_ball_event(

    match_id,

    innings,

    batting_team,

    bowling_team,

    over_num,

    ball_num,

    striker,

    non_striker,

    bowler,

    runs_off_bat,

    extras,

    extra_type,

    total_runs,

    wicket,

    wicket_type,

    player_out,

    commentary=""
):

    query = """

    INSERT INTO ball_by_ball (

        match_id,
        innings,
        batting_team,
        bowling_team,
        over_num,
        ball_num,
        striker,
        non_striker,
        bowler,
        runs_off_bat,
        extras,
        extra_type,
        total_runs,
        wicket,
        wicket_type,
        player_out,
        commentary,
        created_at

    )

    VALUES (

        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?

    )

    """

    execute_query(

        query,

        (

            match_id,

            innings,

            batting_team,

            bowling_team,

            over_num,

            ball_num,

            striker,

            non_striker,

            bowler,

            runs_off_bat,

            extras,

            extra_type,

            total_runs,

            wicket,

            wicket_type,

            player_out,

            commentary,

            str(datetime.now())
        )
    )

# ==========================================
# FETCH BALL DATA
# ==========================================

def fetch_ball_data(
    match_id
):

    query = """

    SELECT *

    FROM ball_by_ball

    WHERE match_id=?

    ORDER BY id ASC

    """

    return fetch_all(
        query,
        (match_id,)
    )

# ==========================================
# PLAYER QUERIES
# ==========================================

def create_player(

    player_id,

    player_name,

    team,

    role,

    batting_style,

    bowling_style
):

    query = """

    INSERT INTO players (

        player_id,
        player_name,
        team,
        role,
        batting_style,
        bowling_style,
        created_at

    )

    VALUES (?, ?, ?, ?, ?, ?, ?)

    """

    execute_query(

        query,

        (

            player_id,

            player_name,

            team,

            role,

            batting_style,

            bowling_style,

            str(datetime.now())
        )
    )

# ==========================================
# FETCH PLAYERS
# ==========================================

def fetch_players():

    query = """

    SELECT *

    FROM players

    WHERE is_active=1

    ORDER BY player_name ASC

    """

    return fetch_all(query)

# ==========================================
# FETCH TEAM PLAYERS
# ==========================================

def fetch_team_players(
    team_name
):

    query = """

    SELECT *

    FROM players

    WHERE team=?
    AND is_active=1

    ORDER BY player_name ASC

    """

    return fetch_all(
        query,
        (team_name,)
    )

# ==========================================
# DEACTIVATE PLAYER
# ==========================================

def deactivate_player(
    player_name
):

    query = """

    UPDATE players

    SET is_active=0

    WHERE player_name=?

    """

    execute_query(
        query,
        (player_name,)
    )

# ==========================================
# TEAM QUERIES
# ==========================================

def fetch_teams():

    query = """

    SELECT *

    FROM teams

    ORDER BY team_name ASC

    """

    return fetch_all(query)

# ==========================================
# CREATE TEAM
# ==========================================

def create_team(
    team_name
):

    query = """

    INSERT INTO teams (
        team_name,
        created_at
    )

    VALUES (?, ?)

    """

    execute_query(

        query,

        (
            team_name,
            str(datetime.now())
        )
    )

# ==========================================
# MATCH STATE
# ==========================================

def create_match_state(
    match_id
):

    query = """

    INSERT OR IGNORE INTO match_state (

        match_id,
        updated_at

    )

    VALUES (?, ?)

    """

    execute_query(

        query,

        (
            match_id,
            str(datetime.now())
        )
    )

# ==========================================
# FETCH MATCH STATE
# ==========================================

def fetch_match_state(
    match_id
):

    query = """

    SELECT *

    FROM match_state

    WHERE match_id=?

    """

    return fetch_one(
        query,
        (match_id,)
    )

# ==========================================
# UPDATE MATCH STATE
# ==========================================

def update_match_state(

    match_id,

    innings,

    striker,

    non_striker,

    bowler,

    batting_team,

    bowling_team,

    current_over,

    current_ball,

    legal_balls,

    current_score,

    wickets,

    target,

    last_event,

    free_hit,

    match_completed
):

    query = """

    UPDATE match_state

    SET innings=?,
        striker=?,
        non_striker=?,
        bowler=?,
        batting_team=?,
        bowling_team=?,
        current_over=?,
        current_ball=?,
        legal_balls=?,
        current_score=?,
        wickets=?,
        target=?,
        last_event=?,
        free_hit=?,
        match_completed=?,
        updated_at=?

    WHERE match_id=?

    """

    execute_query(

        query,

        (

            innings,

            striker,

            non_striker,

            bowler,

            batting_team,

            bowling_team,

            current_over,

            current_ball,

            legal_balls,

            current_score,

            wickets,

            target,

            last_event,

            free_hit,

            match_completed,

            str(datetime.now()),

            match_id
        )
    )

# ==========================================
# DELETE MATCH
# ==========================================

def delete_match(
    match_id
):

    execute_query(

        "DELETE FROM matches WHERE match_id=?",

        (match_id,)
    )

    execute_query(

        "DELETE FROM ball_by_ball WHERE match_id=?",

        (match_id,)
    )

    execute_query(

        "DELETE FROM match_state WHERE match_id=?",

        (match_id,)
    )