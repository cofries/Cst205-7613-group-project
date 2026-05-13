<<<<<<< HEAD
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
=======
import random

from PIL import Image, ImageDraw, ImageFont

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QLineEdit,
    QFrame,
    QMessageBox,
)


class MemeGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.original_image = None
        self.final_image = None

        self.captions = [
            ("WHEN THE CODE WORKS", "BUT YOU DON'T KNOW WHY"),
            ("ME TRYING TO DEBUG", "ONE SMALL ERROR FOR 3 HOURS"),
            ("WHEN THE GROUP PROJECT STARTS", "AND EVERYONE SAYS THEY'LL HELP"),
            ("PYTHON SAID ERROR", "BUT I SAID PLEASE"),
            ("WHEN THE MEME GENERATOR WORKS", "INSTANT A+ ENERGY"),
            ("WHEN YOU FORGET TO SAVE", "PAIN"),
            ("GROUP PROJECT MEETING", "EVERYONE IS SILENT"),
            ("WHEN THE DESIGN DOC SAYS SIMPLE", "BUT THE CODE SAYS NO"),
        ]

        self.setStyleSheet("""
            QLabel#title {
                font-size: 36px;
                font-weight: bold;
                color: #f9fafb;
            }

            QLabel#subtitle {
                font-size: 18px;
                color: #d1d5db;
            }

            QFrame#card {
                background-color: #1f2937;
                border-radius: 18px;
                padding: 20px;
            }

            QPushButton {
                background-color: #ec4899;
                color: white;
                border-radius: 12px;
                padding: 14px;
                font-size: 17px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #db2777;
            }

            QLineEdit {
                background-color: #374151;
                color: white;
                border-radius: 10px;
                padding: 12px;
                font-size: 16px;
            }

            QLabel#preview {
                background-color: #111827;
                border: 2px solid #374151;
                border-radius: 14px;
                padding: 10px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(20)

        title = QLabel("Meme Generator")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Upload an image, randomize a caption, edit the text, and save your meme.")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)

        card = QFrame()
        card.setObjectName("card")

        card_layout = QVBoxLayout()
        card_layout.setSpacing(18)

        self.preview = QLabel("Upload an image to start")
        self.preview.setObjectName("preview")
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setMinimumHeight(420)

        self.top_text_input = QLineEdit()
        self.top_text_input.setPlaceholderText("Top meme text")

        self.bottom_text_input = QLineEdit()
        self.bottom_text_input.setPlaceholderText("Bottom meme text")

        button_row = QHBoxLayout()

        upload_button = QPushButton("Upload Image")
        upload_button.clicked.connect(self.upload_image)

        random_button = QPushButton("Randomize Caption")
        random_button.clicked.connect(self.randomize_caption)

        generate_button = QPushButton("Generate Meme")
        generate_button.clicked.connect(self.generate_meme)

        save_button = QPushButton("Save Meme")
        save_button.clicked.connect(self.save_meme)

        button_row.addWidget(upload_button)
        button_row.addWidget(random_button)
        button_row.addWidget(generate_button)
        button_row.addWidget(save_button)

        card_layout.addWidget(self.preview)
        card_layout.addWidget(self.top_text_input)
        card_layout.addWidget(self.bottom_text_input)
        card_layout.addLayout(button_row)

        card.setLayout(card_layout)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(card)

        self.setLayout(layout)

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Choose an image",
            "",
            "Image Files (*.png *.jpg *.jpeg)"
        )

        if file_path:
            self.original_image = Image.open(file_path).convert("RGB")
            self.final_image = self.original_image.copy()
            self.show_image(self.original_image)

    def randomize_caption(self):
        top_text, bottom_text = random.choice(self.captions)
        self.top_text_input.setText(top_text)
        self.bottom_text_input.setText(bottom_text)

    def generate_meme(self):
        if self.original_image is None:
            QMessageBox.warning(self, "No Image", "Please upload an image first.")
            return

        top_text = self.top_text_input.text().strip()
        bottom_text = self.bottom_text_input.text().strip()

        if top_text == "" and bottom_text == "":
            self.randomize_caption()
            top_text = self.top_text_input.text().strip()
            bottom_text = self.bottom_text_input.text().strip()

        meme = self.original_image.copy()
        draw = ImageDraw.Draw(meme)

        font_size = max(24, meme.width // 12)

        try:
            font = ImageFont.truetype("impact.ttf", font_size)
        except:
            font = ImageFont.load_default()

        self.draw_text(draw, meme, top_text, font, 25)

        bottom_box = draw.textbbox((0, 0), bottom_text.upper(), font=font)
        bottom_height = bottom_box[3] - bottom_box[1]
        bottom_y = meme.height - bottom_height - 35

        self.draw_text(draw, meme, bottom_text, font, bottom_y)

        self.final_image = meme
        self.show_image(meme)

    def draw_text(self, draw, image, text, font, y):
        text = text.upper()

        if text == "":
            return

        box = draw.textbbox((0, 0), text, font=font)
        text_width = box[2] - box[0]
        x = (image.width - text_width) // 2

        for x_offset in range(-3, 4):
            for y_offset in range(-3, 4):
                draw.text(
                    (x + x_offset, y + y_offset),
                    text,
                    font=font,
                    fill="black"
                )

        draw.text((x, y), text, font=font, fill="white")

    def show_image(self, pil_image):
        image = pil_image.copy()
        image.thumbnail((700, 420))

        image_bytes = image.tobytes("raw", "RGB")

        qimage = QImage(
            image_bytes,
            image.width,
            image.height,
            image.width * 3,
            QImage.Format_RGB888
        )

        pixmap = QPixmap.fromImage(qimage)

        self.preview.setPixmap(
            pixmap.scaled(
                700,
                420,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )

    def save_meme(self):
        if self.final_image is None:
            QMessageBox.warning(self, "No Meme", "Please generate a meme first.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save meme",
            "my_meme.png",
            "PNG Image (*.png)"
        )

        if file_path:
            if not file_path.lower().endswith(".png"):
                file_path += ".png"

            self.final_image.save(file_path)
            QMessageBox.information(self, "Saved", "Your meme was saved successfully!")


def create_meme_tab():
    return MemeGenerator()
>>>>>>> origin/main
