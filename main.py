import sys
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Mood Meme Studio")

layout = QVBoxLayout()

label = QLabel("Welcome to Mood Meme Studio 👀")
layout.addWidget(label)

window.setLayout(layout)
window.resize(400, 200)
window.show()

sys.exit(app.exec())