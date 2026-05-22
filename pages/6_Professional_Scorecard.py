import streamlit as st
import pandas as pd

from services.match_service import (
    get_all_matches
)

from services.stats_service import (

    batting_scorecard_service,

    bowling_scorecard_service,

    get_match_summary_service
)

from utils.charts import (

    generate_manhattan_chart,

    generate_worm_chart,

    generate_run_rate_chart
)

from database.queries import (
    fetch_ball_data
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Professional Scorecard",
    layout="wide"
)

# ==========================================
# TITLE
# ==========================================

st.title("📑 Professional Scorecard")

# ==========================================
# MATCHES
# ==========================================

matches_df = get_all_matches()

if matches_df.empty:

    st.warning(
        "No matches available."
    )

    st.stop()

match_options = {

    f'{row["team1"]} vs '
    f'{row["team2"]} '
    f'({row["match_id"]})':

    row["match_id"]

    for _, row in
    matches_df.iterrows()
}

selected_match = st.selectbox(
    "Select Match",
    list(match_options.keys())
)

match_id = match_options[
    selected_match
]

# ==========================================
# DATA
# ==========================================

summary = (
    get_match_summary_service(
        match_id
    )
)

batting_df = (
    batting_scorecard_service(
        match_id
    )
)

bowling_df = (
    bowling_scorecard_service(
        match_id
    )
)

balls = fetch_ball_data(
    match_id
)

ball_df = pd.DataFrame(
    balls
)

# ==========================================
# HEADER
# ==========================================

st.markdown(
    f"""
    ## 🏏 {summary.get('match_title', '')}

    ### Result:
    {summary.get('result', 'Match in progress')}
    """
)

# ==========================================
# MATCH METRICS
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Score",
        summary.get(
            "score",
            "0/0"
        )
    )

with col2:

    st.metric(
        "Overs",
        summary.get(
            "overs",
            "0.0"
        )
    )

with col3:

    st.metric(
        "Run Rate",
        summary.get(
            "run_rate",
            0
        )
    )

with col4:

    st.metric(
        "Extras",
        summary.get(
            "extras",
            0
        )
    )

# ==========================================
# BATTING
# ==========================================

st.divider()

st.subheader("🟢 Batting Scorecard")

if batting_df.empty:

    st.info(
        "No batting data."
    )

else:

    st.dataframe(

        batting_df,

        use_container_width=True,

        hide_index=True
    )

# ==========================================
# BOWLING
# ==========================================

st.divider()

st.subheader("🔴 Bowling Scorecard")

if bowling_df.empty:

    st.info(
        "No bowling data."
    )

else:

    st.dataframe(

        bowling_df,

        use_container_width=True,

        hide_index=True
    )

# ==========================================
# CHARTS
# ==========================================

st.divider()

st.subheader("📈 Match Analytics")

if not ball_df.empty:

    col5, col6 = st.columns(2)

    with col5:

        manhattan = (
            generate_manhattan_chart(
                ball_df
            )
        )

        st.plotly_chart(

            manhattan,

            use_container_width=True
        )

    with col6:

        worm = generate_worm_chart(
            ball_df
        )

        st.plotly_chart(

            worm,

            use_container_width=True
        )

    run_rate_chart = (
        generate_run_rate_chart(
            ball_df
        )
    )

    st.plotly_chart(

        run_rate_chart,

        use_container_width=True
    )

# ==========================================
# INNINGS BREAKDOWN
# ==========================================

st.divider()

st.subheader("📋 Innings Breakdown")

if not ball_df.empty:

    innings_summary = []

    innings_list = sorted(

        ball_df[
            "innings"
        ].unique()
    )

    for innings in innings_list:

        innings_df = ball_df[
            ball_df["innings"]
            == innings
        ]

        total_runs = int(

            innings_df[
                "total_runs"
            ].sum()
        )

        wickets = int(

            innings_df[

                innings_df[
                    "wicket"
                ] == "Yes"

            ].shape[0]
        )

        overs = innings_df[
            "over_num"
        ].max()

        innings_summary.append({

            "Innings":
            innings,

            "Runs":
            total_runs,

            "Wickets":
            wickets,

            "Overs":
            overs
        })

    st.dataframe(

        pd.DataFrame(
            innings_summary
        ),

        use_container_width=True,

        hide_index=True
    )

# ==========================================
# BOUNDARY STATS
# ==========================================

st.divider()

st.subheader("💥 Boundary Analysis")

if not ball_df.empty:

    fours = int(

        ball_df[

            ball_df[
                "runs_off_bat"
            ] == 4

        ].shape[0]
    )

    sixes = int(

        ball_df[

            ball_df[
                "runs_off_bat"
            ] == 6

        ].shape[0]
    )

    dots = int(

        ball_df[

            ball_df[
                "total_runs"
            ] == 0

        ].shape[0]
    )

    col7, col8, col9 = st.columns(3)

    with col7:

        st.metric(
            "Fours",
            fours
        )

    with col8:

        st.metric(
            "Sixes",
            sixes
        )

    with col9:

        st.metric(
            "Dot Balls",
            dots
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

        label="⬇ Download Batting Scorecard",

        data=batting_csv,

        file_name=(
            f"{match_id}_batting.csv"
        ),

        mime="text/csv"
    )

if not bowling_df.empty:

    bowling_csv = bowling_df.to_csv(
        index=False
    )

    st.download_button(

        label="⬇ Download Bowling Scorecard",

        data=bowling_csv,

        file_name=(
            f"{match_id}_bowling.csv"
        ),

        mime="text/csv"
    )

# ==========================================
# NOTES
# ==========================================

with st.expander(
    "ℹ️ Professional Scorecard"
):

    st.markdown(
        """
        This page provides:

        - Full batting scorecard
        - Full bowling scorecard
        - Match analytics
        - Boundary statistics
        - Run progression charts
        - Downloadable reports
        """
    )