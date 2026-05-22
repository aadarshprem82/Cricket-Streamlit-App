import pandas as pd

# ==========================================
# BOWLING SCORECARD
# ==========================================

def generate_bowling_scorecard(
    ball_df
):

    if ball_df.empty:
        return pd.DataFrame()

    bowlers = []

    unique_bowlers = (
        ball_df["bowler"]
        .dropna()
        .unique()
    )

    for bowler in unique_bowlers:

        bowler_df = ball_df[
            ball_df["bowler"]
            == bowler
        ]

        legal_deliveries = bowler_df[

            ~bowler_df["extra_type"]

            .isin([
                "wide",
                "no_ball"
            ])
        ]

        balls = int(
            legal_deliveries.shape[0]
        )

        overs = (
            f"{balls // 6}."
            f"{balls % 6}"
        )

        runs = int(
            bowler_df["total_runs"]
            .sum()
        )

        wickets = int(

            bowler_df[
                bowler_df["wicket"]
                == "Yes"
            ].shape[0]
        )

        economy = 0

        if balls > 0:

            economy = round(
                (runs / balls) * 6,
                2
            )

        maidens = calculate_maidens(
            bowler_df
        )

        dot_balls = int(

            legal_deliveries[
                legal_deliveries[
                    "total_runs"
                ] == 0
            ].shape[0]
        )

        bowlers.append({

            "Bowler": bowler,

            "O": overs,

            "M": maidens,

            "R": runs,

            "W": wickets,

            "ECO": economy,

            "Dots": dot_balls
        })

    scorecard = pd.DataFrame(
        bowlers
    )

    if scorecard.empty:
        return scorecard

    return scorecard.sort_values(

        by=["W", "ECO"],

        ascending=[False, True]
    )

# ==========================================
# MAIDENS
# ==========================================

def calculate_maidens(
    bowler_df
):

    if bowler_df.empty:
        return 0

    maidens = 0

    grouped = bowler_df.groupby(
        "over_num"
    )

    for _, over_df in grouped:

        legal = over_df[

            ~over_df["extra_type"]

            .isin([
                "wide",
                "no_ball"
            ])
        ]

        if legal.shape[0] < 6:
            continue

        runs = int(
            over_df["total_runs"]
            .sum()
        )

        if runs == 0:
            maidens += 1

    return maidens

# ==========================================
# BEST BOWLER
# ==========================================

def best_bowler(
    scorecard_df
):

    if scorecard_df.empty:
        return None

    return scorecard_df.iloc[0]

# ==========================================
# TOTAL WICKETS
# ==========================================

def total_wickets(
    scorecard_df
):

    if scorecard_df.empty:
        return 0

    return int(
        scorecard_df["W"]
        .sum()
    )

# ==========================================
# TOTAL DOT BALLS
# ==========================================

def total_dot_balls(
    scorecard_df
):

    if scorecard_df.empty:
        return 0

    return int(
        scorecard_df["Dots"]
        .sum()
    )

# ==========================================
# BEST ECONOMY
# ==========================================

def best_economy(
    scorecard_df,
    min_overs=1
):

    if scorecard_df.empty:
        return None

    filtered = scorecard_df.copy()

    filtered["overs_float"] = (

        filtered["O"]

        .astype(str)

        .apply(convert_overs_to_float)
    )

    filtered = filtered[
        filtered["overs_float"]
        >= min_overs
    ]

    if filtered.empty:
        return None

    return filtered.sort_values(

        by="ECO",

        ascending=True
    ).iloc[0]

# ==========================================
# CONVERT OVERS
# ==========================================

def convert_overs_to_float(
    overs
):

    try:

        parts = str(overs).split(".")

        over = int(parts[0])

        balls = int(parts[1])

        return over + (balls / 6)

    except:
        return 0

# ==========================================
# BOWLING SUMMARY
# ==========================================

def bowling_summary(
    scorecard_df
):

    if scorecard_df.empty:

        return {

            "runs": 0,

            "wickets": 0,

            "maidens": 0,

            "dot_balls": 0
        }

    return {

        "runs": int(
            scorecard_df["R"]
            .sum()
        ),

        "wickets": int(
            scorecard_df["W"]
            .sum()
        ),

        "maidens": int(
            scorecard_df["M"]
            .sum()
        ),

        "dot_balls": int(
            scorecard_df["Dots"]
            .sum()
        )
    }

# ==========================================
# FIVE WICKETS
# ==========================================

def five_wicket_hauls(
    scorecard_df
):

    if scorecard_df.empty:
        return pd.DataFrame()

    return scorecard_df[
        scorecard_df["W"] >= 5
    ]

# ==========================================
# MOST ECONOMICAL SPELL
# ==========================================

def economical_spell(
    scorecard_df,
    min_overs=2
):

    if scorecard_df.empty:
        return None

    filtered = scorecard_df.copy()

    filtered["overs_float"] = (

        filtered["O"]

        .astype(str)

        .apply(convert_overs_to_float)
    )

    filtered = filtered[
        filtered["overs_float"]
        >= min_overs
    ]

    if filtered.empty:
        return None

    return filtered.sort_values(

        by="ECO",

        ascending=True
    ).iloc[0]

# ==========================================
# STRIKE RATE
# ==========================================

def bowling_strike_rate(
    runs,
    wickets
):

    if wickets <= 0:
        return 0

    return round(
        runs / wickets,
        2
    )

# ==========================================
# AVERAGE ECONOMY
# ==========================================

def average_economy(
    scorecard_df
):

    if scorecard_df.empty:
        return 0

    return round(

        scorecard_df["ECO"]
        .mean(),

        2
    )