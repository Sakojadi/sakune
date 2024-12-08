from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QGridLayout, QHBoxLayout, QMessageBox, QLineEdit, QFileDialog, QDialog
)
from PyQt5.QtGui import QPixmap, QFont, QPalette, QBrush
from PyQt5.QtCore import Qt, pyqtSignal
import sys
import requests
from profil import PersonalCabinet
from qthw import MovieWindow
API_URL = "https://sakojadi.pythonanywhere.com"

class AddMovieWindow(QDialog):
    new_movie_added = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить фильм")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: #232527;")

        # Layout for adding movie
        layout = QVBoxLayout()

        # Movie Title
        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("Название фильма")
        self.title_input.setFixedSize(295, 40)
        self.title_input.setStyleSheet(
            "background-color: #FFFFFF; color: black; font-size: 16px; border: none; border-radius: 5px; padding-left: 10px;"
        )
        layout.addWidget(self.title_input)

        # Upload image button
        self.upload_button = QPushButton("Загрузить изображение")
        self.upload_button.clicked.connect(self.upload_image)
        self.upload_button.setFixedSize(295, 40)
        self.upload_button.setStyleSheet(
            "background-color: #2323A7; color: white; font-size: 16px; border: none; border-radius: 5px;"
        )
        layout.addWidget(self.upload_button)
        
        self.background_button = QPushButton("Загрузить фоновое изоброжение")
        self.background_button.clicked.connect(self.upload_background)
        self.background_button.setFixedSize(295, 40)
        self.background_button.setStyleSheet(
            "background-color: #2323A7; color: white; font-size: 16px; border: none; border-radius: 5px;"
        )
        layout.addWidget(self.background_button)

        # Add movie button
        self.add_button = QPushButton("Добавить фильм")
        self.add_button.clicked.connect(self.add_movie)
        self.add_button.setFixedSize(295, 40)
        self.add_button.setStyleSheet(
            "background-color: #2323A7; color: white; font-size: 16px; border: none; border-radius: 5px;"
        )
        layout.addWidget(self.add_button)
        
        
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

    def add_movie(self):
        # Send movie data and image path to the Flask API
        movie_title = self.title_input.text()
        if movie_title and hasattr(self, "image_path"):
            # Send movie data to the Flask API
            self.upload_movie_to_api(movie_title)
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля")

    def upload_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Images (*.png *.jpg *.bmp)")
        if file_name:
            self.image_path = file_name
    
    def upload_background(self):
        bg_file_name, _ = QFileDialog.getOpenFileName(self, "Выберите фоновое изображение", "", "Images (*.png *.jpg *.bmp)")
        if bg_file_name:
            self.background_image_path = bg_file_name

    def upload_movie_to_api(self, movie_title):
        with open(self.image_path, 'rb') as img_file:
            image_data = {'file': img_file}
            img_response = requests.post(f"{API_URL}/upload_image", files=image_data)

        with open(self.background_image_path, 'rb') as bg_file:
            bg_data = {'file': bg_file}
            bg_response = requests.post(f"{API_URL}/upload_image", files=bg_data)

        if img_response.status_code == 200 and bg_response.status_code == 200:
            movie_data = {
                "title": movie_title,
                "image": img_response.json()["url"],
                "background": bg_response.json()["url"],
            }

            # Отправляем данные фильма в API
            response = requests.post(f"{API_URL}/add_movie", json=movie_data)

            if response.status_code == 200:
                self.new_movie_added.emit()  # Отправляем весь объект фильма
                self.close()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось добавить фильм")
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить изображение")
