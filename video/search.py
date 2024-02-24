import requests

# Replace with your API key and desired search term
api_key = "YOUR_API_KEY"
search_term = "coding tutorials"

# Build the search URL
url = f"https://api.vimeo.com/videos?q={search_term}"

# Add authentication header
headers = {"Authorization": f"Bearer {api_key}"}

# Send the GET request
response = requests.get(url, headers=headers)

# Handle response and extract video data
if response.status_code == 200:
    data = response.json()
    videos = data["data"]
    for video in videos:
        print(f"Title: {video['name']}")
        print(f"Description: {video['description']}")
        print(f"URL: {video['link']}")
        print("----------------")
else:
    print(f"Error: {response.status_code}")