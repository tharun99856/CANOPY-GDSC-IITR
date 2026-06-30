
Canopy turns any GitHub repository into a live, interactive dependency graph. Connect with a Personal Access Token, pick a repo, and explore how every file connects to every other file — with AI-powered summaries for each node.

**Live:** [canopy-gdsc-iitr.vercel.app](https://canopy-gdsc-iitr.vercel.app/)
**Backend:** [canopy-gdsc-iitr-production.up.railway.app](https://canopy-gdsc-iitr-production.up.railway.app)

---

## What it does

1. **Connect** — paste a GitHub PAT, your repos load instantly
2. **Pick** — select any repo from your account (public or private)
3. **Visualize** — file nodes laid out left-to-right by dependency depth, edges showing import direction
4. **Explore** — click any node for a 3-sentence AI summary of what that file does
5. **Search** — type a filename, matching nodes highlight, everything else dims

No cloning. No local file access. Everything runs through the GitHub API.

---

## Tech Stack

| Layer | Tech |
|-------|------|
| Backend | Python, FastAPI, httpx |
| Parser | Regex-based import extraction (Python + JS/TS) |
| AI | Groq (LLaMA) |
| Frontend | React 19, Vite, react-flow, dagre |
| Hosting | Railway (backend), Vercel (frontend) |

---

## Setup (Local)

### Backend

``bash
cd backend
pip install -r requirements.txt
Create .env:

GROQ_KEY=your_groq_key_here
uvicorn main:app --reload
Frontend
cd frontend
npm install
Create .env.local:

VITE_BACKEND=http://localhost:8000
npm run dev
GitHub PAT
GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
Generate new token with repo scope
Paste it in the Canopy connect panel
How it works
github_api.py — fetches repo list, file tree, and raw content via GitHub REST API
parser.py — extracts import edges from Python (import/from) and JS/TS (import/require) files, counts lines of code
ai_layer.py — sends file content to Groq for 3-sentence summaries, caches by MD5 hash
main.py — FastAPI with /repos, /load-repo, and /summarise endpoints
Frontend — react-flow canvas with dagre LR layout, custom node cards with file-type colour coding, floating search bar, side panel with AI summaries
Project Structure
canopy/
  backend/
    main.py           — FastAPI app, routes, CORS
    github_api.py     — GitHub REST API calls
    parser.py         — import extraction, LoC counter, graph builder
    ai_layer.py       — Groq summarisation, MD5 cache
    utils.py          — base64 decode, extension checks
    requirements.txt
  frontend/
    src/
      App.jsx         — root layout, global state
      GithubConnect.jsx — PAT input, repo list, repo picker
      GraphCanvas.jsx — react-flow canvas + dagre layout
      NodeCard.jsx    — custom node with type colour + LoC badge
      SidePanel.jsx   — file info + AI summary
      SearchBar.jsx   — floating search with highlight/dim
      api.js          — all fetch calls
      index.css       — full Canopy forest theme
Limitations
Parses Python, JS, TS, JSX, TSX only
Repos capped at 300 parseable files
GitHub API: 5000 req/hr with PAT
No real-time file watching or graph export
Built for GDSC 2026.
