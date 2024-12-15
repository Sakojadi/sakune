from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,QMessageBox
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import sys
import requests

API_URL = "https://sakojadi.pythonanywhere.com"
# API_URL = "http://127.0.0.1:5000"


class SignUpWindow(QWidget):
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

        self.title_label = QLabel("SAKUNE", self)
        self.title_label.setFont(QFont("RocknRoll One", 42))
        self.title_label.setStyleSheet("color: white;")
        self.title_label.setAlignment(Qt.AlignCenter)
        
        self.form_container = QWidget(self)
        self.form_container.setFixedSize(400, 360)
        self.form_container.setStyleSheet("background-color: rgba(16, 31, 52, 0.88); border-radius: 15px;")

        self.sign_label = QLabel("SIGN UP", self.form_container)
        self.sign_label.setFont(QFont("RocknRoll One", 32))
        self.sign_label.setStyleSheet("color: white;")
        self.sign_label.setAlignment(Qt.AlignCenter)
        
        
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedSize(295, 40)
        self.username_input.setStyleSheet("""
    QLineEdit {
        border: 2px solid #FFFFFF; /* Цвет рамки */
        border-radius: 15px;      /* Радиус закругления */
        background-color: #101F34; /* Цвет фона */
        color: white;
        padding-left: 10px;       /* Отступ текста от края */
        height: 40px;             /* Высота поля */
    }
""")
        
       
        
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setFixedSize(295, 40)
        self.password_input.setStyleSheet("""
    QLineEdit {
        border: 2px solid #FFFFFF; /* Цвет рамки */
        border-radius: 15px;      /* Радиус закругления */
        background-color: #101F34; /* Цвет фона */
        color: white;
        padding-left: 10px;       /* Отступ текста от края */
        height: 40px;             /* Высота поля */
    }
""")
        self.password_input.setEchoMode(QLineEdit.Password)
        
       
        
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setPlaceholderText("Confirm password")
        self.confirm_password_input.setFixedSize(295, 40)
        self.confirm_password_input.setStyleSheet("""
    QLineEdit {
        border: 2px solid #FFFFFF; /* Цвет рамки */
        border-radius: 15px;      /* Радиус закругления */
        background-color: #101F34; /* Цвет фона */
        color: white;
        padding-left: 10px;       /* Отступ текста от края */
        height: 40px;             /* Высота поля */
    }
""")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        self.register_button = QPushButton("Register", self)
        self.register_button.setFixedSize(295, 30)
        self.register_button.setStyleSheet(
            "background-color: #1C3AA9; color: white; font-size: 16px; border: none; border-radius: 5px;"
        )
        
        self.back_button = QPushButton("Back", self)
        self.back_button.setFixedSize(295, 30)
        self.back_button.setStyleSheet(
            "background-color: #B27272; color: white; font-size: 16px; border: none; border-radius: 5px;"
        )


        # Компоновка элементов внутри контейнера
        form_layout = QVBoxLayout(self.form_container)
        form_layout.setAlignment(Qt.AlignCenter)
        form_layout.setSpacing(15)
        form_layout.addWidget(self.sign_label)
        form_layout.addWidget(self.title_label)
        # form_layout.addWidget(self.input)
        form_layout.addWidget(self.username_input)
        # form_layout.addWidget(self.input_password)
        form_layout.addWidget(self.password_input)
        # form_layout.addWidget(self.input_confirm)
        form_layout.addWidget(self.confirm_password_input)
        form_layout.addWidget(self.register_button)
        form_layout.addWidget(self.back_button)

        # Основной компоновщик для центрирования формы
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)
        layout.addWidget(self.form_container)  # Add the form container to the main layout

        # Register button click signal connection (only once)
        self.register_button.clicked.connect(self.register_user)
        self.back_button.clicked.connect(self.back_to)
        
    def back_to(self):
        from login import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        # Validate inputs before registration attempt
        if not username or not password:
            QMessageBox.warning(self, "Error", "All fields are required!")
            return  # Exit early if fields are empty
        
        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match!")
            return  # Exit early if passwords don't match
        
        # Disable the button to prevent duplicate submissions
        self.register_button.setDisabled(True)
        
        response = requests.post(f"{API_URL}/register", json={"username": username, "password": password})
        print(f"Server response: {response.status_code}, {response.json()}")  # Debugging: Print server response
        
        if response.status_code == 201:
            QMessageBox.information(self, "Success", "Registration successful!")
            
            # Clear fields after successful registration
            self.username_input.clear()
            self.password_input.clear()
            self.confirm_password_input.clear()
            
            # Re-enable the button after clearing fields
            self.register_button.setEnabled(True)
            self.back_to()
        
        else:
            # Show the error message
            QMessageBox.warning(self, "Error", response.json().get("error", "Registration failed!"))
            
            # Re-enable the button if the registration failed
            self.register_button.setEnabled(True)