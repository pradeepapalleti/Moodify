from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Data path (assumes dataset is included in repo under data/)
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'spotify_mood_tracks_multilang.csv')


class MoodBasedRecommender:
    def __init__(self, tracks_df):
        self.tracks_df = tracks_df

    def recommend_by_mood_and_language(self, mood, language=None, n_recommendations=10):
        mood_tracks = self.tracks_df[self.tracks_df['mood'] == mood]
        if language and language != 'All':
            mood_tracks = mood_tracks[mood_tracks['language'] == language]
        if len(mood_tracks) == 0:
            return None
        top_tracks = mood_tracks.nlargest(n_recommendations, 'popularity')
        return top_tracks[['id', 'name', 'artist', 'album', 'popularity', 'language']].to_dict('records')

    def get_available_moods(self):
        return self.tracks_df['mood'].value_counts().to_dict()

    def get_available_languages(self):
        return self.tracks_df['language'].value_counts().to_dict()

    def get_stats(self):
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
    print('✓ Dataset loaded successfully (backend)')
except Exception as e:
    print(f'Error loading dataset: {e}')
    recommender = None


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


@app.route('/recommend', methods=['POST'])
def recommend():
    if not recommender:
        return jsonify({'error': 'Recommender not initialized'}), 500
    data = request.get_json() or {}
    mood = data.get('mood')
    language = data.get('language', 'All')
    num_songs = int(data.get('num_songs', 10))
    if not mood:
        return jsonify({'error': 'No mood provided'}), 400
    recommendations = recommender.recommend_by_mood_and_language(mood, language, num_songs)
    if recommendations is None:
        return jsonify({'error': f'No tracks found for mood: {mood} and language: {language}'}), 404
    return jsonify({'mood': mood, 'language': language, 'count': len(recommendations), 'recommendations': recommendations})


@app.route('/stats')
def stats():
    if not recommender:
        return jsonify({'error': 'Recommender not initialized'}), 500
    return jsonify(recommender.get_stats())


@app.route('/chat', methods=['POST'])
def chat():
    if not recommender:
        return jsonify({'error': 'Recommender not initialized'}), 500
    data = request.get_json() or {}
    # Frontend TF.js will send detected mood instead of image; accept either 'message' or 'detected_mood'
    detected_mood = data.get('detected_mood')
    user_message = data.get('message', '')
    language = data.get('language', 'All')
    num_songs = int(data.get('num_songs', 5))

    # If message provided but no detected_mood, do a simple keyword fallback
    if not detected_mood and user_message:
        # naive keyword mapping
        lm = user_message.lower()
        if 'sad' in lm or 'down' in lm:
            detected_mood = 'Sad'
        elif 'happy' in lm or 'joy' in lm or 'excited' in lm:
            detected_mood = 'Happy'
        elif 'energetic' in lm or 'pump' in lm or 'gym' in lm:
            detected_mood = 'Energetic'
        elif 'calm' in lm or 'relax' in lm or 'peace' in lm:
            detected_mood = 'Calm'
        else:
            detected_mood = 'Happy'

    recommendations = recommender.recommend_by_mood_and_language(detected_mood, language, num_songs)
    if recommendations is None:
        recommendations = recommender.recommend_by_mood_and_language(detected_mood, 'All', num_songs)
        language = 'All'

    return jsonify({
        'user_message': user_message,
        'detected_mood': detected_mood,
        'language_used': language,
        'count': len(recommendations),
        'recommendations': recommendations,
        'bot_response': f"Here are {len(recommendations)} {detected_mood} songs",
        'track_ids': [r['id'] for r in recommender.get_available_moods() and []]
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('1', 'true', 'yes')
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
