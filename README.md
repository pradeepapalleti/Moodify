# 🎵 Moodify — AI-Powered Mood-Based Music Recommender

An intelligent music recommendation system that detects your mood through chat, camera, or manual selection and recommends personalized songs across multiple languages.

---

## ✨ Key Features

### 🎭 **Mood Selector Mode**
- Pick from 8 moods: Happy, Sad, Energetic, Calm, Romantic, Motivated, Party, Focus
- Select from 6 languages: English, Hindi, Telugu, Tamil, Malayalam, Kannada
- 1,156+ curated Spotify tracks with real-time playback
- Adjustable recommendation count (1-50 songs)

### 💬 **AI Chat Mode**
- Natural language mood detection ("I'm feeling happy", "I'm sad")
- Multi-language support with auto-detection ("Give me Hindi sad songs")
- Conversation memory (context-aware, remembers previous moods)
- Smart continuations ("more songs" intelligently repeats previous context)
- Session-based conversation history

### 📷 **Camera Mood Detection** (NEW)
- Real-time facial expression analysis
- AI-powered emotion recognition (DeepFace + OpenCV)
- Instant mood mapping: happy, sad, angry, surprise → music recommendations
- Privacy-first: images processed locally, never stored or transmitted
- Fast processing with CLAHE image enhancement

### 🎨 **Spotify-Inspired UI**
- Dark/Light theme toggle with localStorage persistence
- Spotify green (#1DB954) color scheme
- Smooth animations and responsive design
- Fully mobile-friendly interface
- Real-time stats dashboard

---

## 📋 Project Structure

```
Moodify/
├── app.py                                    # Flask backend + all endpoints
├── templates/
│   ├── index.html                           # Mood selector interface
│   └── chat.html                            # Chat + camera detection UI
├── data/
│   ├── spotify_mood_tracks.csv              # Dataset (English)
│   └── spotify_mood_tracks_multilang.csv    # Dataset (Multi-language)
├── notebooks/
│   └── 1_data_collection.ipynb              # Data exploration & processing
├── requirements.txt                         # Python dependencies
├── Dockerfile                               # Docker configuration
└── docker-compose.yml                       # Docker Compose setup
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Webcam (for camera mode)
- Modern web browser

### Installation & Run

```bash
# 1. Clone repository
git clone https://github.com/pradeepapalleti/Moodify.git
cd Moodify

# 2. Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py

# 5. Open browser and visit
http://localhost:5000
```

### Docker Option
```bash
# Build and run with Docker Compose
docker-compose up --build

# Or with Docker directly
docker build -t moodify:latest .
docker run -p 5000:5000 moodify:latest
```

## 💻 How to Use

### Option 1: 🎭 Mood Selector
1. Go to **http://localhost:5000**
2. Select a **language** (All Languages or specific language)
3. Pick a **mood** (Happy, Sad, Energetic, etc.)
4. Set **number of recommendations** (1-50)
5. Click **"Get Recommendations"**
6. Click any **"▶️ Play"** button to open track in Spotify

### Option 2: 💬 Chat Mode
1. Go to **http://localhost:5000/chat-page**
2. Type how you're feeling (examples: "I'm happy", "I want sad Hindi songs", "Give me energetic party music")
3. The AI detects your mood and language automatically
4. Get recommendations instantly
5. Continue the conversation: "more songs", "different mood", etc.
6. Conversation memory remembers your previous context

### Option 3: 📷 Camera Mode
1. Go to **http://localhost:5000/chat-page**
2. Click **"📷 Camera Mode"** button
3. Allow camera access
4. Make a facial expression (happy, sad, angry, etc.)
5. Click **"📸 Capture & Analyze"**
6. AI detects your emotion and recommends songs
7. Click **"▶️ Play"** to open songs in Spotify

**Emotion Mapping:**
- 😊 Happy/Surprised → Happy music
- 😢 Sad → Sad/Romantic songs
- 😠 Angry/Disgusted → Energetic tracks
- 😐 Neutral/Fear → Calm/Focus music

## 🛠️ Tech Stack

| Component | Technology | Version |
|-----------|------------|---------|
| **Backend** | Flask | 3.0.3 |
| **Data Processing** | Pandas, NumPy | 2.3.3, 2.2.6 |
| **Computer Vision** | OpenCV | 4.12.0 |
| **Emotion Detection** | DeepFace | 0.0.95 |
| **Deep Learning** | TensorFlow, tf-keras | 2.20.0 |
| **Frontend** | HTML5, CSS3, JavaScript | ES6+ |
| **Camera** | WebRTC API | Browser Native |
| **Containerization** | Docker, Docker Compose | Latest |
| **API** | Spotify Web Search | REST |
| **Database** | CSV (Pandas) | - |

## 📊 Dataset Overview

- **Total Tracks:** 1,156+ unique songs
- **Languages:** 
  - English (246)
  - Hindi (205)
  - Tamil (199)
  - Telugu (197)
  - Kannada (159)
  - Malayalam (150)
- **Moods:** Happy (164), Energetic (151), Sad (150), Focus (146), Calm (145), Romantic (145), Motivated (133), Party (122)
- **Track Features:** Track ID, Name, Artist, Album, Duration, Popularity Score, Language, Mood
- **Source:** Spotify Web API + Curated Selection
- **Files:** 
  - `spotify_mood_tracks.csv` (English only)
  - `spotify_mood_tracks_multilang.csv` (Multi-language)

## 🔗 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Mood selector interface |
| `/chat-page` | GET | Chat + camera detection interface |
| `/recommend` | POST | Get recommendations by mood & language |
| `/chat` | POST | Natural language chat with mood detection |
| `/detect-emotion` | POST | Facial emotion detection from camera image |
| `/stats` | GET | Dataset statistics (moods, languages, artists) |

### Example Requests

**Get Recommendations:**
```bash
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"mood": "Happy", "language": "English", "num_songs": 10}'
```

**Chat Mode:**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I am feeling happy", "language": null, "num_songs": 5}'
```

