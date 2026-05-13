from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QScrollArea,
)


def create_feature_card(icon, title, description):
    card = QFrame()
    card.setStyleSheet("""
    QFrame {
        background-color: qlineargradient(
            x1:0, y1:0,
            x2:1, y2:1,
            stop:0 #1e1b4b,
            stop:0.5 #111827,
            stop:1 #831843
        );
        border-radius: 24px;
        padding: 24px;
    }
""")

    layout = QVBoxLayout()
    layout.setSpacing(10)

    icon_label = QLabel(icon)
    icon_label.setAlignment(Qt.AlignCenter)
    icon_label.setStyleSheet("""
        font-size: 42px;
        background-color: transparent;
    """)

    title_label = QLabel(title)
    title_label.setAlignment(Qt.AlignCenter)
    title_label.setStyleSheet("""
        font-size: 20px;
        font-weight: bold;
        color: #f9fafb;
        background-color: transparent;
    """)

    desc_label = QLabel(description)
    desc_label.setAlignment(Qt.AlignCenter)
    desc_label.setWordWrap(True)
    desc_label.setStyleSheet("""
        font-size: 14px;
        color: #d1d5db;
        background-color: transparent;
    """)

    layout.addWidget(icon_label)
    layout.addWidget(title_label)
    layout.addWidget(desc_label)

    card.setLayout(layout)
    return card


def create_home_tab():
    home = QWidget()

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)

    container = QWidget()
    layout = QVBoxLayout()
    layout.setContentsMargins(70, 35, 70, 35)
    layout.setSpacing(18)

    title = QLabel("Welcome to Mood Meme Studio")
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("font-size: 42px; font-weight: bold; color: #f9fafb;")

    subtitle = QLabel("Create memes, edit photos, match your mood with music, and save your final image.")
    subtitle.setAlignment(Qt.AlignCenter)
    subtitle.setWordWrap(True)
    subtitle.setStyleSheet("font-size: 20px; color: #d1d5db;")

    banner = QLabel()
    banner.setAlignment(Qt.AlignCenter)

    banner_path = Path(__file__).resolve().parent.parent / "assets" / "banner.png"
    pixmap = QPixmap(str(banner_path))

    if not pixmap.isNull():
        banner.setPixmap(
            pixmap.scaled(
                1000,
                260,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )
    else:
        banner.setText("Mood Meme Studio")
        banner.setStyleSheet("font-size: 32px; font-weight: bold; color: #ec4899;")

    card = QFrame()
    card.setStyleSheet("""
        QFrame {
            background-color: #1f2937;
            border-radius: 20px;
            padding: 22px;
        }
    """)

    card_layout = QVBoxLayout()
    card_layout.setSpacing(18)

    intro = QLabel("What you can do in this app")
    intro.setAlignment(Qt.AlignCenter)
    intro.setStyleSheet("font-size: 24px; font-weight: bold; color: #f9fafb;")

    row_one = QHBoxLayout()
    row_one.addWidget(create_feature_card("🎭", "Mood Generator", "Pick a mood or use the weather to get a matching meme."))
    row_one.addWidget(create_feature_card("🎵", "Spotify Match", "Get song suggestions based on your selected mood."))
    row_one.addWidget(create_feature_card("🖼️", "Photo Editor", "Upload photos and apply filters, brightness, contrast, and rotation."))

    row_two = QHBoxLayout()
    row_two.addWidget(create_feature_card("😂", "Meme Creator", "Add custom top and bottom text with font color and size options."))
    row_two.addWidget(create_feature_card("🌤️", "Weather Mood", "Enter a city and let the weather suggest the vibe."))
    row_two.addWidget(create_feature_card("💾", "Save & Export", "Save your edited images and memes as PNG files."))

    tech = QLabel("Built with PySide6, Pillow, Requests, Spotify API, and Weather API")
    tech.setAlignment(Qt.AlignCenter)
    tech.setStyleSheet("font-size: 14px; color: #9ca3af;")

    card_layout.addWidget(intro)
    card_layout.addLayout(row_one)
    card_layout.addLayout(row_two)
    card_layout.addWidget(tech)

    card.setLayout(card_layout)

    layout.addWidget(title)
    layout.addWidget(subtitle)
    layout.addWidget(banner)
    layout.addWidget(card)

    container.setLayout(layout)
    scroll_area.setWidget(container)

    outer_layout = QVBoxLayout()
    outer_layout.addWidget(scroll_area)
    home.setLayout(outer_layout)

    return home