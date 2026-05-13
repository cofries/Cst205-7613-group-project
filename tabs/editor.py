from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QFrame, QMessageBox, QSlider,
)

from PIL import Image, ImageOps, ImageEnhance

final_img = Image.new("RGB", (500, 500), color=(255, 105, 180))


class PhotoEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.original_image = None
        self.current_image = None
        self.filtered_image = None

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

            QFrame#card {
                background-color: rgba(36, 27, 54, 0.92);
                border: 2px solid #ec95ed;
                border-radius: 26px;
                padding: 24px;
            }

            QLabel#preview {
                background-color: #181825;
                border: 2px solid #7dcff0;
                border-radius: 16px;
                padding: 10px;
                color: #dbeafe;
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

            QSlider::groove:horizontal {
                height: 8px;
                background: #2b1f45;
                border: 1px solid #7dcff0;
                border-radius: 4px;
            }

            QSlider::handle:horizontal {
                background: #ec95ed;
                width: 20px;
                margin: -7px 0;
                border-radius: 10px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(50, 35, 50, 35)
        layout.setSpacing(18)

        title = QLabel("Photo Editor")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Upload a photo and customize it with filters, brightness, and contrast.")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setObjectName("card")

        card_layout = QVBoxLayout()
        card_layout.setSpacing(16)

        self.preview = QLabel("Upload an image to start editing")
        self.preview.setObjectName("preview")
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setMinimumHeight(360)

        button_row = QHBoxLayout()
        button_row.setSpacing(10)

        upload_button = QPushButton("Upload")
        upload_button.clicked.connect(self.upload_image)

        grayscale_button = QPushButton("Grayscale")
        grayscale_button.clicked.connect(self.apply_grayscale)

        sepia_button = QPushButton("Sepia")
        sepia_button.clicked.connect(self.apply_sepia)

        rotate_button = QPushButton("Rotate")
        rotate_button.clicked.connect(self.rotate_image)

        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset_image)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_image)

        for button in [upload_button, grayscale_button, sepia_button, rotate_button, reset_button, save_button]:
            button_row.addWidget(button)

        self.brightness_label = QLabel("Brightness: 100%")
        self.brightness_label.setStyleSheet("color: #ec95ed; font-weight: bold;")

        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setMinimum(50)
        self.brightness_slider.setMaximum(150)
        self.brightness_slider.setValue(100)
        self.brightness_slider.valueChanged.connect(self.apply_adjustments)

        self.contrast_label = QLabel("Contrast: 100%")
        self.contrast_label.setStyleSheet("color: #ec95ed; font-weight: bold;")

        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setMinimum(50)
        self.contrast_slider.setMaximum(150)
        self.contrast_slider.setValue(100)
        self.contrast_slider.valueChanged.connect(self.apply_adjustments)

        self.horizontal_crop_label = QLabel("Horizontal Crop")
        self.horizontal_crop_label.setStyleSheet("color: #ec95ed; font-weight: bold;")

        self.horizontal_crop_slider = QSlider(Qt.Horizontal)
        self.horizontal_crop_slider.setMinimum(0)
        self.horizontal_crop_slider.setMaximum(100)
        self.horizontal_crop_slider.setValue(0)
        self.horizontal_crop_slider.valueChanged.connect(self.apply_adjustments)

        self.vertical_crop_label = QLabel("Vertical Crop")
        self.vertical_crop_label.setStyleSheet("color: #ec95ed; font-weight: bold;")

        self.vertical_crop_slider = QSlider(Qt.Horizontal)
        self.vertical_crop_slider.setMinimum(0)
        self.vertical_crop_slider.setMaximum(100)
        self.vertical_crop_slider.setValue(0)
        self.vertical_crop_slider.valueChanged.connect(self.apply_adjustments)

        card_layout.addWidget(self.preview)
        card_layout.addLayout(button_row)
        card_layout.addWidget(self.brightness_label)
        card_layout.addWidget(self.brightness_slider)
        card_layout.addWidget(self.contrast_label)
        card_layout.addWidget(self.contrast_slider)
        card_layout.addWidget(self.horizontal_crop_label)
        card_layout.addWidget(self.horizontal_crop_slider)
        card_layout.addWidget(self.vertical_crop_label)
        card_layout.addWidget(self.vertical_crop_slider)

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
            self.filtered_image = self.original_image.copy()
            self.current_image = self.original_image.copy()
            self.reset_sliders()
            self.update_final_image()
            self.show_image(self.current_image)

    def apply_grayscale(self):
        if not self.has_image():
            return

        gray = ImageOps.grayscale(self.current_image)
        self.filtered_image = gray.convert("RGB")
        self.apply_adjustments()

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

                pixels[x, y] = (min(255, tr), min(255, tg), min(255, tb))

        self.filtered_image = sepia_image
        self.apply_adjustments()

    def rotate_image(self):
        if not self.has_image():
            return

        self.current_image = self.current_image.rotate(90, expand=True)
        self.filtered_image = self.current_image.copy()
        self.update_final_image()
        self.show_image(self.current_image)

    def apply_adjustments(self):
        if self.filtered_image is None:
            return

        brightness_value = self.brightness_slider.value() / 100
        contrast_value = self.contrast_slider.value() / 100

        edited_image = ImageEnhance.Brightness(self.filtered_image).enhance(brightness_value)
        edited_image = ImageEnhance.Contrast(edited_image).enhance(contrast_value)

        self.current_image = edited_image
        self.brightness_label.setText(f"Brightness: {self.brightness_slider.value()}%")
        self.contrast_label.setText(f"Contrast: {self.contrast_slider.value()}%")

        self.update_final_image()
        self.show_image(self.current_image)

    def reset_image(self):
        if self.original_image is None:
            QMessageBox.warning(self, "No Image", "Please upload an image first.")
            return

        self.filtered_image = self.original_image.copy()
        self.current_image = self.original_image.copy()
        self.reset_sliders()
        self.update_final_image()
        self.show_image(self.current_image)

    def reset_sliders(self):
        self.brightness_slider.blockSignals(True)
        self.contrast_slider.blockSignals(True)

        self.brightness_slider.setValue(100)
        self.contrast_slider.setValue(100)

        self.brightness_slider.blockSignals(False)
        self.contrast_slider.blockSignals(False)

        self.brightness_label.setText("Brightness: 100%")
        self.contrast_label.setText("Contrast: 100%")

    def save_image(self):
        if not self.has_image():
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save edited image", "edited_image.png", "PNG Image (*.png)"
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
        image.thumbnail((680, 360))

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
            pixmap.scaled(680, 360, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )


def create_editor_tab():
    return PhotoEditor()