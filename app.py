from flask import Flask, render_template, request, jsonify, session
import pandas as pd
import os
import re
from datetime import datetime
import base64

app = Flask(__name__)
app.secret_key = 'your-secret-key-for-sessions-12345'  # Required for session management

# Load the dataset
DATA_PATH = 'data/spotify_mood_tracks_multilang.csv'

# Store conversation history (in production, use Redis or database)
conversation_history = {}

class MoodBasedRecommender:
    def __init__(self, tracks_df):
        self.tracks_df = tracks_df
        
        # Language detection patterns
        self.language_patterns = {
            'Hindi': [
                r'\b(hai|hain|kya|kaise|mujhe|mere|tera|tere|bahut|accha|bura|khush|udaas|dukhi|' +
                r'pyaar|mohabbat|dost|yaar|bhai|didi|maa|papa|ghar|kaam|padhai|gaana|' +
                r'सुनना|गाना|खुश|उदास|दुखी|प्यार|मोहब्बत|दोस्त)\b'
            ],
            'Telugu': [
                r'[\u0C00-\u0C7F]+',  # Telugu script
                r'\b(nenu|naaku|meeku|ela|enti|bagundi|ledhu|kavali|anthe)\b'
            ],
            'Tamil': [
                r'[\u0B80-\u0BFF]+',  # Tamil script
                r'\b(naan|enakku|unakku|epdi|enna|nalla|illa|venum|sari)\b'
            ],
            'Malayalam': [
                r'[\u0D00-\u0D7F]+',  # Malayalam script
                r'\b(njan|enikku|ningalkku|engane|enthu|nannaayi|illa|venam|sheriyaanu)\b'
            ],
            'Kannada': [
                r'[\u0C80-\u0CFF]+',  # Kannada script
                r'\b(naanu|nanage|nimage|hege|yenu|chennagide|illa|beku|sari)\b'
            ]
        }
        
        # Mood detection keywords (English + Hinglish)
        self.mood_keywords = {
            'Happy': [
                'happy', 'joy', 'excited', 'great', 'awesome', 'wonderful', 'amazing', 'fantastic',
                'khush', 'mast', 'mazaa', 'maja', 'party', 'celebrate', 'celebration', 'fun',
                'cheerful', 'delighted', 'pleased', 'glad', 'joyful', 'ecstatic', 'blessed'
            ],
            'Sad': [
                'sad', 'unhappy', 'depressed', 'down', 'upset', 'hurt', 'pain', 'crying',
                'udaas', 'dukhi', 'dard', 'rona', 'breakup', 'heartbreak', 'lonely', 'alone',
                'miss', 'missing', 'cry', 'tears', 'lost', 'broken', 'disappointed'
            ],
            'Energetic': [
                'energy', 'energetic', 'pump', 'workout', 'gym', 'exercise', 'run', 'active',
                'power', 'strong', 'intense', 'adrenaline', 'beast mode', 'fired up',
                'josh', 'full energy', 'workout karna hai', 'gym jaana', 'dance', 'jumping'
            ],
            'Calm': [
                'calm', 'peace', 'peaceful', 'relax', 'relaxed', 'chill', 'meditation', 'quiet',
                'shanti', 'aram', 'rest', 'sleep', 'soothing', 'gentle', 'soft', 'tranquil',
                'serene', 'peaceful', 'stress free', 'tension free', 'breathe'
            ],
            'Romantic': [
                'love', 'romance', 'romantic', 'crush', 'date', 'valentine', 'heart', 'lover',
                'pyaar', 'mohabbat', 'ishq', 'dil', 'girlfriend', 'boyfriend', 'propose',
                'kiss', 'hug', 'baby', 'sweetheart', 'darling', 'beautiful', 'handsome'
            ],
            'Motivated': [
                'motivated', 'motivation', 'inspire', 'success', 'goal', 'achieve', 'hustle',
                'grind', 'focus', 'determination', 'dream', 'ambition', 'winner', 'champion',
                'improve', 'better', 'growth', 'progress', 'never give up', 'keep going'
            ],
            'Party': [
                'party', 'club', 'dance', 'dj', 'drinks', 'night out', 'clubbing', 'vibes',
                'lit', 'turn up', 'bass', 'edm', 'beat', 'drop', 'festival', 'rave',
                'friends', 'gang', 'wild', 'crazy night', 'dance floor', 'nightlife'
            ],
            'Focus': [
                'study', 'work', 'focus', 'concentrate', 'concentration', 'exam', 'office',
                'productive', 'productivity', 'reading', 'coding', 'assignment', 'project',
                'deadline', 'padhai', 'kaam', 'working', 'studying', 'learn', 'learning'
            ]
        }
    
    def detect_language_preference_from_text(self, text):
        """Detect language preference from English conversation (e.g., 'hindi songs', 'tamil music')"""
        text_lower = text.lower()
        
        # Check for explicit language mentions in English
        language_mentions = {
            'Hindi': ['hindi', 'bollywood', 'hindustani'],
            'Telugu': ['telugu', 'tollywood'],
            'Tamil': ['tamil', 'kollywood'],
            'Malayalam': ['malayalam', 'mollywood'],
            'Kannada': ['kannada', 'sandalwood'],
            'English': ['english', 'western', 'international']
        }
        
        for language, keywords in language_mentions.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return language
        
        # If no specific language mentioned, return None (will use All)
        return None
    
    def detect_mood_from_text(self, text, conversation_context=None):
        """Detect mood from user message using keyword matching with context"""
        text_lower = text.lower()
        
        # If there's conversation context, consider previous mood
        previous_mood = None
        if conversation_context and len(conversation_context) > 0:
            last_exchange = conversation_context[-1]
            previous_mood = last_exchange.get('detected_mood')
        
        mood_scores = {}
        
        # Count keyword matches for each mood
        for mood, keywords in self.mood_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
            
            # Boost score if it's a continuation of previous mood
            if previous_mood == mood and score == 0:
                # Check for continuation phrases
                continuation_phrases = ['yes', 'yeah', 'yep', 'ha', 'haan', 'more', 'another', 
                                       'similar', 'like that', 'same', 'continue', 'and', 'also']
                for phrase in continuation_phrases:
                    if phrase in text_lower:
                        score += 2  # Boost previous mood
                        break
        
            mood_scores[mood] = score
        
        # Get mood with highest score
        if max(mood_scores.values()) > 0:
            detected_mood = max(mood_scores, key=mood_scores.get)
            return detected_mood
        
        # If no keywords matched, use previous mood if available
        if previous_mood:
            return previous_mood
        
        # Default to Happy if no keywords matched
        return 'Happy'
    
    def recommend_by_mood_and_language(self, mood, language=None, n_recommendations=10):
        """Get top recommendations for a specific mood and optional language"""
        # Filter by mood
        mood_tracks = self.tracks_df[self.tracks_df['mood'] == mood]
        
        # Filter by language if specified
        if language and language != 'All':
            mood_tracks = mood_tracks[mood_tracks['language'] == language]
        
        if len(mood_tracks) == 0:
            return None
        
        # Sort by popularity and get top N
        top_tracks = mood_tracks.nlargest(n_recommendations, 'popularity')
        return top_tracks[['id', 'name', 'artist', 'album', 'popularity', 'language']].to_dict('records')
    
    def get_all_tracks_for_mood_language(self, mood, language=None, limit=50):
        """Get all track IDs for a mood-language combination (for creating playlists)"""
        # Filter by mood
        mood_tracks = self.tracks_df[self.tracks_df['mood'] == mood]
        
        # Filter by language if specified
        if language and language != 'All':
            mood_tracks = mood_tracks[mood_tracks['language'] == language]
        
        if len(mood_tracks) == 0:
            return []
        
        # Get top tracks by popularity
        top_tracks = mood_tracks.nlargest(limit, 'popularity')
        return top_tracks['id'].tolist()
    
    def get_available_moods(self):
        """Get list of available moods with track counts"""
        mood_counts = self.tracks_df['mood'].value_counts().to_dict()
        return mood_counts
    
    def get_available_languages(self):
        """Get list of available languages with track counts"""
        language_counts = self.tracks_df['language'].value_counts().to_dict()
        return language_counts
    
    def get_stats(self):
        """Get dataset statistics"""
        return {
            'total_tracks': len(self.tracks_df),
            'unique_artists': self.tracks_df['artist'].nunique(),
            'unique_albums': self.tracks_df['album'].nunique(),
            'avg_popularity': round(self.tracks_df['popularity'].mean(), 2),
            'languages': len(self.tracks_df['language'].unique()),
            'moods': len(self.tracks_df['mood'].unique())
        }

