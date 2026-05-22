# Architecture Documentation — Cricket Scoring App

## Overview

The Cricket Scoring App follows a layered modular architecture designed for:

- Scalability
- Maintainability
- Real-time scoring
- Tournament management
- Analytics generation
- Railway cloud deployment
- SQLite persistence

---

# High-Level Architecture

```text id="wxyfkn"
Frontend (Streamlit Pages)
            ↓
Service Layer
            ↓
Utility / Engine Layer
            ↓
Database Query Layer
            ↓
SQLite Database