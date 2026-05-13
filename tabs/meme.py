from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

def create_meme_tab():
    tab = QWidget()
    layout = QVBoxLayout()

    title = QLabel("Meme Creator")
    title.setStyleSheet("font-size: 24px; font-weight: bold;")

    message = QLabel("Meme generator features coming soon.")
    message.setStyleSheet("font-size: 16px;")

    layout.addWidget(title)
    layout.addWidget(message)
    tab.setLayout(layout)

    return tab