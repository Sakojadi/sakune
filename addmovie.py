from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QFileDialog, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, pyqtSignal
import requests

API_URL = "https://sakojadi.pythonanywhere.com"
# API_URL = "http://127.0.0.1:5000"


class AddMovieWindow(QDialog):
    new_movie_added = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Movie")
        self.setFixedSize(400, 500)
        self.setStyleSheet("background-color: #101F34;")

        # Layout for adding movie
        layout = QVBoxLayout()
        self.header_label = QLabel("ADD MOVIES", self)
        self.header_label.setFont(QFont("RocknRoll One", 32))
        self.header_label.setStyleSheet("color: white;")
        self.header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.header_label)
        layout.addSpacing(10)

        # Movie Title
        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("movie name")
        self.title_input.setFixedSize(307, 34)
        self.title_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #FFFFFF;
                border-radius: 15px;
                background-color: #101F34;
                color: white;
                padding-left: 10px;
                height: 40px;
            }
        """)
        layout.addWidget(self.title_input)
        layout.addSpacing(10)

        self.seans_input = QLineEdit(self)
        self.seans_input.setPlaceholderText("seans")
        self.seans_input.setFixedSize(307, 34)
        self.seans_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #FFFFFF;
                border-radius: 15px;
                background-color: #101F34;
                color: white;
                padding-left: 10px;
                height: 40px;
            }
        """)
        layout.addWidget(self.seans_input)
        layout.addSpacing(10)


        # Movie Description
        self.description_input = QTextEdit(self)
        self.description_input.setPlaceholderText("description")
        self.description_input.setFixedSize(307, 74)
        self.description_input.setStyleSheet("""
            QTextEdit {
                border: 2px solid #FFFFFF;
                border-radius: 15px;
                background-color: #101F34;
                color: white;
                padding-left: 10px;
                height: 40px;
            }
        """)
        layout.addWidget(self.description_input)
        layout.addSpacing(10)


        # Horizontal layout for image and background
        horizontal_layout = QHBoxLayout()

        # Image placeholder (for movie image)
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(150, 150)
        self.image_label.setStyleSheet("background-color: #3C3F41; border: 2px dashed #FFFFFF;")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setText("Add poster")
        self.image_label.setFont(QFont("Arial", 10))
        self.image_label.mousePressEvent = self.upload_image
        horizontal_layout.addWidget(self.image_label)

        # Background image placeholder
        self.background_label = QLabel(self)
        self.background_label.setFixedSize(150, 150)
        self.background_label.setStyleSheet("background-color: #3C3F41; border: 2px dashed #FFFFFF;")
        self.background_label.setAlignment(Qt.AlignCenter)
        self.background_label.setText("Add background")
        self.background_label.setFont(QFont("Arial", 10))
        self.background_label.mousePressEvent = self.upload_background
        horizontal_layout.addWidget(self.background_label)

        layout.addLayout(horizontal_layout)
        layout.addSpacing(10)


        # Add movie button
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_movie)
        self.add_button.setFixedSize(295, 40)
        self.add_button.setStyleSheet(
            "background-color: #2323A7; color: white; font-size: 16px; border: none; border-radius: 5px;"
        )
        layout.addWidget(self.add_button)

        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

    def upload_image(self, event):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Images (*.png *.jpg *.bmp)")
        if file_name:
            self.image_path = file_name
            pixmap = QPixmap(file_name).scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)

    def upload_background(self, event):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите фоновое изображение", "", "Images (*.png *.jpg *.bmp)")
        if file_name:
            self.background_image_path = file_name
            pixmap = QPixmap(file_name).scaled(self.background_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.background_label.setPixmap(pixmap)

    def add_movie(self):
        movie_title = self.title_input.text()
        movie_description = self.description_input.toPlainText()
        seans = self.seans_input.text()
        if movie_title and movie_description and hasattr(self, "image_path") and hasattr(self, "background_image_path"):
            self.upload_movie_to_api(movie_title, movie_description, seans)
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля и добавьте изображения")

    def upload_movie_to_api(self, movie_title, movie_description, seans):
        with open(self.image_path, 'rb') as img_file:
            image_data = {'file': img_file}
            img_response = requests.post(f"{API_URL}/upload_image", files=image_data)

        with open(self.background_image_path, 'rb') as bg_file:
            bg_data = {'file': bg_file}
            bg_response = requests.post(f"{API_URL}/upload_image", files=bg_data)

        if img_response.status_code == 200 and bg_response.status_code == 200:
            times = str(seans).split(",")
            times = [i.strip() for i in times]
            movie_data = {
                "title": movie_title,
                "description": movie_description,
                "times": times,
                "image": img_response.json()["url"],
                "background": bg_response.json()["url"],
            }

            response = requests.post(f"{API_URL}/add_movie", json=movie_data)

            if response.status_code == 200:
                self.new_movie_added.emit()
                self.close()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось добавить фильм")
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить изображение")
