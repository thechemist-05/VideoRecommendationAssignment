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
        return response.json()  # Return JSON response directly
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# Function to preprocess the data
def preprocess_data(data):
    print("Raw data fetched. Preprocessing...")
    
    # Check if 'posts' field exists in the data
    if 'posts' not in data:
        print("No 'posts' field found in the data.")
        return None
    
    # Extract the posts data from the response
    posts_data = data['posts']
    if not posts_data:
        print("No posts data available.")
        return None
    
    # Convert the posts data into a DataFrame
    df = pd.DataFrame(posts_data)

    print("Available columns in the dataset:")
    print(df.columns)  # Log the columns to see the available data

    # Dynamically handle missing or unknown columns by just working with the available ones
    # We'll try to use the first few columns we find as an example.
    columns_found = df.columns.tolist()  # Get all available columns

    if not columns_found:
        print(f"Warning: No columns were found.")
        return df  # Return whatever data we can, even if not fully processed

    # Process columns that are available, in case there are missing or mismatched columns
    cleaned_df = df[columns_found]  # Just work with whatever columns we have

    print("Data preprocessing completed.")
    return cleaned_df

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
    
    if raw_data is not None and raw_data:
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
