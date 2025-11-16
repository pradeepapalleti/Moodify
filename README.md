# 🎵 Spotify Mood-Based Music Recommender# Mood-Based Song Recommendation AI



AI-powered music recommendation system with facial expression detection, multi-language support, and Spotify integration.This project aims to build an AI model that recommends songs based on the user's mood.



---## Project Structure



## ✨ Features- `app.py`: The main application file.

- `data/`: Contains the dataset for training the model.

### 🎭 **Mood Selector Mode**- `notebooks/`: Jupyter notebooks for exploration and model development.

- 8 moods: Happy, Sad, Energetic, Calm, Romantic, Motivated, Party, Focus- `requirements.txt`: A list of Python dependencies for the project.

- 6 languages: English, Hindi, Telugu, Tamil, Malayalam, Kannada- `.gitignore`: Specifies which files to ignore in git.

- 1,156+ curated Spotify tracks

- Direct Spotify playback integration## How to get started



### 💬 **AI Chat Mode**1. **Install dependencies**:

- Natural language mood detection ("I'm feeling happy")   ```bash

- Conversation memory (context-aware responses)   pip install -r requirements.txt

- Auto language detection from text ("Give me Hindi sad songs")   ```

- Smart continuations ("more songs" remembers previous context)2. **Find a dataset**: You'll need a dataset of songs with mood labels. Some potential sources are the Million Song Dataset, or you can create your own by scraping data from services like Spotify or Last.fm.

3. **Data Preprocessing and Feature Extraction**: Clean the data and extract relevant features from the audio or metadata.

### 📷 **NEW: Camera Mood Detection**4. **Model Training**: Train a machine learning model to predict the mood of a song.

- Real-time facial expression analysis5. **Build the Recommendation System**: Use the trained model to recommend songs that match a user's mood.

- AI-powered emotion recognition (DeepFace + TensorFlow)
- Automatic mood mapping: happy, sad, angry, surprise → music moods
- Privacy-focused: local processing, no data saved

### 🎨 **Spotify-Inspired UI**
- Dark/Light mode with localStorage persistence
- Spotify green (#1DB954) color palette
- Smooth animations and transitions
- Fully responsive design

---

## 🚀 Quick Start

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Open browser
http://localhost:5000
```

### Requirements
```
Flask==3.0.3
pandas==2.3.3
opencv-python==4.12.0.88
deepface==0.0.95
tensorflow==2.20.0
```

---

## 📖 How to Use

### Option 1: Mood Selector
1. Select a mood (Happy, Sad, etc.)
2. Choose a language (or All Languages)
3. Set number of recommendations
4. Get instant song suggestions

### Option 2: AI Chat
1. Type how you're feeling: "I'm sad"
2. Specify language: "Give me Hindi romantic songs"
3. Continue conversation: "more songs like that"
4. Get context-aware recommendations

### Option 3: Camera Detection 📸
1. Click **"📷 Face Mood"** button
2. Allow camera access
3. Make a facial expression
4. Click **"📸 Capture & Analyze"**
5. AI detects your emotion and recommends songs!

**Emotion Mapping:**
- 😊 Happy → Happy music
- 😢 Sad → Sad songs
- 😠 Angry → Energetic tracks
- 😐 Neutral → Calm vibes

---

## 🛠️ Tech Stack

**Frontend:** HTML5, CSS3, JavaScript (WebRTC for camera)  
**Backend:** Flask, Pandas  
**AI/ML:** DeepFace, TensorFlow, OpenCV  
**Data:** 1,156 Spotify tracks with metadata  
**Design:** Spotify-inspired dark/light theme

---

## 📊 Dataset

- **Total Tracks:** 1,156 unique songs
- **Languages:** English (246), Hindi (205), Tamil (199), Telugu (197), Kannada (159), Malayalam (150)
- **Moods:** Happy (164), Energetic (151), Sad (150), Focus (146), Calm (145), Romantic (145), Motivated (133), Party (122)
- **Features:** Track ID, name, artist, album, popularity, duration, release date

---

## 🎯 API Endpoints

- `GET /` - Mood selector page
- `GET /chat-page` - AI chat interface
- `POST /recommend` - Get recommendations by mood/language
- `POST /chat` - Natural language chat with mood detection
- `POST /detect-emotion` - Facial emotion detection from camera
- `GET /stats` - Dataset statistics

---

## 🔒 Privacy & Security

- Camera access only on user request
- Images processed locally, not stored
- No external data transmission
- Session-based conversation memory (not persisted)

---

## 📁 Project Structure

```
practice/
├── app.py                              # Flask backend + AI logic
├── templates/
│   ├── index.html                      # Mood selector UI
│   └── chat.html                       # Chat + camera UI
├── data/
│   └── spotify_mood_tracks_multilang.csv  # 1,156 tracks dataset
├── requirements.txt                    # Python dependencies
└── practice_backup/                    # Backup of all files
```

---

## 🎨 UI Highlights

- **Spotify Color Palette:** #1DB954 green, #121212 dark bg
- **CSS Variables:** Dynamic theming support
- **Theme Toggle:** 🌙/☀️ button with persistence
- **Play Buttons:** ▶️ Individual track playback
- **Album Links:** 🎵 Open full Spotify search
- **Responsive:** Works on mobile, tablet, desktop

---

## 💡 Technologies

| Category | Tools |
|----------|-------|
| **Web Framework** | Flask 3.0.3 |
| **Data Processing** | Pandas, NumPy |
| **Computer Vision** | OpenCV 4.12 |
| **AI/ML** | DeepFace, TensorFlow 2.20 |
| **API** | Spotify Web API (Search) |
| **Frontend** | HTML5, CSS3, JavaScript ES6 |

---

## 🔧 Advanced Features

- **Conversation Memory:** Stores last 10 exchanges per session
- **Language Detection:** Regex-based keyword matching ("Hindi songs", "Tamil music")
- **Mood Synonyms:** Maps "joyful", "cheerful" → Happy
- **Continuation Logic:** "more songs" retrieves same mood/language
- **Lazy Loading:** TensorFlow imports only when camera used (fast startup)

---

## 📝 Credits

**Data Source:** Spotify Web API  
**AI Model:** DeepFace (pre-trained facial recognition)  
**Design Inspiration:** Spotify official color palette

---

## 🎉 Enjoy Your Personalized Music Experience!

Match your mood with perfect songs - type it, select it, or just show your face! 🎶✨

---

**Version:** 2.0 with Camera Detection  
**Last Updated:** November 2025

---

**Docker Deployment**

- **Build image (PowerShell):**

```powershell
docker build -t moodify:latest .
```

- **Run container (PowerShell):**

```powershell
# Run detached, map port 5000
docker run -d -p 5000:5000 --name moodify_app --rm moodify:latest

# View logs
docker logs -f moodify_app

# Stop
docker stop moodify_app
```

- **Using Docker Compose (recommended for development):**

```powershell
# Build and start (attach logs)
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop and remove
docker-compose down
```

Notes:
- The Docker image uses `python:3.11-slim` and installs `opencv`, `deepface` and `tensorflow`. The image may be large; be patient during the first build.
- If you prefer to keep dataset files outside the image, add `data/` to `.dockerignore` and mount `- ./data:/app/data` in `docker-compose.yml`.
- For GPU acceleration with TensorFlow, build a GPU-enabled image on a machine with NVIDIA Docker support (this Dockerfile is CPU-only).

If you'd like, I can:
- Add a multi-stage production Dockerfile (smaller runtime image)
- Create a separate `Dockerfile.cpu` and `Dockerfile.gpu` with guidance for GPU setup
- Prepare a small PowerShell script for common docker commands
