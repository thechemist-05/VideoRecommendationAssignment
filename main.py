import requests

# API URL for fetching viewed posts
API_URL = "https://api.socialverseapp.com/posts/view?page=1&page_size=10"

# Authorization Token
HEADERS = {
    "Flic-Token": "flic_6e2d8d25dc29a4ddd382c2383a903cf4a688d1a117f6eb43b35a1e7fadbb84b8"
}

# Function to fetch data
def fetch_data():
    response = requests.get(API_URL, headers=HEADERS)
    if response.status_code == 200:
        return response.json()  # Return the data as JSON
    else:
        return f"Error {response.status_code}: {response.text}"

# Run the fetch and display data
if __name__ == "__main__":
    data = fetch_data()
    print(data)
