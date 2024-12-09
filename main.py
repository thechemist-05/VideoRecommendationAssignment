import requests
import pandas as pd

# API URL and Authorization Token
API_URL = "https://api.socialverseapp.com/posts/view?page=1&page_size=10"
HEADERS = {
    "Flic-Token": "flic_6e2d8d25dc29a4ddd382c2383a903cf4a688d1a117f6eb43b35a1e7fadbb84b8"
}

# Function to fetch data from API
def fetch_data():
    response = requests.get(API_URL, headers=HEADERS)
    if response.status_code == 200:
        return response.json()  # Returns data as JSON
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Function to preprocess fetched data into a structured DataFrame
def preprocess_data(data):
    # Convert JSON data to DataFrame
    df = pd.DataFrame(data['posts'])  # Assuming 'posts' is the key containing post data

    # Select relevant columns (modify these based on your dataset structure)
    df = df[['id', 'title', 'category', 'createdAt']]

    # Handle missing values by replacing with 'Unknown'
    df.fillna('Unknown', inplace=True)

    return df

# Main execution
if __name__ == "__main__":
    # Fetch data
    raw_data = fetch_data()

    # Preprocess data if fetching was successful
    if raw_data:
        processed_data = preprocess_data(raw_data)
        print("\nProcessed Data:")
        print(processed_data)
    else:
        print("Failed to fetch data.")
        
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Recommendation Algorithm
def recommend_videos(user_liked_videos, all_videos, top_n=5):
    """
    Recommend videos based on content similarity.
    
    Args:
    - user_liked_videos (DataFrame): Videos the user interacted with.
    - all_videos (DataFrame): All available videos.
    - top_n (int): Number of recommendations to return.
    
    Returns:
    - recommendations (DataFrame): Top N recommended videos.
    """
    # Combine video titles and categories for content analysis
    all_videos['content'] = all_videos['title'] + " " + all_videos['category']
    user_liked_videos['content'] = user_liked_videos['title'] + " " + user_liked_videos['category']

    # TF-IDF Vectorization
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(all_videos['content'])

    # Compute similarity scores between user-liked videos and all videos
    similarity_scores = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Identify indices of videos liked by the user
    liked_indices = user_liked_videos.index.tolist()

    # Aggregate similarity scores for videos the user liked
    scores = similarity_scores[liked_indices].sum(axis=0)

    # Sort videos by score and exclude already-liked videos
    all_videos['similarity'] = scores
    recommendations = all_videos[~all_videos.index.isin(liked_indices)]
    recommendations = recommendations.sort_values('similarity', ascending=False).head(top_n)

    return recommendations[['id', 'title', 'category', 'similarity']]

# Example Execution
if __name__ == "__main__":
    raw_data = fetch_data()
    if raw_data:
        # Preprocess data
        all_videos = preprocess_data(raw_data)
        
        # Simulating user-liked videos (can be replaced with actual user data)
        user_liked_videos = all_videos.sample(2)  # Randomly select 2 videos as liked
        print("\nUser Liked Videos:")
        print(user_liked_videos)

        # Get recommendations
        recommendations = recommend_videos(user_liked_videos, all_videos)
        print("\nRecommended Videos:")
        print(recommendations)
