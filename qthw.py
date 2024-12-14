from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QGridLayout, QHBoxLayout, QMessageBox, QLineEdit, QFileDialog, QDialog
)
from PyQt5.QtGui import QPixmap, QFont, QPalette, QBrush
from PyQt5.QtCore import Qt, pyqtSignal
import sys
import requests
from profil import PersonalCabinet

API_URL = "https://sakojadi.pythonanywhere.com"


class MovieWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Movies")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #101F34;")  # Dark gray background
        self.username = username 
        self.movie_data = []

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)  # Center-align everything in the main layout

        # Header layout (title and add button)
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)

        # Profile button
        profile_button = QPushButton("Profile")
        profile_button.setFixedSize(100, 40)
        profile_button.setStyleSheet(
            "background-color: #1C3AA9; color: white; font-size: 14px; border-radius: 10px; border: none;"
        )
        profile_button.clicked.connect(self.open_profile_window)
        header_layout.addWidget(profile_button)
        header_layout.addSpacing(100)

        # Title
        title_label = QLabel("MOVIES")
        title_label.setFont(QFont("Arial", 36, QFont.Bold))
        title_label.setStyleSheet("color: white; text-align:center")
        header_layout.addWidget(title_label)
        header_layout.addSpacing(100)

        # Add button
        add_button = QPushButton("Add")
        add_button.setFixedSize(100, 40)
        add_button.setStyleSheet(
            "background-color: #1C3AA9; color: white; font-size: 14px; border-radius: 10px; border: none;"
        )
        add_button.clicked.connect(self.open_add_movie_window)
        header_layout.addWidget(add_button)

        main_layout.addLayout(header_layout)
        main_layout.addSpacing(20)

        # Scroll area for movie posters
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedSize(740, 500)
        scroll_area.setStyleSheet("border: none; background-color: #101F34;")
        scroll_area.setAlignment(Qt.AlignCenter)

        # Movies container
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: rgba(0, 0, 0, 0.88); border-radius: 15px;")

        central_layout = QVBoxLayout(scroll_content)
        central_layout.setAlignment(Qt.AlignCenter)

        # Movie grid
        self.movies_layout = QGridLayout()
        self.movies_layout.setAlignment(Qt.AlignCenter)
        self.movies_layout.setHorizontalSpacing(20)
        self.movies_layout.setVerticalSpacing(20)

        central_layout.addLayout(self.movies_layout)
        scroll_area.setWidget(scroll_content)

        main_layout.addWidget(scroll_area)
        main_layout.addSpacing(20)
        self.setLayout(main_layout)

        # Fetch movies (mock for demonstration)
        self.fetch_movies()

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
            movie_button.setStyleSheet("border: 0; background-color: black;")
            movie_button.clicked.connect(lambda checked, m=movie: self.show_movie_details(m))

            # Display image using URL
            pixmap = QPixmap()
            movie_label = QLabel(movie_button)
            image_url = f"{API_URL}{movie['image']}"
            image_data = requests.get(image_url).content

            if pixmap.loadFromData(image_data):
                movie_label.setPixmap(pixmap.scaled(150, 200, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
            else:
                movie_label.setText("Ошибка загрузки изображения")
                print(f"Не удалось загрузить изображение: {image_url}")

            # Overlay for title
            overlay = QLabel(movie_button)
            overlay.setText(movie["title"])
            overlay.setFont(QFont("Arial", 10, QFont.Bold))
            overlay.setStyleSheet("color: white; background-color: rgba(63, 78, 133, 1); padding: 5px;border-radius: 0;")
            overlay.setAlignment(Qt.AlignCenter)
            overlay.setFixedHeight(30)
            overlay.setFixedWidth(150)
            overlay.move(0, 190)

            self.movies_layout.addWidget(movie_button, i // 4, i % 4)

    def show_movie_details(self, movie):
        from detaiwin import MovieDetailWindow
        # Open the MovieDetailWindow with the selected movie details
        self.movie_detail_window = MovieDetailWindow(movie, self.username)
        self.movie_detail_window.show()
        self.close()

    def open_profile_window(self):
        self.profile_window = PersonalCabinet(self.username)
        self.profile_window.show()


    def open_add_movie_window(self):
        from addmovie import AddMovieWindow
        self.add_movie_window = AddMovieWindow()
        self.add_movie_window.new_movie_added.connect(self.fetch_movies)
        self.add_movie_window.exec()

    # def add_movie_to_list(self, movie):
    #     self.movie_data.append(movie)
    #     self.update_movie_list()