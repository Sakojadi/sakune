from PyQt5.QtWidgets import (
    QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget, QComboBox, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5 import QtCore  
import requests

API_URL = "https://sakojadi.pythonanywhere.com"

class ReportWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reports")
        self.setGeometry(0, 0, 800, 600)
        self.setStyleSheet("background-color: #101F34;")  # Dark gray background 

        self.movies = []  # Store movie list
        self.times = []   # Store times for selected movie
        self.initUI()
        self.load_movies()

    def initUI(self):
        layout = QVBoxLayout()

        # Back button
        self.back_button = QPushButton("назад")
        self.back_button.setFixedSize(100, 40)
        self.back_button.setStyleSheet(
            "background-color: #1C3AA9; color: white; font-size: 14px; border-radius: 10px; border: none;"
        )
        self.back_button.clicked.connect(self.close)
        layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

        # Movie selection
        self.movie_label = QLabel("Select Movie:")
        self.movie_label.setStyleSheet("color: white;")
        layout.addWidget(self.movie_label, alignment=Qt.AlignCenter)

        self.movie_combo = QComboBox()
        self.movie_combo.setFixedSize(295, 40)
        self.movie_combo.addItem("Movie")  # Add a placeholder item
        self.movie_combo.setItemData(0, True, role=QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)  # Disable the placeholder

        self.movie_combo.setStyleSheet("""
        QComboBox {
            border: 2px solid #FFFFFF;
            border-radius: 15px;
            background-color: #101F34;
            color: white;
            padding-left: 10px;
            height: 40px;
        }

        QComboBox QAbstractItemView {
            color: white;
            background-color: #101F34;
        }

        QComboBox::item {
            color: white;
        }

        QComboBox::item:disabled {
            color: gray;
        }
        """)
        self.movie_combo.currentIndexChanged.connect(self.load_times)
        layout.addWidget(self.movie_combo, alignment=Qt.AlignCenter)

        # Time selection
        self.time_label = QLabel("Select Time:")
        self.time_label.setStyleSheet("color: white;")
        layout.addWidget(self.time_label, alignment=Qt.AlignCenter)

        self.time_combo = QComboBox()
        self.time_combo.addItem("Time")  # Add a placeholder item
        self.time_combo.setItemData(0, True, role=QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)  # Disable the placeholder
        self.time_combo.setFixedSize(295, 40)

        self.time_combo.setStyleSheet("""
        QComboBox {
            border: 2px solid #FFFFFF;
            border-radius: 15px;
            background-color: #101F34;
            color: white;
            padding-left: 10px;
            height: 40px;
        }

        QComboBox QAbstractItemView {
            color: white;
            background-color: #101F34;
        }

        QComboBox::item {
            color: white;
        }

        QComboBox::item:disabled {
            color: gray;
        }
        """)

        self.time_combo.currentIndexChanged.connect(self.load_report_data)
        layout.addWidget(self.time_combo, alignment=Qt.AlignCenter)

        # Table widget
        self.table = QTableWidget()
        self.table.setColumnCount(5)  # Including Total Cost column
        self.table.setHorizontalHeaderLabels(["Movie Title", "Time", "Seats", "Booked By", "Total Cost"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("color: white; border: none;")
        layout.addWidget(self.table)

        # Total cost label
        self.total_cost_label = QLabel("Total Cost: 0 KZT")
        self.total_cost_label.setStyleSheet("color: white; font-size: 16px;")
        layout.addWidget(self.total_cost_label, alignment=Qt.AlignRight)

        # Container
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_movies(self):
        try:
            response = requests.get(f"{API_URL}/movies")
            response.raise_for_status()
            self.movies = response.json().get("movies", [])

            self.movie_combo.clear()
            self.movie_combo.addItem("Movie")  # Add the placeholder again after clearing
            for movie in self.movies:
                self.movie_combo.addItem(movie.get("title"), movie.get("id"))

            self.time_combo.clear()  # Ensure the Time combo is blank initially
            self.load_report_data()
        except requests.exceptions.RequestException as e:
            print(f"Failed to load movies: {e}")

    def load_times(self):
        movie_id = self.movie_combo.currentData()

        self.time_combo.clear()  # Clear the existing items
        self.time_combo.addItem("Time")  # Add the placeholder item

        if not movie_id:  # If no movie is selected
            self.load_report_data()  # Show all data
            return

        try:
            response = requests.get(f"{API_URL}/movie_times/{movie_id}")
            response.raise_for_status()
            self.times = response.json().get("times", [])

            for time in self.times:
                self.time_combo.addItem(time)

            self.load_report_data()  # Load report for selected movie only
        except requests.exceptions.RequestException as e:
            print(f"Failed to load times: {e}")


    def load_report_data(self):
        movie_title = self.movie_combo.currentText()
        time = self.time_combo.currentText()

        params = {}

        # Case 1: No movie selected, show all movies' reports
        if movie_title != "Movie":  # If any movie is selected (not the placeholder)
            params["movie"] = movie_title

        # Case 2: Movie is selected but time is not chosen, show all times for the movie
        if time != "Time" and movie_title != "Movie":  # If time is selected but a movie is chosen
            params["time"] = time
        elif time == "Time" and movie_title != "Movie":  # If no time is selected but a movie is chosen
            # Load all reports for that movie (no specific time)
            pass

        try:
            response = requests.get(f"{API_URL}/get_report", params=params)
            response.raise_for_status()
            bookings = response.json().get("bookings", [])

            # Update the table structure
            self.table.setRowCount(len(bookings))
            total_cost = 0  # Initialize total cost

            for row, booking in enumerate(bookings):
                # Extracting data from the API response
                movie = booking.get("movie_title", "-")
                time = booking.get("time", "-")
                seats = booking.get("seats", [])
                username = booking.get("username", "-")
                cost = len(seats) * 350  # Calculate the cost for current booking
                total_cost += cost  # Add to total cost

                # Fill the table
                self.table.setItem(row, 0, QTableWidgetItem(movie))
                self.table.setItem(row, 1, QTableWidgetItem(time))
                self.table.setItem(row, 2, QTableWidgetItem(", ".join(map(str, seats))))
                self.table.setItem(row, 3, QTableWidgetItem(username))
                self.table.setItem(row, 4, QTableWidgetItem(f"{cost} KZT"))

                # Align items in the center
                for col in range(5):
                    self.table.item(row, col).setTextAlignment(Qt.AlignCenter)

            # Update total cost label
            self.total_cost_label.setText(f"Total Cost: {total_cost} KZT")

        except requests.exceptions.RequestException as e:
            print(f"Failed to load report data: {e}")
