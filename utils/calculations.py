import pandas as pd

# ==========================================
# TOTAL RUNS
# ==========================================

def calculate_total_runs(
    ball_df
):

    if ball_df.empty:
        return 0

    return int(
        ball_df["total_runs"]
        .sum()
    )

# ==========================================
# TOTAL WICKETS
# ==========================================

def calculate_total_wickets(
    ball_df
):

    if ball_df.empty:
        return 0

    wickets = ball_df[
        ball_df["wicket"]
        == "Yes"
    ]

    return int(
        wickets.shape[0]
    )

# ==========================================
# LEGAL BALLS
# ==========================================

def calculate_legal_balls(
    ball_df
):

    if ball_df.empty:
        return 0

    legal_df = ball_df[

        ~ball_df["extra_type"]

        .isin([
            "wide",
            "no_ball"
        ])
    ]

    return int(
        legal_df.shape[0]
    )

# ==========================================
# OVERS
# ==========================================

def calculate_overs(
    legal_balls
):

    overs = legal_balls // 6

    balls = legal_balls % 6

    return f"{overs}.{balls}"

# ==========================================
# RUN RATE
# ==========================================

def calculate_run_rate(
    total_runs,
    legal_balls
):

    if legal_balls <= 0:
        return 0

    overs = legal_balls / 6

    if overs <= 0:
        return 0

    return round(
        total_runs / overs,
        2
    )

# ==========================================
# MATCH SUMMARY
# ==========================================

def get_match_summary(
    ball_df
):

    if ball_df.empty:

        return {

            "runs": 0,

            "wickets": 0,

            "overs": "0.0",

            "legal_balls": 0,

            "run_rate": 0
        }

    total_runs = (
        calculate_total_runs(
            ball_df
        )
    )

    wickets = (
        calculate_total_wickets(
            ball_df
        )
    )

    legal_balls = (
        calculate_legal_balls(
            ball_df
        )
    )

    overs = calculate_overs(
        legal_balls
    )

    run_rate = calculate_run_rate(

        total_runs,

        legal_balls
    )

    return {

        "runs": total_runs,

        "wickets": wickets,

        "overs": overs,

        "legal_balls": legal_balls,

        "run_rate": run_rate
    }

# ==========================================
# EXTRA RUNS
# ==========================================

def calculate_extras(
    ball_df
):

    if ball_df.empty:
        return 0

    return int(
        ball_df["extras"]
        .sum()
    )

# ==========================================
# BOUNDARIES
# ==========================================

def calculate_fours(
    ball_df
):

    if ball_df.empty:
        return 0

    return int(

        ball_df[
            ball_df["runs_off_bat"]
            == 4
        ].shape[0]
    )

def calculate_sixes(
    ball_df
):

    if ball_df.empty:
        return 0

    return int(

        ball_df[
            ball_df["runs_off_bat"]
            == 6
        ].shape[0]
    )

# ==========================================
# DOT BALLS
# ==========================================

def calculate_dot_balls(
    ball_df
):

    if ball_df.empty:
        return 0

    return int(

        ball_df[
            ball_df["total_runs"]
            == 0
        ].shape[0]
    )

# ==========================================
# HIGHEST OVER
# ==========================================

def highest_scoring_over(
    ball_df
):

    if ball_df.empty:
        return None

    grouped = (

        ball_df

        .groupby("over_num")[
            "total_runs"
        ]

        .sum()
    )

    if grouped.empty:
        return None

    over = grouped.idxmax()

    runs = grouped.max()

    return {

        "over": int(over),

        "runs": int(runs)
    }

# ==========================================
# PHASE RUNS
# ==========================================

def phase_runs(
    ball_df
):

    if ball_df.empty:

        return {

            "powerplay": 0,

            "middle": 0,

            "death": 0
        }

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

    return {

        "powerplay": powerplay,

        "middle": middle,

        "death": death
    }

# ==========================================
# REQUIRED RUN RATE
# ==========================================

def calculate_required_rr(

    current_score,

    target,

    balls_remaining
):

    if balls_remaining <= 0:
        return 0

    runs_required = (
        target - current_score
    )

    if runs_required <= 0:
        return 0

    overs_remaining = (
        balls_remaining / 6
    )

    return round(
        runs_required / overs_remaining,
        2
    )

# ==========================================
# BALLS REMAINING
# ==========================================

def calculate_balls_remaining(

    total_overs,

    legal_balls
):

    total_balls = (
        int(total_overs) * 6
    )

    remaining = (
        total_balls - legal_balls
    )

    return max(remaining, 0)

# ==========================================
# CURRENT PARTNERSHIP
# ==========================================

def current_partnership(
    ball_df
):

    if ball_df.empty:

        return {

            "runs": 0,

            "balls": 0
        }

    wicket_df = ball_df[
        ball_df["wicket"]
        == "Yes"
    ]

    if wicket_df.empty:

        return {

            "runs": int(
                ball_df["total_runs"]
                .sum()
            ),

            "balls": int(
                ball_df.shape[0]
            )
        }

    last_wicket = (
        wicket_df.index[-1]
    )

    partnership_df = ball_df.loc[
        last_wicket + 1:
    ]

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
# LAST OVER RUNS
# ==========================================

def last_over_runs(
    ball_df
):

    if ball_df.empty:
        return 0

    recent = ball_df.tail(6)

    return int(
        recent["total_runs"]
        .sum()
    )

# ==========================================
# WICKET FALLS
# ==========================================

def wicket_falls(
    ball_df
):

    if ball_df.empty:
        return []

    wickets = ball_df[
        ball_df["wicket"]
        == "Yes"
    ]

    outputs = []

    score = 0

    wickets_count = 0

    for _, row in ball_df.iterrows():

        score += int(
            row["total_runs"]
        )

        if row["wicket"] == "Yes":

            wickets_count += 1

            outputs.append({

                "score": score,

                "wicket": wickets_count,

                "player": row["player_out"],

                "over": (

                    f'{row["over_num"]}.'

                    f'{row["ball_num"]}'
                )
            })

    return outputs