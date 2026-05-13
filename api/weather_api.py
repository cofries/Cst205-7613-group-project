from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_weather(city):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=imperial"
    )

    print("API KEY:", API_KEY)
    print("URL:", url)

    response = requests.get(url)

    print("STATUS CODE:", response.status_code)
    print("RESPONSE:", response.text)

    if response.status_code != 200:
        return None

    data = response.json()

    weather = data["weather"][0]["main"]
    temperature = data["main"]["temp"]

    return {
        "weather": weather,
        "temperature": temperature
    }


def suggest_mood(weather):
    mood_map = {
        "Clear": "Happy ☀️",
        "Clouds": "Chill ☁️",
        "Rain": "Sad 🌧️",
        "Snow": "Cozy ❄️",
        "Thunderstorm": "Energetic ⚡"
    }

    return mood_map.get(weather, "Relaxed 🎵")
if __name__ == "__main__":
    weather_data = get_weather("Monterey")

    print(weather_data)

    if weather_data:
        mood = suggest_mood(weather_data["weather"])
        print("Suggested mood:", mood)