import pandas as pd

# ==========================================
# BATTING SCORECARD
# ==========================================

def generate_batting_scorecard(
    ball_df
):

    if ball_df.empty:
        return pd.DataFrame()

    batters = []

    unique_batters = pd.concat([

        ball_df["striker"],

        ball_df["non_striker"]

    ]).dropna().unique()

    for batter in unique_batters:

        batter_df = ball_df[
            ball_df["striker"]
            == batter
        ]

        runs = int(
            batter_df[
                "runs_off_bat"
            ].sum()
        )

        balls = int(

            batter_df[

                ~batter_df["extra_type"]

                .isin([
                    "wide"
                ])

            ].shape[0]
        )

        fours = int(

            batter_df[
                batter_df[
                    "runs_off_bat"
                ] == 4
            ].shape[0]
        )

        sixes = int(

            batter_df[
                batter_df[
                    "runs_off_bat"
                ] == 6
            ].shape[0]
        )

        strike_rate = 0

        if balls > 0:

            strike_rate = round(
                (runs / balls) * 100,
                2
            )

        dismissal = get_dismissal_info(

            ball_df,
            batter
        )

        batters.append({

            "Batter": batter,

            "R": runs,

            "B": balls,

            "4s": fours,

            "6s": sixes,

            "SR": strike_rate,

            "Dismissal": dismissal
        })

    scorecard = pd.DataFrame(
        batters
    )

    if scorecard.empty:
        return scorecard

    return scorecard.sort_values(

        by="R",

        ascending=False
    )

# ==========================================
# DISMISSAL INFO
# ==========================================

def get_dismissal_info(

    ball_df,

    batter
):

    wickets = ball_df[

        (ball_df["player_out"] == batter)

        &

        (ball_df["wicket"] == "Yes")
    ]

    if wickets.empty:

        return "Not Out"

    row = wickets.iloc[0]

    wicket_type = row[
        "wicket_type"
    ]

    bowler = row["bowler"]

    return (

        f"{wicket_type} "

        f"b {bowler}"
    )

# ==========================================
# TOP SCORER
# ==========================================

def top_scorer(
    scorecard_df
):

    if scorecard_df.empty:
        return None

    return scorecard_df.iloc[0]

# ==========================================
# TOTAL BATTING RUNS
# ==========================================

def total_batting_runs(
    scorecard_df
):

    if scorecard_df.empty:
        return 0

    return int(
        scorecard_df["R"]
        .sum()
    )

# ==========================================
# TOTAL BOUNDARIES
# ==========================================

def total_boundaries(
    scorecard_df
):

    if scorecard_df.empty:

        return {

            "4s": 0,

            "6s": 0
        }

    return {

        "4s": int(
            scorecard_df["4s"]
            .sum()
        ),

        "6s": int(
            scorecard_df["6s"]
            .sum()
        )
    }

# ==========================================
# TEAM STRIKE RATE
# ==========================================

def team_strike_rate(
    scorecard_df
):

    if scorecard_df.empty:
        return 0

    total_runs = int(
        scorecard_df["R"]
        .sum()
    )

    total_balls = int(
        scorecard_df["B"]
        .sum()
    )

    if total_balls <= 0:
        return 0

    return round(
        (total_runs / total_balls)
        * 100,
        2
    )

# ==========================================
# FIFTIES
# ==========================================

def total_fifties(
    scorecard_df
):

    if scorecard_df.empty:
        return 0

    return int(

        scorecard_df[
            scorecard_df["R"] >= 50
        ].shape[0]
    )

# ==========================================
# HUNDREDS
# ==========================================

def total_hundreds(
    scorecard_df
):

    if scorecard_df.empty:
        return 0

    return int(

        scorecard_df[
            scorecard_df["R"] >= 100
        ].shape[0]
    )

# ==========================================
# NOT OUT BATTERS
# ==========================================

def not_out_batters(
    scorecard_df
):

    if scorecard_df.empty:
        return []

    not_out = scorecard_df[

        scorecard_df["Dismissal"]
        == "Not Out"
    ]

    return not_out[
        "Batter"
    ].tolist()

# ==========================================
# BATTING SUMMARY
# ==========================================

def batting_summary(
    scorecard_df
):

    if scorecard_df.empty:

        return {

            "runs": 0,

            "balls": 0,

            "4s": 0,

            "6s": 0,

            "strike_rate": 0
        }

    return {

        "runs": int(
            scorecard_df["R"]
            .sum()
        ),

        "balls": int(
            scorecard_df["B"]
            .sum()
        ),

        "4s": int(
            scorecard_df["4s"]
            .sum()
        ),

        "6s": int(
            scorecard_df["6s"]
            .sum()
        ),

        "strike_rate": team_strike_rate(
            scorecard_df
        )
    }

# ==========================================
# BOUNDARY %
# ==========================================

def boundary_percentage(
    scorecard_df
):

    if scorecard_df.empty:
        return 0

    total_runs = int(
        scorecard_df["R"]
        .sum()
    )

    if total_runs <= 0:
        return 0

    boundary_runs = (

        int(
            scorecard_df["4s"]
            .sum()
        ) * 4

        +

        int(
            scorecard_df["6s"]
            .sum()
        ) * 6
    )

    return round(
        (boundary_runs / total_runs)
        * 100,
        2
    )

# ==========================================
# BEST STRIKE RATE
# ==========================================

def best_strike_rate(
    scorecard_df,
    min_balls=10
):

    if scorecard_df.empty:
        return None

    filtered = scorecard_df[
        scorecard_df["B"]
        >= min_balls
    ]

    if filtered.empty:
        return None

    return filtered.sort_values(

        by="SR",

        ascending=False
    ).iloc[0]