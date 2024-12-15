from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import QTimer
import random

import random
from PyQt5.QtCore import QTimer

class SnowfallEffect:
    def __init__(self, parent, width, height):
        self.parent = parent
        self.width = width
        self.height = height
        self.snowflakes = self.generate_snowflakes()

    def generate_snowflakes(self):
        """Генерирует случайные снежинки"""
        return [{'x': random.randint(0, self.width), 'y': random.randint(0, self.height), 'size': random.randint(5, 15)} for _ in range(100)]

    def update(self):
        """Обновляет позиции снежинок"""
        for snowflake in self.snowflakes:
            snowflake['y'] += random.randint(1, 3)  # Снег падает вниз
            if snowflake['y'] > self.height:
                snowflake['y'] = 0  # Перезапуск на верхней части экрана
                snowflake['x'] = random.randint(0, self.width)  # Случайное положение по оси X

    def draw(self, painter):
        """Рисует снежинки"""
        for snowflake in self.snowflakes:
            painter.setBrush(QColor(255, 255, 255))
            painter.drawEllipse(snowflake['x'], snowflake['y'], snowflake['size'], snowflake['size'])
