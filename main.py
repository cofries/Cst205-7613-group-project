"""
Course: CST 205 M/W 2-4 
Title: Mood Meme Studio
Abstract: A PySide6 multimedia desktop app for editing photos, creating memes,
and generating mood-based music, weather, and meme suggestions through APIs.
Authors: Silvia Pineda Jimenez, Teddy Santoyo, Conrad Fries Reuschling, Christopher Dlamini
Class: CST205 M/W 2-4 
Date: May 13 2026
GitHub Repository: https://github.com/cofries/Cst205-7613-group-project
Trello link : https://trello.com/invite/b/69e9382f6de4581a66ca8b5c/ATTI763076b1993f31d9729997d9eaa121fe94B4A6B9/team7613

Chris: worked on the meme creation part of the project
allowing users to upload an image and create/customize their own meme

Teddy: worked on the save and dowload features for users to be able to save their memes directly to their devices.

Conrad: worked on the filters page so users were able to apply filters and crop their memes.

Silvia: worked on setting up the app with the API's to be able to load on the mood tab. Also created the app home page and banner.
She also customized the layout of the app.

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
