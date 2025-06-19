# Turkish Series Library

This project fetches Turkish series episodes (dubbed & subbed) automatically from multiple sources, avoids duplicates, and updates `episodes.json` via GitHub Actions every 6 hours.

## Setup

1. Create a new GitHub repo and push this structure.
2. Add a **Secrets** > `ACTIONS_TOKEN` if private.
3. Workflow runs every 6h or manually via "Run workflow".

## Local Run

```bash
pip install -r requirements.txt
python fetch_episodes.py
