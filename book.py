import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QGridLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
    QHBoxLayout
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import requests

API_URL = "https://sakojadi.pythonanywhere.com"

class SeatSelectionWindow(QMainWindow):
    def __init__(self, movie_title, movie_time, username, bought_seats=None):
        super().__init__()
        self.movie_title = movie_title
        self.movie_time = movie_time
        self.username = username
        self.selected_seats = []
        self.bought_seats = bought_seats or []  # List of already booked seats [(row, col), ...]

        self.setWindowTitle(f"{self.movie_title} - {self.movie_time}")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #1e1e1e;")  # Dark background for the window

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Back button (top left)
        back_button = QPushButton("назад")
        back_button.setStyleSheet("background-color: #2a2a2a; color: white; padding: 10px;")
        back_button.clicked.connect(self.go_back)
        
        # Title and time
        title_label = QLabel(f"{self.movie_title}")
        time_label = QLabel(f"{self.movie_time}")
        title_label.setAlignment(Qt.AlignCenter)
        time_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white; font-size: 24px; padding: 10px;")
        time_label.setStyleSheet("color: white; font-size: 18px; padding: 5px;")
        
        layout.addWidget(back_button)
        layout.addWidget(title_label)
        layout.addWidget(time_label)

        # Seat grid
        self.grid_layout = QGridLayout()
        rows, cols = 8, 10
        for row in range(rows):
            for col in range(cols):
                btn = QPushButton()
                btn.setFixedSize(40, 40)
                btn.setStyleSheet("background-color: lightblue; border-radius: 5px;")  # Light blue for available seats
                if (row, col) in self.bought_seats:
                    btn.setStyleSheet("background-color: blue; border-radius: 5px;")  # Blue for bought seats
                    btn.setEnabled(False)
                btn.clicked.connect(lambda _, r=row, c=col: self.toggle_seat(r, c))
                self.grid_layout.addWidget(btn, row, col)

        layout.addLayout(self.grid_layout)

        # Legend (bottom right)
        legend_layout = QVBoxLayout()
        legend_layout.addWidget(QLabel("Занято: синий"), alignment=Qt.AlignLeft)
        legend_layout.addWidget(QLabel("Ваши места: оранжевый"), alignment=Qt.AlignLeft)

        # Book button
        self.book_button = QPushButton("Забронировать")
        self.book_button.setStyleSheet("background-color: #2a2a2a; color: white; padding: 10px;")
        self.book_button.clicked.connect(self.book_tickets)

        layout.addLayout(legend_layout)
        layout.addWidget(self.book_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def toggle_seat(self, row, col):
        seat = (row, col)
        button = self.grid_layout.itemAtPosition(row, col).widget()

        if seat in self.selected_seats:
            button.setStyleSheet("background-color: lightblue; border-radius: 5px;")
            self.selected_seats.remove(seat)
        else:
            button.setStyleSheet("background-color: orange; border-radius: 5px;")
            self.selected_seats.append(seat)

    def book_tickets(self):
        if not self.selected_seats:
            print("No seats selected.")
            return

        try:
            response = requests.post(
                f"{API_URL}/book",
                json={
                    "username": self.username,
                    "movie_id": 1,  # Adjust this ID as needed
                    "time": self.movie_time,
                    "seats": self.selected_seats,
                },
            )
            response.raise_for_status()

            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError:
                print(f"Failed to parse JSON: {response.text}")
                return

            if response.status_code == 200:
                print(data.get("message", "Tickets booked successfully."))
                # Mark seats as booked in UI
                for seat in self.selected_seats:
                    btn = self.grid_layout.itemAtPosition(*seat).widget()
                    btn.setStyleSheet("background-color: blue; border-radius: 5px;")
                    btn.setEnabled(False)
                self.selected_seats.clear()
            else:
                print(f"Failed to book tickets: {data.get('error', 'Unknown error')}")

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

    def go_back(self):
        self.close()
