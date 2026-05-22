import streamlit as st

from database.db import (
    initialize_database
)

# ==========================================
# INITIALIZE DATABASE
# ==========================================

initialize_database()

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(

    page_title="Cricket Scoring App",

    page_icon="🏏",

    layout="wide",

    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS
# ==========================================

def load_css():

    try:

        with open(
            "assets/css/style.css"
        ) as f:

            st.markdown(

                f"<style>{f.read()}</style>",

                unsafe_allow_html=True
            )

    except:
        pass

load_css()

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("🏏 Cricket Scoring")

    st.markdown("---")

    st.markdown(
        """
        ### Navigation

        Use the sidebar pages to access:

        - Create Match
        - Live Scoring
        - Scoreboards
        - Analytics
        - Career Stats
        - Tournament Manager
        """
    )

    st.markdown("---")

    st.success(
        "SQLite + Railway Ready"
    )

# ==========================================
# HOME PAGE
# ==========================================

st.title(
    "🏏 Cricket Scoring Platform"
)

st.subheader(
    "Professional Local Cricket Management System"
)

st.markdown("---")

# ==========================================
# FEATURES
# ==========================================

col1, col2, col3 = st.columns(3)

with col1:

    st.info(
        """
        ### 🎯 Live Scoring

        - Ball-by-ball scoring
        - Strike rotation
        - Innings engine
        - Match completion
        """
    )

with col2:

    st.success(
        """
        ### 📊 Analytics

        - Worm charts
        - Manhattan charts
        - Partnerships
        - Career stats
        """
    )

with col3:

    st.warning(
        """
        ### 🏆 Tournament Engine

        - Points table
        - Rankings
        - Team stats
        - Match history
        """
    )

# ==========================================
# SYSTEM INFO
# ==========================================

st.markdown("---")

st.subheader(
    "⚙️ System Architecture"
)

architecture = {

    "Frontend": "Streamlit",

    "Database": "SQLite",

    "Hosting": "Railway",

    "Charts": "Plotly",

    "Backend Pattern": "Service Layer",

    "Storage": "Persistent Volume"
}

st.json(architecture)

# ==========================================
# QUICK START
# ==========================================

st.markdown("---")

st.subheader(
    "🚀 Quick Start"
)

st.markdown(
    """
    1. Add Teams
    2. Add Players
    3. Create Match
    4. Start Live Scoring
    5. Watch Real-Time Analytics

    Your database is automatically initialized.
    """
)

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "Built with Streamlit + SQLite + Railway"
)