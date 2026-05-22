import pandas as pd

from utils.calculations import (

    get_match_summary,

    calculate_extras,

    calculate_fours,

    calculate_sixes,

    calculate_dot_balls,

    highest_scoring_over,

    phase_runs,

    wicket_falls
)

from utils.partnerships import (
    generate_partnerships
)

# ==========================================
# FULL MATCH SUMMARY
# ==========================================

def generate_match_summary(
    ball_df
):

    if ball_df.empty:
        return {}

    basic = get_match_summary(
        ball_df
    )

    extras = calculate_extras(
        ball_df
    )

    fours = calculate_fours(
        ball_df
    )

    sixes = calculate_sixes(
        ball_df
    )

    dots = calculate_dot_balls(
        ball_df
    )

    highest_over = (
        highest_scoring_over(
            ball_df
        )
    )

    phases = phase_runs(
        ball_df
    )

    wickets = wicket_falls(
        ball_df
    )

    partnerships = (
        generate_partnerships(
            ball_df
        )
    )

    return {

        "score": (

            f'{basic["runs"]}/'

            f'{basic["wickets"]}'
        ),

        "overs": basic["overs"],

        "run_rate": basic["run_rate"],

        "extras": extras,

        "fours": fours,

        "sixes": sixes,

        "dot_balls": dots,

        "highest_over":
        highest_over,

        "phase_runs": phases,

        "wickets": wickets,

        "partnerships":
        partnerships
    }

# ==========================================
# MATCH HEADER
# ==========================================

def match_header(
    match_data,
    summary
):

    return {

        "title": (

            f'{match_data["team1"]} '

            f'vs '

            f'{match_data["team2"]}'
        ),

        "score": summary["score"],

        "overs": summary["overs"],

        "run_rate": summary["run_rate"]
    }

# ==========================================
# POWERPLAY SUMMARY
# ==========================================

def powerplay_summary(
    ball_df
):

    if ball_df.empty:
        return {}

    pp_df = ball_df[
        ball_df["over_num"] < 6
    ]

    summary = get_match_summary(
        pp_df
    )

    return {

        "runs": summary["runs"],

        "wickets":
        summary["wickets"],

        "overs":
        summary["overs"],

        "run_rate":
        summary["run_rate"]
    }

# ==========================================
# DEATH OVERS SUMMARY
# ==========================================

def death_overs_summary(
    ball_df
):

    if ball_df.empty:
        return {}

    death_df = ball_df[
        ball_df["over_num"] >= 15
    ]

    summary = get_match_summary(
        death_df
    )

    return {

        "runs": summary["runs"],

        "wickets":
        summary["wickets"],

        "overs":
        summary["overs"],

        "run_rate":
        summary["run_rate"]
    }

# ==========================================
# OVER BY OVER
# ==========================================

def over_by_over_summary(
    ball_df
):

    if ball_df.empty:
        return pd.DataFrame()

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

    grouped.columns = [

        "Over",

        "Runs",

        "Wickets"
    ]

    return grouped

# ==========================================
# FALL OF WICKETS
# ==========================================

def fall_of_wickets(
    ball_df
):

    wickets = wicket_falls(
        ball_df
    )

    if not wickets:
        return pd.DataFrame()

    return pd.DataFrame(
        wickets
    )

# ==========================================
# MATCH FACTS
# ==========================================

def match_facts(
    ball_df
):

    if ball_df.empty:
        return {}

    summary = generate_match_summary(
        ball_df
    )

    return {

        "Total Runs":
        summary["score"],

        "Boundaries": (

            summary["fours"]

            +

            summary["sixes"]
        ),

        "Dot Balls":
        summary["dot_balls"],

        "Extras":
        summary["extras"],

        "Run Rate":
        summary["run_rate"]
    }

# ==========================================
# FASTEST SCORING OVER
# ==========================================

def fastest_over(
    ball_df
):

    highest = highest_scoring_over(
        ball_df
    )

    if not highest:
        return None

    return (

        f'Over {highest["over"]} '

        f'({highest["runs"]} runs)'
    )

# ==========================================
# MATCH TIMELINE
# ==========================================

def match_timeline(
    ball_df
):

    if ball_df.empty:
        return []

    timeline = []

    cumulative = 0

    wickets = 0

    for _, row in ball_df.iterrows():

        cumulative += int(
            row["total_runs"]
        )

        if row["wicket"] == "Yes":

            wickets += 1

        timeline.append({

            "over": (

                f'{row["over_num"]}.'

                f'{row["ball_num"]}'
            ),

            "score": (
                f"{cumulative}/"
                f"{wickets}"
            ),

            "event":
            row["commentary"]
        })

    return timeline

# ==========================================
# TEAM BOUNDARY %
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