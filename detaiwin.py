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
        from qthw import MovieWindow
        win = MovieWindow(self.username)
        win.show()
        self.close()
        
    def book_open(self, movie_title, movie_time, username, m_id):
        from book import SeatSelectionWindow
        self.seat_selection_window = SeatSelectionWindow(movie_title, movie_time, username, m_id)
        self.seat_selection_window.show()
