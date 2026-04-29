import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget

from tabs.home import create_home_tab
from tabs.mood import create_mood_tab


class MoodMemeStudio(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mood Meme Studio")
        self.resize(1200, 900)

        self.setStyleSheet("""
            QWidget {
                background-color: #111827;
                color: white;
                font-family: Arial;
                font-size: 16px;
            }

            QTabBar::tab {
                background-color: #1f2937;
                color: white;
                padding: 12px 25px;
                font-size: 16px;
            }

            QTabBar::tab:selected {
                background-color: #ec4899;
                font-weight: bold;
            }
        """)

        layout = QVBoxLayout()

        tabs = QTabWidget()
        tabs.addTab(create_home_tab(), "Home")
        tabs.addTab(create_mood_tab(), "Mood Generator")

        layout.addWidget(tabs)
        self.setLayout(layout)


app = QApplication(sys.argv)
window = MoodMemeStudio()
window.showMaximized()
sys.exit(app.exec())