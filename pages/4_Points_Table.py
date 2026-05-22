import streamlit as st
import pandas as pd

from services.tournament_service import (

    all_tournaments,

    points_table,

    tournament_summary,

    qualifiers
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Points Table",
    layout="wide"
)

# ==========================================
# TITLE
# ==========================================

st.title("🏆 Tournament Points Table")

# ==========================================
# LOAD TOURNAMENTS
# ==========================================

tournaments_df = all_tournaments()

if tournaments_df.empty:

    st.warning(
        "No tournaments available."
    )

    st.stop()

# ==========================================
# TOURNAMENT SELECT
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

# ==========================================
# DATA
# ==========================================

summary = tournament_summary(
    tournament_id
)

points_df = points_table(
    tournament_id
)

qualified_df = qualifiers(
    tournament_id
)

# ==========================================
# TOURNAMENT SUMMARY
# ==========================================

st.subheader("📋 Tournament Summary")

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
        "Matches",
        summary["Matches"]
    )

# ==========================================
# POINTS TABLE
# ==========================================

st.divider()

st.subheader("📊 Standings")

if points_df.empty:

    st.info(
        "Points table empty."
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
# QUALIFIED TEAMS
# ==========================================

st.divider()

st.subheader("✅ Qualified Teams")

if qualified_df.empty:

    st.info(
        "No qualified teams yet."
    )

else:

    qualified_display = (
        qualified_df[
            [
                "team_name",
                "played",
                "won",
                "points",
                "net_run_rate"
            ]
        ]
    )

    qualified_display.columns = [

        "Team",

        "Played",

        "Won",

        "Points",

        "NRR"
    ]

    st.dataframe(

        qualified_display,

        use_container_width=True,

        hide_index=True
    )

# ==========================================
# LEADERBOARD
# ==========================================

st.divider()

st.subheader("🥇 Leaderboard")

if not points_df.empty:

    leader = points_df.iloc[0]

    col5, col6, col7 = st.columns(3)

    with col5:

        st.metric(
            "Leader",
            leader["team_name"]
        )

    with col6:

        st.metric(
            "Points",
            leader["points"]
        )

    with col7:

        st.metric(
            "NRR",
            leader["net_run_rate"]
        )

# ==========================================
# STATS
# ==========================================

st.divider()

st.subheader("📈 Tournament Stats")

if not points_df.empty:

    total_points = int(
        points_df["points"]
        .sum()
    )

    total_matches = int(
        points_df["played"]
        .sum() / 2
    )

    best_nrr = round(

        points_df[
            "net_run_rate"
        ].max(),

        2
    )

    col8, col9, col10 = st.columns(3)

    with col8:

        st.metric(
            "Matches Played",
            total_matches
        )

    with col9:

        st.metric(
            "Total Points",
            total_points
        )

    with col10:

        st.metric(
            "Best NRR",
            best_nrr
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
            f"{tournament_id}_points_table.csv"
        ),

        mime="text/csv"
    )

# ==========================================
# NOTES
# ==========================================

with st.expander(
    "ℹ️ Points System"
):

    st.markdown(
        """
        ### Tournament Rules

        - Win → 2 Points
        - Tie → 1 Point
        - Loss → 0 Points

        ### Ranking Priority

        1. Points
        2. Net Run Rate
        3. Wins

        ### Qualification

        Top teams qualify based on:
        - Points
        - NRR
        """
    )