**Get Stats:**
```bash
curl http://localhost:5000/stats
```

## 🔒 Privacy & Security

- ✅ **Local Processing:** All facial analysis happens in your browser/server (no cloud)
- ✅ **No Data Storage:** Camera images are processed instantly and never saved
- ✅ **No External Transmission:** Images never leave your device
- ✅ **Session Privacy:** Conversation history is session-based, not persisted to disk
- ✅ **Open Source:** Full code transparency for security audit

## 🎨 UI/UX Features

- **Color Scheme:** Spotify green (#1DB954), Dark gray (#121212), Light accents (#b3b3b3)
- **Theme Toggle:** 🌙 Dark / ☀️ Light modes with localStorage persistence
- **Animations:** Smooth fade-ins, hover effects, spinning loaders
- **Responsive Layout:** CSS Grid & Flexbox for mobile/tablet/desktop
- **Interactive Elements:**
  - Mood selection buttons with active states
  - Language selector with badge counts
  - Real-time stats dashboard
  - Song cards with artist/album info
  - Play buttons linking directly to Spotify
  - Full album search links
- **Accessibility:** Semantic HTML, proper contrast ratios, keyboard navigation

## 🔧 Advanced Features

- **Conversation Memory:** Stores up to 10 recent exchanges per session
- **Language Detection:** Regex patterns to detect language from user text ("Hindi songs", "Tamil music")
- **Mood Synonyms:** Maps colloquial mood expressions to mood categories
- **Smart Continuations:** "more songs" automatically repeats the previous mood/language
- **Image Enhancement:** CLAHE (Contrast Limited Adaptive Histogram Equalization) for better face detection in poor lighting
- **Multiple Face Detectors:** Falls back through RetinaFace → MTCNN → OpenCV → SSD if one fails
- **Lazy Loading:** TensorFlow and DeepFace only imported when camera is used (faster startup)
- **Confidence Thresholds:** Emotion detection only accepted if confidence > 30%

## 📝 Credits & References

- **Data:** Spotify Web API for track metadata
- **Facial Recognition:** DeepFace (Facebook Research)
- **Computer Vision:** OpenCV library
- **Deep Learning Framework:** TensorFlow & Keras
- **Backend Framework:** Flask
- **Design Inspiration:** Spotify official brand guidelines
- **Dataset Curation:** Manual selection and validation

## 📄 License

This project is open-source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs and issues
- Suggest new features
- Improve documentation
- Optimize performance
- Add more languages/moods

## 📧 Contact & Support

For issues, feature requests, or questions:
- GitHub Issues: [pradeepapalleti/Moodify](https://github.com/pradeepapalleti/Moodify/issues)
- Email: pradeepapalleti@example.com

---

## 🎉 Enjoy Moodify!

Match your mood with perfect songs — **type it, select it, or just show your face!** 🎶✨

**Current Version:** 2.0 (with Camera Detection)  
**Last Updated:** December 2025  
**Status:** Active Development
