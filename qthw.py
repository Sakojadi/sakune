from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QGridLayout, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QFont, QPalette, QBrush
from PyQt5.QtCore import Qt
import sys


class MovieDetailWindow(QWidget):
    def __init__(self, movie_info):
        super().__init__()
        self.setWindowTitle(movie_info["title"])
        self.setFixedSize(800, 600)

        # Manually set the background image based on the movie title
        backgrounds = {
            "гладиатор 2": "images.jpg",
            "начало последствий": "background_beggining.jpg",
            "моана 2: возвращение": "background_moana.jpg",
            "красный дракон": "background_red_dragon.jpg",
            "огненный шторм": "background_firestorm.jpg",
            "красный рассвет": "background_red_dawn.jpg",
            "гладиатор 2: судьба Рима": "background_gladiator_fate.jpg",
            "начало новой эры": "background_new_era.jpg",
            "моана 2: новые горизонты": "background_moana_horizons.jpg",
        }
        background_image = backgrounds.get(movie_info["title"], "default_background.jpg")

        # Фоновое изображение
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap(background_image).scaled(
            self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        ))
        self.background_label.setGeometry(0, 0, 800, 600)

        # Полупрозрачный затемняющий слой
        self.overlay = QLabel(self)
        self.overlay.setGeometry(0, 0, 800, 600)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")

        # Main layout for the detail window
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Black rectangle container
        content_container = QWidget()
        content_container.setStyleSheet(
            "background-color: rgba(0, 0, 0, 0.8); border-radius: 15px;")
        content_container.setFixedSize(400, 340)  # Adjust dimensions as needed

        container_layout = QVBoxLayout()
        container_layout.setAlignment(Qt.AlignCenter)

        # Movie title
        title_label = QLabel(movie_info["title"])
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: white;")  # Remove padding and background
        title_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(title_label)

        # Show available times
        times = ["12:00", "14:00", "16:30", "20:00"]
        for time in times:
            time_button = QPushButton(time)
            time_button.setFixedSize(100, 40)
            time_button.setStyleSheet(
                "background-color: #2323A7; color: white; font-size: 14px; border-radius: 10px; border: none;"
            )
            container_layout.addWidget(time_button, alignment=Qt.AlignCenter)

        # Back button
        back_button = QPushButton("назад")
        back_button.setFixedSize(100, 40)
        back_button.setStyleSheet(
            "background-color: #A72323; color: white; font-size: 14px; border-radius: 10px; border: none;"
        )
        back_button.clicked.connect(self.close)
        container_layout.addWidget(back_button, alignment=Qt.AlignCenter)

        content_container.setLayout(container_layout)
        main_layout.addWidget(content_container)

        self.setLayout(main_layout)



class MovieWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Movies")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #1E1E1E;")  # Dark gray background
        self.username = username 
        
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
        central_layout.setAlignment(Qt.AlignCenter)

        movies_layout = QGridLayout()
        movies_layout.setAlignment(Qt.AlignCenter)
        movies_layout.setHorizontalSpacing(20)
        movies_layout.setVerticalSpacing(20)

        # Movie data: (image_path, title)
        self.movies = [
            {"image": "gladiator.jpg", "title": "гладиатор 2"},
            {"image": "beggining.jpg", "title": "начало последствий"},
            {"image": "moana.jpg", "title": "моана 2: возвращение"},
            {"image": "red.jpg", "title": "красный дракон"},
            {"image": "red.jpg", "title": "огненный шторм"},
            {"image": "red.jpg", "title": "красный рассвет"},
            {"image": "gladiator.jpg", "title": "гладиатор 2: судьба Рима"},
            {"image": "beggining.jpg", "title": "начало новой эры"},
            {"image": "moana.jpg", "title": "моана 2: новые горизонты"},
        ]

        for i, movie in enumerate(self.movies):
            # Movie button (image + title combined)
            movie_button = QPushButton()
            movie_button.setFixedSize(150, 220)
            movie_button.setStyleSheet("border: none; background-color: black;")
            movie_button.clicked.connect(lambda checked, m=movie: self.open_movie_detail(m))

            # Add poster
            pixmap = QPixmap(movie["image"]).scaled(150, 200, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            movie_label = QLabel(movie_button)
            movie_label.setPixmap(pixmap)
            movie_label.setAlignment(Qt.AlignCenter)

            # Overlay for title
            overlay = QLabel(movie_button)
            overlay.setText(movie["title"])
            overlay.setFont(QFont("Arial", 10, QFont.Bold))
            overlay.setStyleSheet(
                "color: white; background-color: rgba(0, 0, 0, 0.7); padding: 5px;"
            )
            overlay.setAlignment(Qt.AlignCenter)
            overlay.setFixedHeight(30)
            overlay.setFixedWidth(150)
            overlay.move(0, 190)

            # Add to grid
            movies_layout.addWidget(movie_button, i // 4, i % 4)

        # Add movies_layout to central_layout
        central_layout.addLayout(movies_layout)
        scroll_area.setWidget(scroll_content)

        # Add scroll area to the main layout
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def open_movie_detail(self, movie):
        self.detail_window = MovieDetailWindow(movie)
        self.detail_window.show()

