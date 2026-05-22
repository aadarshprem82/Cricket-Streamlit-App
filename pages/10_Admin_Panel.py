import streamlit as st
import pandas as pd

from services.tournament_service import (

    create_new_tournament,

    all_tournaments,

    tournament_summary,

    begin_tournament,

    finish_tournament,

    points_table
)

from services.player_service import (
    teams_list
)

from utils.constants import (
    TOURNAMENT_FORMATS
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Tournament Manager",
    layout="wide"
)

# ==========================================
# TITLE
# ==========================================

st.title("🏆 Tournament Manager")

# ==========================================
# CREATE TOURNAMENT
# ==========================================

st.subheader("➕ Create Tournament")

available_teams = teams_list()

with st.form("create_tournament_form"):

    tournament_name = st.text_input(
        "Tournament Name"
    )

    format_type = st.selectbox(
        "Format",
        TOURNAMENT_FORMATS
    )

    selected_teams = st.multiselect(
        "Select Teams",
        available_teams
    )

    create_btn = st.form_submit_button(
        "Create Tournament"
    )

# ==========================================
# CREATE ACTION
# ==========================================

if create_btn:

    if not tournament_name:

        st.error(
            "Tournament name required."
        )

    elif len(selected_teams) < 2:

        st.error(
            "Select at least 2 teams."
        )

    else:

        tournament_id = (
            create_new_tournament(

                tournament_name=
                tournament_name,

                format_type=
                format_type,

                teams=
                selected_teams
            )
        )

        st.success(

            f"Tournament Created "

            f"({tournament_id})"
        )

# ==========================================
# TOURNAMENT LIST
# ==========================================

st.divider()

st.subheader("📋 All Tournaments")

tournaments_df = (
    all_tournaments()
)

if tournaments_df.empty:

    st.info(
        "No tournaments available."
    )

    st.stop()

st.dataframe(

    tournaments_df,

    use_container_width=True,

    hide_index=True
)

# ==========================================
# SELECT TOURNAMENT
# ==========================================

tournament_options = {

    f'{row["tournament_name"]} '
    f'({row["tournament_id"]})':

    row["tournament_id"]

    for _, row in
    tournaments_df.iterrows()
}

selected = st.selectbox(
    "Select Tournament",
    list(tournament_options.keys())
)

tournament_id = (
    tournament_options[selected]
)

summary = tournament_summary(
    tournament_id
)

# ==========================================
# SUMMARY
# ==========================================

st.divider()

st.subheader("📊 Tournament Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Tournament",
        summary["Tournament"]
    )

with col2:

    st.metric(
        "Format",
        summary["Format"]
    )

with col3:

    st.metric(
        "Teams",
        summary["Teams"]
    )

with col4:

    st.metric(
        "Status",
        summary["Status"]
    )

# ==========================================
# TOURNAMENT CONTROLS
# ==========================================

st.divider()

st.subheader("🎮 Tournament Controls")

col5, col6 = st.columns(2)

with col5:

    if st.button(
        "▶ Start Tournament"
    ):

        begin_tournament(
            tournament_id
        )

        st.success(
            "Tournament started."
        )

        st.rerun()

with col6:

    winner_team = st.text_input(
        "Winner Team"
    )

    if st.button(
        "🏆 Finish Tournament"
    ):

        finish_tournament(

            tournament_id,

            winner_team
        )

        st.success(
            "Tournament completed."
        )

        st.rerun()

# ==========================================
# POINTS TABLE
# ==========================================

st.divider()

st.subheader("📈 Points Table")

points_df = points_table(
    tournament_id
)

if points_df.empty:

    st.info(
        "No standings available."
    )

else:

    display_df = points_df.copy()

    display_df.index = (
        display_df.index + 1
    )

    st.dataframe(

        display_df,

        use_container_width=True
    )

# ==========================================
# TOURNAMENT INSIGHTS
# ==========================================

st.divider()

st.subheader("📌 Tournament Insights")

if not points_df.empty:

    highest_points = int(

        points_df[
            "points"
        ].max()
    )

    best_nrr = round(

        points_df[
            "net_run_rate"
        ].max(),

        2
    )

    matches_played = int(

        points_df[
            "played"
        ].sum() / 2
    )

    leader = points_df.iloc[0][
        "team_name"
    ]

    col7, col8, col9, col10 = st.columns(4)

    with col7:

        st.metric(
            "Leader",
            leader
        )

    with col8:

        st.metric(
            "Highest Points",
            highest_points
        )

    with col9:

        st.metric(
            "Best NRR",
            best_nrr
        )

    with col10:

        st.metric(
            "Matches",
            matches_played
        )

# ==========================================
# DOWNLOAD
# ==========================================

st.divider()

if not points_df.empty:

    csv = points_df.to_csv(
        index=False
    )

    st.download_button(

        label="⬇ Download Points Table",

        data=csv,

        file_name=(
            f"{tournament_id}_points.csv"
        ),

        mime="text/csv"
    )

# ==========================================
# HELP
# ==========================================

with st.expander(
    "ℹ️ Tournament Manager Help"
):

    st.markdown(
        """
        ### Features

        - Create tournaments
        - Manage standings
        - Start tournaments
        - Finish tournaments
        - Download points table

        ### Formats

        - League
        - Knockout
        - Round Robin

        ### Notes

        - Teams must exist beforehand
        - Matches can be attached later
        - NRR updates dynamically
        """
    )