# Initialize recommender
try:
    tracks_df = pd.read_csv(DATA_PATH)
    recommender = MoodBasedRecommender(tracks_df)
    print("✓ Dataset loaded successfully!")
except Exception as e:
    print(f"Error loading dataset: {e}")
    recommender = None

@app.route('/')
def home():
    """Home page"""
    if recommender:
        moods = recommender.get_available_moods()
        languages = recommender.get_available_languages()
        stats = recommender.get_stats()
        return render_template('index.html', moods=moods, languages=languages, stats=stats)
    else:
        return "Error: Dataset not found. Please run the notebook first to create the dataset."

@app.route('/chat-page')
def chat_page():
    """Chat interface page"""
    if recommender:
        languages = recommender.get_available_languages()
        return render_template('chat.html', languages=languages)
    else:
        return "Error: Dataset not found. Please run the notebook first to create the dataset."

@app.route('/recommend', methods=['POST'])
def recommend():
    """Get recommendations based on selected mood and language"""
    if not recommender:
        return jsonify({'error': 'Recommender not initialized'}), 500
    
    data = request.get_json()
    mood = data.get('mood')
    language = data.get('language', 'All')
    num_songs = int(data.get('num_songs', 10))
    
    recommendations = recommender.recommend_by_mood_and_language(mood, language, num_songs)
    
    if recommendations is None:
        return jsonify({'error': f'No tracks found for mood: {mood} and language: {language}'}), 404
    
    return jsonify({
        'mood': mood,
        'language': language,
        'count': len(recommendations),
        'recommendations': recommendations
    })

