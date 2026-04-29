import requests

def get_meme_by_mood(mood):
    subreddit_map = {
        "Happy": "wholesomememes",
        "Sad": "me_irl",
        "Chill": "memes",
        "Workout": "gymmemes",
        "Romantic": "love_memes",
        "Party": "dankmemes"
    }

    subreddit = subreddit_map.get(mood, "memes")

    url = f"https://meme-api.com/gimme/{subreddit}"

    response = requests.get(url)

    if response.status_code != 200:
        print("Error fetching meme")
        return None

    data = response.json()

    return {
        "title": data["title"],
        "url": data["url"]
    }