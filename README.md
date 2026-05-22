# 🏏 Cricket Scoring App

Professional local cricket scoring and analytics platform built using:

- Streamlit
- SQLite
- Railway
- Plotly

Designed for:
- local tournaments
- friends cricket leagues
- club cricket
- custom IPL-style scoring systems

---

# 🚀 Features

## Live Match Engine

- Ball-by-ball scoring
- Strike rotation
- Extras
- Wickets
- Partnerships
- Innings management
- Match completion logic

---

## Professional Scorecards

- Batting scorecards
- Bowling scorecards
- Fall of wickets
- Partnerships
- Match summaries

---

## Advanced Analytics

- Worm charts
- Manhattan charts
- Run distribution
- Phase analysis
- Required run rate tracking

---

## Career Statistics

### Batting
- Runs
- Average
- Strike Rate
- 50s / 100s
- Highest score

### Bowling
- Wickets
- Economy
- Best figures
- Bowling average

### Team Stats
- Rankings
- Win %
- Team records

---

# 🏗️ Architecture

```text
Streamlit UI
    ↓
Service Layer
    ↓
Business Logic
    ↓
SQLite Database
```

---

# 📁 Project Structure

```text
cricket-scoring-app/
│
├── app.py
├── database/
├── pages/
├── services/
├── utils/
├── assets/
└── tests/
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone <your-repository-url>
cd cricket-scoring-app
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Application

```bash
streamlit run app.py
```

---

# 🗄️ Database

The app uses SQLite.

Database file:

```text
database/cricket.db
```

Database initializes automatically on first launch.

---

# 🚂 Railway Deployment

## Create Railway Project

Go to:

https://railway.app/

---

## Deploy

### Option 1 — GitHub Deploy

1. Push code to GitHub
2. Connect Railway to GitHub repo
3. Deploy automatically

---

### Option 2 — Railway CLI

```bash
railway login
railway init
railway up
```

---

# 🌐 Railway Start Command

```bash
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

---

# 🔥 Recommended Future Upgrades

- PostgreSQL migration
- Authentication
- Live WebSocket scoring
- Fantasy cricket
- API layer
- Mobile app
- AI insights
- Auction engine
- Player ratings
- IPL-style UI

---

# 🧪 Testing

Run tests:

```bash
pytest
```

---

# 📊 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Database | SQLite |
| Hosting | Railway |
| Analytics | Plotly |
| Language | Python |

---

# 🛡️ Production Notes

SQLite is perfect for:
- local leagues
- friends tournaments
- small-medium scoring systems

For very large scale:
- migrate to PostgreSQL

The architecture is already designed for easy migration.

---

# 👨‍💻 Developer Notes

This project follows:
- service-layer architecture
- modular utilities
- event-driven scoring
- persistent database state

---

# 📄 License

MIT License

---

# ❤️ Built For Cricket Lovers