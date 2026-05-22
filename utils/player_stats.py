import pandas as pd

# ==========================================
# BATTING CAREER STATS
# ==========================================

def batting_career_stats(
    ball_df
):

    if ball_df.empty:
        return pd.DataFrame()

    stats = []

    players = pd.concat([

        ball_df["striker"],

        ball_df["non_striker"]

    ]).dropna().unique()

    for player in players:

        batter_df = ball_df[
            ball_df["striker"]
            == player
        ]

        runs = int(
            batter_df[
                "runs_off_bat"
            ].sum()
        )

        balls = int(

            batter_df[

                ~batter_df["extra_type"]

                .isin(["wide"])

            ].shape[0]
        )

        outs = int(

            ball_df[
                ball_df["player_out"]
                == player
            ].shape[0]
        )

        innings = int(
            batter_df.shape[0] > 0
        )

        average = 0

        if outs > 0:

            average = round(
                runs / outs,
                2
            )

        strike_rate = 0

        if balls > 0:

            strike_rate = round(
                (runs / balls) * 100,
                2
            )

        highest = highest_score(
            ball_df,
            player
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

        stats.append({

            "Player": player,

            "Matches": innings,

            "Runs": runs,

            "Balls": balls,

            "Highest": highest,

            "Average": average,

            "Strike Rate":
            strike_rate,

            "4s": fours,

            "6s": sixes
        })

    df = pd.DataFrame(stats)

    if df.empty:
        return df

    return df.sort_values(

        by="Runs",

        ascending=False
    )

# ==========================================
# HIGHEST SCORE
# ==========================================

def highest_score(
    ball_df,
    player
):

    batter_df = ball_df[
        ball_df["striker"]
        == player
    ]

    if batter_df.empty:
        return 0

    grouped = (

        batter_df

        .groupby("match_id")[
            "runs_off_bat"
        ]

        .sum()
    )

    if grouped.empty:
        return 0

    return int(
        grouped.max()
    )

# ==========================================
# BOWLING CAREER STATS
# ==========================================

def bowling_career_stats(
    ball_df
):

    if ball_df.empty:
        return pd.DataFrame()

    stats = []

    bowlers = (

        ball_df["bowler"]

        .dropna()

        .unique()
    )

    for bowler in bowlers:

        bowler_df = ball_df[
            ball_df["bowler"]
            == bowler
        ]

        legal = bowler_df[

            ~bowler_df["extra_type"]

            .isin([
                "wide",
                "no_ball"
            ])
        ]

        balls = int(
            legal.shape[0]
        )

        overs = round(
            balls / 6,
            1
        )

        runs = int(
            bowler_df[
                "total_runs"
            ].sum()
        )

        wickets = int(

            bowler_df[
                bowler_df["wicket"]
                == "Yes"
            ].shape[0]
        )

        economy = 0

        if overs > 0:

            economy = round(
                runs / overs,
                2
            )

        best = best_bowling(
            ball_df,
            bowler
        )

        stats.append({

            "Bowler": bowler,

            "Overs": overs,

            "Runs": runs,

            "Wickets": wickets,

            "Economy": economy,

            "Best": best
        })

    df = pd.DataFrame(stats)

    if df.empty:
        return df

    return df.sort_values(

        by="Wickets",

        ascending=False
    )

# ==========================================
# BEST BOWLING
# ==========================================

def best_bowling(
    ball_df,
    bowler
):

    bowler_df = ball_df[
        ball_df["bowler"]
        == bowler
    ]

    if bowler_df.empty:
        return "0/0"

    grouped = (

        bowler_df

        .groupby("match_id")

        .agg({

            "wicket": lambda x:
            (x == "Yes").sum(),

            "total_runs": "sum"
        })
    )

    grouped.columns = [

        "wickets",

        "runs"
    ]

    grouped = grouped.sort_values(

        by=["wickets", "runs"],

        ascending=[False, True]
    )

    best = grouped.iloc[0]

    return (

        f'{int(best["wickets"])}/'

        f'{int(best["runs"])}'
    )

# ==========================================
# ORANGE CAP
# ==========================================

def orange_cap(
    batting_df
):

    if batting_df.empty:
        return None

    return batting_df.iloc[0]

# ==========================================
# PURPLE CAP
# ==========================================

def purple_cap(
    bowling_df
):

    if bowling_df.empty:
        return None

    return bowling_df.iloc[0]

# ==========================================
# BEST STRIKE RATE
# ==========================================

def best_strike_rate(
    batting_df,
    min_runs=20
):

    if batting_df.empty:
        return None

    filtered = batting_df[
        batting_df["Runs"]
        >= min_runs
    ]

    if filtered.empty:
        return None

    return filtered.sort_values(

        by="Strike Rate",

        ascending=False
    ).iloc[0]

# ==========================================
# BEST ECONOMY
# ==========================================

def best_economy(
    bowling_df,
    min_overs=2
):

    if bowling_df.empty:
        return None

    filtered = bowling_df[
        bowling_df["Overs"]
        >= min_overs
    ]

    if filtered.empty:
        return None

    return filtered.sort_values(

        by="Economy",

        ascending=True
    ).iloc[0]

# ==========================================
# MOST SIXES
# ==========================================

def most_sixes(
    batting_df
):

    if batting_df.empty:
        return None

    return batting_df.sort_values(

        by="6s",

        ascending=False
    ).iloc[0]

# ==========================================
# MOST FOURS
# ==========================================

def most_fours(
    batting_df
):

    if batting_df.empty:
        return None

    return batting_df.sort_values(

        by="4s",

        ascending=False
    ).iloc[0]

# ==========================================
# PLAYER SUMMARY
# ==========================================

def player_summary(
    player_name,
    batting_df,
    bowling_df
):

    batting = batting_df[
        batting_df["Player"]
        == player_name
    ]

    bowling = bowling_df[
        bowling_df["Bowler"]
        == player_name
    ]

    return {

        "batting":

        batting.iloc[0].to_dict()

        if not batting.empty

        else None,

        "bowling":

        bowling.iloc[0].to_dict()

        if not bowling.empty

        else None
    }