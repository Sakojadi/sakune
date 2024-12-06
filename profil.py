from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFileDialog, QPushButton
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QRegion, QBitmap
from PyQt5.QtCore import Qt



class PersonalCabinet(QWidget):
    def __init__(self, username):
        super().__init__()

        self.setWindowTitle("Личный кабинет")
        self.setFixedSize(400, 450)
        self.setStyleSheet("background-color: #2B2B2B; color: white; font-family: Arial;")

        self.header_label = QLabel("Личный кабинет", self)
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        # Иконка пользователя
        self.icon_label = QLabel(self)
        self.icon_label.setFixedSize(100, 100)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_icon("iconpr.webp")  # Путь к вашей иконке

        # Кнопка для изменения изображения
        self.change_icon_button = QPushButton("Изменить картинку", self)
        self.change_icon_button.setStyleSheet("margin-top: 10px;")
        self.change_icon_button.clicked.connect(self.change_icon)

        # Имя пользователя
        self.username_label = QLabel(username, self)
        self.username_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.username_label.setStyleSheet("font-size: 16px; margin-top: 10px;")

        # Ссылки
        self.my_movies_label = QLabel("Мои фильмы >", self)
        self.my_movies_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.my_movies_label.setStyleSheet("font-size: 14px; margin-top: 20px; cursor: pointer;")

        self.reports_label = QLabel("Отчеты по фильмам >", self)
        self.reports_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.reports_label.setStyleSheet("font-size: 14px; margin-top: 5px; cursor: pointer;")

        # Компоновка элементов
        layout = QVBoxLayout(self)
        layout.addWidget(self.header_label)
        layout.addWidget(self.icon_label)
        layout.addWidget(self.change_icon_button)
        layout.addWidget(self.username_label)
        layout.addWidget(self.my_movies_label)
        layout.addWidget(self.reports_label)
        layout.addStretch()  # Чтобы элементы выровнялись по верхней части
        self.setLayout(layout)

    def set_icon(self, image_path):
        pixmap = QPixmap(image_path).scaled(
            100, 100, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation
        )

        # Создание маски в форме круга
        # mask = QBitmap(pixmap.size())
        # mask.fill(Qt.GlobalColor.transparent)

        # painter = QPainter(mask)
        # painter.setBrush(Qt.GlobalColor.white)
        # painter.drawEllipse(0, 0, pixmap.width(), pixmap.height())
        # painter.end()

        # pixmap.setMask(mask)

        # Устанавливаем иконку в QLabel
        self.icon_label.setPixmap(pixmap)

    def change_icon(self):
        # Открываем диалог для выбора файла
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.webp)")
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            self.set_icon(file_path)
