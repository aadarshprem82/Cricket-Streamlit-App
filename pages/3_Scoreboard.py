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

from utils.partnerships import (
    generate_partnerships
)

from database.queries import (
    fetch_ball_data
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Scoreboard",
    layout="wide"
)

# ==========================================
# TITLE
# ==========================================

st.title("📊 Match Scoreboard")

# ==========================================
# MATCH LIST
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

ball_df = pd.DataFrame(balls)

partnerships_df = (
    generate_partnerships(
        ball_df
    )
)

# ==========================================
# MATCH SUMMARY
# ==========================================

st.subheader("🏏 Match Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Score",
        summary.get("score", "0/0")
    )

with col2:

    st.metric(
        "Overs",
        summary.get("overs", "0.0")
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
# BATTING SCORECARD
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
# BOWLING SCORECARD
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
# PARTNERSHIPS
# ==========================================

st.divider()

st.subheader("🤝 Partnerships")

if partnerships_df.empty:

    st.info(
        "No partnerships available."
    )

else:

    st.dataframe(

        partnerships_df,

        use_container_width=True,

        hide_index=True
    )

# ==========================================
# FALL OF WICKETS
# ==========================================

st.divider()

st.subheader("❌ Fall Of Wickets")

wickets = ball_df[
    ball_df["wicket"]
    == "Yes"
]

if wickets.empty:

    st.info(
        "No wickets recorded."
    )

else:

    fow_data = []

    score = 0

    wicket_count = 0

    for _, row in ball_df.iterrows():

        score += int(
            row["total_runs"]
        )

        if row["wicket"] == "Yes":

            wicket_count += 1

            fow_data.append({

                "Wicket":
                wicket_count,

                "Score":
                score,

                "Player":
                row["player_out"],

                "Over":

                f'{row["over_num"]}.'

                f'{row["ball_num"]}'
            })

    st.dataframe(

        pd.DataFrame(fow_data),

        use_container_width=True,

        hide_index=True
    )

# ==========================================
# RECENT OVERS
# ==========================================

st.divider()

st.subheader("📌 Recent Deliveries")

if ball_df.empty:

    st.info(
        "No ball data available."
    )

else:

    recent_df = ball_df.tail(12)

    recent_df = recent_df[[

        "over_num",

        "ball_num",

        "striker",

        "bowler",

        "runs_off_bat",

        "extra_type",

        "total_runs",

        "wicket"
    ]]

    st.dataframe(

        recent_df,

        use_container_width=True,

        hide_index=True
    )

# ==========================================
# DOWNLOAD
# ==========================================

st.divider()

csv = batting_df.to_csv(
    index=False
)

st.download_button(

    label="⬇ Download Batting Scorecard",

    data=csv,

    file_name=(
        f"{match_id}_batting.csv"
    ),

    mime="text/csv"
)

# ==========================================
# SUMMARY NOTES
# ==========================================

with st.expander(
    "ℹ️ Match Insights"
):

    st.markdown(

        f"""
        ### Match Facts

        - Boundaries:
          {summary.get('fours', 0)}
          fours &
          {summary.get('sixes', 0)}
          sixes

        - Dot Balls:
          {summary.get('dot_balls', 0)}

        - Highest Over:
          {summary.get('highest_over')}

        - Current Run Rate:
          {summary.get('run_rate', 0)}
        """
    )