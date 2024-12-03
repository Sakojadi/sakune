import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

API_URL = "http://127.0.0.1:5000"
  # Replace with your PythonAnywhere domain

class MovieApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Movie Theater")
        self.layout = QVBoxLayout()

        # Registration/Login
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter username")
        self.layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.register_user)
        self.layout.addWidget(self.register_button)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login_user)
        self.layout.addWidget(self.login_button)

        self.message_label = QLabel(self)
        self.layout.addWidget(self.message_label)

        # Movies
        self.movies_label = QLabel("Available Movies:", self)
        self.layout.addWidget(self.movies_label)

        self.setLayout(self.layout)

    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username and password:
            response = requests.post(f"{API_URL}/register", json={"username": username, "password": password})
            if response.status_code == 201:
                QMessageBox.information(self, "Success", "User registered successfully!")
            else:
                QMessageBox.warning(self, "Error", response.json().get("error"))
        else:
            QMessageBox.warning(self, "Error", "Please fill all fields.")

    def login_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username and password:
            response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Login successful!")
                self.show_movies()
            else:
                QMessageBox.warning(self, "Error", response.json().get("error"))
        else:
            QMessageBox.warning(self, "Error", "Please fill all fields.")

    def show_movies(self):
        response = requests.get(f"{API_URL}/movies")
        if response.status_code == 200:
            movies = response.json().get("movies", [])
            movies_text = "\n".join([f"{movie['title']} ({movie['genre']})" for movie in movies])
            self.movies_label.setText(f"Available Movies:\n{movies_text}")
        else:
            QMessageBox.warning(self, "Error", "Could not fetch movies.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    movie_app = MovieApp()
    movie_app.show()
    sys.exit(app.exec_())
