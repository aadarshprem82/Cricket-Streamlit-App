import streamlit as st
import pandas as pd

from services.stats_service import (

    player_batting_stats,

    player_bowling_stats,

    player_profile,

    team_stats_service,

    orange_cap_holder,

    purple_cap_holder
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Career Stats",
    layout="wide"
)

# ==========================================
# TITLE
# ==========================================

st.title("📈 Career Statistics")

# ==========================================
# PLAYER STATS
# ==========================================

batting_df = (
    player_batting_stats()
)

bowling_df = (
    player_bowling_stats()
)

team_df = (
    team_stats_service()
)

# ==========================================
# TOP PLAYERS
# ==========================================

st.subheader("🏅 Tournament Leaders")

orange_cap = orange_cap_holder()

purple_cap = purple_cap_holder()

col1, col2 = st.columns(2)

with col1:

    if orange_cap is not None:

        st.metric(
            "Orange Cap",
            orange_cap["Player"],
            orange_cap["Runs"]
        )

with col2:

    if purple_cap is not None:

        st.metric(
            "Purple Cap",
            purple_cap["Bowler"],
            purple_cap["Wickets"]
        )

# ==========================================
# PLAYER PROFILE
# ==========================================

st.divider()

st.subheader("👤 Player Profile")

if not batting_df.empty:

    player_options = sorted(

        batting_df[
            "Player"
        ].unique()
    )

    selected_player = st.selectbox(
        "Select Player",
        player_options
    )

    profile = player_profile(
        selected_player
    )

    batting_profile = (
        profile.get("batting")
    )

    bowling_profile = (
        profile.get("bowling")
    )

    # ======================================
    # BATTING PROFILE
    # ======================================

    if batting_profile:

        st.markdown(
            "### 🟢 Batting"
        )

        col3, col4, col5, col6 = st.columns(4)

        with col3:

            st.metric(
                "Runs",
                batting_profile.get(
                    "Runs",
                    0
                )
            )

        with col4:

            st.metric(
                "Balls",
                batting_profile.get(
                    "Balls",
                    0
                )
            )

        with col5:

            st.metric(
                "Average",
                batting_profile.get(
                    "Average",
                    0
                )
            )

        with col6:

            st.metric(
                "Strike Rate",
                batting_profile.get(
                    "Strike Rate",
                    0
                )
            )

    # ======================================
    # BOWLING PROFILE
    # ======================================

    if bowling_profile:

        st.markdown(
            "### 🔴 Bowling"
        )

        col7, col8, col9, col10 = st.columns(4)

        with col7:

            st.metric(
                "Wickets",
                bowling_profile.get(
                    "Wickets",
                    0
                )
            )

        with col8:

            st.metric(
                "Runs Conceded",
                bowling_profile.get(
                    "Runs",
                    0
                )
            )

        with col9:

            st.metric(
                "Economy",
                bowling_profile.get(
                    "Economy",
                    0
                )
            )

        with col10:

            st.metric(
                "Overs",
                bowling_profile.get(
                    "Overs",
                    0
                )
            )

# ==========================================
# FULL BATTING TABLE
# ==========================================

st.divider()

st.subheader("🟢 Batting Career Stats")

if batting_df.empty:

    st.info(
        "No batting data available."
    )

else:

    st.dataframe(

        batting_df,

        use_container_width=True,

        hide_index=True
    )

# ==========================================
# FULL BOWLING TABLE
# ==========================================

st.divider()

st.subheader("🔴 Bowling Career Stats")

if bowling_df.empty:

    st.info(
        "No bowling data available."
    )

else:

    st.dataframe(

        bowling_df,

        use_container_width=True,

        hide_index=True
    )

# ==========================================
# TEAM STATS
# ==========================================

st.divider()

st.subheader("🏏 Team Statistics")

if team_df.empty:

    st.info(
        "No team data available."
    )

else:

    st.dataframe(

        team_df,

        use_container_width=True,

        hide_index=True
    )

# ==========================================
# PLATFORM INSIGHTS
# ==========================================

st.divider()

st.subheader("📊 Platform Insights")

if not batting_df.empty:

    total_runs = int(

        batting_df[
            "Runs"
        ].sum()
    )

    total_players = int(
        batting_df.shape[0]
    )

    top_score = int(

        batting_df[
            "Runs"
        ].max()
    )

    best_average = round(

        batting_df[
            "Average"
        ].max(),

        2
    )

    col11, col12, col13, col14 = st.columns(4)

    with col11:

        st.metric(
            "Total Runs",
            total_runs
        )

    with col12:

        st.metric(
            "Players",
            total_players
        )

    with col13:

        st.metric(
            "Highest Runs",
            top_score
        )

    with col14:

        st.metric(
            "Best Average",
            best_average
        )

# ==========================================
# DOWNLOADS
# ==========================================

st.divider()

if not batting_df.empty:

    batting_csv = batting_df.to_csv(
        index=False
    )

    st.download_button(

        label="⬇ Download Batting Stats",

        data=batting_csv,

        file_name="batting_stats.csv",

        mime="text/csv"
    )

if not bowling_df.empty:

    bowling_csv = bowling_df.to_csv(
        index=False
    )

    st.download_button(

        label="⬇ Download Bowling Stats",

        data=bowling_csv,

        file_name="bowling_stats.csv",

        mime="text/csv"
    )

# ==========================================
# HELP
# ==========================================

with st.expander(
    "ℹ️ Career Stats Guide"
):

    st.markdown(
        """
        ### Features

        - Career batting records
        - Career bowling records
        - Team statistics
        - Orange cap leaderboard
        - Purple cap leaderboard

        ### Metrics

        Batting:
        - Runs
        - Average
        - Strike Rate

        Bowling:
        - Wickets
        - Economy
        - Overs
        """
    )