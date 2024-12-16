from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QHBoxLayout, QStackedWidget
)
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import Qt
import requests

API_URL = "https://sakojadi.pythonanywhere.com"
# API_URL = "http://127.0.0.1:5000"

class MovieDetailWindow(QWidget):
    def __init__(self, movie_info, username):
        super().__init__()
        self.movie_info = movie_info
        self.setWindowTitle(movie_info["title"])
        self.setFixedSize(839, 600)
        self.setStyleSheet("background-color: #101F34;")

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
        back_button = QPushButton("Back")
        back_button.setFixedSize(100, 30)
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
        top_buttons_layout.addSpacing(100)

        seans_button = QPushButton("Add seans")
        seans_button.setFixedSize(100, 30)
        seans_button.setStyleSheet("""
            background-color: #2323A7;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border-radius: 5px;
            border: none;
        """)
        seans_button.clicked.connect(self.open_add_seans_window)
        top_buttons_layout.addWidget(seans_button)
        top_buttons_layout.addSpacing(5)

        # About Button
        about_button = QPushButton("About")
        about_button.setFixedSize(100, 30)
        about_button.setStyleSheet("""
            background-color: #2323A7;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border-radius: 5px;
            border: none;
        """)
        about_button.clicked.connect(self.toggle_about)
        top_buttons_layout.addWidget(about_button)

        sessions_layout.addLayout(top_buttons_layout)

        # Title
        title_label = QLabel(movie_info["title"])
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: white; background-color: transparent;")
        title_label.setAlignment(Qt.AlignLeft)
        sessions_layout.addWidget(title_label)

        # Dynamic Showtimes (Horizontal Layout)
        times_scroll_area = QScrollArea()
        times_scroll_area.setWidgetResizable(True)
        times_scroll_area.setFixedSize(600, 120)
        times_scroll_area.setStyleSheet("""
            QScrollBar:horizontal {
                background: #2323A7;
                height: 10px;
                margin: 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:horizontal {
                background: #4557FF;
                border-radius: 5px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background: none;
                width: 0px;
            }
        """)

        times_container = QWidget()
        times_container.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.5);
            border-radius: 10px;
        """)
        self.times_layout = QHBoxLayout(times_container)
        self.times_layout.setAlignment(Qt.AlignCenter)
        for time in movie_info["times"]:
            self.add_time(time)
            
        times_scroll_area.setWidget(times_container)
        sessions_layout.addWidget(times_scroll_area, alignment=Qt.AlignCenter)
        scroll_layout.addWidget(sessions_container)

        # Price Label
        price_label = QLabel("price : 350")
        price_label.setFont(QFont("Arial", 16))
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
        self.about_text.setGeometry(0,0,800, 600)

        # Save the movie description
        self.movie_description = movie_info.get("description", "No description available.")

    def add_time(self,time):
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
        time_button.clicked.connect(lambda _, t=time: self.book_open(self.movie_info["title"], t, self.username, self.movie_info['id']))
        self.times_layout.addWidget(time_button)

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

    def open_add_seans_window(self):
        from addseans import AddSeansWindow
        self.add_seans_window = AddSeansWindow(self.movie_info['id'])
        self.add_seans_window.new_seans_added.connect(self.update_seans_list)
        self.add_seans_window.show()


    def update_seans_list(self, time):
        """Обновление списка сеансов."""
        # Добавляем новую кнопку с сеансом
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
        time_button.clicked.connect(lambda _, t=time: self.book_open(self.movie_info["title"], t, self.username, self.movie_info['id']))
        self.times_layout.addWidget(time_button)  # Добавляем кнопку в текущий layout

