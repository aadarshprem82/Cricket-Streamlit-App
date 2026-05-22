import hashlib

from database.db import (

    execute_query,

    fetch_one,

    fetch_all
)

# ==========================================
# HASH PASSWORD
# ==========================================

def hash_password(
    password
):

    return hashlib.sha256(

        password.encode()

    ).hexdigest()

# ==========================================
# CREATE USER
# ==========================================

def create_user(

    username,

    password,

    role="viewer"
):

    query = """

    INSERT INTO users (

        username,
        password_hash,
        role,
        is_active,
        created_at

    )

    VALUES (?, ?, ?, ?, datetime('now'))

    """

    password_hash = hash_password(
        password
    )

    execute_query(

        query,

        (
            username,
            password_hash,
            role,
            1
        )
    )

# ==========================================
# AUTHENTICATE USER
# ==========================================

def authenticate_user(

    username,

    password
):

    query = """

    SELECT *

    FROM users

    WHERE username=?
    AND is_active=1

    """

    user = fetch_one(
        query,
        (username,)
    )

    if not user:
        return None

    password_hash = hash_password(
        password
    )

    if (

        user["password_hash"]

        ==

        password_hash
    ):

        return user

    return None

# ==========================================
# FETCH USERS
# ==========================================

def fetch_users():

    query = """

    SELECT id,
           username,
           role,
           is_active,
           created_at

    FROM users

    ORDER BY username ASC

    """

    return fetch_all(query)

# ==========================================
# USER EXISTS
# ==========================================

def user_exists(
    username
):

    query = """

    SELECT username

    FROM users

    WHERE username=?

    """

    user = fetch_one(
        query,
        (username,)
    )

    return user is not None

# ==========================================
# CHANGE PASSWORD
# ==========================================

def change_password(

    username,

    new_password
):

    password_hash = hash_password(
        new_password
    )

    query = """

    UPDATE users

    SET password_hash=?

    WHERE username=?

    """

    execute_query(

        query,

        (
            password_hash,
            username
        )
    )

# ==========================================
# CHANGE ROLE
# ==========================================

def change_user_role(

    username,

    role
):

    query = """

    UPDATE users

    SET role=?

    WHERE username=?

    """

    execute_query(

        query,

        (
            role,
            username
        )
    )

# ==========================================
# DEACTIVATE USER
# ==========================================

def deactivate_user(
    username
):

    query = """

    UPDATE users

    SET is_active=0

    WHERE username=?

    """

    execute_query(
        query,
        (username,)
    )

# ==========================================
# ACTIVATE USER
# ==========================================

def activate_user(
    username
):

    query = """

    UPDATE users

    SET is_active=1

    WHERE username=?

    """

    execute_query(
        query,
        (username,)
    )

# ==========================================
# IS ADMIN
# ==========================================

def is_admin(
    username
):

    query = """

    SELECT role

    FROM users

    WHERE username=?

    """

    user = fetch_one(
        query,
        (username,)
    )

    if not user:
        return False

    return (
        user["role"]
        ==
        "admin"
    )

# ==========================================
# LOGIN SESSION
# ==========================================

def login_user(
    user
):

    import streamlit as st

    st.session_state[
        "logged_in"
    ] = True

    st.session_state[
        "username"
    ] = user["username"]

    st.session_state[
        "role"
    ] = user["role"]

# ==========================================
# LOGOUT SESSION
# ==========================================

def logout_user():

    import streamlit as st

    keys = [

        "logged_in",

        "username",

        "role"
    ]

    for key in keys:

        if key in st.session_state:

            del st.session_state[key]

# ==========================================
# REQUIRE LOGIN
# ==========================================

def require_login():

    import streamlit as st

    if not st.session_state.get(
        "logged_in",
        False
    ):

        st.warning(
            "Please login first."
        )

        st.stop()

# ==========================================
# REQUIRE ADMIN
# ==========================================

def require_admin():

    import streamlit as st

    require_login()

    if st.session_state.get(
        "role"
    ) != "admin":

        st.error(
            "Admin access required."
        )

        st.stop()

# ==========================================
# CURRENT USER
# ==========================================

def current_user():

    import streamlit as st

    if not st.session_state.get(
        "logged_in"
    ):

        return None

    return {

        "username":

        st.session_state.get(
            "username"
        ),

        "role":

        st.session_state.get(
            "role"
        )
    }