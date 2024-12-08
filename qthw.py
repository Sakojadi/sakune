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

