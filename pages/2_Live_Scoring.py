import streamlit as st
import pandas as pd

from services.match_service import (
    get_live_matches
)

from services.scoring_service import (

    add_runs,

    add_dot_ball,

    add_wide,

    add_no_ball,

    add_byes,

    add_leg_byes,

    add_wicket,

    live_score,

    live_overs,

    current_batters,

    current_bowler,

    current_state,

    innings_transition_check
)

from services.player_service import (
    team_player_names
)

from utils.live_metrics import (
    get_last_six_balls,
    projected_score
)

from database.queries import (
    fetch_ball_data
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Live Scoring",
    layout="wide"
)

# ==========================================
# TITLE
# ==========================================

st.title("🏏 Live Scoring")

# ==========================================
# MATCHES
# ==========================================

live_matches_df = get_live_matches()

if live_matches_df.empty:

    st.warning(
        "No live matches available."
    )

    st.stop()

match_options = {

    f'{row["team1"]} vs '
    f'{row["team2"]} '
    f'({row["match_id"]})':

    row["match_id"]

    for _, row in
    live_matches_df.iterrows()
}

selected_label = st.selectbox(
    "Select Match",
    list(match_options.keys())
)

match_id = match_options[
    selected_label
]

state = current_state(
    match_id
)

if not state:

    st.error(
        "Match state not found."
    )

    st.stop()

# ==========================================
# HEADER
# ==========================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Score",
        live_score(match_id)
    )

with col2:

    st.metric(
        "Overs",
        live_overs(match_id)
    )

with col3:

    legal_balls = int(
        state["legal_balls"]
    )

    projection = projected_score(

        current_runs=state[
            "current_score"
        ],

        legal_balls=legal_balls,

        total_overs=20
    )

    st.metric(
        "Projected",
        projection
    )

# ==========================================
# CURRENT PLAYERS
# ==========================================

batters = current_batters(
    match_id
)

bowler = current_bowler(
    match_id
)

st.markdown(
    f"""
    ### 🏏 Striker:
    {batters["striker"]}

    ### 🏃 Non-Striker:
    {batters["non_striker"]}

    ### 🎯 Bowler:
    {bowler}
    """
)

# ==========================================
# SCORING BUTTONS
# ==========================================

st.subheader("Scoring Controls")

col1, col2, col3, col4 = st.columns(4)

with col1:

    if st.button("0"):
        add_dot_ball(match_id)
        st.rerun()

    if st.button("1"):
        add_runs(match_id, 1)
        st.rerun()

with col2:

    if st.button("2"):
        add_runs(match_id, 2)
        st.rerun()

    if st.button("3"):
        add_runs(match_id, 3)
        st.rerun()

with col3:

    if st.button("4"):
        add_runs(match_id, 4)
        st.rerun()

    if st.button("6"):
        add_runs(match_id, 6)
        st.rerun()

with col4:

    if st.button("Wide"):
        add_wide(match_id)
        st.rerun()

    if st.button("No Ball"):
        add_no_ball(match_id)
        st.rerun()

# ==========================================
# EXTRAS
# ==========================================

st.subheader("Extras")

col5, col6 = st.columns(2)

with col5:

    byes = st.number_input(
        "Byes",
        min_value=0,
        max_value=6,
        value=0,
        key="byes"
    )

    if st.button("Add Byes"):

        add_byes(
            match_id,
            byes
        )

        st.rerun()

with col6:

    leg_byes = st.number_input(
        "Leg Byes",
        min_value=0,
        max_value=6,
        value=0,
        key="legbyes"
    )

    if st.button("Add Leg Byes"):

        add_leg_byes(
            match_id,
            leg_byes
        )

        st.rerun()

# ==========================================
# WICKET
# ==========================================

st.subheader("Wicket")

team_players = team_player_names(
    state["batting_team"]
)

available_new_batters = [

    player

    for player in team_players

    if player not in [

        state["striker"],
        state["non_striker"]
    ]
]

col7, col8 = st.columns(2)

with col7:

    wicket_type = st.selectbox(

        "Wicket Type",

        [

            "Bowled",

            "Caught",

            "LBW",

            "Run Out",

            "Stumped"
        ]
    )

with col8:

    new_batter = st.selectbox(

        "New Batter",

        available_new_batters
    )

if st.button("Add Wicket"):

    add_wicket(

        match_id,

        wicket_type,

        new_batter
    )

    innings_transition_check(
        match_id
    )

    st.rerun()

# ==========================================
# LAST SIX BALLS
# ==========================================

st.subheader("Last Six Balls")

balls = fetch_ball_data(
    match_id
)

ball_df = pd.DataFrame(balls)

recent = get_last_six_balls(
    ball_df
)

st.write(" | ".join(recent))

# ==========================================
# RECENT BALLS TABLE
# ==========================================

st.subheader("Ball By Ball")

if not ball_df.empty:

    display_columns = [

        "over_num",

        "ball_num",

        "striker",

        "bowler",

        "runs_off_bat",

        "extra_type",

        "total_runs",

        "wicket"
    ]

    st.dataframe(

        ball_df[
            display_columns
        ].tail(20),

        use_container_width=True
    )

# ==========================================
# AUTO REFRESH
# ==========================================

st.caption(
    "Live scoring updates instantly."
)