from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QHBoxLayout, QStackedWidget
)
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import Qt
import requests

API_URL = "https://sakojadi.pythonanywhere.com"

class MovieDetailWindow(QWidget):
    def __init__(self, movie_info, username):
        super().__init__()
        self.setWindowTitle(movie_info["title"])
        self.setFixedSize(839, 600)
        self.username = username

        # Main Scrollable Area (Vertical Scroll Only)
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollBar:vertical {
                background: #2323A7;
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #4557FF;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                height: 0px;
            }
        """)

        # Scrollable content container
        scroll_content = QWidget()
        scroll_content.setFixedWidth(800)  # Fix width to avoid horizontal scrolling
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setAlignment(Qt.AlignTop)
        scroll_layout.setContentsMargins(0, 0, 0, 0)  # Remove extra margins
        scroll_layout.setSpacing(0)  # Remove spacing between elements

        # Dynamically load the background image
        background_url = movie_info.get("background", "default_background.jpg")
        background_pixmap = QPixmap()
        background_pixmap.loadFromData(requests.get(f"{API_URL}{background_url}").content)

        # Background Label
        self.background_label = QLabel()
        self.background_label.setPixmap(
            background_pixmap.scaled(800, 600, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        )
        self.background_label.setFixedSize(800, 600)
        scroll_layout.addWidget(self.background_label)

        # "Sessions" Section
        sessions_container = QWidget()
        sessions_layout = QVBoxLayout(sessions_container)
        sessions_container.setStyleSheet("background-color: #101F34;")
        sessions_container.setFixedWidth(800)
        sessions_container.setFixedHeight(310)  # Set height to 310
        sessions_layout.setContentsMargins(20, 20, 20, 0)  # Add space at the top

        # Top Row (Back and About Buttons)
        top_buttons_layout = QHBoxLayout()
        top_buttons_layout.setAlignment(Qt.AlignTop)

        # Back Button
        back_button = QPushButton("назад")
        back_button.setFixedSize(100, 40)
        back_button.setStyleSheet("""
            background-color: #2323A7;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border-radius: 5px;
            border: none;
        """)
        back_button.clicked.connect(self.back_to)
        top_buttons_layout.addWidget(back_button, alignment=Qt.AlignLeft)

        # About Button
        about_button = QPushButton("About")
        about_button.setFixedSize(100, 40)
        about_button.setStyleSheet("""
            background-color: #2323A7;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border-radius: 5px;
            border: none;
        """)
        about_button.clicked.connect(self.toggle_about)
        top_buttons_layout.addWidget(about_button, alignment=Qt.AlignRight)

        sessions_layout.addLayout(top_buttons_layout)

        # Title
        title_label = QLabel(movie_info["title"])
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: white; background-color: transparent;")
        title_label.setAlignment(Qt.AlignLeft)
        sessions_layout.addWidget(title_label)

        # Dynamic Showtimes (Horizontal Layout)
        times_container = QWidget()
        times_container.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.5);
            border-radius: 10px;
        """)
        times_container.setFixedWidth(650)
        times_container.setFixedHeight(120)
        times_layout = QHBoxLayout(times_container)
        times_layout.setAlignment(Qt.AlignCenter)

        for time in movie_info["times"]:
            time_button = QPushButton(time)
            time_button.setFixedSize(110, 25)
            time_button.setStyleSheet("""
                background-color: #2323A7;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 10px;
                border: none;
            """)
            time_button.clicked.connect(lambda _, t=time: self.book_open(movie_info["title"], t, self.username, movie_info['id']))
            times_layout.addWidget(time_button)

        sessions_layout.addWidget(times_container, alignment=Qt.AlignCenter)

        # Price Label
        price_label = QLabel("price :")
        price_label.setFont(QFont("Arial", 14))
        price_label.setStyleSheet("color: white; background-color: transparent;")
        price_label.setAlignment(Qt.AlignLeft)
        sessions_layout.addWidget(price_label)

        scroll_layout.addWidget(sessions_container)

        # Set scroll area content
        scroll_area.setWidget(scroll_content)

        # Main Layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        # Overlay for About Section
        self.about_overlay = QLabel(scroll_content)  # Attach to the scroll_content, not the main window
        self.about_overlay.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.8);
        """)
        self.about_overlay.setAlignment(Qt.AlignTop)
        self.about_overlay.setGeometry(0, 0, 800, 600)  # Position overlay relative to scrollable area
        self.about_overlay.hide()  # Initially hidden

        self.about_text = QLabel(self.about_overlay)  # Use instance variable for dynamic updates
        self.about_text.setFont(QFont("Arial", 16))
        self.about_text.setStyleSheet("color: black; background-color: transparent;")
        self.about_text.setAlignment(Qt.AlignCenter)
        self.about_text.setGeometry(150, 200, 500, 200)

        # Save the movie description
        self.movie_description = movie_info.get("description", "No description available.")

    def toggle_about(self):
        """Toggle the overlay visibility."""
        if self.about_overlay.isVisible():
            self.about_overlay.hide()  # Hide overlay if it's already visible
        else:
            # Update text with the movie description
            self.about_text.setText(f"About this movie:\n{self.movie_description}")
            self.about_overlay.show() 
    def back_to(self):
        from qthw import MovieWindow
        win = MovieWindow(self.username)
        win.show()
        self.close()

    def book_open(self, movie_title, movie_time, username, m_id):
        from book import SeatSelectionWindow
        self.seat_selection_window = SeatSelectionWindow(movie_title, movie_time, username, m_id)
        self.seat_selection_window.show()
