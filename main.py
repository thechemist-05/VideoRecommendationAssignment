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
