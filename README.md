# Canopy

> See your codebase from above.

Canopy is a self-hosted tool that visualizes your GitHub repositories as
interactive dependency graphs. Paste a GitHub Personal Access Token, pick any
repo from your account, and explore its file structure with an AI-powered map.

## What it does

- **Connect** to GitHub with a Personal Access Token
- **Browse** your repos and pick one to analyse
- **Visualise** the dependency graph — files as nodes, imports as edges
- **Explore** — click any file node for an AI summary
- **Search** — filter nodes by filename

## Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # then fill in your keys
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

*Built for GDSC 2026.*
