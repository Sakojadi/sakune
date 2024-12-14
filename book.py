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
from PyQt5.QtCore import Qt
import requests

API_URL = "https://sakojadi.pythonanywhere.com"
# API_URL = "http://127.0.0.1:5000"


class SeatSelectionWindow(QMainWindow):
    def __init__(self, movie_title, movie_time, username, m_id):
        super().__init__()
        self.movie_title = movie_title
        self.movie_time = movie_time
        self.username = username
        self.selected_seats = []
        self.movie_id = m_id
        self.bought_seats, self.user_bought = self.fetch_booked_seats()

        self.setWindowTitle(f"{self.movie_title} - {self.movie_time}")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #1e1e1e;")

        self.initUI()

    def fetch_booked_seats(self):
        try:
            # Fetch all booked seats
            response = requests.get(
                f"{API_URL}/get_booked_seats",
                params={"movie_id": self.movie_id, "time": self.movie_time}
            )
            response.raise_for_status()
            data = response.json()

            booked_seats = []
            for user_seats in data.get("booked_seats", {}).values():
                booked_seats.extend(user_seats)

            # Fetch user-specific booked seats
            res = requests.get(
                f"{API_URL}/get_my_booked",
                params={"movie_id": self.movie_id, "time": self.movie_time, "buyers": self.username}
            )
            res.raise_for_status()
            user_data = res.json()
            user_bought = user_data.get("user_bought", [])
            return booked_seats, user_bought

        except requests.exceptions.RequestException as e:
            print(f"API error: {e}")
            return [], []
        except ValueError as e:
            print(f"JSON error: {e}")
            return [], []

    def initUI(self):
        layout = QVBoxLayout()
        hl = QHBoxLayout()
        hl.setAlignment(Qt.AlignTop)
        # Back button (top left)
        back_button = QPushButton("back")
        back_button.setFixedSize(100, 30)
        back_button.setStyleSheet(
            "background-color: #1C3AA9; color: white; font-size: 10px; border: none; border-radius: 5px;"
        )
        back_button.clicked.connect(self.go_back)
        hl.addWidget(back_button)
        hl.addSpacing(200)
        
        # Title and time
        name_layout = QVBoxLayout()
        title_label = QLabel(f"{self.movie_title}")
        time_label = QLabel(f"{self.movie_time}")
        title_label.setAlignment(Qt.AlignCenter)
        time_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white; font-size: 24px; padding: 10px;")
        time_label.setStyleSheet("color: white; font-size: 18px; padding: 5px;")
        name_layout.addWidget(title_label)
        name_layout.addWidget(time_label)

        hl.addLayout(name_layout)
        hl.addSpacing(200)
        

        legend_layout = QVBoxLayout()
        legend_item_1 = QHBoxLayout()
        empty_square = QLabel()
        empty_square.setFixedSize(20, 20)
        empty_square.setStyleSheet("background-color: lightblue; border-radius: 5px;")
        empty_label = QLabel("Empty")
        empty_label.setStyleSheet("color: white;")
        legend_item_1.addWidget(empty_square)
        legend_item_1.addWidget(empty_label)

        # Legend (bottom left)
        legend_layout = QVBoxLayout()
        legend_item_2 = QHBoxLayout()
        booked_square = QLabel()
        booked_square.setFixedSize(20, 20)
        booked_square.setStyleSheet("background-color: #3F4E85; border-radius: 5px;")
        booked_label = QLabel("Booked")
        booked_label.setStyleSheet("color: white;")
        legend_item_2.addWidget(booked_square)
        legend_item_2.addWidget(booked_label)

        legend_layout = QVBoxLayout()
        legend_item_3 = QHBoxLayout()
        your_square = QLabel()
        your_square.setFixedSize(20, 20)
        your_square.setStyleSheet("background-color: #B27272; border-radius: 5px;")
        your_label = QLabel("Your seats")
        your_label.setStyleSheet("color: white;")
        legend_item_3.addWidget(your_square)
        legend_item_3.addWidget(your_label)

        legend_layout.addLayout(legend_item_1)
        legend_layout.addLayout(legend_item_2)
        legend_layout.addLayout(legend_item_3)

        hl.addLayout(legend_layout)
        layout.addLayout(hl)

        # Seat grid
        self.grid_layout = QGridLayout()
        rows, cols = 8, 10
        for row in range(rows):
            for col in range(cols):
                btn = QPushButton()
                btn.setFixedSize(30, 30)
                if [row, col] in self.user_bought:
                    btn.setStyleSheet("background-color: #B27272; border-radius: 5px;")
                    btn.setEnabled(False)
                elif [row, col] in self.bought_seats:
                    btn.setStyleSheet("background-color: #3F4E85; border-radius: 5px;")
                    btn.setEnabled(False)
                else:
                    btn.setStyleSheet("background-color: lightblue; border-radius: 5px;")
                btn.clicked.connect(lambda _, r=row, c=col: self.toggle_seat(r, c))
                self.grid_layout.addWidget(btn, row, col)

        layout.addLayout(self.grid_layout)
        layout.addSpacing(60)

        

        


        # layout.addLayout(legend_layout)
        
        # Book button
        self.book_button = QPushButton("BOOK")
        self.book_button.setFixedHeight(30)
        self.book_button.setStyleSheet(
            "background-color: #1C3AA9; color: white; font-size: 10px; border: none; border-radius: 5px;"
        )
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
                    "movie_id": self.movie_id,
                    "time": self.movie_time,
                    "seats": self.selected_seats,
                },
            )
            response.raise_for_status()

            data = response.json()
            if response.status_code == 200:
                print(data.get("message", "Tickets booked successfully."))
                for seat in self.selected_seats:
                    btn = self.grid_layout.itemAtPosition(*seat).widget()
                    btn.setStyleSheet("background-color: #B27272; border-radius: 5px;")
                    btn.setEnabled(False)
                self.selected_seats.clear()
            else:
                print(f"Failed to book tickets: {data.get('error', 'Unknown error')}")

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

    def go_back(self):
        self.close()
