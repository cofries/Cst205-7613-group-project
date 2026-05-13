import random

from PIL import Image, ImageDraw, ImageFont

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QLineEdit, QFrame, QMessageBox, QComboBox,
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
            QWidget {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #181825, stop:0.5 #221b3a, stop:1 #2b1f45);
                color: white;
                font-family: Arial;
                font-size: 16px;
            }

            QLabel { background-color: transparent; }

            QLabel#title {
                font-size: 38px;
                font-weight: bold;
                color: #ffffff;
            }

            QLabel#subtitle {
                font-size: 18px;
                color: #7dcff0;
            }

            QLabel#label {
                color: #ec95ed;
                font-size: 15px;
                font-weight: bold;
            }

            QFrame#card {
                background-color: rgba(36, 27, 54, 0.92);
                border: 2px solid #ec95ed;
                border-radius: 26px;
                padding: 24px;
            }

            QPushButton {
                background-color: #eb8ae4;
                color: white;
                border-radius: 14px;
                padding: 13px;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #7dcff0;
                color: #181825;
            }

            QLineEdit, QComboBox {
                background-color: #2b1f45;
                color: white;
                border: 2px solid #7dcff0;
                border-radius: 12px;
                padding: 12px;
                font-size: 16px;
            }

            QLabel#preview {
                background-color: #181825;
                border: 2px solid #7dcff0;
                border-radius: 16px;
                padding: 10px;
                color: #dbeafe;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(50, 30, 50, 30)
        layout.setSpacing(14)

        title = QLabel("Meme Creator")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Upload an image, customize the caption style, and save your meme.")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)

        card = QFrame()
        card.setObjectName("card")

        card_layout = QVBoxLayout()
        card_layout.setSpacing(12)

        self.preview = QLabel("Upload an image to start")
        self.preview.setObjectName("preview")
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setFixedHeight(300)

        self.top_text_input = QLineEdit()
        self.top_text_input.setPlaceholderText("Top meme text")

        self.bottom_text_input = QLineEdit()
        self.bottom_text_input.setPlaceholderText("Bottom meme text")

        options_row = QHBoxLayout()
        options_row.setSpacing(12)

        font_size_label = QLabel("Font Size")
        font_size_label.setObjectName("label")

        self.font_size_dropdown = QComboBox()
        self.font_size_dropdown.addItems(["Small", "Medium", "Large"])

        font_color_label = QLabel("Font Color")
        font_color_label.setObjectName("label")

        self.font_color_dropdown = QComboBox()
        self.font_color_dropdown.addItems(["White", "Pink", "Yellow", "Black", "Blue"])

        options_row.addWidget(font_size_label)
        options_row.addWidget(self.font_size_dropdown)
        options_row.addWidget(font_color_label)
        options_row.addWidget(self.font_color_dropdown)

        button_row = QHBoxLayout()
        button_row.setSpacing(10)

        upload_button = QPushButton("Upload")
        upload_button.clicked.connect(self.upload_image)

        random_button = QPushButton("Random Caption")
        random_button.clicked.connect(self.randomize_caption)

        generate_button = QPushButton("Generate")
        generate_button.clicked.connect(self.generate_meme)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_meme)

        button_row.addWidget(upload_button)
        button_row.addWidget(random_button)
        button_row.addWidget(generate_button)
        button_row.addWidget(save_button)

        card_layout.addWidget(self.preview)
        card_layout.addWidget(self.top_text_input)
        card_layout.addWidget(self.bottom_text_input)
        card_layout.addLayout(options_row)
        card_layout.addLayout(button_row)

        card.setLayout(card_layout)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(card)

        self.setLayout(layout)

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Choose an image", "", "Image Files (*.png *.jpg *.jpeg)"
        )

        if file_path:
            self.original_image = Image.open(file_path).convert("RGB")
            self.final_image = self.original_image.copy()
            self.show_image(self.original_image)

    def randomize_caption(self):
        top_text, bottom_text = random.choice(self.captions)
        self.top_text_input.setText(top_text)
        self.bottom_text_input.setText(bottom_text)

    def get_font_size(self, meme):
        size_choice = self.font_size_dropdown.currentText()

        if size_choice == "Small":
            return max(20, meme.width // 16)
        elif size_choice == "Large":
            return max(36, meme.width // 8)
        else:
            return max(28, meme.width // 12)

    def get_font_color(self):
        color = self.font_color_dropdown.currentText()

        if color == "Pink":
            return "#ec95ed"
        elif color == "Yellow":
            return "yellow"
        elif color == "Black":
            return "black"
        elif color == "Blue":
            return "#7dcff0"
        else:
            return "white"

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

        font_size = self.get_font_size(meme)
        font_color = self.get_font_color()

        try:
            font = ImageFont.truetype("impact.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()

        self.draw_text(draw, meme, top_text, font, 25, font_color)

        bottom_box = draw.textbbox((0, 0), bottom_text.upper(), font=font)
        bottom_height = bottom_box[3] - bottom_box[1]
        bottom_y = meme.height - bottom_height - 35

        self.draw_text(draw, meme, bottom_text, font, bottom_y, font_color)

        self.final_image = meme
        self.show_image(meme)

    def draw_text(self, draw, image, text, font, y, fill_color):
        text = text.upper()

        if text == "":
            return

        box = draw.textbbox((0, 0), text, font=font)
        text_width = box[2] - box[0]
        x = (image.width - text_width) // 2

        outline_color = "black"
        if fill_color == "black":
            outline_color = "white"

        for x_offset in range(-3, 4):
            for y_offset in range(-3, 4):
                draw.text((x + x_offset, y + y_offset), text, font=font, fill=outline_color)

        draw.text((x, y), text, font=font, fill=fill_color)

    def show_image(self, pil_image):
        image = pil_image.copy()
        image.thumbnail((500, 280))

        image_bytes = image.tobytes("raw", "RGB")

        qimage = QImage(
            image_bytes,
            image.width,
            image.height,
            image.width * 3,
            QImage.Format_RGB888,
        )

        pixmap = QPixmap.fromImage(qimage)

        self.preview.setPixmap(
            pixmap.scaled(500, 280, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

    def save_meme(self):
        if self.final_image is None:
            QMessageBox.warning(self, "No Meme", "Please generate a meme first.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save meme", "my_meme.png", "PNG Image (*.png)"
        )

        if file_path:
            if not file_path.lower().endswith(".png"):
                file_path += ".png"

            self.final_image.save(file_path)
            QMessageBox.information(self, "Saved", "Your meme was saved successfully!")


def create_meme_tab():
    return MemeGenerator()