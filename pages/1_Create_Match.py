import streamlit as st
import pandas as pd

from services.match_service import (
    create_new_match,
    start_match
)

from services.player_service import (
    teams_list
)

from utils.validators import (
    validate_team_name,
    validate_overs
)

from utils.constants import (
    PAGE_CREATE_MATCH,
    DEFAULT_OVERS
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title=PAGE_CREATE_MATCH,
    layout="wide"
)

# ==========================================
# TITLE
# ==========================================

st.title("🏏 Create Match")

st.markdown(
    "Create a new cricket match and initialize live scoring."
)

# ==========================================
# LOAD TEAMS
# ==========================================

available_teams = teams_list()

# ==========================================
# FORM
# ==========================================

with st.form("create_match_form"):

    col1, col2 = st.columns(2)

    with col1:

        team1 = st.selectbox(
            "Team 1",
            options=available_teams
            if available_teams
            else []
        )

    with col2:

        team2 = st.selectbox(
            "Team 2",
            options=available_teams
            if available_teams
            else []
        )

    col3, col4 = st.columns(2)

    with col3:

        overs = st.number_input(
            "Overs",
            min_value=1,
            max_value=100,
            value=DEFAULT_OVERS
        )

    with col4:

        toss_winner = st.selectbox(
            "Toss Winner",
            options=[team1, team2]
            if team1 and team2
            else []
        )

    elected = st.radio(
        "Elected To",
        ["Bat", "Bowl"],
        horizontal=True
    )

    submit = st.form_submit_button(
        "Create Match"
    )

# ==========================================
# VALIDATION
# ==========================================

if submit:

    errors = []

    if not validate_team_name(team1):

        errors.append(
            "Invalid Team 1"
        )

    if not validate_team_name(team2):

        errors.append(
            "Invalid Team 2"
        )

    if team1 == team2:

        errors.append(
            "Teams cannot be same"
        )

    if not validate_overs(overs):

        errors.append(
            "Invalid overs"
        )

    # ======================================
    # SHOW ERRORS
    # ======================================

    if errors:

        for error in errors:

            st.error(error)

    else:

        match_id = create_new_match(
            team1=team1,
            team2=team2,
            overs=int(overs),
            toss_winner=toss_winner,
            elected=elected
        )

        start_match(match_id)

        st.success(
            f"Match Created Successfully — {match_id}"
        )

        st.info(
            "Go to Live Scoring page to start scoring."
        )

# ==========================================
# PREVIEW PANEL
# ==========================================

st.divider()

st.subheader("📋 Match Preview")

if team1 and team2:

    batting_first = None

    bowling_first = None

    if elected == "Bat":

        batting_first = toss_winner

        bowling_first = (
            team2
            if toss_winner == team1
            else team1
        )

    else:

        bowling_first = toss_winner

        batting_first = (
            team2
            if toss_winner == team1
            else team1
        )

    preview = pd.DataFrame([

        {
            "Field": "Team 1",
            "Value": team1
        },

        {
            "Field": "Team 2",
            "Value": team2
        },

        {
            "Field": "Overs",
            "Value": overs
        },

        {
            "Field": "Toss Winner",
            "Value": toss_winner
        },

        {
            "Field": "Decision",
            "Value": elected
        },

        {
            "Field": "Batting First",
            "Value": batting_first
        },

        {
            "Field": "Bowling First",
            "Value": bowling_first
        }
    ])

    st.dataframe(
        preview,
        use_container_width=True,
        hide_index=True
    )

# ==========================================
# HELP
# ==========================================

with st.expander("ℹ️ Instructions"):

    st.markdown(
        """
        ### Steps

        1. Select two teams
        2. Choose overs
        3. Select toss winner
        4. Choose bat or bowl
        5. Create match
        6. Start scoring from Live Scoring page

        ### Notes

        - Teams must already exist
        - Players should be added beforehand
        - Match automatically becomes LIVE
        """
    )
