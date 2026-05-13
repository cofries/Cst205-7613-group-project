from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QFrame,
    QMessageBox,
)

from PIL import Image, ImageOps

final_img = Image.new("RGB", (500, 500), color=(255, 105, 180))


class PhotoEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.original_image = None
        self.current_image = None

        self.setStyleSheet("""
            QWidget {
                background-color: #111827;
                color: white;
                font-family: Arial;
                font-size: 16px;
            }

            QLabel#title {
                font-size: 34px;
                font-weight: bold;
                color: #f9fafb;
            }

            QLabel#subtitle {
                font-size: 17px;
                color: #d1d5db;
            }

            QFrame#card {
                background-color: #1f2937;
                border-radius: 18px;
                padding: 20px;
            }

            QLabel#preview {
                background-color: #111827;
                border: 2px solid #374151;
                border-radius: 14px;
                padding: 10px;
            }

            QPushButton {
                background-color: #ec4899;
                color: white;
                border-radius: 12px;
                padding: 13px;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #db2777;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(50, 40, 50, 40)
        layout.setSpacing(20)

        title = QLabel("Photo Editor")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Upload a photo and customize it with simple filters.")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout()
        card_layout.setSpacing(18)

        self.preview = QLabel("Upload an image to start editing")
        self.preview.setObjectName("preview")
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setMinimumHeight(420)

        button_row = QHBoxLayout()

        upload_button = QPushButton("Upload Image")
        upload_button.clicked.connect(self.upload_image)

        grayscale_button = QPushButton("Grayscale")
        grayscale_button.clicked.connect(self.apply_grayscale)

        sepia_button = QPushButton("Sepia")
        sepia_button.clicked.connect(self.apply_sepia)

        rotate_button = QPushButton("Rotate")
        rotate_button.clicked.connect(self.rotate_image)

        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset_image)

        save_button = QPushButton("Save Image")
        save_button.clicked.connect(self.save_image)

        button_row.addWidget(upload_button)
        button_row.addWidget(grayscale_button)
        button_row.addWidget(sepia_button)
        button_row.addWidget(rotate_button)
        button_row.addWidget(reset_button)
        button_row.addWidget(save_button)

        card_layout.addWidget(self.preview)
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
            self.current_image = self.original_image.copy()
            self.update_final_image()
            self.show_image(self.current_image)

    def apply_grayscale(self):
        if not self.has_image():
            return

        gray = ImageOps.grayscale(self.current_image)
        self.current_image = gray.convert("RGB")
        self.update_final_image()
        self.show_image(self.current_image)

    def apply_sepia(self):
        if not self.has_image():
            return

        sepia_image = self.current_image.copy().convert("RGB")
        pixels = sepia_image.load()

        for y in range(sepia_image.height):
            for x in range(sepia_image.width):
                r, g, b = pixels[x, y]

                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)

                pixels[x, y] = (
                    min(255, tr),
                    min(255, tg),
                    min(255, tb),
                )

        self.current_image = sepia_image
        self.update_final_image()
        self.show_image(self.current_image)

    def rotate_image(self):
        if not self.has_image():
            return

        self.current_image = self.current_image.rotate(90, expand=True)
        self.update_final_image()
        self.show_image(self.current_image)

    def reset_image(self):
        if self.original_image is None:
            QMessageBox.warning(self, "No Image", "Please upload an image first.")
            return

        self.current_image = self.original_image.copy()
        self.update_final_image()
        self.show_image(self.current_image)

    def save_image(self):
        if not self.has_image():
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save edited image",
            "edited_image.png",
            "PNG Image (*.png)"
        )

        if file_path:
            if not file_path.lower().endswith(".png"):
                file_path += ".png"

            self.current_image.save(file_path)
            QMessageBox.information(self, "Saved", "Your edited image was saved!")

    def has_image(self):
        if self.current_image is None:
            QMessageBox.warning(self, "No Image", "Please upload an image first.")
            return False

        return True

    def update_final_image(self):
        global final_img
        final_img = self.current_image.copy()

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


def create_editor_tab():
    return PhotoEditor()