import streamlit as st
import pandas as pd
import time

from services.match_service import (
    get_live_matches
)

from services.scoring_service import (

    live_score,

    live_overs,

    current_state
)

from database.queries import (
    fetch_ball_data
)

from utils.live_metrics import (

    current_run_rate,

    projected_score,

    get_last_six_balls
)

from utils.charts import (
    generate_worm_chart
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Live Match Center",
    layout="wide"
)

# ==========================================
# TITLE
# ==========================================

st.title("📡 Live Match Center")

# ==========================================
# LIVE MATCHES
# ==========================================

live_matches_df = get_live_matches()

if live_matches_df.empty:

    st.warning(
        "No live matches currently."
    )

    st.stop()

# ==========================================
# MATCH SELECT
# ==========================================

match_options = {

    f'{row["team1"]} vs '
    f'{row["team2"]} '
    f'({row["match_id"]})':

    row["match_id"]

    for _, row in
    live_matches_df.iterrows()
}

selected_match = st.selectbox(
    "Select Live Match",
    list(match_options.keys())
)

match_id = match_options[
    selected_match
]

# ==========================================
# STATE
# ==========================================

state = current_state(
    match_id
)

if not state:

    st.error(
        "Unable to load match."
    )

    st.stop()

# ==========================================
# SCORE HEADER
# ==========================================

st.markdown(
    f"""
    # 🏏 {state['batting_team']}

    ## {live_score(match_id)}
    ({live_overs(match_id)})

    ### vs
    {state['bowling_team']}
    """
)

# ==========================================
# LIVE METRICS
# ==========================================

balls = fetch_ball_data(
    match_id
)

ball_df = pd.DataFrame(
    balls
)

legal_balls = int(
    state["legal_balls"]
)

run_rate = current_run_rate(
    state["current_score"],
    legal_balls
)

projection = projected_score(

    current_runs=state[
        "current_score"
    ],

    legal_balls=legal_balls,

    total_overs=20
)

wickets = state["wickets"]

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Run Rate",
        run_rate
    )

with col2:

    st.metric(
        "Projected Score",
        projection
    )

with col3:

    st.metric(
        "Wickets",
        wickets
    )

# ==========================================
# CURRENT PLAYERS
# ==========================================

st.divider()

st.subheader("👥 Current Players")

col4, col5, col6 = st.columns(3)

with col4:

    st.metric(
        "Striker",
        state["striker"]
    )

with col5:

    st.metric(
        "Non-Striker",
        state["non_striker"]
    )

with col6:

    st.metric(
        "Bowler",
        state["bowler"]
    )

# ==========================================
# RECENT BALLS
# ==========================================

st.divider()

st.subheader("📌 Last Six Balls")

recent_balls = get_last_six_balls(
    ball_df
)

if recent_balls:

    st.markdown(

        " | ".join(recent_balls)
    )

else:

    st.info(
        "No deliveries yet."
    )

# ==========================================
# WORM CHART
# ==========================================

st.divider()

st.subheader("📈 Match Momentum")

if not ball_df.empty:

    worm_chart = (
        generate_worm_chart(
            ball_df
        )
    )

    st.plotly_chart(

        worm_chart,

        use_container_width=True
    )

# ==========================================
# LIVE COMMENTARY
# ==========================================

st.divider()

st.subheader("🎙️ Live Commentary")

if ball_df.empty:

    st.info(
        "Commentary not available."
    )

else:

    commentary_df = (

        ball_df.tail(15)

        .sort_values(
            by="id",
            ascending=False
        )
    )

    for _, row in commentary_df.iterrows():

        over_ball = (

            f'{row["over_num"]}.'

            f'{row["ball_num"]}'
        )

        commentary = (

            row["commentary"]

            if row["commentary"]

            else

            "Ball recorded"
        )

        st.markdown(

            f"""
            **{over_ball}**
            —
            {commentary}
            """
        )

# ==========================================
# SCORE PROGRESSION
# ==========================================

st.divider()

st.subheader("📊 Match Progress")

if not ball_df.empty:

    total_runs = int(

        ball_df[
            "total_runs"
        ].sum()
    )

    total_balls = int(
        ball_df.shape[0]
    )

    boundaries = int(

        ball_df[

            ball_df[
                "runs_off_bat"
            ]

            .isin([4, 6])

        ].shape[0]
    )

    extras = int(

        ball_df[
            "extras"
        ].sum()
    )

    col7, col8, col9, col10 = st.columns(4)

    with col7:

        st.metric(
            "Runs",
            total_runs
        )

    with col8:

        st.metric(
            "Balls",
            total_balls
        )

    with col9:

        st.metric(
            "Boundaries",
            boundaries
        )

    with col10:

        st.metric(
            "Extras",
            extras
        )

# ==========================================
# RECENT DELIVERIES TABLE
# ==========================================

st.divider()

st.subheader("📋 Ball Timeline")

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

        use_container_width=True,

        hide_index=True
    )

# ==========================================
# AUTO REFRESH
# ==========================================

refresh = st.checkbox(
    "Auto Refresh",
    value=False
)

if refresh:

    time.sleep(5)

    st.rerun()

# ==========================================
# FOOTER
# ==========================================

st.caption(
    "Live Match Center updates in real time."
)