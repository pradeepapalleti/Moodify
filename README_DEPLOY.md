Deployment guide — Backend (Render) and Frontend (Vercel)
=====================================================

This repository contains a lightweight backend (Flask) in `backend/` and a static frontend in `frontend/`.

Overview
- Backend: `backend/app.py` — provides `/recommend`, `/chat`, `/stats`. Deploy this to Render as a Python web service.
- Frontend: static HTML/JS in `frontend/` — uses `face-api.js` (TF.js) for browser-side emotion detection. Deploy this to Vercel as a static site.

Before you deploy
- Make sure `data/spotify_mood_tracks_multilang.csv` is present (the dataset used by the recommender). The backend reads this file at startup.
- Update `frontend/config.js` to set `BACKEND_URL` to the Render service URL once backend is deployed.

Render — Backend deployment (steps)
1. Create a new Web Service on Render.
2. Connect your GitHub repository and choose the `main` branch (or the branch you want).
3. In Render service settings:
   - Environment: `Python 3`
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - Set the root to the repository root (Render will run build from repo root).
4. Add any environment variables if needed.
5. Deploy — Render will install the packages and start the service.

Vercel — Frontend deployment (steps)
1. Create a new project on Vercel and import this repository.
2. When selecting settings, set the Root Directory to `frontend` so Vercel deploys only the `frontend` folder as a static site.
3. No build command is required for static HTML. You can leave Build Command empty and Output Directory empty.
4. Deploy the project.
5. After deployment, copy the Vercel frontend URL.

Final wiring
1. After backend is deployed on Render, copy the Render service URL (for example `https://moodify-backend.onrender.com`).
2. Edit `frontend/config.js` and set `BACKEND_URL` to your Render URL, for example:
   ```js
   const BACKEND_URL = 'https://moodify-backend.onrender.com';
   ```
3. Re-deploy the frontend on Vercel (trigger redeploy) so the frontend uses the live backend.

Local testing
- Start backend locally:
```powershell
cd backend
python -m pip install -r requirements.txt
gunicorn app:app --bind 0.0.0.0:5000
```
- Open `frontend/chat.html` directly in the browser (or serve `frontend/` with a simple static server) and set `BACKEND_URL` in `frontend/config.js` to `http://localhost:5000`.

Notes & Troubleshooting
- If your dataset CSV is large, Render may take longer to start. Consider compressing or moving to object storage for production.
- The original `app.py` in repo root contains optional DeepFace/OpenCV code (heavy). The `backend/` service here is intentionally lightweight and does not require system-level libraries.
