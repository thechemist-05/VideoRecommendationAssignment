import requests
import pandas as pd

# Function to fetch data from the API
def fetch_data(api_url):
    print("Fetching data from API...")
    headers = {"Flic-Token": "flic_6e2d8d25dc29a4ddd382c2383a903cf4a688d1a117f6eb43b35a1e7fadbb84b8"}
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx, 5xx)
        print("Data fetched successfully.")
        return pd.DataFrame(response.json())  # Convert JSON response to DataFrame
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# Function to preprocess the data
def preprocess_data(data):
    print("Raw data fetched. Preprocessing...")
    print("Available columns in the dataset:")
    print(data.columns)

    # List of required columns, checking if they exist
    required_columns = ['createdAt', 'title', 'category']
    missing_columns = [col for col in required_columns if col not in data.columns]
    
    if missing_columns:
        print(f"Missing columns: {missing_columns}")
        return None
    
    # Check for variations in 'createdAt' column name (e.g., 'created_at')
    if 'createdAt' not in data.columns:
        if 'created_at' in data.columns:
            data = data.rename(columns={'created_at': 'createdAt'})
        else:
            print("Missing 'createdAt' column.")
            return None

    # Handle datetime parsing with error handling
    try:
        data['createdAt'] = pd.to_datetime(data['createdAt'], errors='coerce')  # 'coerce' turns invalid dates into NaT
        data = data.dropna(subset=['createdAt'])  # Drop rows where 'createdAt' is NaT (invalid)
    except Exception as e:
        print(f"Error parsing 'createdAt' column: {e}")
        return None
    
    # Select only the necessary columns and drop rows with missing data in them
    data = data[['createdAt', 'title', 'category']]

    print("Data preprocessing completed successfully.")
    return data

# Function to save the processed data to CSV
def save_to_csv(data, filename='processed_data.csv'):
    print(f"Saving processed data to {filename}...")
    try:
        data.to_csv(filename, index=False)
        print(f"Data saved to {filename} successfully.")
    except Exception as e:
        print(f"Error saving data: {e}")

# Main function to orchestrate the workflow
def main():
    api_url = "https://api.socialverseapp.com/posts/summary/get?page=1&page_size=1000"
    raw_data = fetch_data(api_url)
    
    if raw_data is not None and not raw_data.empty:
        processed_data = preprocess_data(raw_data)
        
        if processed_data is not None:
            save_to_csv(processed_data)
        else:
            print("Data preprocessing failed. Please check the input data.")
    else:
        print("No data fetched. Please check the API or network connection.")

# Run the main function
if __name__ == "__main__":
    main()
