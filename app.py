from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Simulate preloaded data for simplicity (use actual fetch_data and preprocess_data in production)
def load_sample_data():
    return pd.DataFrame({
        "id": [1, 2, 3, 4],
        "title": ["Motivational Speech", "Success Story", "Fitness Tips", "Daily Hacks"],
        "category": ["Motivation", "Inspiration", "Health", "Life"],
        "category_id": [1, 1, 2, 3]
    })

all_videos = load_sample_data()

def recommend_videos(user_liked, videos, top_n=3):
    """
    Recommends videos based on similarity to the user's liked videos.
    """
    videos['content'] = videos['title'] + " " + videos['category']
    user_liked['content'] = user_liked['title'] + " " + user_liked['category']

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(videos['content'])
    similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)

    liked_indices = user_liked.index.tolist()
    scores = similarity[liked_indices].sum(axis=0)

    videos['similarity'] = scores
    recommendations = videos[~videos.index.isin(liked_indices)].sort_values('similarity', ascending=False)
    return recommendations.head(top_n)[['id', 'title', 'category']].to_dict(orient='records')

@app.route("/feed", methods=["GET"])
def feed():
    username = request.args.get("username")
    category_id = request.args.get("category_id")
    mood = request.args.get("mood")

    user_liked_videos = all_videos.sample(2)  # Simulated user likes for demo

    # Filter by category if provided
    if category_id:
        filtered_videos = all_videos[all_videos['category_id'] == int(category_id)]
    else:
        filtered_videos = all_videos

    recommendations = recommend_videos(user_liked_videos, filtered_videos)

    return jsonify({
        "username": username,
        "category_id": category_id,
        "mood": mood,
        "recommendations": recommendations
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
