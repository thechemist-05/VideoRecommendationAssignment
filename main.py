import requests
import pandas as pd

# Fetch data from API
def fetch_data(api_url):
    print("Fetching data from API...")
    headers = {"Flic-Token": "flic_6e2d8d25dc29a4ddd382c2383a903cf4a688d1a117f6eb43b35a1e7fadbb84b8"}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        print("Data fetched successfully.")
        return pd.DataFrame(response.json())  # Convert JSON response to DataFrame
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

# Preprocess the data
def preprocess_data(data):
    print("Raw data fetched. Preprocessing...")
    print("Available columns in the dataset:")
    print(data.columns)

    # Map column names to standardized versions
    column_mapping = {
        'created_at': 'createdAt',  # Map created_at to createdAt
        'title': 'title',
        'category': 'category'
    }

    # Check for required columns
    required_columns = ['createdAt', 'title', 'category']
    missing_columns = [key for key in required_columns if key not in column_mapping.values()]
    
    if any(col not in data.columns for col in column_mapping.keys()):
        print(f"Missing columns: {missing_columns}")
        return None

    # Rename and select required columns
    data = data.rename(columns=column_mapping)
    data = data[['createdAt', 'title', 'category']]  # Select only required columns
    data['createdAt'] = pd.to_datetime(data['createdAt'])  # Convert to datetime
    print("Data preprocessing completed successfully.")
    return data

# Save processed data to CSV
def save_to_csv(data, filename='processed_data.csv'):
    print(f"Saving processed data to {filename}...")
    data.to_csv(filename, index=False)
    print(f"Data saved to {filename} successfully.")

# Main function
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

if __name__ == "__main__":
    main()
