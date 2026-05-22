import pandas as pd

from utils.calculations import (
    calculate_run_rate
)

# ==========================================
# CURRENT PARTNERSHIP
# ==========================================

def calculate_current_partnership(
    ball_df
):

    if ball_df.empty:

        return {

            "runs": 0,

            "balls": 0
        }

    wicket_indices = ball_df[

        ball_df["wicket"]
        == "Yes"

    ].index.tolist()

    if wicket_indices:

        start_index = (
            wicket_indices[-1] + 1
        )

        partnership_df = ball_df.loc[
            start_index:
        ]

    else:

        partnership_df = ball_df

    return {

        "runs": int(

            partnership_df[
                "total_runs"
            ].sum()
        ),

        "balls": int(
            partnership_df.shape[0]
        )
    }

# ==========================================
# LAST SIX BALLS
# ==========================================

def get_last_six_balls(
    ball_df
):

    if ball_df.empty:
        return []

    recent = ball_df.tail(6)

    outputs = []

    for _, row in recent.iterrows():

        if row["wicket"] == "Yes":

            outputs.append("W")

        elif row["extra_type"] == "wide":

            outputs.append("WD")

        elif row["extra_type"] == "no_ball":

            outputs.append("NB")

        else:

            outputs.append(
                str(row["total_runs"])
            )

    return outputs

# ==========================================
# RECENT RUN RATE
# ==========================================

def calculate_recent_run_rate(
    ball_df,
    recent_balls=12
):

    if ball_df.empty:
        return 0

    recent = ball_df.tail(
        recent_balls
    )

    runs = int(
        recent["total_runs"]
        .sum()
    )

    legal = recent[

        ~recent["extra_type"]

        .isin([
            "wide",
            "no_ball"
        ])
    ]

    legal_balls = int(
        legal.shape[0]
    )

    return calculate_run_rate(
        runs,
        legal_balls
    )

# ==========================================
# CHASE SUMMARY
# ==========================================

def generate_chase_summary(

    current_score,

    target,

    legal_balls,

    max_overs
):

    total_balls = (
        int(max_overs) * 6
    )

    balls_remaining = max(

        total_balls
        -
        legal_balls,

        0
    )

    runs_required = max(

        target
        -
        current_score,

        0
    )

    required_rr = 0

    if balls_remaining > 0:

        required_rr = round(

            runs_required

            /

            (balls_remaining / 6),

            2
        )

    return {

        "runs_required":
        runs_required,

        "balls_remaining":
        balls_remaining,

        "required_rr":
        required_rr
    }

# ==========================================
# MOMENTUM
# ==========================================

def get_momentum_status(

    current_rr,

    required_rr
):

    if required_rr <= 0:

        return "Match Won"

    difference = (
        current_rr - required_rr
    )

    if difference >= 2:

        return "Batting Dominating"

    if difference >= 0:

        return "Batting Ahead"

    if difference > -2:

        return "Bowling Pressure"

    return "Bowling Dominating"

# ==========================================
# PROJECTED SCORE
# ==========================================

def projected_score(

    current_runs,

    legal_balls,

    total_overs
):

    if legal_balls <= 0:
        return 0

    current_rr = calculate_run_rate(

        current_runs,

        legal_balls
    )

    projection = round(
        current_rr * total_overs
    )

    return projection

# ==========================================
# BOUNDARY %
# ==========================================

def boundary_percentage(
    ball_df
):

    if ball_df.empty:
        return 0

    total_runs = int(
        ball_df["total_runs"]
        .sum()
    )

    if total_runs <= 0:
        return 0

    boundary_runs = int(

        ball_df[

            ball_df["runs_off_bat"]

            .isin([4, 6])

        ]["runs_off_bat"]

        .sum()
    )

    return round(

        (boundary_runs / total_runs)
        * 100,

        2
    )

# ==========================================
# DOT BALL %
# ==========================================

def dot_ball_percentage(
    ball_df
):

    if ball_df.empty:
        return 0

    legal = ball_df[

        ~ball_df["extra_type"]

        .isin([
            "wide",
            "no_ball"
        ])
    ]

    if legal.empty:
        return 0

    dots = legal[
        legal["total_runs"] == 0
    ]

    percentage = (

        len(dots)
        /
        len(legal)

    ) * 100

    return round(
        percentage,
        2
    )

# ==========================================
# WICKET PRESSURE
# ==========================================

def wicket_pressure_index(
    wickets,
    legal_balls
):

    if legal_balls <= 0:
        return 0

    overs = legal_balls / 6

    pressure = round(
        wickets / overs,
        2
    )

    return pressure

# ==========================================
# SCORING FREQUENCY
# ==========================================

def scoring_frequency(
    ball_df
):

    if ball_df.empty:
        return {}

    frequencies = {}

    for run in [

        0, 1, 2, 3, 4, 6
    ]:

        frequencies[str(run)] = int(

            ball_df[
                ball_df["runs_off_bat"]
                == run
            ].shape[0]
        )

    return frequencies

# ==========================================
# OVER MOMENTUM
# ==========================================

def over_momentum(
    ball_df
):

    if ball_df.empty:
        return pd.DataFrame()

    grouped = (

        ball_df

        .groupby("over_num")[
            "total_runs"
        ]

        .sum()

        .reset_index()
    )

    grouped.columns = [

        "Over",

        "Runs"
    ]

    grouped["Momentum"] = grouped[
        "Runs"
    ].diff()

    return grouped

# ==========================================
# PRESSURE OVERS
# ==========================================

def pressure_overs(
    ball_df,
    threshold=4
):

    if ball_df.empty:
        return pd.DataFrame()

    grouped = (

        ball_df

        .groupby("over_num")[
            "total_runs"
        ]

        .sum()

        .reset_index()
    )

    grouped.columns = [

        "Over",

        "Runs"
    ]

    return grouped[
        grouped["Runs"]
        <= threshold
    ]