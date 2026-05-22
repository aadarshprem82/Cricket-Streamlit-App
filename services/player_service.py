import pandas as pd

from database.queries import (

    create_player,

    fetch_players,

    fetch_team_players,

    deactivate_player
)

from utils.helpers import (
    generate_player_id
)

# ==========================================
# CREATE PLAYER
# ==========================================

def create_new_player(

    player_name,

    team,

    role,

    batting_style,

    bowling_style
):

    player_id = generate_player_id()

    create_player(

        player_id=player_id,

        player_name=player_name,

        team=team,

        role=role,

        batting_style=batting_style,

        bowling_style=bowling_style
    )

    return player_id

# ==========================================
# ALL PLAYERS
# ==========================================

def get_all_players():

    players = fetch_players()

    return pd.DataFrame(players)

# ==========================================
# TEAM PLAYERS
# ==========================================

def get_players_by_team(
    team_name
):

    players = fetch_team_players(
        team_name
    )

    return pd.DataFrame(players)

# ==========================================
# PLAYER NAMES
# ==========================================

def player_names():

    players_df = get_all_players()

    if players_df.empty:
        return []

    return sorted(

        players_df[
            "player_name"
        ].tolist()
    )

# ==========================================
# TEAM PLAYER NAMES
# ==========================================

def team_player_names(
    team_name
):

    players_df = get_players_by_team(
        team_name
    )

    if players_df.empty:
        return []

    return sorted(

        players_df[
            "player_name"
        ].tolist()
    )

# ==========================================
# BOWLERS
# ==========================================

def bowlers_by_team(
    team_name
):

    players_df = get_players_by_team(
        team_name
    )

    if players_df.empty:
        return []

    bowlers = players_df[

        players_df["role"]

        .isin([
            "Bowler",
            "All Rounder"
        ])
    ]

    return sorted(

        bowlers[
            "player_name"
        ].tolist()
    )

# ==========================================
# BATTERS
# ==========================================

def batters_by_team(
    team_name
):

    players_df = get_players_by_team(
        team_name
    )

    if players_df.empty:
        return []

    return sorted(

        players_df[
            "player_name"
        ].tolist()
    )

# ==========================================
# SEARCH PLAYER
# ==========================================

def search_player(
    keyword
):

    players_df = get_all_players()

    if players_df.empty:
        return players_df

    keyword = keyword.lower()

    filtered = players_df[

        players_df["player_name"]

        .str.lower()

        .str.contains(
            keyword,
            na=False
        )
    ]

    return filtered

# ==========================================
# DEACTIVATE PLAYER
# ==========================================

def remove_player(
    player_name
):

    deactivate_player(
        player_name
    )

# ==========================================
# PLAYER EXISTS
# ==========================================

def player_exists(
    player_name
):

    players_df = get_all_players()

    if players_df.empty:
        return False

    return (

        player_name

        in

        players_df[
            "player_name"
        ].tolist()
    )

# ==========================================
# PLAYER DETAILS
# ==========================================

def player_details(
    player_name
):

    players_df = get_all_players()

    if players_df.empty:
        return None

    player = players_df[

        players_df["player_name"]
        == player_name
    ]

    if player.empty:
        return None

    return player.iloc[0].to_dict()

# ==========================================
# TEAM COUNT
# ==========================================

def team_player_count(
    team_name
):

    players_df = get_players_by_team(
        team_name
    )

    return int(
        players_df.shape[0]
    )

# ==========================================
# ROLE DISTRIBUTION
# ==========================================

def role_distribution():

    players_df = get_all_players()

    if players_df.empty:
        return {}

    distribution = (

        players_df[
            "role"
        ]

        .value_counts()

        .to_dict()
    )

    return distribution

# ==========================================
# ACTIVE PLAYERS
# ==========================================

def active_players_count():

    players_df = get_all_players()

    return int(
        players_df.shape[0]
    )

# ==========================================
# TEAMS LIST
# ==========================================

def teams_list():

    players_df = get_all_players()

    if players_df.empty:
        return []

    teams = players_df[
        "team"
    ].dropna().unique()

    return sorted(
        list(teams)
    )

# ==========================================
# PLAYER SUMMARY
# ==========================================

def player_summary(
    player_name
):

    details = player_details(
        player_name
    )

    if not details:
        return None

    return {

        "Player":
        details["player_name"],

        "Team":
        details["team"],

        "Role":
        details["role"],

        "Batting":
        details["batting_style"],

        "Bowling":
        details["bowling_style"]
    }