from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QFileDialog, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, pyqtSignal
import requests

# API_URL = "https://sakojadi.pythonanywhere.com"
API_URL = "http://127.0.0.1:5000"


class AddSeansWindow(QDialog):
    new_seans_added = pyqtSignal(str)
    def __init__(self, movie_id):
        super().__init__()
        self.setWindowTitle("Add Seans")
        self.setFixedSize(400, 200)
        self.setStyleSheet("background-color: #101F34;")
        self.movie_id = movie_id
        layout = QVBoxLayout(self)

        # Поле для ввода времени сеанса
        self.time_input = QLineEdit()
        self.time_input.setPlaceholderText("Enter seans time (e.g., 15:00)")
        self.time_input.setStyleSheet("""
    QLineEdit {
        border: 2px solid #FFFFFF; /* Цвет рамки */
        border-radius: 15px;      /* Радиус закругления */
        background-color: #101F34; /* Цвет фона */
        color: white;
        padding-left: 10px;       /* Отступ текста от края */
        height: 40px;             /* Высота поля */
    }
    
""")
        layout.addWidget(self.time_input)

        # Кнопка для отправки
        submit_button = QPushButton("Submit")
        submit_button.setStyleSheet(
            "background-color: #1C3AA9; color: white; font-size: 16px; border: none; border-radius: 5px;"
        )
        submit_button.clicked.connect(self.submit_seans)
        layout.addWidget(submit_button)

    def submit_seans(self):
        """Отправка данных на сервер Flask."""
        time = self.time_input.text()

        if not time:
            QMessageBox.warning(self, "Input Error", "Please enter a valid time.")
            return

        try:
            response = requests.post(f"{API_URL}/add_seans", json={
                "movie_id": self.movie_id,
                "time": time
            })

            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Seans added successfully.")
                self.new_seans_added.emit(time)
                self.close()
            else:
                error_message = response.json().get("error", "Unknown error")
                QMessageBox.warning(self, "Error", f"Failed to add seans: {error_message}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Network Error", str(e))
