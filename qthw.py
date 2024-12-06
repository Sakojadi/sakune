from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QGridLayout, QHBoxLayout, QMessageBox, QLineEdit, QFileDialog, QDialog
)
from PyQt5.QtGui import QPixmap, QFont, QPalette, QBrush
from PyQt5.QtCore import Qt, pyqtSignal
import sys
import requests
from profil import PersonalCabinet


API_URL = "https://sakojadi.pythonanywhere.com"

class MovieDetailWindow(QWidget):
    def __init__(self, movie_info, username):
        super().__init__()
        self.setWindowTitle(movie_info["title"])
        self.setFixedSize(800, 600)
        self.username = username

        # Dynamically load the background image
        background_url = movie_info.get("background", "default_background.jpg")
        background_pixmap = QPixmap()
        background_pixmap.loadFromData(requests.get(f"{API_URL}{background_url}").content)

        self.background_label = QLabel(self)
        self.background_label.setPixmap(
            background_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        )
        self.background_label.setGeometry(0, 0, 800, 600)

        # Poluprozrachnyy overlay
        self.overlay = QLabel(self)
        self.overlay.setGeometry(0, 0, 800, 600)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Black container for content
        content_container = QWidget()
        content_container.setStyleSheet("background-color: rgba(0, 0, 0, 0.8); border-radius: 15px;")
        content_container.setFixedSize(400, 340)

        container_layout = QVBoxLayout()
        container_layout.setAlignment(Qt.AlignCenter)

        # Movie Title
        title_label = QLabel(movie_info["title"])
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        title_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(title_label)

        # Dynamic Showtimes
        print(movie_info)
        for time in movie_info["times"]:
            time_button = QPushButton(time)
            time_button.setFixedSize(100, 40)
            time_button.setStyleSheet("background-color: #2323A7; color: white; font-size: 14px; border-radius: 10px; border: none;")
            container_layout.addWidget(time_button, alignment=Qt.AlignCenter)
            time_button.clicked.connect(lambda _, t=time: self.book_open(movie_info["title"], t, self.username, movie_info['id']))

        # Back Button
        back_button = QPushButton("назад")
        back_button.setFixedSize(100, 40)
        back_button.setStyleSheet("background-color: #A72323; color: white; font-size: 14px; border-radius: 10px; border: none;")
        back_button.clicked.connect(self.back_to)
        container_layout.addWidget(back_button, alignment=Qt.AlignCenter)

        content_container.setLayout(container_layout)
        main_layout.addWidget(content_container)

        self.setLayout(main_layout)
        
    def back_to(self, username):
        win = MovieWindow(self.username)
        win.show()
        self.close()
        
    def book_open(self, movie_title, movie_time, username, m_id):
        from book import SeatSelectionWindow
        self.seat_selection_window = SeatSelectionWindow(movie_title, movie_time, username, m_id)
        self.seat_selection_window.show()



class MovieWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Movies")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #1E1E1E;")  # Dark gray background
        self.username = username 
        self.movie_data = []
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        # Header layout (title and add button)
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignTop)
        # Profile button
        profile_button = QPushButton("profile")
        profile_button.setFixedSize(100, 40)
        profile_button.setStyleSheet(
            "background-color: #2323A7; color: white; font-size: 14px; border-radius: 10px; border: none;"
        )
        profile_button.clicked.connect(self.open_profile_window)
        header_layout.addWidget(profile_button)


        # Title
        title_label = QLabel("MOVIES")
        title_label.setFont(QFont("Arial", 36, QFont.Bold))
        title_label.setStyleSheet("color: white; text-align:center")
        header_layout.addWidget(title_label)
        header_layout.setAlignment(title_label, Qt.AlignCenter)


        # Spacer
        header_layout.addStretch()
        
        # Add button
        add_button = QPushButton("add")
        add_button.setFixedSize(100, 40)
        add_button.setStyleSheet(
            "background-color: #2323A7; color: white; font-size: 14px; border-radius: 10px; border: none;"
        )
        add_button.clicked.connect(self.open_add_movie_window)
        header_layout.addWidget(add_button)
        main_layout.addLayout(header_layout)

        # Scroll area for movie posters
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")

        # Movies container (grid layout)
        scroll_content = QWidget()
        central_layout = QVBoxLayout(scroll_content)
        central_layout.setAlignment(Qt.AlignCenter)

        self.movies_layout = QGridLayout()
        self.movies_layout.setAlignment(Qt.AlignCenter)
        self.movies_layout.setHorizontalSpacing(20)
        self.movies_layout.setVerticalSpacing(20)
        
        self.setLayout(main_layout)
        self.fetch_movies() 

        # Add movies_layout to central_layout
        central_layout.addLayout(self.movies_layout)
        scroll_area.setWidget(scroll_content)

        # Add scroll area to the main layout
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)
        
    def fetch_movies(self):
        response = requests.get(f"{API_URL}/movies")
        if response.status_code == 200:
            self.movie_data = response.json()["movies"]  # Access the list properly
            self.update_movie_list()
        else:
            print("Failed to fetch movies")

    def update_movie_list(self):
        while self.movies_layout.count():
            child = self.movies_layout.takeAt(0).widget()
            if child:
                child.deleteLater()

        for i, movie in enumerate(self.movie_data):
            movie_button = QPushButton()
            movie_button.setFixedSize(150, 220)
            movie_button.setStyleSheet("border: none; background-color: black;")
            movie_button.clicked.connect(lambda checked, m=movie: self.show_movie_details(m))

            # Display image using URL
            pixmap = QPixmap()
            pixmap.loadFromData(requests.get(f"{API_URL}{movie['image']}").content)
            movie_label = QLabel(movie_button)
            movie_label.setPixmap(pixmap.scaled(150, 200, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

            # Overlay for title
            overlay = QLabel(movie_button)
            overlay.setText(movie["title"])
            overlay.setFont(QFont("Arial", 10, QFont.Bold))
            overlay.setStyleSheet("color: white; background-color: rgba(21, 8, 142, 0.7); padding: 5px;")
            overlay.setAlignment(Qt.AlignCenter)
            overlay.setFixedHeight(30)
            overlay.setFixedWidth(150)
            overlay.move(0, 190)

            self.movies_layout.addWidget(movie_button, i // 4, i % 4)

    def show_movie_details(self, movie):
        # Open the MovieDetailWindow with the selected movie details
        self.movie_detail_window = MovieDetailWindow(movie, self.username)
        self.movie_detail_window.show()
        self.close()

    def open_profile_window(self):
        self.profile_window = PersonalCabinet(self.username)
        self.profile_window.show()


    def open_add_movie_window(self):
        self.add_movie_window = AddMovieWindow()
        self.add_movie_window.new_movie_added.connect(self.add_movie_to_list)
        self.add_movie_window.exec()

    def add_movie_to_list(self, movie_data):
        self.movie_data.append(movie_data)
        self.update_movie_list()

    def add_movie_to_list(self, movie_data):
        self.movie_data.append(movie_data)
        self.update_movie_list()

class AddMovieWindow(QDialog):
    new_movie_added = pyqtSignal(dict)
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
                "background": bg_response.json()["url"]
            }
            response = requests.post(f"{API_URL}/add_movie", json=movie_data)
            if response.status_code == 200:
                QMessageBox.information(self, "Успех", "Фильм успешно добавлен")
                self.new_movie_added.emit(movie_data)
                self.close()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось добавить фильм")
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить изображение")