import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# MANHATTAN CHART
# ==========================================

def generate_manhattan_chart(
    ball_df
):

    if ball_df.empty:
        return go.Figure()

    grouped = (

        ball_df

        .groupby("over_num")[
            "total_runs"
        ]

        .sum()

        .reset_index()
    )

    fig = px.bar(

        grouped,

        x="over_num",

        y="total_runs",

        title="Runs Per Over"
    )

    fig.update_layout(

        xaxis_title="Over",

        yaxis_title="Runs"
    )

    return fig

# ==========================================
# WORM CHART
# ==========================================

def generate_worm_chart(
    ball_df
):

    if ball_df.empty:
        return go.Figure()

    cumulative = []

    total = 0

    labels = []

    for _, row in ball_df.iterrows():

        total += int(
            row["total_runs"]
        )

        cumulative.append(total)

        labels.append(

            f'{row["over_num"]}.'

            f'{row["ball_num"]}'
        )

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=labels,

            y=cumulative,

            mode="lines+markers",

            name="Score"
        )
    )

    fig.update_layout(

        title="Worm Chart",

        xaxis_title="Overs",

        yaxis_title="Score"
    )

    return fig

# ==========================================
# REQUIRED RR CHART
# ==========================================

def generate_required_rr_chart(

    current_score,

    target,

    balls_remaining
):

    fig = go.Figure()

    if balls_remaining <= 0:
        return fig

    rr_data = []

    overs = []

    runs_required = (
        target - current_score
    )

    for balls in range(

        balls_remaining,

        0,

        -6
    ):

        over = balls / 6

        rr = round(
            runs_required / over,
            2
        )

        rr_data.append(rr)

        overs.append(over)

    fig.add_trace(

        go.Scatter(

            x=overs,

            y=rr_data,

            mode="lines+markers",

            name="Required RR"
        )
    )

    fig.update_layout(

        title="Required Run Rate",

        xaxis_title="Overs Remaining",

        yaxis_title="Required RR"
    )

    return fig

# ==========================================
# OVER COMPARISON
# ==========================================

def generate_over_comparison_chart(
    ball_df
):

    if ball_df.empty:
        return go.Figure()

    grouped = (

        ball_df

        .groupby("over_num")

        .agg({

            "total_runs": "sum",

            "wicket": lambda x:
            (x == "Yes").sum()
        })

        .reset_index()
    )

    fig = go.Figure()

    fig.add_trace(

        go.Bar(

            x=grouped["over_num"],

            y=grouped["total_runs"],

            name="Runs"
        )
    )

    fig.add_trace(

        go.Scatter(

            x=grouped["over_num"],

            y=grouped["wicket"],

            mode="lines+markers",

            name="Wickets"
        )
    )

    fig.update_layout(

        title="Over Comparison",

        xaxis_title="Over"
    )

    return fig

# ==========================================
# RUN DISTRIBUTION
# ==========================================

def generate_run_distribution_chart(
    ball_df
):

    if ball_df.empty:
        return go.Figure()

    counts = (

        ball_df["runs_off_bat"]

        .value_counts()

        .sort_index()
    )

    fig = px.pie(

        names=counts.index,

        values=counts.values,

        title="Run Distribution"
    )

    return fig

# ==========================================
# WICKET TIMELINE
# ==========================================

def generate_wicket_timeline(
    ball_df
):

    if ball_df.empty:
        return go.Figure()

    wickets = ball_df[
        ball_df["wicket"]
        == "Yes"
    ]

    if wickets.empty:
        return go.Figure()

    labels = [

        f'{row["over_num"]}.'
        f'{row["ball_num"]}'

        for _, row in wickets.iterrows()
    ]

    scores = []

    total = 0

    for _, row in ball_df.iterrows():

        total += int(
            row["total_runs"]
        )

        if row["wicket"] == "Yes":

            scores.append(total)

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=labels,

            y=scores,

            mode="markers+text",

            text=wickets[
                "player_out"
            ],

            textposition="top center"
        )
    )

    fig.update_layout(

        title="Wicket Timeline",

        xaxis_title="Over",

        yaxis_title="Score"
    )

    return fig

# ==========================================
# PHASE RUNS
# ==========================================

def generate_phase_runs_chart(
    ball_df
):

    if ball_df.empty:
        return go.Figure()

    powerplay = int(

        ball_df[
            ball_df["over_num"] < 6
        ]["total_runs"].sum()
    )

    middle = int(

        ball_df[

            (ball_df["over_num"] >= 6)

            &

            (ball_df["over_num"] < 15)

        ]["total_runs"].sum()
    )

    death = int(

        ball_df[
            ball_df["over_num"] >= 15
        ]["total_runs"].sum()
    )

    phases = pd.DataFrame({

        "Phase": [

            "Powerplay",

            "Middle",

            "Death"
        ],

        "Runs": [

            powerplay,

            middle,

            death
        ]
    })

    fig = px.bar(

        phases,

        x="Phase",

        y="Runs",

        title="Phase Runs"
    )

    return fig

# ==========================================
# BATTER WAGON
# ==========================================

def generate_batter_runs_chart(
    batting_df
):

    if batting_df.empty:
        return go.Figure()

    fig = px.bar(

        batting_df,

        x="Batter",

        y="R",

        title="Batting Runs"
    )

    return fig

# ==========================================
# BOWLING ANALYSIS
# ==========================================

def generate_bowling_chart(
    bowling_df
):

    if bowling_df.empty:
        return go.Figure()

    fig = px.bar(

        bowling_df,

        x="Bowler",

        y="W",

        title="Bowling Wickets"
    )

    return fig

# ==========================================
# RUN RATE PROGRESSION
# ==========================================

def generate_run_rate_chart(
    ball_df
):

    if ball_df.empty:
        return go.Figure()

    cumulative_runs = 0

    legal_balls = 0

    rr = []

    labels = []

    for _, row in ball_df.iterrows():

        cumulative_runs += int(
            row["total_runs"]
        )

        if row["extra_type"] not in [

            "wide",

            "no_ball"
        ]:

            legal_balls += 1

        if legal_balls > 0:

            current_rr = round(
                cumulative_runs
                /
                (legal_balls / 6),
                2
            )

        else:

            current_rr = 0

        rr.append(current_rr)

        labels.append(

            f'{row["over_num"]}.'

            f'{row["ball_num"]}'
        )

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=labels,

            y=rr,

            mode="lines"
        )
    )

    fig.update_layout(

        title="Run Rate Progression",

        xaxis_title="Overs",

        yaxis_title="Run Rate"
    )

    return fig