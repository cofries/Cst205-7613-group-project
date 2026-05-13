import sys
import webbrowser
import requests

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QListWidget,
    QListWidgetItem,
    QFrame,
    QScrollArea,
    QLineEdit,
)

from api.spotify_api import search_tracks_by_mood
from api.meme_api import get_meme_by_mood


class MoodMemeStudio(QWidget):
    def __init__(self):
        super().__init__()

        self.songs = []
        self.current_meme = None

        self.setWindowTitle("Mood Meme Studio")
        self.resize(1200, 900)

        self.setStyleSheet("""
            QWidget {
                background-color: #111827;
                color: white;
                font-family: Arial;
                font-size: 16px;
            }

            QLabel#title {
                font-size: 36px;
                font-weight: bold;
                color: #f9fafb;
            }

            QLabel#subtitle {
                font-size: 18px;
                color: #d1d5db;
            }

            QFrame#card {
                background-color: #1f2937;
                border-radius: 18px;
                padding: 20px;
            }

            QComboBox, QLineEdit {
                background-color: #374151;
                color: white;
                border-radius: 10px;
                padding: 12px;
                font-size: 16px;
            }

            QPushButton {
                background-color: #ec4899;
                color: white;
                border-radius: 12px;
                padding: 14px;
                font-size: 17px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #db2777;
            }

            QListWidget {
                background-color: #111827;
                border: 2px solid #374151;
                border-radius: 14px;
                padding: 10px;
                min-height: 180px;
            }

            QListWidget::item {
                padding: 14px;
                border-bottom: 1px solid #374151;
            }

            QListWidget::item:hover {
                background-color: #374151;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 40, 50, 40)
        main_layout.setSpacing(25)

        title = QLabel("Mood Meme Studio")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Pick a mood, use the weather, get a meme, and find matching Spotify songs.")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout()
        card_layout.setSpacing(18)

        mood_label = QLabel("Choose a mood:")
        self.mood_dropdown = QComboBox()
        self.mood_dropdown.addItems(["Happy", "Sad", "Chill", "Workout", "Romantic", "Party"])

        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Enter city for weather mood, example: Monterey")

        self.weather_button = QPushButton("Use Weather to Pick Mood 🌤️")
        self.weather_button.clicked.connect(self.fetch_weather_mood)

        self.weather_result = QLabel("Weather mood suggestion will appear here.")
        self.weather_result.setAlignment(Qt.AlignCenter)
        self.weather_result.setWordWrap(True)
        self.weather_result.setStyleSheet("color: #d1d5db; font-size: 15px;")

        self.meme_button = QPushButton("Get Meme 😂")
        self.meme_button.clicked.connect(self.fetch_meme)

        self.meme_title = QLabel("Meme title will appear here")
        self.meme_title.setAlignment(Qt.AlignCenter)
        self.meme_title.setWordWrap(True)

        self.meme_label = QLabel("Meme will appear here")
        self.meme_label.setAlignment(Qt.AlignCenter)
        self.meme_label.setMinimumHeight(320)

        self.button = QPushButton("Get Spotify Song Suggestions 🎧")
        self.button.clicked.connect(self.fetch_songs)

        self.song_list = QListWidget()
        self.song_list.itemClicked.connect(self.open_song)

        card_layout.addWidget(mood_label)
        card_layout.addWidget(self.mood_dropdown)
        card_layout.addWidget(self.city_input)
        card_layout.addWidget(self.weather_button)
        card_layout.addWidget(self.weather_result)
        card_layout.addWidget(self.meme_button)
        card_layout.addWidget(self.meme_title)
        card_layout.addWidget(self.meme_label)
        card_layout.addWidget(self.button)
        card_layout.addWidget(self.song_list)

        card.setLayout(card_layout)
        main_layout.addWidget(card)

        footer = QLabel("Tip: Click a song to open it on Spotify.")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #9ca3af; font-size: 14px;")
        main_layout.addWidget(footer)

        container = QWidget()
        container.setLayout(main_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(container)

        outer_layout = QVBoxLayout()
        outer_layout.addWidget(scroll_area)

        self.setLayout(outer_layout)

    def fetch_weather_mood(self):
        city = self.city_input.text().strip()

        if city == "":
            self.weather_result.setText("Please enter a city first.")
            return

        try:
            url = f"https://wttr.in/{city}?format=j1"
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                self.weather_result.setText("Could not load weather. Try another city.")
                return

            data = response.json()
            current = data["current_condition"][0]
            weather_text = current["weatherDesc"][0]["value"]
            temperature = current["temp_F"]

            suggested_mood = self.suggest_mood_from_weather(weather_text)

            index = self.mood_dropdown.findText(suggested_mood)
            if index >= 0:
                self.mood_dropdown.setCurrentIndex(index)

            self.weather_result.setText(
                f"Weather in {city}: {weather_text}, {temperature}°F\n"
                f"Suggested mood: {suggested_mood}"
            )

        except Exception:
            self.weather_result.setText("Weather API error. Check internet or try another city.")

    def suggest_mood_from_weather(self, weather_text):
        weather_text = weather_text.lower()

        if "rain" in weather_text or "drizzle" in weather_text or "storm" in weather_text:
            return "Sad"
        elif "sunny" in weather_text or "clear" in weather_text:
            return "Happy"
        elif "cloud" in weather_text or "mist" in weather_text or "fog" in weather_text:
            return "Chill"
        elif "snow" in weather_text:
            return "Romantic"
        else:
            return "Party"

    def fetch_songs(self):
        mood = self.mood_dropdown.currentText()
        self.song_list.clear()

        self.song_list.addItem(QListWidgetItem("Loading songs..."))
        self.songs = search_tracks_by_mood(mood)
        self.song_list.clear()

        if not self.songs:
            self.song_list.addItem("No songs found. Try another mood.")
            return

        for song in self.songs:
            display_text = f"🎵 {song['name']}\n   by {song['artist']}"
            self.song_list.addItem(display_text)

    def open_song(self, item):
        index = self.song_list.row(item)

        if index < len(self.songs):
            webbrowser.open(self.songs[index]["url"])

    def fetch_meme(self):
        mood = self.mood_dropdown.currentText()
        meme = get_meme_by_mood(mood)

        if not meme:
            self.meme_title.setText("Failed to load meme")
            self.meme_label.clear()
            return

        self.current_meme = meme
        self.meme_title.setText(meme["title"])

        response = requests.get(meme["url"])

        if response.status_code != 200:
            self.meme_label.setText("Failed to load image")
            return

        pixmap = QPixmap()
        pixmap.loadFromData(response.content)

        self.meme_label.setPixmap(
            pixmap.scaled(500, 320, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )


def create_mood_tab():
    return MoodMemeStudio()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MoodMemeStudio()
    window.showMaximized()
    sys.exit(app.exec())