from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import QLabel, QWidget


class CircleTimer(QWidget):
    def __init__(self, total_time=30 * 60, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 300)
        self.total_time = int(total_time)
        self.remaining_time = int(total_time)
        self._current_mode = "work"
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(0, 0, 300, 300)
        font = QFont("Inter", 40)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #3D3D3D; background: transparent;")
        self.update_label()

    def set_mode(self, mode):
        """Устанавливает текущий режим"""
        self._current_mode = mode
        self.update()

    def set_time(self, seconds):
        """Устанавливает новое время"""
        self.remaining_time = seconds
        self.update_label()
        self.update()

    def update_timer(self):
        self.remaining_time -= 1
        if self.remaining_time <= 0:
            self.remaining_time = 0
            self.timer.stop()
        self.update_label()
        self.update()

    def update_label(self):
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.label.setText(f"{minutes:02}:{seconds:02}")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        margin = 12
        rect = self.rect().adjusted(margin, margin, -margin, -margin)

        if self.total_time > 0:
            progress = float(self.remaining_time) / float(self.total_time)
        else:
            progress = 0.0

        # Выбираем цвет в зависимости от режима
        if self._current_mode == "short_break":
            color = QColor("#81FF5B")
        elif self._current_mode == "long_break":
            color = QColor("#3680E0")
        else:
            color = QColor("#F54242")

        pen = QPen(color, 12)
        painter.setPen(pen)

        remaining_angle = int(360.0 * progress * 16)
        painter.drawArc(rect, 90 * 16, -remaining_angle)
