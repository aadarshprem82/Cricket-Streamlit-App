import pandas as pd

from database.queries import (

    create_player,

    fetch_players,

    fetch_team_players,

    deactivate_player
)

# ==========================================
# ADD PLAYER
# ==========================================

def add_player(

    player_id,

    player_name,

    team,

    role,

    batting_style,

    bowling_style
):

    create_player(

        player_id=player_id,

        player_name=player_name,

        team=team,

        role=role,

        batting_style=batting_style,

        bowling_style=bowling_style
    )

# ==========================================
# GET ALL PLAYERS
# ==========================================

def get_players():

    players = fetch_players()

    return pd.DataFrame(players)

# ==========================================
# GET TEAM PLAYERS
# ==========================================

def get_team_players(
    team_name
):

    players = fetch_team_players(
        team_name
    )

    if not players:
        return []

    return [

        player["player_name"]

        for player in players
    ]

# ==========================================
# GET BOWLERS
# ==========================================

def get_bowlers(
    team_name
):

    players = fetch_team_players(
        team_name
    )

    if not players:
        return []

    bowlers = []

    for player in players:

        role = str(
            player["role"]
        ).lower()

        bowling_style = str(
            player["bowling_style"]
        ).lower()

        if (

            "bowler" in role

            or

            "all rounder" in role

            or

            bowling_style != "none"

        ):

            bowlers.append(
                player["player_name"]
            )

    return bowlers

# ==========================================
# SEARCH PLAYERS
# ==========================================

def search_players(
    keyword
):

    players_df = get_players()

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
# DEACTIVATE
# ==========================================

def deactivate_player_record(
    player_name
):

    deactivate_player(
        player_name
    )

# ==========================================
# ROLE SUMMARY
# ==========================================

def get_team_role_summary(
    team_name
):

    players = fetch_team_players(
        team_name
    )

    summary = {

        "Batters": 0,

        "Bowlers": 0,

        "All Rounders": 0,

        "Wicket Keepers": 0
    }

    for player in players:

        role = str(
            player["role"]
        ).lower()

        if "batter" in role:

            summary["Batters"] += 1

        elif "bowler" in role:

            summary["Bowlers"] += 1

        elif "all rounder" in role:

            summary[
                "All Rounders"
            ] += 1

        elif "wicket keeper" in role:

            summary[
                "Wicket Keepers"
            ] += 1

    return summary

# ==========================================
# PLAYER EXISTS
# ==========================================

def player_exists(
    player_name
):

    players_df = get_players()

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
# TEAM EXISTS
# ==========================================

def team_has_players(
    team_name
):

    players = fetch_team_players(
        team_name
    )

    return len(players) > 0

# ==========================================
# ACTIVE PLAYER COUNT
# ==========================================

def active_player_count():

    players_df = get_players()

    if players_df.empty:
        return 0

    return int(
        players_df.shape[0]
    )

# ==========================================
# TEAM PLAYER COUNT
# ==========================================

def team_player_count(
    team_name
):

    players = fetch_team_players(
        team_name
    )

    return len(players)

# ==========================================
# BATTERS
# ==========================================

def get_batters(
    team_name
):

    players = fetch_team_players(
        team_name
    )

    batters = []

    for player in players:

        role = str(
            player["role"]
        ).lower()

        if (

            "batter" in role

            or

            "all rounder" in role

            or

            "wicket keeper" in role

        ):

            batters.append(
                player["player_name"]
            )

    return batters

# ==========================================
# WICKET KEEPERS
# ==========================================

def get_wicket_keepers(
    team_name
):

    players = fetch_team_players(
        team_name
    )

    keepers = []

    for player in players:

        role = str(
            player["role"]
        ).lower()

        if "wicket keeper" in role:

            keepers.append(
                player["player_name"]
            )

    return keepers

# ==========================================
# PLAYER DATAFRAME
# ==========================================

def team_players_dataframe(
    team_name
):

    players = fetch_team_players(
        team_name
    )

    return pd.DataFrame(players)

# ==========================================
# PLAYER ROLES
# ==========================================

def player_role(
    player_name
):

    players_df = get_players()

    if players_df.empty:
        return None

    player = players_df[

        players_df["player_name"]
        == player_name
    ]

    if player.empty:
        return None

    return player.iloc[0]["role"]