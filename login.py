from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QMessageBox
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import sys
import requests


API_URL = "https://sakojadi.pythonanywhere.com"  # Update this if Flask runs on a different host/port

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Настройка окна
        self.setWindowTitle("SAKUNE")
        self.setFixedSize(800, 600)

        # Фоновое изображение
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("anime.jpg").scaled(
            self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        ))
        self.background_label.setGeometry(0, 0, 800, 600)

        # Полупрозрачный затемняющий слой
        self.overlay = QLabel(self)
        self.overlay.setGeometry(0, 0, 800, 600)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")

        # Текст "Авторизация"
        self.title_label = QLabel("SAKUNE", self)
        self.title_label.setFont(QFont("RocknRoll One", 42))
        self.title_label.setStyleSheet("color: white;")
        self.title_label.setAlignment(Qt.AlignCenter)

        # Container for the form (with black background and size 400x470)
        self.form_container = QWidget(self)
        self.form_container.setFixedSize(400, 340)
        self.form_container.setStyleSheet("background-color: #232527; border-radius: 10px;")

        # Поля ввода
        self.input = QLabel("username",self)
        self.input.setStyleSheet("color: white;")
        self.input.setFont(QFont("RocknRoll One", 8))
        
        self.username_input = QLineEdit(self.form_container)
        self.username_input.setPlaceholderText("Don't write your name")
        self.username_input.setFixedSize(295, 40)
        self.username_input.setStyleSheet("border-radius: 5px; background-color: #FFFFFF")
        
        self.input_pass = QLabel("password",self)
        self.input_pass.setStyleSheet("color: white;")
        self.input_pass.setFont(QFont("RocknRoll One", 8))
        
        self.password_input = QLineEdit(self.form_container)
        self.password_input.setPlaceholderText("make a strong one")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedSize(295, 40)
        self.password_input.setStyleSheet("border-radius: 5px; background-color: #FFFFFF")

        # Кнопка входа
        self.login_button = QPushButton("LOGIN", self.form_container)
        self.login_button.setFixedSize(295, 40)
        self.login_button.setStyleSheet(
            "background-color: #34609D; color: white; font-size: 16px; border: none; border-radius: 5px;"
        )

        # Чекбокс reCAPTCHA
        self.recaptcha_checkbox = QCheckBox("I'm not a robot", self.form_container)
        self.recaptcha_checkbox.setStyleSheet("color: white;")

        # Ссылка регистрации
        self.register_link = QLabel('<a href="#">Регистрация</a>', self.form_container)
        self.register_link.setStyleSheet("color: lightblue;")
        self.register_link.setAlignment(Qt.AlignCenter)

        # Компоновка элементов внутри контейнера
        form_layout = QVBoxLayout(self.form_container)
        form_layout.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(self.title_label)
        form_layout.addWidget(self.input)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.input_pass)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.login_button)
        form_layout.addWidget(self.recaptcha_checkbox, alignment=Qt.AlignCenter)
        form_layout.addWidget(self.register_link)

        # Основной компоновщик для центрирования формы
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.form_container)  # Add the form container to the main layout

        # Сигнал для открытия окна регистрации
        self.register_link.linkActivated.connect(self.open_signup_window)
        self.login_button.clicked.connect(self.login_user)

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
        from signup import SignUpWindow
        self.signup_window = SignUpWindow()
        self.signup_window.show()
        self.close()
        

    def open_movie_window(self, username):
        from qthw import MovieWindow
        self.movie_window = MovieWindow(username)  # Pass the username
        self.close()  # Close the login window
        self.movie_window.show()  # Show the movie window


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())