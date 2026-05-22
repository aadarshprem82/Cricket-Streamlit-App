import streamlit as st
import pandas as pd

from services.player_service import (

    create_new_player,

    get_all_players,

    get_players_by_team,

    remove_player,

    teams_list
)

from utils.validators import (

    validate_player_name,

    validate_role,

    validate_batting_style,

    validate_bowling_style
)

from utils.constants import (

    PLAYER_ROLES,

    BATTING_STYLES,

    BOWLING_STYLES
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Player Management",
    layout="wide"
)

# ==========================================
# TITLE
# ==========================================

st.title("👤 Player Management")

# ==========================================
# CREATE PLAYER
# ==========================================

st.subheader("➕ Add New Player")

with st.form("player_form"):

    col1, col2 = st.columns(2)

    with col1:

        player_name = st.text_input(
            "Player Name"
        )

        team = st.text_input(
            "Team Name"
        )

        role = st.selectbox(
            "Role",
            PLAYER_ROLES
        )

    with col2:

        batting_style = st.selectbox(
            "Batting Style",
            BATTING_STYLES
        )

        bowling_style = st.selectbox(
            "Bowling Style",
            BOWLING_STYLES
        )

    submit = st.form_submit_button(
        "Create Player"
    )

# ==========================================
# CREATE ACTION
# ==========================================

if submit:

    errors = []

    if not validate_player_name(
        player_name
    ):

        errors.append(
            "Invalid player name"
        )

    if not validate_role(role):

        errors.append(
            "Invalid role"
        )

    if not validate_batting_style(
        batting_style
    ):

        errors.append(
            "Invalid batting style"
        )

    if not validate_bowling_style(
        bowling_style
    ):

        errors.append(
            "Invalid bowling style"
        )

    if errors:

        for error in errors:

            st.error(error)

    else:

        player_id = create_new_player(

            player_name=player_name,

            team=team,

            role=role,

            batting_style=batting_style,

            bowling_style=bowling_style
        )

        st.success(

            f"Player created successfully "

            f"({player_id})"
        )

# ==========================================
# PLAYER LIST
# ==========================================

st.divider()

st.subheader("📋 Players")

players_df = get_all_players()

if players_df.empty:

    st.info(
        "No players available."
    )

else:

    st.dataframe(

        players_df,

        use_container_width=True,

        hide_index=True
    )

# ==========================================
# FILTER BY TEAM
# ==========================================

st.divider()

st.subheader("🏏 Team Players")

teams = teams_list()

if teams:

    selected_team = st.selectbox(
        "Select Team",
        teams
    )

    team_players_df = (
        get_players_by_team(
            selected_team
        )
    )

    if not team_players_df.empty:

        st.dataframe(

            team_players_df,

            use_container_width=True,

            hide_index=True
        )

    else:

        st.info(
            "No players in this team."
        )

# ==========================================
# REMOVE PLAYER
# ==========================================

st.divider()

st.subheader("❌ Remove Player")

if not players_df.empty:

    player_to_remove = st.selectbox(

        "Select Player",

        players_df[
            "player_name"
        ].tolist()
    )

    if st.button(
        "Deactivate Player"
    ):

        remove_player(
            player_to_remove
        )

        st.success(
            f"{player_to_remove} deactivated."
        )

        st.rerun()

# ==========================================
# ROLE DISTRIBUTION
# ==========================================

st.divider()

st.subheader("📊 Role Distribution")

if not players_df.empty:

    role_counts = (

        players_df[
            "role"
        ]

        .value_counts()

        .reset_index()
    )

    role_counts.columns = [

        "Role",

        "Count"
    ]

    st.dataframe(

        role_counts,

        use_container_width=True,

        hide_index=True
    )

# ==========================================
# PLAYER STATS
# ==========================================

st.divider()

st.subheader("📈 Player Statistics")

if not players_df.empty:

    total_players = int(
        players_df.shape[0]
    )

    total_teams = int(

        players_df[
            "team"
        ].nunique()
    )

    all_rounders = int(

        players_df[
            players_df["role"]

            ==

            "All Rounder"
        ].shape[0]
    )

    col3, col4, col5 = st.columns(3)

    with col3:

        st.metric(
            "Total Players",
            total_players
        )

    with col4:

        st.metric(
            "Teams",
            total_teams
        )

    with col5:

        st.metric(
            "All Rounders",
            all_rounders
        )

# ==========================================
# EXPORT
# ==========================================

st.divider()

if not players_df.empty:

    csv = players_df.to_csv(
        index=False
    )

    st.download_button(

        label="⬇ Download Players",

        data=csv,

        file_name="players.csv",

        mime="text/csv"
    )

# ==========================================
# HELP
# ==========================================

with st.expander(
    "ℹ️ Player Management Help"
):

    st.markdown(
        """
        ### Features

        - Add players
        - Assign roles
        - Manage teams
        - Filter players
        - Deactivate players

        ### Roles

        - Batter
        - Bowler
        - All Rounder
        - Wicket Keeper

        ### Notes

        - Deactivated players remain in history
        - Team names are case-sensitive
        """
    )