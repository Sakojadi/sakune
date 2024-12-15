from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QMessageBox, QFileDialog
)
from PyQt5.QtGui import QPixmap, QFont, QPalette, QColor, QPainter, QTransform
from PyQt5.QtCore import Qt
import sys
import requests
import random
import string
from snowflakes import SnowfallBackground

API_URL = "https://sakojadi.pythonanywhere.com"
# API_URL = "http://127.0.0.1:5000"

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Настройка окна
        self.setWindowTitle("SAKUNE")
        self.setFixedSize(800, 600)
        self.snowfall_background = SnowfallBackground(self)

        # Фоновое изображение
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("bka.jpg").scaled(
            self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        ))
        self.background_label.setGeometry(0, 0, 800, 600)

        # Полупрозрачный затемняющий слой
        self.overlay = QLabel(self)
        self.overlay.setGeometry(0, 0, 800, 600)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.0);")
        self.snowfall_background.create_snowflakes()
        self.snowfall_background.raise_()


        # Заголовок "SAKUNE"
        # self.title_label = QLabel("SAKUNE", self)
        # self.title_label.setFont(QFont("RocknRoll One", 42))
        # self.title_label.setStyleSheet("color: white;")
        # self.title_label.setAlignment(Qt.AlignCenter)

        # Контейнер для формы
        self.form_container = QWidget(self)
        self.form_container.setFixedSize(400, 360)
        self.form_container.setStyleSheet("background-color: rgba(16, 31, 52, 0.88); border-radius: 15px;")

        self.login_label = QLabel("LOGIN", self.form_container)
        self.login_label.setFont(QFont("RocknRoll One", 32))
        self.login_label.setStyleSheet("color: white;")
        self.login_label.setAlignment(Qt.AlignCenter)

        # Поля ввода
        self.username_input = QLineEdit(self.form_container)
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedSize(295, 40)
        # self.username_input.setStyleSheet("border-radius: 10px; background-color: #FFFFFF; padding-left: 10px;")
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
        palette = self.username_input.palette()
        palette.setColor(QPalette.PlaceholderText, QColor("white"))  # Белый цвет текста-заполнителя
        self.username_input.setPalette(palette)

        self.password_input = QLineEdit(self.form_container)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
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
        palette = self.password_input.palette()
        palette.setColor(QPalette.PlaceholderText, QColor("white"))  # Белый цвет текста-заполнителя
        self.password_input.setPalette(palette)

        

        # Кнопка входа
        self.login_button = QPushButton("LOGIN", self.form_container)
        self.login_button.setFixedSize(295, 30)
        self.login_button.setStyleSheet(
            "background-color: #1C3AA9; color: white; font-size: 16px; border: none; border-radius: 5px;"
        )

        # Чекбокс reCAPTCHA
        self.captcha_input = QLineEdit(self.form_container)
        self.captcha_input.setPlaceholderText("Enter CAPTCHA text")
        self.captcha_input.setFixedSize(295,30)
        self.captcha_input.setStyleSheet("""
    QLineEdit {
        border: 2px solid #FFFFFF; /* Цвет рамки */
        border-radius: 15px;      /* Радиус закругления */
        background-color: #101F34; /* Цвет фона */
        color: white;
        padding-left: 10px;       /* Отступ текста от края */
        height: 40px;             /* Высота поля */
    }
""")
        # Сгенерировать капчу
        self.captcha_text = self.generate_captcha_text()
        self.captcha_label = QLabel(self.form_container)
        # self.captcha_label.setFixedSize(295,40)
        self.update_captcha_image()

        # Ссылка регистрации
        self.register_link = QLabel('<a href="#">Sign up</a>', self.form_container)
        self.register_link.setStyleSheet("color: lightblue;")
        self.register_link.setAlignment(Qt.AlignCenter)

        # Компоновка элементов
        form_layout = QVBoxLayout(self.form_container)
        form_layout.setAlignment(Qt.AlignCenter)
        form_layout.setSpacing(15)
        form_layout.addWidget(self.login_label)
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.captcha_label)
        form_layout.addWidget(self.captcha_input)
        form_layout.addWidget(self.login_button)
        form_layout.addWidget(self.register_link)

        # Основной компоновщик для окна
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        # main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.form_container)

        

        # Сигнал для открытия окна регистрации
        self.register_link.linkActivated.connect(self.open_signup_window)
        self.login_button.clicked.connect(self.login_user)


    def generate_captcha_text(self):
        """Генерирует случайный текст для капчи"""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    def update_captcha_image(self):
        """Создает изображение с текстом капчи с искажениями"""
        pixmap = QPixmap(295, 60)
        pixmap.fill(QColor(255, 255, 255))
        painter = QPainter(pixmap)
        painter.setFont(QFont("Arial", 35))

        # Искажение текста
        for i, char in enumerate(self.captcha_text):
            # Случайные смещения по осям X и Y
            offset_x = random.randint(-3, 3)
            offset_y = random.randint(-3, 3)

            # Случайное вращение символа
            transform = QTransform()
            transform.rotate(random.randint(-3, 3))  # Угол вращения символа

            painter.setPen(QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))  # Случайный цвет текста
            painter.setTransform(transform)

            # Рисуем каждый символ с смещением и случайным углом
            painter.drawText(30 + i * 30 + offset_x, 50 + offset_y, char)

        painter.end()
        self.captcha_label.setPixmap(pixmap)

    def login_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        entered_captcha = self.captcha_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Username and password are required!")
            return
        
        if entered_captcha != self.captcha_text:
            QMessageBox.warning(self, "Ошибка", "Неверный код с картинки капчи!")
            self.captcha_text = self.generate_captcha_text()  # Генерируем новый код
            self.update_captcha_image()  # Обновляем картинку
            self.captcha_input.clear()  # Очищаем поле ввода капчи
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
    # app.setStyle('Fusion')
    with open("style.qss", "r") as style_file:
        app.setStyleSheet(style_file.read())
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())