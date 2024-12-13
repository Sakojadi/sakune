from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPainterPath
from PyQt5.QtCore import Qt, QRectF
import requests

class PersonalCabinet(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("sakune")
        self.setFixedSize(400, 450)
        self.setStyleSheet("background-color: #101F34; color: white; font-family: Arial;")
        
        self.icon_url = f"https://sakojadi.pythonanywhere.com/get_icon/{self.username}"
        self.upload_url = "https://sakojadi.pythonanywhere.com/upload_icon"

        self.header_label = QLabel("PROFILE", self)
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.icon_label = QLabel(self)
        self.icon_label.setFixedSize(100, 100)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setCursor(Qt.PointingHandCursor)  # Указатель при наведении
        self.icon_label.mousePressEvent = self.change_icon  # Привязываем клик к смене иконки

        self.username_label = QLabel(username, self)
        self.username_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.username_label.setStyleSheet("font-size: 16px; margin-top: 10px;")

        layout = QVBoxLayout(self)
        layout.addWidget(self.header_label)
        layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.username_label)
        layout.addStretch()
        self.setLayout(layout)

        # Загрузка иконки
        self.load_icon()

    def load_icon(self):
        try:
            response = requests.get(self.icon_url, stream=True)
            if response.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                self.set_icon_pixmap(pixmap)
            else:
                self.set_icon_pixmap(QPixmap("iconpr.webp"))  # Установить иконку по умолчанию
        except Exception as e:
            print("Failed to load icon:", e)
            self.set_icon_pixmap(QPixmap("iconpr.webp"))

    def set_icon_pixmap(self, pixmap):
        """Устанавливает круглый аватар из QPixmap."""
        rounded_pixmap = QPixmap(self.icon_label.size())
        rounded_pixmap.fill(Qt.transparent)

        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addEllipse(QRectF(0, 0, self.icon_label.width(), self.icon_label.height()))
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap.scaled(self.icon_label.size(), Qt.KeepAspectRatioByExpanding))
        painter.end()

        self.icon_label.setPixmap(rounded_pixmap)

    def change_icon(self, event):
        """Вызывает диалог для выбора нового изображения."""
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.webp)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            if file_path:
                self.set_icon(file_path)
                self.save_icon_to_server(file_path)

    def save_icon_to_server(self, file_path):
        """Загружает новую иконку на сервер."""
        try:
            with open(file_path, "rb") as file:
                response = requests.post(self.upload_url, files={"icon": file}, data={"username": self.username})
                if response.status_code == 200:
                    print("Icon uploaded successfully")
                else:
                    print(f"Failed to upload icon: {response.text}")
        except Exception as e:
            print(f"Error uploading icon: {e}")

    def set_icon(self, icon_path):
        """Устанавливает иконку из локального пути."""
        pixmap = QPixmap(icon_path)
        self.set_icon_pixmap(pixmap)
