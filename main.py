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

    # Handle possible variations in column names
    possible_column_names = ['createdAt', 'created_at']

    # Check for the existence of the column 'createdAt' or 'created_at'
    found_column = None
    for col in possible_column_names:
        if col in data.columns:
            found_column = col
            break
    
    if not found_column:
        print(f"Missing columns: {possible_column_names}")
        return None
    
    # Rename column to 'createdAt' for consistency
    data = data.rename(columns={found_column: 'createdAt'})

    # Ensure required columns are present
    required_columns = ['createdAt', 'title', 'category']
    missing_columns = [col for col in required_columns if col not in data.columns]
    
    if missing_columns:
        print(f"Missing columns: {missing_columns}")
        return None

    # Select only required columns and ensure 'createdAt' is in datetime format
    data = data[['createdAt', 'title', 'category']]  
    data['createdAt'] = pd.to_datetime(data['createdAt'], errors='coerce')  # Handle any invalid dates

    # Drop rows where 'createdAt' is NaT (Not a Time)
    data = data.dropna(subset=['createdAt'])

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
