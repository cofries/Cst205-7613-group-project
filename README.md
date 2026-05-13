# Mood Meme Studio

Mood Meme Studio is a Python PySide6 desktop application that allows users to edit photos, generate memes, and discover mood-based music and weather suggestions through multiple API integrations.

The app combines image editing, meme generation, weather-based mood detection, and Spotify music recommendations into one interactive multimedia experience.

---

## Features

### Mood Generator
- Select a mood to generate matching memes and Spotify songs
- Weather-based mood suggestions using a city search
- Spotify song recommendations based on mood
- Play available Spotify 30-second song previews directly inside the app
- Double-click songs to open them in Spotify

### Meme Creator
- Upload your own images
- Add custom top and bottom meme text
- Random meme caption generator
- Customize font size
- Customize font color
- Save generated memes as PNG images

### Photo Editor
- Upload and preview images
- Apply grayscale filter
- Apply sepia filter
- Rotate images
- Adjust brightness
- Adjust contrast
- Reset edited images
- Save edited images as PNG files

### Save & Export
- Export final images directly to the desktop
- Save memes and edited images as PNG files

---

## APIs Used

- Spotify Web API — used to fetch mood-based song suggestions and song preview links
- wttr.in Weather API — used to get weather conditions and suggest moods based on weather
- Meme API (Reddit-based) — https://meme-api.com/gimme

---

## Technologies Used

- Python
- PySide6
- Pillow
- Requests
- Spotify Web API
- Weather API
- Meme API

---

## Installation

Clone the repository:

```bash
git clone https://github.com/cofries/Cst205-7613-group-project.git
```

Navigate into the project folder:

```bash
cd Cst205-7613-group-project
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project directory:

```bash
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
```

Run the application:

```bash
python main.py
```

---

## Project Structure

```text
Cst205-7613-group-project/
│
├── api/
│   ├── spotify_api.py
│   ├── meme_api.py
│   └── weather_api.py
│
├── tabs/
│   ├── home.py
│   ├── mood.py
│   ├── meme.py
│   ├── editor.py
│   └── save.py
│
├── assets/
│   └── banner.png
│
├── main.py
├── requirements.txt
└── README.md
```

---

## How to Use

1. Open the application.
2. Use the Mood Generator tab to select a mood or enter a city for weather-based mood suggestions.
3. Generate memes and Spotify song recommendations.
4. Preview available Spotify song clips directly inside the app.
5. Use the Photo Editor tab to customize uploaded images.
6. Use the Meme Creator tab to add custom meme captions and styling.
7. Save/export final images as PNG files.

---

## Authors

- Silvia Pineda Jimenez
- Chris Dlamini
- Conrad Fries
- Teddy Santoyo
- CST205 Final Project Team

---

## Future Improvements

- More image filters and editing tools
- Additional meme templates
- Playlist generation
- Dark/light mode toggle
- GIF meme support
- More music streaming integrations