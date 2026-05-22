import re

# ==========================================
# REQUIRED FIELD
# ==========================================

def validate_required(
    value
):

    if value is None:
        return False

    if str(value).strip() == "":
        return False

    return True

# ==========================================
# TEAM NAME
# ==========================================

def validate_team_name(
    team_name
):

    if not validate_required(
        team_name
    ):

        return False

    if len(team_name) < 2:
        return False

    return True

# ==========================================
# PLAYER NAME
# ==========================================

def validate_player_name(
    player_name
):

    if not validate_required(
        player_name
    ):

        return False

    if len(player_name) < 2:
        return False

    return True

# ==========================================
# OVERS
# ==========================================

def validate_overs(
    overs
):

    try:

        overs = int(overs)

        return overs > 0

    except:
        return False

# ==========================================
# RUN VALUE
# ==========================================

def validate_runs(
    runs
):

    valid_runs = [

        0, 1, 2, 3, 4, 5, 6
    ]

    return runs in valid_runs

# ==========================================
# WICKET TYPE
# ==========================================

def validate_wicket_type(
    wicket_type
):

    valid_types = [

        "Bowled",

        "Caught",

        "LBW",

        "Run Out",

        "Stumped",

        "Hit Wicket",

        "Retired Out"
    ]

    return wicket_type in valid_types

# ==========================================
# MATCH ID
# ==========================================

def validate_match_id(
    match_id
):

    if not validate_required(
        match_id
    ):

        return False

    pattern = r"^[A-Z0-9_]+$"

    return bool(
        re.match(
            pattern,
            str(match_id)
        )
    )

# ==========================================
# TOURNAMENT ID
# ==========================================

def validate_tournament_id(
    tournament_id
):

    if not validate_required(
        tournament_id
    ):

        return False

    pattern = r"^[A-Z0-9_]+$"

    return bool(
        re.match(
            pattern,
            str(tournament_id)
        )
    )

# ==========================================
# USERNAME
# ==========================================

def validate_username(
    username
):

    if not validate_required(
        username
    ):

        return False

    pattern = r"^[a-zA-Z0-9_]+$"

    return bool(
        re.match(
            pattern,
            username
        )
    )

# ==========================================
# PASSWORD
# ==========================================

def validate_password(
    password
):

    if not validate_required(
        password
    ):

        return False

    return len(password) >= 6

# ==========================================
# EMAIL
# ==========================================

def validate_email(
    email
):

    if not validate_required(
        email
    ):

        return False

    pattern = (

        r"^[a-zA-Z0-9_.+-]+"

        r"@[a-zA-Z0-9-]+"

        r"\.[a-zA-Z0-9-.]+$"
    )

    return bool(
        re.match(
            pattern,
            email
        )
    )

# ==========================================
# BALL NUMBER
# ==========================================

def validate_ball_number(
    ball_number
):

    try:

        ball_number = int(
            ball_number
        )

        return (
            1 <= ball_number <= 6
        )

    except:
        return False

# ==========================================
# INNINGS
# ==========================================

def validate_innings(
    innings
):

    try:

        innings = int(innings)

        return innings in [1, 2]

    except:
        return False

# ==========================================
# SCORE
# ==========================================

def validate_score(
    score
):

    try:

        score = int(score)

        return score >= 0

    except:
        return False

# ==========================================
# ROLE
# ==========================================

def validate_role(
    role
):

    valid_roles = [

        "Batter",

        "Bowler",

        "All Rounder",

        "Wicket Keeper"
    ]

    return role in valid_roles

# ==========================================
# BATTING STYLE
# ==========================================

def validate_batting_style(
    style
):

    valid_styles = [

        "Right Hand Bat",

        "Left Hand Bat"
    ]

    return style in valid_styles

# ==========================================
# BOWLING STYLE
# ==========================================

def validate_bowling_style(
    style
):

    valid_styles = [

        "None",

        "Right Arm Fast",

        "Left Arm Fast",

        "Right Arm Spin",

        "Left Arm Spin"
    ]

    return style in valid_styles

# ==========================================
# FILE EXTENSION
# ==========================================

def validate_file_extension(

    filename,

    allowed_extensions
):

    if "." not in filename:
        return False

    extension = (

        filename

        .split(".")[-1]

        .lower()
    )

    return extension in allowed_extensions

# ==========================================
# POINTS TABLE ENTRY
# ==========================================

def validate_points(
    points
):

    try:

        points = int(points)

        return points >= 0

    except:
        return False

# ==========================================
# NET RUN RATE
# ==========================================

def validate_net_run_rate(
    nrr
):

    try:

        float(nrr)

        return True

    except:
        return False