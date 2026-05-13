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
                stop:0 #2b1f45,
                stop:0.5 #31204f,
                stop:1 #40235f
            );
            border: 2px solid #ec95ed;
            border-radius: 26px;
            padding: 26px;
        }

        QFrame:hover {
            border: 2px solid #7dcff0;
        }
    """)

    layout = QVBoxLayout()
    layout.setSpacing(12)

    icon_label = QLabel(icon)
    icon_label.setAlignment(Qt.AlignCenter)
    icon_label.setStyleSheet("""
        font-size: 46px;
        background-color: transparent;
    """)

    title_label = QLabel(title)
    title_label.setAlignment(Qt.AlignCenter)
    title_label.setStyleSheet("""
        font-size: 21px;
        font-weight: bold;
        color: #ffffff;
        background-color: transparent;
    """)

    desc_label = QLabel(description)
    desc_label.setAlignment(Qt.AlignCenter)
    desc_label.setWordWrap(True)
    desc_label.setStyleSheet("""
        font-size: 14px;
        color: #dbeafe;
        line-height: 1.4em;
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
    scroll_area.setStyleSheet("""
        QScrollArea {
            border: none;
            background-color: transparent;
        }
    """)

    container = QWidget()

    container.setStyleSheet("""
        QWidget {
            background-color: qlineargradient(
                x1:0, y1:0,
                x2:1, y2:1,
                stop:0 #181825,
                stop:0.5 #221b3a,
                stop:1 #2b1f45
            );
        }
    """)

    layout = QVBoxLayout()
    layout.setContentsMargins(65, 25, 65, 40)
    layout.setSpacing(24)

    subtitle = QLabel("CREATE • EDIT • MATCH • SHARE")
    subtitle.setAlignment(Qt.AlignCenter)

    subtitle.setStyleSheet("""
        font-size: 18px;
        font-weight: bold;
        color: #7dcff0;
        letter-spacing: 4px;
    """)

    banner = QLabel()
    banner.setAlignment(Qt.AlignCenter)

    banner_path = Path(__file__).resolve().parent.parent / "assets" / "banner.png"
    pixmap = QPixmap(str(banner_path))

    if not pixmap.isNull():
        banner.setPixmap(
            pixmap.scaled(
                1080,
                300,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )
    else:
        banner.setText("Mood Meme Studio")
        banner.setStyleSheet("""
            font-size: 34px;
            font-weight: bold;
            color: #ec95ed;
        """)

    card = QFrame()

    card.setStyleSheet("""
        QFrame {
            background-color: rgba(36, 27, 54, 0.92);
            border: 2px solid #ec95ed;
            border-radius: 28px;
            padding: 28px;
        }
    """)

    card_layout = QVBoxLayout()
    card_layout.setSpacing(22)

    intro = QLabel("Choose your creative tool")
    intro.setAlignment(Qt.AlignCenter)

    intro.setStyleSheet("""
        font-size: 28px;
        font-weight: bold;
        color: #ffffff;
    """)

    row_one = QHBoxLayout()
    row_one.setSpacing(18)

    row_one.addWidget(create_feature_card(
        "🎭",
        "Mood Generator",
        "Pick a mood or use weather-based suggestions to discover memes."
    ))

    row_one.addWidget(create_feature_card(
        "🎵",
        "Spotify Match",
        "Get curated songs and playlists that match your selected mood."
    ))

    row_one.addWidget(create_feature_card(
        "🖼️",
        "Photo Editor",
        "Apply filters, brightness, contrast, rotation, and photo effects."
    ))

    row_two = QHBoxLayout()
    row_two.setSpacing(18)

    row_two.addWidget(create_feature_card(
        "😂",
        "Meme Creator",
        "Customize memes with your own captions, colors, and font styles."
    ))

    row_two.addWidget(create_feature_card(
        "🌤️",
        "Weather Mood",
        "Enter a city and let the current weather inspire the vibe."
    ))

    row_two.addWidget(create_feature_card(
        "💾",
        "Save & Export",
        "Save your memes and edited photos as high-quality PNG images."
    ))

    tech = QLabel(
        "Built with PySide6 • Pillow • Requests • Spotify API • Weather API"
    )

    tech.setAlignment(Qt.AlignCenter)

    tech.setStyleSheet("""
        font-size: 14px;
        color: #7dcff0;
        margin-top: 10px;
    """)

    card_layout.addWidget(intro)
    card_layout.addLayout(row_one)
    card_layout.addLayout(row_two)
    card_layout.addWidget(tech)

    card.setLayout(card_layout)

    layout.addWidget(subtitle)
    layout.addWidget(banner)
    layout.addWidget(card)

    container.setLayout(layout)

    scroll_area.setWidget(container)

    outer_layout = QVBoxLayout()
    outer_layout.setContentsMargins(0, 0, 0, 0)
    outer_layout.addWidget(scroll_area)

    home.setLayout(outer_layout)

    return home