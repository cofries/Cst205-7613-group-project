import os
import base64
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")


def get_access_token():
    """
    Gets Spotify access token using Client Credentials Flow
    """
    url = "https://accounts.spotify.com/api/token"

    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code != 200:
        print("Error getting token:", response.json())
        return None

    return response.json()["access_token"]


def search_tracks_by_mood(mood):
    """
    Searches Spotify for songs based on mood
    """
    token = get_access_token()
    if not token:
        return []

    # Map moods to search queries
    mood_map = {
        "Happy": "happy upbeat",
        "Sad": "sad emotional",
        "Chill": "lofi chill",
        "Workout": "gym hype",
        "Romantic": "love songs",
        "Party": "party hits"
    }

    query = mood_map.get(mood, mood)

    url = "https://api.spotify.com/v1/search"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "q": query,
        "type": "track",
        "limit": 5
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print("Error searching tracks:", response.json())
        return []

    tracks = response.json()["tracks"]["items"]

    results = []
    for track in tracks:
        name = track["name"]
        artist = track["artists"][0]["name"]
        link = track["external_urls"]["spotify"]
        preview_url = track.get("preview_url")

        results.append({
            "name": name,
            "artist": artist,
            "url": link,
            "preview_url": preview_url
        })

    return results