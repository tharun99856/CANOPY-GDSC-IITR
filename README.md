# Canopy

See your codebase from above. Canopy turns a GitHub repo into an interactive
dependency graph and uses AI to summarise each file.

## Setup

Backend:

    cd backend
    pip install -r requirements.txt
    cp .env.example .env   # add your GEMINI_KEY
    uvicorn main:app --reload

Frontend:

    cd frontend
    npm install
    cp .env.local.example .env.local
    npm run dev

You need a GitHub personal access token (repo scope) and a Gemini API key.

Built for GDSC 2026.
