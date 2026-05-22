import streamlit as st
from datetime import datetime

# ==========================================
# CACHE KEYS
# ==========================================

CACHE_KEYS = [

    "match_cache",

    "player_cache",

    "scorecard_cache",

    "stats_cache",

    "points_table_cache",

    "timeline_cache"
]

# ==========================================
# INITIALIZE CACHE
# ==========================================

def initialize_cache():

    for key in CACHE_KEYS:

        if key not in st.session_state:

            st.session_state[key] = {}

# ==========================================
# SET CACHE
# ==========================================

def set_cache(

    cache_name,

    cache_key,

    value
):

    initialize_cache()

    if cache_name not in st.session_state:

        st.session_state[
            cache_name
        ] = {}

    st.session_state[
        cache_name
    ][cache_key] = {

        "value": value,

        "timestamp":
        str(datetime.now())
    }

# ==========================================
# GET CACHE
# ==========================================

def get_cache(

    cache_name,

    cache_key
):

    initialize_cache()

    cache = st.session_state.get(
        cache_name,
        {}
    )

    if cache_key not in cache:
        return None

    return cache[cache_key][
        "value"
    ]

# ==========================================
# CACHE EXISTS
# ==========================================

def cache_exists(

    cache_name,

    cache_key
):

    initialize_cache()

    cache = st.session_state.get(
        cache_name,
        {}
    )

    return cache_key in cache

# ==========================================
# CLEAR CACHE
# ==========================================

def clear_cache(
    cache_name=None
):

    initialize_cache()

    if cache_name:

        st.session_state[
            cache_name
        ] = {}

        return

    for key in CACHE_KEYS:

        st.session_state[key] = {}

# ==========================================
# REMOVE CACHE KEY
# ==========================================

def remove_cache_key(

    cache_name,

    cache_key
):

    initialize_cache()

    cache = st.session_state.get(
        cache_name,
        {}
    )

    if cache_key in cache:

        del cache[cache_key]

# ==========================================
# CACHE TIMESTAMP
# ==========================================

def cache_timestamp(

    cache_name,

    cache_key
):

    initialize_cache()

    cache = st.session_state.get(
        cache_name,
        {}
    )

    if cache_key not in cache:
        return None

    return cache[cache_key][
        "timestamp"
    ]

# ==========================================
# MATCH CACHE
# ==========================================

def cache_match_data(

    match_id,

    data
):

    set_cache(

        "match_cache",

        match_id,

        data
    )

# ==========================================
# GET MATCH CACHE
# ==========================================

def get_match_cache(
    match_id
):

    return get_cache(

        "match_cache",

        match_id
    )

# ==========================================
# PLAYER CACHE
# ==========================================

def cache_player_stats(

    player_name,

    stats
):

    set_cache(

        "player_cache",

        player_name,

        stats
    )

# ==========================================
# GET PLAYER CACHE
# ==========================================

def get_player_cache(
    player_name
):

    return get_cache(

        "player_cache",

        player_name
    )

# ==========================================
# SCORECARD CACHE
# ==========================================

def cache_scorecard(

    match_id,

    scorecard
):

    set_cache(

        "scorecard_cache",

        match_id,

        scorecard
    )

# ==========================================
# GET SCORECARD CACHE
# ==========================================

def get_scorecard_cache(
    match_id
):

    return get_cache(

        "scorecard_cache",

        match_id
    )

# ==========================================
# STATS CACHE
# ==========================================

def cache_stats(

    cache_key,

    stats
):

    set_cache(

        "stats_cache",

        cache_key,

        stats
    )

# ==========================================
# GET STATS CACHE
# ==========================================

def get_stats_cache(
    cache_key
):

    return get_cache(

        "stats_cache",

        cache_key
    )

# ==========================================
# POINTS TABLE CACHE
# ==========================================

def cache_points_table(

    tournament_id,

    table
):

    set_cache(

        "points_table_cache",

        tournament_id,

        table
    )

# ==========================================
# GET POINTS TABLE CACHE
# ==========================================

def get_points_table_cache(
    tournament_id
):

    return get_cache(

        "points_table_cache",

        tournament_id
    )

# ==========================================
# CACHE SUMMARY
# ==========================================

def cache_summary():

    initialize_cache()

    summary = {}

    for key in CACHE_KEYS:

        cache = st.session_state.get(
            key,
            {}
        )

        summary[key] = len(cache)

    return summary

# ==========================================
# CACHE HEALTH
# ==========================================

def cache_health():

    summary = cache_summary()

    total = sum(
        summary.values()
    )

    return {

        "total_cached_items":
        total,

        "cache_breakdown":
        summary
    }

# ==========================================
# RESET APPLICATION CACHE
# ==========================================

def reset_application_cache():

    clear_cache()

    st.cache_data.clear()

    st.cache_resource.clear()