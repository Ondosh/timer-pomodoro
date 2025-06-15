import sys
from PyQt5 import QtWidgets, QtCore
from main_window import Ui_MainWindow
from main_window import CircleTimer
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPainter, QPen, QFont, QColor
from PyQt5.QtCore import Qt, QTimer

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # === Инициализация параметров Pomodoro ===
        self.work_time = 30 * 60  # по умолчанию
        self.short_break = 5 * 60
        self.long_break = 30 * 60
        self.cycles = 4
        self.current_cycle = 0
        self.remaining = self.work_time
        self.timer_active = False
        self.current_mode = "work"
        self.stackedWidget.setCurrentIndex(0)

        self.timer_widget = CircleTimer(self.work_time, self.Main_Page)
        self.timer_widget.move(50, 8)  # Установи координаты под твой макет
        self.timer_widget.show()

        # === Таймер ===
        self.qtimer = QtCore.QTimer()
        self.qtimer.timeout.connect(self.update_timer)

        # === Привязка событий ===
        self.TimerButton.clicked.connect(self.toggle_timer)
        self.ApplyButton.clicked.connect(self.apply_settings_and_return)

        # === Меню ===
        self.actionThemes.triggered.connect(self.open_settings_page)

        # === Слайдеры (начальные подписи) ===
        self.WorkTimeSlider.valueChanged.connect(self.update_labels)
        self.ShortBreakSlider.valueChanged.connect(self.update_labels)
        self.LongBreakSlider.valueChanged.connect(self.update_labels)
        self.CyclesSlider.valueChanged.connect(self.update_labels)

        self.update_labels()


    # === Переключение на страницу настроек ===
    def open_settings_page(self):
        self.stackedWidget.setCurrentIndex(1)
        
    # === Применение настроек и возврат на главную ===
    def apply_settings_and_return(self):
        self.work_time = self.WorkTimeSlider.value() * 60
        self.short_break = self.ShortBreakSlider.value() * 60
        self.long_break = self.LongBreakSlider.value() * 60
        self.cycles = self.CyclesSlider.value()
        self.timer_widget.total_time = self.work_time  # Добавьте эту строку
        self.reset_timer()
        self.stackedWidget.setCurrentIndex(0)

    # === Обновление меток со значением слайдеров ===
    def update_work_time_label(self, value):
        self.WorkTimeLabel.setText(f"Work: {value} min")

    def update_short_break_label(self, value):
        self.ShortBreakLabel.setText(f"Short Break: {value} min")

    def update_long_break_label(self, value):
        self.LongBreakLabel.setText(f"Long Break: {value} min")

    def update_cycles_label(self, value):
        self.CyclesLabel.setText(f"Cycles: {value}")
    
    def update_labels(self):
        self.update_work_time_label(self.WorkTimeSlider.value())
        self.update_short_break_label(self.ShortBreakSlider.value())
        self.update_long_break_label(self.LongBreakSlider.value())
        self.update_cycles_label(self.CyclesSlider.value())
        self.update_timer_display()

    def update_timer_display(self):
        """Обновляет отображение таймера"""
        self.timer_widget.set_time(self.remaining)
        
        mode_text = {
            "work": "Work",
            "short_break": "Short Break",
            "long_break": "Long Break"
        }.get(self.current_mode, "")
        

    # === Логика таймера ===
    def toggle_timer(self):
        if not self.timer_active:
            self.start_timer()
        else:
            self.stop_timer()

    def start_timer(self):
        self.timer_active = True
        self.TimerButton.setText("Stop")
        self.qtimer.start(1000)

    def stop_timer(self):
        self.timer_active = False
        self.TimerButton.setText("Start")
        self.qtimer.stop()
        self.reset_timer() 

    def reset_timer(self):
        if self.current_mode == "work":
            self.remaining = self.work_time
            self.timer_widget.total_time = self.work_time
        elif self.current_mode == "short_break":
            self.remaining = self.short_break
            self.timer_widget.total_time = self.short_break
        elif self.current_mode == "long_break":
            self.remaining = self.long_break
            self.timer_widget.total_time = self.long_break
        self.timer_widget.set_mode(self.current_mode)  
        self.update_labels()
        self.timer_widget.set_time(self.remaining)

    def update_timer(self):
        self.remaining -= 1
        if self.remaining <= 0:
            self.next_phase()
        self.update_labels()

    def next_phase(self):
        if self.current_mode == "work":
            self.current_cycle += 1
            if self.current_cycle < self.cycles:
                self.current_mode = "short_break"
                self.remaining = self.short_break
            else:
                self.current_mode = "long_break"
                self.remaining = self.long_break
                self.current_cycle = 0
        elif self.current_mode in ["short_break", "long_break"]:
            self.current_mode = "work"
            self.remaining = self.work_time
    
        # Обновляем режим в таймере
        self.timer_widget.set_mode(self.current_mode)
        self.update_timer_display()

    def update_label(self):
        minutes = self.remaining // 60
        seconds = self.remaining % 60
        
        # Форматируем время как "MM:SS"
        time_text = f"{minutes:02d}:{seconds:02d}"
        
        # Обновляем текст в виджете таймера
        self.timer_widget.label.setText(time_text)
        
        # Обновляем прогресс круга (если нужно)
        self.timer_widget.update_timer(self.remaining)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())