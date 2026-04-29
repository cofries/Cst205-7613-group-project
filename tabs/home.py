from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame


def create_home_tab():
    home = QWidget()

    layout = QVBoxLayout()
    layout.setContentsMargins(80, 60, 80, 60)
    layout.setSpacing(25)

    title = QLabel("Welcome to Mood Meme Studio")
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("""
        font-size: 42px;
        font-weight: bold;
        color: #f9fafb;
    """)

    subtitle = QLabel("Create, edit, and match your photos with memes and music.")
    subtitle.setAlignment(Qt.AlignCenter)
    subtitle.setStyleSheet("""
        font-size: 20px;
        color: #d1d5db;
    """)

    card = QFrame()
    card.setStyleSheet("""
        QFrame {
            background-color: #1f2937;
            border-radius: 20px;
            padding: 30px;
        }
    """)

    card_layout = QVBoxLayout()

    instructions = QLabel("""
What you can do in this app:

• Pick a mood and get a random meme
• Get Spotify song suggestions based on that same mood
• Upload and edit your own photos
• Add text to create your own meme
• Save your final image as a PNG

How to start:
Use the Mood Generator tab to generate memes and songs.
Later, use the Photo Editor and Meme Creator tabs to customize your own image.
""")

    instructions.setWordWrap(True)
    instructions.setAlignment(Qt.AlignLeft)
    instructions.setStyleSheet("""
        font-size: 19px;
        color: #f3f4f6;
    """)

    card_layout.addWidget(instructions)
    card.setLayout(card_layout)

    layout.addWidget(title)
    layout.addWidget(subtitle)
    layout.addWidget(card)
    layout.addStretch()

    home.setLayout(layout)
    return home