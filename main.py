"""
Course: CST 205 M/W 2-4 
Title: Mood Meme Studio
Abstract: A PySide6 multimedia desktop app for editing photos, creating memes,
and generating mood-based music, weather, and meme suggestions through APIs.
Authors: Silvia Pineda Jimenez, Teddy Santoyo, Conrad Fries Reuschling, Christopher Dlamini
Class: CST205 M/W 2-4 
Date: May 13 2026
GitHub Repository: https://github.com/cofries/Cst205-7613-group-project
"""


import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget

from tabs.home import create_home_tab
from tabs.mood import create_mood_tab
from tabs.editor import create_editor_tab
from tabs.meme import create_meme_tab
from tabs.save import create_save_tab
from tabs.meme import create_meme_tab


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
        tabs.addTab(create_editor_tab(), "Photo Editor")
        tabs.addTab(create_meme_tab(), "Meme Creator")
        tabs.addTab(create_save_tab(), "Save")

        layout.addWidget(tabs)
        self.setLayout(layout)


app = QApplication(sys.argv)
window = MoodMemeStudio()
window.showMaximized()
sys.exit(app.exec())