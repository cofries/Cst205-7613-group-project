import sys
import webbrowser
import requests

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPixmap
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
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

        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.7)

        self.setWindowTitle("Mood Meme Studio")
        self.resize(1200, 900)

        self.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(
                    x1:0, y1:0,
                    x2:1, y2:1,
                    stop:0 #181825,
                    stop:0.5 #221b3a,
                    stop:1 #2b1f45
                );
                color: white;
                font-family: Arial;
                font-size: 16px;
            }

            QLabel {
                background-color: transparent;
            }

            QLabel#title {
                font-size: 38px;
                font-weight: bold;
                color: #f9fafb;
            }

            QLabel#subtitle {
                font-size: 18px;
                color: #7dcff0;
            }

            QLabel#sectionLabel {
                color: #ec95ed;
                font-size: 17px;
                font-weight: bold;
            }

            QFrame#card {
                background-color: rgba(36, 27, 54, 0.92);
                border: 2px solid #ec95ed;
                border-radius: 26px;
                padding: 24px;
            }

            QComboBox, QLineEdit {
                background-color: #2b1f45;
                color: white;
                border: 2px solid #7dcff0;
                border-radius: 12px;
                padding: 12px;
                font-size: 16px;
            }

            QPushButton {
                background-color: #eb8ae4;
                color: white;
                border-radius: 14px;
                padding: 14px;
                font-size: 17px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #7dcff0;
                color: #181825;
            }

            QListWidget {
                background-color: #181825;
                border: 2px solid #ec95ed;
                border-radius: 16px;
                padding: 10px;
                min-height: 180px;
            }

            QListWidget::item {
                background-color: #2b1f45;
                color: #f9fafb;
                padding: 14px;
                margin: 5px;
                border-radius: 10px;
            }

            QListWidget::item:hover {
                background-color: #40235f;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(55, 35, 55, 35)
        main_layout.setSpacing(22)

        title = QLabel("Mood Generator")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Use your mood or weather to find matching memes and Spotify songs.")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        card = QFrame()
        card.setObjectName("card")

        card_layout = QVBoxLayout()
        card_layout.setSpacing(16)

        mood_label = QLabel("Choose a mood:")
        mood_label.setObjectName("sectionLabel")

        self.mood_dropdown = QComboBox()
        self.mood_dropdown.addItems(["Happy", "Sad", "Chill", "Workout", "Romantic", "Party"])

        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Enter city for weather mood, example: Monterey")

        self.weather_button = QPushButton("Use Weather to Pick Mood 🌤️")
        self.weather_button.clicked.connect(self.fetch_weather_mood)

        self.weather_result = QLabel("Weather mood suggestion will appear here.")
        self.weather_result.setAlignment(Qt.AlignCenter)
        self.weather_result.setWordWrap(True)
        self.weather_result.setStyleSheet("""
            color: #7dcff0;
            font-size: 15px;
            font-weight: bold;
            background-color: transparent;
        """)

        self.meme_button = QPushButton("Get Meme 😂")
        self.meme_button.clicked.connect(self.fetch_meme)

        self.meme_title = QLabel("Meme title will appear here")
        self.meme_title.setAlignment(Qt.AlignCenter)
        self.meme_title.setWordWrap(True)
        self.meme_title.setStyleSheet("""
            color: #f9fafb;
            font-size: 17px;
            font-weight: bold;
            background-color: transparent;
        """)

        self.meme_label = QLabel("Meme will appear here")
        self.meme_label.setAlignment(Qt.AlignCenter)
        self.meme_label.setMinimumHeight(300)
        self.meme_label.setStyleSheet("""
            background-color: #181825;
            border: 2px solid #7dcff0;
            border-radius: 16px;
            padding: 10px;
            color: #dbeafe;
        """)

        self.song_button = QPushButton("Get Spotify Song Suggestions 🎧")
        self.song_button.clicked.connect(self.fetch_songs)

        self.preview_button = QPushButton("▶️ Play Selected Song Preview")
        self.preview_button.clicked.connect(self.play_song_preview)

        self.song_list = QListWidget()
        self.song_list.itemDoubleClicked.connect(self.open_song)

        card_layout.addWidget(mood_label)
        card_layout.addWidget(self.mood_dropdown)
        card_layout.addWidget(self.city_input)
        card_layout.addWidget(self.weather_button)
        card_layout.addWidget(self.weather_result)
        card_layout.addWidget(self.meme_button)
        card_layout.addWidget(self.meme_title)
        card_layout.addWidget(self.meme_label)
        card_layout.addWidget(self.song_button)
        card_layout.addWidget(self.song_list)
        card_layout.addWidget(self.preview_button)  

        card.setLayout(card_layout)
        main_layout.addWidget(card)

        footer = QLabel("Tip: Select a song to preview it, or double-click a song to open it on Spotify.")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("""
            color: #ec95ed;
            font-size: 14px;
            background-color: transparent;
        """)

        main_layout.addWidget(footer)

        container = QWidget()
        container.setLayout(main_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(container)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(0, 0, 0, 0)
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
            preview_text = "preview available" if song.get("preview_url") else "no preview"
            display_text = f"🎵 {song['name']}\n   by {song['artist']} • {preview_text}"
            self.song_list.addItem(display_text)

    def play_song_preview(self):
        selected_item = self.song_list.currentItem()

        if selected_item is None:
            self.weather_result.setText("Select a song first, then click Play Song Preview.")
            return

        index = self.song_list.row(selected_item)

        if index >= len(self.songs):
            return

        preview_url = self.songs[index].get("preview_url")

        if not preview_url:
            self.weather_result.setText("No Spotify preview available for this song. Try another one.")
            return

        self.player.setSource(QUrl(preview_url))
        self.player.play()

        self.weather_result.setText("Playing 30-second Spotify preview inside the app...")

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
            pixmap.scaled(500, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )


def create_mood_tab():
    return MoodMemeStudio()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MoodMemeStudio()
    window.showMaximized()
    sys.exit(app.exec())