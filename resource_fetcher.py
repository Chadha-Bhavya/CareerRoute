import os
import requests
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_youtube_links(skill, max_results=2):
    query = f"best beginner {skill} tutorial"
    url = "https://www.googleapis.com/youtube/v3/search"
    
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "key": YOUTUBE_API_KEY,
        "maxResults": max_results,
        "order": "relevance",         
        "videoDuration": "medium"     
    }

    r = requests.get(url, params=params)
    items = r.json().get("items", [])
    links = [
        f"https://www.youtube.com/watch?v={item['id']['videoId']}" 
        for item in items
    ]
    return links