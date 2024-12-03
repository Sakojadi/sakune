import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QDialog
)
from PyQt5.QtGui import QPixmap

API_URL = "http://127.0.0.1:5000"  # Update this if Flask runs on a different host/port


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 300)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Username input
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter username")
        layout.addWidget(self.username_input)

        # Password input
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Login button
        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login_user)
        layout.addWidget(self.login_button)

        # Sign Up button
        self.signup_button = QPushButton("Sign Up", self)
        self.signup_button.clicked.connect(self.open_signup_window)
        layout.addWidget(self.signup_button)

        self.setLayout(layout)

    def login_user(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Username and password are required!")
            return

        # API request for login
        response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
        if response.status_code == 200:
            QMessageBox.information(self, "Success", "Login successful!")
            self.open_movie_window(username)  # Pass the username to the movie window
        else:
            QMessageBox.warning(self, "Error", response.json().get("error", "Login failed!"))

    def open_signup_window(self):
        self.signup_window = SignUpWindow(self)
        self.signup_window.exec_()

    def open_movie_window(self, username):
        self.movie_window = MovieWindow(username)  # Pass the username
        self.movie_window.show()  # Show the movie window
        self.close()  # Close the login window



class SignUpWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sign Up")
        self.setGeometry(100, 100, 300, 200)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setPlaceholderText("Confirm password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.confirm_password_input)

        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.register_user)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "All fields are required!")
        elif password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match!")
        else:
            response = requests.post(f"{API_URL}/register", json={"username": username, "password": password})
            if response.status_code == 201:
                QMessageBox.information(self, "Success", "Registration successful!")
                self.close()
            else:
                QMessageBox.warning(self, "Error", response.json().get("error", "Registration failed!"))


class MovieWindow(QWidget):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.username = username
        self.setWindowTitle("Movies")
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Fetch movies from the Flask API
        response = requests.get(f"{API_URL}/movies")
        if response.status_code == 200:
            movies = response.json().get("movies", [])
            for movie in movies:
                movie_layout = QHBoxLayout()

                # Movie poster
                poster_label = QLabel(self)
                pixmap = QPixmap()
                pixmap.loadFromData(requests.get(movie["poster_url"]).content)  # Load poster from URL
                poster_label.setPixmap(pixmap.scaled(100, 150))
                movie_layout.addWidget(poster_label)

                # Movie details and booking
                details_layout = QVBoxLayout()
                details_layout.addWidget(QLabel(movie["title"]))
                for time in movie["times"]:
                    time_button = QPushButton(f"Book {time}", self)
                    time_button.clicked.connect(lambda _, m=movie, t=time: self.book_ticket(m, t))
                    details_layout.addWidget(time_button)
                movie_layout.addLayout(details_layout)

                layout.addLayout(movie_layout)

        else:
            layout.addWidget(QLabel("Failed to load movies!"))

        self.setLayout(layout)

    def book_ticket(self, movie, time):
        QMessageBox.information(self, "Booking", f"Selected {movie['title']} at {time}")
        # Placeholder: Booking logic can go here!


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