@app.route('/stats')
def stats():
    """Get dataset statistics"""
    if not recommender:
        return jsonify({'error': 'Recommender not initialized'}), 500
    
    return jsonify(recommender.get_stats())

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint - detect mood from user message and recommend songs"""
    if not recommender:
        return jsonify({'error': 'Recommender not initialized'}), 500
    
    data = request.get_json()
    user_message = data.get('message', '')
    language_preference = data.get('language', None)  # Can be None for auto-detect
    num_songs = int(data.get('num_songs', 5))
    session_id = data.get('session_id', 'default')  # Session ID for conversation tracking
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Get or create conversation history
    if session_id not in conversation_history:
        conversation_history[session_id] = []
    
    context = conversation_history[session_id]
    
    # Detect language preference from the conversation
    detected_language_pref = recommender.detect_language_preference_from_text(user_message)
    
    # Determine which language to use
    language_to_use = None
    language_source = None
    
    if language_preference and language_preference != 'Auto':
        # User has set a preference in the selector
        language_to_use = language_preference
        language_source = 'preference'
    elif detected_language_pref:
        # User mentioned a language in their message
        language_to_use = detected_language_pref
        language_source = 'detected_from_message'
    elif context and len(context) > 0:
        # Check if previous conversation had a language preference
        last_language = context[-1].get('language_used')
        if last_language and last_language != 'All':
            language_to_use = last_language
            language_source = 'continued_from_context'
    else:
        # Default to All (mixed languages)
        language_to_use = 'All'
        language_source = 'default_all'
    
    # Detect mood from message with conversation context
    detected_mood = recommender.detect_mood_from_text(user_message, context)
    
    # Get recommendations
    recommendations = recommender.recommend_by_mood_and_language(detected_mood, language_to_use, num_songs)
    
    if recommendations is None:
        # Fallback to 'All' languages if specific language has no tracks
        recommendations = recommender.recommend_by_mood_and_language(detected_mood, 'All', num_songs)
        language_to_use = 'All'
        language_source = 'fallback'
    
    # Get all track IDs for playlist creation
    all_track_ids = recommender.get_all_tracks_for_mood_language(detected_mood, language_to_use, limit=50)
    
    # Create a friendly response with context awareness
    is_continuation = False
    if context and len(context) > 0:
        last_mood = context[-1].get('detected_mood')
        if last_mood == detected_mood:
            is_continuation = True
    
    if is_continuation:
        response_messages = {
            'Happy': '😊 More happy vibes coming your way!',
            'Sad': '😢 Here are some more comforting songs...',
            'Energetic': '⚡ Here are more high-energy tracks!',
            'Calm': '🧘 More peaceful songs to keep you relaxed...',
            'Romantic': '💕 More love songs for you!',
            'Motivated': '🔥 Keep that motivation going!',
            'Party': '🎉 More party bangers!',
            'Focus': '📚 More focus music to help you concentrate!'
        }
    else:
        response_messages = {
            'Happy': '😊 Yay! Looks like you\'re in a great mood! Here are some happy songs for you:',
            'Sad': '😢 I sense you\'re feeling down. Here are some songs that might help:',
            'Energetic': '⚡ Feeling pumped up! Here are some energetic tracks to match your vibe:',
            'Calm': '🧘 You seem to want some peace. Here are calming songs for you:',
            'Romantic': '💕 Love is in the air! Here are some romantic songs:',
            'Motivated': '🔥 Ready to conquer the world! Here are some motivational tracks:',
            'Party': '🎉 Party time! Here are some bangers for you:',
            'Focus': '📚 Time to focus! Here are some concentration-friendly tracks:'
        }
    
    bot_response = response_messages.get(detected_mood, 'Here are some songs for you:')
    
    # Add language info to response
    if language_source == 'detected_from_message':
        bot_response += f' (I see you want {language_to_use} songs!)'
    elif language_source == 'default_all':
        bot_response += ' (Showing songs from all languages!)'
    elif language_source == 'continued_from_context':
        bot_response += f' (Continuing with {language_to_use} songs)'
    
    # Store this exchange in conversation history
    conversation_history[session_id].append({
        'user_message': user_message,
        'detected_mood': detected_mood,
        'detected_language_pref': detected_language_pref,
        'language_used': language_to_use,
        'language_source': language_source,
        'timestamp': datetime.now().isoformat()
    })
    
    # Keep only last 10 exchanges to avoid memory issues
    if len(conversation_history[session_id]) > 10:
        conversation_history[session_id] = conversation_history[session_id][-10:]
    
    return jsonify({
        'user_message': user_message,
        'detected_mood': detected_mood,
        'detected_language': detected_language_pref,
        'language_used': language_to_use,
        'language_source': language_source,
        'bot_response': bot_response,
        'count': len(recommendations),
        'recommendations': recommendations,
        'is_continuation': is_continuation,
        'track_ids': all_track_ids  # For creating Spotify playlist/album link
    })

@app.route('/detect-emotion', methods=['POST'])
def detect_emotion():
    """Detect emotion from camera image using facial expression analysis"""
    try:
        # Lazy import to avoid slow startup
        import cv2
        import numpy as np
        from deepface import DeepFace
        
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'error': 'No image provided'}), 400
        
        # Remove the data URL prefix
        if 'base64,' in image_data:
            image_data = image_data.split('base64,')[1]
        
        # Decode base64 image
        img_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({'error': 'Invalid image data'}), 400
        
        # Resize to smaller frame for faster processing (max 480px width for speed)
        height, width = img.shape[:2]
        max_width = 480  # Smaller frame = faster processing
        if width > max_width:
            scale = max_width / width
            new_width = max_width
            new_height = int(height * scale)
            img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        # Enhance image for better face detection
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        l = clahe.apply(l)
        img = cv2.merge([l, a, b])
        img = cv2.cvtColor(img, cv2.COLOR_LAB2BGR)
        
        # Increase brightness and contrast if needed
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        if brightness < 120:
            # Increase brightness for dark images
            img = cv2.convertScaleAbs(img, alpha=1.3, beta=40)
        
        # Try multiple detector backends for better reliability
        detectors = ['retinaface', 'mtcnn', 'opencv', 'ssd']
        result = None
        last_error = None
        
        for detector in detectors:
            try:
                print(f"Trying detector: {detector}")
                result = DeepFace.analyze(
                    img, 
                    actions=['emotion'], 
                    enforce_detection=False,  # Don't require face detection
                    detector_backend=detector,
                    silent=True,
                    align=True  # Align faces for better accuracy
                )
                print(f"Success with {detector} detector!")
                break  # Success, exit loop
            except Exception as e:
                last_error = str(e)
                print(f"{detector} detector failed: {last_error}")
                continue
        
        # If all detectors failed, return error
        if result is None:
            print(f"All detectors failed. Last error: {last_error}")
            return jsonify({
                'error': 'Could not detect face in image',
                'details': 'Please ensure your face is clearly visible, well-lit, and facing the camera directly.',
                'debug': last_error
            }), 400
        
        # Handle both single result and list of results
        if isinstance(result, list):
            if len(result) == 0:
                return jsonify({
                    'error': 'No face detected in image',
                    'details': 'Please ensure your face is clearly visible and try again.'
                }), 400
            result = result[0]
        
        emotions = result.get('emotion', {})
        dominant_emotion = result.get('dominant_emotion', 'neutral')
        
        # Convert all NumPy types to Python native types (fix JSON serialization)
        emotions_clean = {}
        for key, value in emotions.items():
            # Convert numpy.float32/float64 to Python float
            if hasattr(value, 'item'):
                emotions_clean[key] = float(value.item())
            else:
                emotions_clean[key] = float(value)
        
        # Map DeepFace emotions to our mood categories
        emotion_to_mood = {
            'happy': 'Happy',
            'sad': 'Sad',
            'angry': 'Energetic',
            'surprise': 'Happy',  # Changed from Excited to Happy
            'fear': 'Calm',
            'disgust': 'Focus',
            'neutral': 'Calm'
        }
        
        # Get the detected mood
        detected_mood = emotion_to_mood.get(dominant_emotion.lower(), 'Happy')
        
        # Get confidence score and convert to Python float
        confidence = emotions_clean.get(dominant_emotion, 0.0)
        
        # Apply confidence threshold for stability (only accept if confidence > 30%)
        if confidence < 30.0:
            # If confidence is low, use neutral/calm mood
            detected_mood = 'Calm'
            dominant_emotion = 'neutral'
        
        # IMAGE IS AUTOMATICALLY DELETED - Python variables are garbage collected
        # No need to manually delete, img and result will be cleared from memory
        
        return jsonify({
            'success': True,
            'detected_mood': str(detected_mood),  # Ensure string type
            'dominant_emotion': str(dominant_emotion),  # Ensure string type
            'confidence': round(float(confidence), 2),
            'all_emotions': {k: round(float(v), 2) for k, v in emotions_clean.items()},
            'message': f"Detected {dominant_emotion} expression! Suggesting {detected_mood} music."
        })
    
    except Exception as e:
        print(f"Error in emotion detection: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎵 Spotify Mood-Based Music Recommendation System")
    print("="*60)
    print("\nStarting Flask server...")
    print("Open your browser and go to: http://localhost:5000")
    print("\nPress CTRL+C to stop the server")
    print("="*60 + "\n")
    # Use PORT environment variable when provided (Render and other PaaS set this)
    port = int(os.environ.get('PORT', 5000))
    # Disable debug in production by default; allow override with FLASK_DEBUG
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('1', 'true', 'yes')
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
