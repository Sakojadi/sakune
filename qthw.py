from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QHBoxLayout, QMessageBox, QDialog, QSpacerItem, QSizePolicy,QGridLayout, QScrollArea
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import sys
import requests

API_URL = "http://127.0.0.1:5000" 

class MovieWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Movies")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #1E1E1E;")  # Dark gray background

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        # Header layout (title and add button)
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignTop)

        # Title
        title_label = QLabel("MOVIES")
        title_label.setFont(QFont("Arial", 36, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        header_layout.addWidget(title_label)

        # Spacer
        header_layout.addStretch()

        # Add button
        add_button = QPushButton("добавить")
        add_button.setFixedSize(100, 40)
        add_button.setStyleSheet(
            "background-color: #2323A7; color: white; font-size: 14px; border-radius: 10px; border: none;"
        )
        header_layout.addWidget(add_button)
        main_layout.addLayout(header_layout)

        # Scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")

        # Movies container
        scroll_content = QWidget()
        central_layout = QVBoxLayout(scroll_content)
        central_layout.setAlignment(Qt.AlignCenter)  # Центрирование фильмов

        movies_layout = QGridLayout()
        movies_layout.setAlignment(Qt.AlignCenter)  # Центрирование внутри сетки
        movies_layout.setHorizontalSpacing(20)
        movies_layout.setVerticalSpacing(20)

        # Movie data: (image_path, title)
        movies = [
            ("gladiator.jpg", "гладиатор 2"),
            ("beggining.jpg", "начало последствий"),
            ("images.jpg", "моана 2: возвращение"),
            ("red.jpg", "красный дракон"),
            ("red.jpg", "огненный шторм"),
            ("red.jpg", "красный рассвет"),
            ("gladiator.jpg", "гладиатор 2: судьба Рима"),
            ("beggining.jpg", "начало новой эры"),
            ("images.jpg", "моана 2: новые горизонты"),
        ]

        for i, (image, title) in enumerate(movies):
            # Movie container (image + title combined)
            movie_container = QLabel()
            movie_container.setFixedSize(150, 220)
            movie_container.setStyleSheet("border-radius: 10px; overflow: hidden; background-color: black;")
            
            # Add poster
            pixmap = QPixmap(image).scaled(150, 200, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            movie_container.setPixmap(pixmap)
            movie_container.setAlignment(Qt.AlignBottom)

            # Overlay for title
            overlay = QLabel(movie_container)
            overlay.setText(title)
            overlay.setFont(QFont("Arial", 10, QFont.Bold))
            overlay.setStyleSheet(
                "color: white; background-color: rgba(0, 0, 0, 0.7); padding: 5px; border-radius: 0px;"
            )
            overlay.setAlignment(Qt.AlignCenter)
            overlay.setFixedHeight(30)  # Fix height for the overlay
            overlay.setFixedWidth(movie_container.width())
            overlay.move(0, movie_container.height() - overlay.height())

            # Add to grid
            movies_layout.addWidget(movie_container, i // 4, i % 4)

        # Add movies_layout to central_layout
        central_layout.addLayout(movies_layout)
        scroll_area.setWidget(scroll_content)

        # Add scroll area to the main layout
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def book_ticket(self, movie, time):
        QMessageBox.information(self, "Booking", f"Selected {movie['title']} at {time}")
        # Placeholder: Booking logic can go here!