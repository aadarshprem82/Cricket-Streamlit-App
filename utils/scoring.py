from datetime import datetime

from database.queries import (
    insert_ball_event
)

# ==========================================
# NORMAL RUNS
# ==========================================

def score_runs(

    match_id,

    innings,

    batting_team,

    bowling_team,

    over_num,

    ball_num,

    striker,

    non_striker,

    bowler,

    runs
):

    insert_ball_event(

        match_id=match_id,

        innings=innings,

        batting_team=batting_team,

        bowling_team=bowling_team,

        over_num=over_num,

        ball_num=ball_num,

        striker=striker,

        non_striker=non_striker,

        bowler=bowler,

        runs_off_bat=runs,

        extras=0,

        extra_type="",

        total_runs=runs,

        wicket="No",

        wicket_type="",

        player_out="",

        commentary=generate_commentary(
            striker,
            bowler,
            runs
        )
    )

# ==========================================
# DOT BALL
# ==========================================

def score_dot_ball(

    match_id,

    innings,

    batting_team,

    bowling_team,

    over_num,

    ball_num,

    striker,

    non_striker,

    bowler
):

    insert_ball_event(

        match_id=match_id,

        innings=innings,

        batting_team=batting_team,

        bowling_team=bowling_team,

        over_num=over_num,

        ball_num=ball_num,

        striker=striker,

        non_striker=non_striker,

        bowler=bowler,

        runs_off_bat=0,

        extras=0,

        extra_type="",

        total_runs=0,

        wicket="No",

        wicket_type="",

        player_out="",

        commentary=(
            f"{bowler} to "
            f"{striker}, dot ball."
        )
    )

# ==========================================
# WIDE
# ==========================================

def score_wide(

    match_id,

    innings,

    batting_team,

    bowling_team,

    over_num,

    ball_num,

    striker,

    non_striker,

    bowler,

    extra_runs=1
):

    insert_ball_event(

        match_id=match_id,

        innings=innings,

        batting_team=batting_team,

        bowling_team=bowling_team,

        over_num=over_num,

        ball_num=ball_num,

        striker=striker,

        non_striker=non_striker,

        bowler=bowler,

        runs_off_bat=0,

        extras=extra_runs,

        extra_type="wide",

        total_runs=extra_runs,

        wicket="No",

        wicket_type="",

        player_out="",

        commentary=(
            f"{bowler} bowls wide."
        )
    )

# ==========================================
# NO BALL
# ==========================================

def score_no_ball(

    match_id,

    innings,

    batting_team,

    bowling_team,

    over_num,

    ball_num,

    striker,

    non_striker,

    bowler,

    bat_runs=0
):

    total = 1 + bat_runs

    insert_ball_event(

        match_id=match_id,

        innings=innings,

        batting_team=batting_team,

        bowling_team=bowling_team,

        over_num=over_num,

        ball_num=ball_num,

        striker=striker,

        non_striker=non_striker,

        bowler=bowler,

        runs_off_bat=bat_runs,

        extras=1,

        extra_type="no_ball",

        total_runs=total,

        wicket="No",

        wicket_type="",

        player_out="",

        commentary=(
            f"{bowler} bowls "
            f"a no ball."
        )
    )

# ==========================================
# BYES
# ==========================================

def score_byes(

    match_id,

    innings,

    batting_team,

    bowling_team,

    over_num,

    ball_num,

    striker,

    non_striker,

    bowler,

    byes
):

    insert_ball_event(

        match_id=match_id,

        innings=innings,

        batting_team=batting_team,

        bowling_team=bowling_team,

        over_num=over_num,

        ball_num=ball_num,

        striker=striker,

        non_striker=non_striker,

        bowler=bowler,

        runs_off_bat=0,

        extras=byes,

        extra_type="byes",

        total_runs=byes,

        wicket="No",

        wicket_type="",

        player_out="",

        commentary=(
            f"{byes} byes taken."
        )
    )

# ==========================================
# LEG BYES
# ==========================================

def score_leg_byes(

    match_id,

    innings,

    batting_team,

    bowling_team,

    over_num,

    ball_num,

    striker,

    non_striker,

    bowler,

    leg_byes
):

    insert_ball_event(

        match_id=match_id,

        innings=innings,

        batting_team=batting_team,

        bowling_team=bowling_team,

        over_num=over_num,

        ball_num=ball_num,

        striker=striker,

        non_striker=non_striker,

        bowler=bowler,

        runs_off_bat=0,

        extras=leg_byes,

        extra_type="leg_byes",

        total_runs=leg_byes,

        wicket="No",

        wicket_type="",

        player_out="",

        commentary=(
            f"{leg_byes} leg byes."
        )
    )

# ==========================================
# WICKET
# ==========================================

def score_wicket(

    match_id,

    innings,

    batting_team,

    bowling_team,

    over_num,

    ball_num,

    striker,

    non_striker,

    bowler,

    player_out,

    wicket_type,

    runs=0
):

    insert_ball_event(

        match_id=match_id,

        innings=innings,

        batting_team=batting_team,

        bowling_team=bowling_team,

        over_num=over_num,

        ball_num=ball_num,

        striker=striker,

        non_striker=non_striker,

        bowler=bowler,

        runs_off_bat=runs,

        extras=0,

        extra_type="",

        total_runs=runs,

        wicket="Yes",

        wicket_type=wicket_type,

        player_out=player_out,

        commentary=generate_wicket_commentary(

            bowler,

            player_out,

            wicket_type
        )
    )

# ==========================================
# RETIRED OUT
# ==========================================

def retired_out(

    match_id,

    innings,

    batting_team,

    bowling_team,

    over_num,

    ball_num,

    striker,

    non_striker,

    bowler,

    player_out
):

    insert_ball_event(

        match_id=match_id,

        innings=innings,

        batting_team=batting_team,

        bowling_team=bowling_team,

        over_num=over_num,

        ball_num=ball_num,

        striker=striker,

        non_striker=non_striker,

        bowler=bowler,

        runs_off_bat=0,

        extras=0,

        extra_type="",

        total_runs=0,

        wicket="Yes",

        wicket_type="Retired Out",

        player_out=player_out,

        commentary=(
            f"{player_out} retired out."
        )
    )

# ==========================================
# COMMENTARY
# ==========================================

def generate_commentary(

    batter,

    bowler,

    runs
):

    if runs == 4:

        return (

            f"{bowler} to {batter}, "
            f"FOUR!"
        )

    if runs == 6:

        return (

            f"{bowler} to {batter}, "
            f"SIX!"
        )

    if runs == 0:

        return (

            f"{bowler} to {batter}, "
            f"dot ball."
        )

    return (

        f"{bowler} to {batter}, "
        f"{runs} run."
    )

# ==========================================
# WICKET COMMENTARY
# ==========================================

def generate_wicket_commentary(

    bowler,

    player_out,

    wicket_type
):

    return (

        f"WICKET! {bowler} dismisses "

        f"{player_out} "

        f"({wicket_type})."
    )

# ==========================================
# SUPER OVER CHECK
# ==========================================

def is_super_over(
    innings,
    max_innings=2
):

    return innings > max_innings

# ==========================================
# FREE HIT CHECK
# ==========================================

def grants_free_hit(
    extra_type
):

    return extra_type == "no_ball"

# ==========================================
# LEGIT DELIVERY
# ==========================================

def is_legal_delivery(
    extra_type
):

    illegal = [

        "wide",

        "no_ball"
    ]

    return extra_type not in illegal

# ==========================================
# TIMESTAMP
# ==========================================

def current_timestamp():

    return str(
        datetime.now()
    )