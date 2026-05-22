import pandas as pd

# ==========================================
# TEAM CAREER STATS
# ==========================================

def team_career_stats(

    matches_df,

    ball_df
):

    if matches_df.empty:
        return pd.DataFrame()

    teams = pd.concat([

        matches_df["team1"],

        matches_df["team2"]

    ]).dropna().unique()

    stats = []

    for team in teams:

        played = int(

            matches_df[

                (matches_df["team1"] == team)

                |

                (matches_df["team2"] == team)

            ].shape[0]
        )

        wins = int(

            matches_df[
                matches_df["winner"]
                == team
            ].shape[0]
        )

        losses = max(
            played - wins,
            0
        )

        team_batting = ball_df[
            ball_df["batting_team"]
            == team
        ]

        runs_scored = int(
            team_batting[
                "total_runs"
            ].sum()
        )

        wickets_lost = int(

            team_batting[
                team_batting["wicket"]
                == "Yes"
            ].shape[0]
        )

        highest = highest_team_score(
            ball_df,
            team
        )

        lowest = lowest_team_score(
            ball_df,
            team
        )

        rr = team_run_rate(
            team_batting
        )

        win_pct = 0

        if played > 0:

            win_pct = round(
                (wins / played) * 100,
                2
            )

        stats.append({

            "Team": team,

            "Played": played,

            "Wins": wins,

            "Losses": losses,

            "Win %": win_pct,

            "Runs": runs_scored,

            "Wickets Lost":
            wickets_lost,

            "Highest":
            highest,

            "Lowest":
            lowest,

            "Run Rate":
            rr
        })

    df = pd.DataFrame(stats)

    if df.empty:
        return df

    return df.sort_values(

        by=["Wins", "Run Rate"],

        ascending=[False, False]
    )

# ==========================================
# HIGHEST TEAM SCORE
# ==========================================

def highest_team_score(
    ball_df,
    team
):

    team_df = ball_df[
        ball_df["batting_team"]
        == team
    ]

    if team_df.empty:
        return 0

    grouped = (

        team_df

        .groupby([
            "match_id",
            "innings"
        ])["total_runs"]

        .sum()
    )

    if grouped.empty:
        return 0

    return int(
        grouped.max()
    )

# ==========================================
# LOWEST TEAM SCORE
# ==========================================

def lowest_team_score(
    ball_df,
    team
):

    team_df = ball_df[
        ball_df["batting_team"]
        == team
    ]

    if team_df.empty:
        return 0

    grouped = (

        team_df

        .groupby([
            "match_id",
            "innings"
        ])["total_runs"]

        .sum()
    )

    if grouped.empty:
        return 0

    return int(
        grouped.min()
    )

# ==========================================
# TEAM RUN RATE
# ==========================================

def team_run_rate(
    team_df
):

    if team_df.empty:
        return 0

    legal = team_df[

        ~team_df["extra_type"]

        .isin([
            "wide",
            "no_ball"
        ])
    ]

    legal_balls = int(
        legal.shape[0]
    )

    if legal_balls <= 0:
        return 0

    overs = legal_balls / 6

    runs = int(
        team_df["total_runs"]
        .sum()
    )

    return round(
        runs / overs,
        2
    )

# ==========================================
# BEST TEAM
# ==========================================

def best_team(
    team_df
):

    if team_df.empty:
        return None

    return team_df.iloc[0]

# ==========================================
# HIGHEST SCORING TEAM
# ==========================================

def highest_scoring_team(
    team_df
):

    if team_df.empty:
        return None

    return team_df.sort_values(

        by="Runs",

        ascending=False
    ).iloc[0]

# ==========================================
# BEST RUN RATE TEAM
# ==========================================

def best_run_rate_team(
    team_df
):

    if team_df.empty:
        return None

    return team_df.sort_values(

        by="Run Rate",

        ascending=False
    ).iloc[0]

# ==========================================
# TEAM RANKINGS
# ==========================================

def generate_team_rankings(
    team_df
):

    if team_df.empty:
        return pd.DataFrame()

    rankings = team_df.copy()

    rankings = rankings.sort_values(

        by=["Wins", "Run Rate"],

        ascending=[False, False]
    )

    rankings["Rank"] = range(

        1,

        len(rankings) + 1
    )

    columns = [

        "Rank",

        "Team",

        "Played",

        "Wins",

        "Losses",

        "Win %",

        "Run Rate"
    ]

    return rankings[
        columns
    ]

# ==========================================
# TEAM SUMMARY
# ==========================================

def team_summary(
    team_name,
    team_df
):

    team = team_df[
        team_df["Team"]
        == team_name
    ]

    if team.empty:
        return None

    return team.iloc[0].to_dict()

# ==========================================
# UNBEATEN TEAMS
# ==========================================

def unbeaten_teams(
    team_df
):

    if team_df.empty:
        return pd.DataFrame()

    return team_df[
        team_df["Losses"] == 0
    ]

# ==========================================
# MOST MATCHES
# ==========================================

def most_matches_played(
    team_df
):

    if team_df.empty:
        return None

    return team_df.sort_values(

        by="Played",

        ascending=False
    ).iloc[0]

# ==========================================
# BEST WIN %
# ==========================================

def best_win_percentage(
    team_df,
    min_matches=1
):

    if team_df.empty:
        return None

    filtered = team_df[
        team_df["Played"]
        >= min_matches
    ]

    if filtered.empty:
        return None

    return filtered.sort_values(

        by="Win %",

        ascending=False
    ).iloc[0]