import pandas as pd

# ==========================================
# PARTNERSHIPS
# ==========================================

def generate_partnerships(
    ball_df
):

    if ball_df.empty:
        return pd.DataFrame()

    partnerships = []

    current_runs = 0

    current_balls = 0

    striker = None

    non_striker = None

    wicket_no = 0

    for _, row in ball_df.iterrows():

        if striker is None:

            striker = row["striker"]

            non_striker = (
                row["non_striker"]
            )

        current_runs += int(
            row["total_runs"]
        )

        current_balls += 1

        if row["wicket"] == "Yes":

            wicket_no += 1

            partnerships.append({

                "Wicket": wicket_no,

                "Batters": (
                    f"{striker} & "
                    f"{non_striker}"
                ),

                "Runs": current_runs,

                "Balls": current_balls,

                "Run Rate": partnership_rr(
                    current_runs,
                    current_balls
                )
            })

            current_runs = 0

            current_balls = 0

            striker = row["striker"]

            non_striker = (
                row["non_striker"]
            )

    # ======================================
    # CURRENT PARTNERSHIP
    # ======================================

    if current_runs > 0:

        partnerships.append({

            "Wicket": wicket_no + 1,

            "Batters": (
                f"{striker} & "
                f"{non_striker}"
            ),

            "Runs": current_runs,

            "Balls": current_balls,

            "Run Rate": partnership_rr(
                current_runs,
                current_balls
            )
        })

    return pd.DataFrame(
        partnerships
    )

# ==========================================
# PARTNERSHIP RUN RATE
# ==========================================

def partnership_rr(
    runs,
    balls
):

    if balls <= 0:
        return 0

    overs = balls / 6

    return round(
        runs / overs,
        2
    )

# ==========================================
# HIGHEST PARTNERSHIP
# ==========================================

def highest_partnership(
    partnerships_df
):

    if partnerships_df.empty:
        return None

    return partnerships_df.sort_values(

        by="Runs",

        ascending=False
    ).iloc[0]

# ==========================================
# CURRENT PARTNERSHIP
# ==========================================

def current_partnership(
    partnerships_df
):

    if partnerships_df.empty:
        return None

    return partnerships_df.iloc[-1]

# ==========================================
# TOTAL PARTNERSHIPS
# ==========================================

def total_partnerships(
    partnerships_df
):

    if partnerships_df.empty:
        return 0

    return int(
        partnerships_df.shape[0]
    )

# ==========================================
# FIFTY PARTNERSHIPS
# ==========================================

def fifty_partnerships(
    partnerships_df
):

    if partnerships_df.empty:
        return pd.DataFrame()

    return partnerships_df[
        partnerships_df["Runs"] >= 50
    ]

# ==========================================
# HUNDRED PARTNERSHIPS
# ==========================================

def hundred_partnerships(
    partnerships_df
):

    if partnerships_df.empty:
        return pd.DataFrame()

    return partnerships_df[
        partnerships_df["Runs"] >= 100
    ]

# ==========================================
# PARTNERSHIP SUMMARY
# ==========================================

def partnership_summary(
    partnerships_df
):

    if partnerships_df.empty:

        return {

            "highest": 0,

            "average": 0,

            "total": 0
        }

    highest = int(
        partnerships_df["Runs"]
        .max()
    )

    average = round(

        partnerships_df["Runs"]
        .mean(),

        2
    )

    total = int(
        partnerships_df.shape[0]
    )

    return {

        "highest": highest,

        "average": average,

        "total": total
    }

# ==========================================
# BEST RUN RATE
# ==========================================

def best_partnership_rr(
    partnerships_df,
    min_runs=20
):

    if partnerships_df.empty:
        return None

    filtered = partnerships_df[
        partnerships_df["Runs"]
        >= min_runs
    ]

    if filtered.empty:
        return None

    return filtered.sort_values(

        by="Run Rate",

        ascending=False
    ).iloc[0]

# ==========================================
# LONGEST PARTNERSHIP
# ==========================================

def longest_partnership(
    partnerships_df
):

    if partnerships_df.empty:
        return None

    return partnerships_df.sort_values(

        by="Balls",

        ascending=False
    ).iloc[0]

# ==========================================
# AVERAGE PARTNERSHIP RR
# ==========================================

def average_partnership_rr(
    partnerships_df
):

    if partnerships_df.empty:
        return 0

    return round(

        partnerships_df[
            "Run Rate"
        ].mean(),

        2
    )

# ==========================================
# PARTNERSHIP BREAKDOWN
# ==========================================

def partnership_breakdown(
    partnerships_df
):

    if partnerships_df.empty:

        return {

            "0-25": 0,

            "25-50": 0,

            "50-100": 0,

            "100+": 0
        }

    breakdown = {

        "0-25": 0,

        "25-50": 0,

        "50-100": 0,

        "100+": 0
    }

    for runs in partnerships_df[
        "Runs"
    ]:

        if runs < 25:

            breakdown["0-25"] += 1

        elif runs < 50:

            breakdown["25-50"] += 1

        elif runs < 100:

            breakdown["50-100"] += 1

        else:

            breakdown["100+"] += 1

    return breakdown