import requests
import pandas as pd

# API URL and Token
API_URL = "https://api.socialverseapp.com/posts/summary/get?page=1&page_size=1000"
FLIC_TOKEN = "flic_6e2d8d25dc29a4ddd382c2383a903cf4a688d1a117f6eb43b35a1e7fadbb84b8"

# Function to fetch data from API
def fetch_data():
    try:
        headers = {"Flic-Token": FLIC_TOKEN}
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data['posts'])  # Assuming 'posts' is the key in API response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return pd.DataFrame()

# Function to preprocess data
def preprocess_data(data):
    # Print the columns to verify their names
    print("Available columns in the dataset:")
    print(data.columns)

    # Adjust these column names based on the actual dataset structure
    required_columns = ['createdAt', 'title', 'category']  # Default expected columns

    # Handle column name differences (e.g., API might return different keys)
    column_mapping = {
        'createdAt': 'creation_date',  # Example adjustment
        'title': 'post_title',         # Example adjustment
        'category': 'post_category'   # Example adjustment
    }

    # Map column names based on availability
    for key, value in column_mapping.items():
        if value in data.columns:
            required_columns[required_columns.index(key)] = value

    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        print(f"Missing columns: {missing_columns}")
        return None

    processed_data = data[required_columns]
    # Rename columns to a standardized format
    processed_data.columns = ['createdAt', 'title', 'category']
    processed_data['createdAt'] = pd.to_datetime(processed_data['createdAt'])  # Convert to datetime
    return processed_data

# Main function
def main():
    print("Fetching data from API...")
    raw_data = fetch_data()

    if raw_data.empty:
        print("No data fetched from the API. Exiting.")
        return

    print("Raw data fetched. Preprocessing...")
    processed_data = preprocess_data(raw_data)

    if processed_data is None:
        print("Data preprocessing failed due to missing or mismatched columns.")
        return

    print("Preprocessed data:")
    print(processed_data.head())

    # Save the processed data to a CSV file
    processed_data.to_csv("processed_data.csv", index=False)
    print("Data saved to 'processed_data.csv'.")

if __name__ == "__main__":
    main()
