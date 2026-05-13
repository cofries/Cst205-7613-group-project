import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QMessageBox,
    QLineEdit,
    QFrame,
)


def save_image(img, save_name):
    folder = os.path.join(os.path.expanduser("~"), "Desktop")
    img.save(os.path.join(folder, f"{save_name}.png"))


def create_save_tab():
    widget = QWidget()

    widget.setStyleSheet("""
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

        QFrame#card {
            background-color: rgba(36, 27, 54, 0.92);
            border: 2px solid #ec95ed;
            border-radius: 26px;
            padding: 26px;
        }

        QLineEdit {
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
    """)

    layout = QVBoxLayout(widget)
    layout.setContentsMargins(50, 40, 50, 40)
    layout.setSpacing(14)

    title = QLabel("Save & Export")
    title.setObjectName("title")
    title.setAlignment(Qt.AlignCenter)

    subtitle = QLabel("Enter a file name and save your final image as a PNG.")
    subtitle.setObjectName("subtitle")
    subtitle.setAlignment(Qt.AlignCenter)

    card = QFrame()
    card.setObjectName("card")
    card.setFixedWidth(520)

    card_layout = QVBoxLayout(card)
    card_layout.setSpacing(18)

    name_input = QLineEdit()
    name_input.setPlaceholderText("Example: my_final_meme")

    save_btn = QPushButton("Save to Desktop 💾")
    save_btn.clicked.connect(lambda: save_clicked(name_input))

    card_layout.addWidget(name_input)
    card_layout.addWidget(save_btn)

    layout.addStretch()
    layout.addWidget(title)
    layout.addWidget(subtitle)
    layout.addSpacing(20)
    layout.addWidget(card, alignment=Qt.AlignCenter)
    layout.addStretch()

    return widget


def save_clicked(name_input):
    save_name = name_input.text().strip()

    if save_name == "":
        QMessageBox.warning(None, "No save name", "Please enter a save name.")
        return

    from tabs.editor import final_img

    if final_img is None:
        QMessageBox.warning(None, "No Image", "No image found.")
        return

    save_image(final_img, save_name)
    QMessageBox.information(None, "Saved", f"Saved as {save_name}.png on your Desktop.")

    

