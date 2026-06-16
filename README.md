canopy-gdsc-iitr-production.up.railway.app   - backend 
https://canopy-gdsc-iitr.vercel.app/ - frontend 


# Canopy

See your codebase from above. Canopy turns a GitHub repo into an interactive
dependency graph and uses AI to summarise each file.

## Setup

Backend:

    cd backend
    pip install -r requirements.txt
    cp .env.example .env   # add your GROQ_KEY
    uvicorn main:app --reload

Frontend:

    cd frontend
    npm install
    cp .env.local.example .env.local
    npm run dev

You need a GitHub personal access token (repo scope) and a Groq API key.

## Tests

    pip install -r requirements-dev.txt
    pytest backend/tests

Built for GDSC 2026.
