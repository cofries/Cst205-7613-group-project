import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox,QLineEdit,QFrame)
from PySide6.QtCore import Slot
from PySide6.QtCore import Qt


def save_image(img,save_name):
    folder = os.path.join(os.path.expanduser("~"), "Desktop")
    img.save(os.path.join(folder, f'{save_name}.png'))
    #img.show()

def create_save_tab():

    widget = QWidget()
    widget.setStyleSheet("""
            QWidget {
                background-color: #111827;
                color: white;
                font-family: Arial;
                font-size: 16px;
            }

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

            QLineEdit#name_input{
                background-color: #374151;
                color: white;
                border-radius: 10px;
                padding: 12px;
                font-size: 16px;         
                         
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

        """)

    layout = QVBoxLayout(widget)
    layout.setContentsMargins(50, 40, 50, 40)
    layout.setSpacing(10)

    title = QLabel("Save Image")
    title.setObjectName("title")
    title.setAlignment(Qt.AlignCenter)
         

    subtitle = QLabel("Enter a name and save your meme as a PNG.")
    subtitle.setObjectName("subtitle")
    subtitle.setAlignment(Qt.AlignCenter)
    

    card = QFrame()
    card.setObjectName("card")
    card.setFixedWidth(500)
    card_layout = QVBoxLayout(card)
    card_layout.setSpacing(18)
    

    name_input = QLineEdit()
    name_input.setPlaceholderText("Save As")
    

    

    save_btn = QPushButton("Save")
    save_btn.clicked.connect(lambda:save_clicked(name_input))
    
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
    
    save_name = name_input.text()
    
    if save_name == "":
        QMessageBox.warning(None, "No save name", "Please enter a save name.")
        return
    from tabs.editor import final_img
    if final_img is None:
        QMessageBox.warning (None,"No Image","No Image Found")
    save_image(final_img,save_name)
    QMessageBox.information(None, "Saved", f'Saved as {save_name}.png')






    

