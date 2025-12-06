# Battle Arena (Flask)

A minimal Turn-Based Battle Arena RPG built with Flask to demonstrate OOP in Python.
Features:
- Flask backend with modular OOP game engine
- User auth (Flask-Login)
- Start battles vs AI, perform actions (attack/defend)
- Persistent match results and leaderboard (SQLite)
- Minimal JS frontend using fetch()

## Quick start
1. Create a virtualenv and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```bash
   python -c "from app import create_app, db; app=create_app(); app.app_context().__enter__(); db.create_all(); print('DB created')"
   ```
4. Run:
   ```bash
   python run.py
   ```
5. Open http://127.0.0.1:5000

This repository is a starting point — expand AI, add more actions, polish UI, and add tests.
