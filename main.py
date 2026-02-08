import sys
from PyQt5 import QtCore, QtWidgets

from main_controller import MainController
from pomodoro_state import PomodoroState
from main_window_ui import Ui_MainWindow
from circle_timer import CircleTimer


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.timer_widget = CircleTimer(30 * 60, self.ui.Main_Page)
        self.timer_widget.move(50, 8)
        self.timer_widget.show()

        self.state = PomodoroState(
            work_time = 30 * 60,
            short_break = 5 * 60,
            long_break = 30 * 60,
            cycles = 4,
        )

        self.controller = MainController(
            self.ui,
            self.timer_widget,
            self.state
        )

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())