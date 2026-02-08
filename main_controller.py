from PyQt5 import QtCore


class MainController:
    def __init__(self, ui, timer_widget, state):
        self.ui = ui
        self.timer_widget = timer_widget
        self.state = state
        self.state.remaining = self.state.work_time

        self.timer_active = False
        self.qtimer = QtCore.QTimer()
        self.qtimer.timeout.connect(self.update_timer)

        self.ui.TimerButton.setText("Start")
        self.ui.stackedWidget.setCurrentIndex(0)

        # === Настройка слайдеров ===
        self.ui.WorkTimeSlider.setMinimum(20)
        self.ui.WorkTimeSlider.setMaximum(60)
        self.ui.WorkTimeSlider.setValue(30)

        self.ui.ShortBreakSlider.setMinimum(3)
        self.ui.ShortBreakSlider.setMaximum(15)
        self.ui.ShortBreakSlider.setValue(5)

        self.ui.LongBreakSlider.setMinimum(20)
        self.ui.LongBreakSlider.setMaximum(60)
        self.ui.LongBreakSlider.setValue(30)

        self.ui.CyclesSlider.setMinimum(1)
        self.ui.CyclesSlider.setMaximum(6)
        self.ui.CyclesSlider.setValue(4)

        self.ui.WorkTimeSlider.setValue(self.state.work_time // 60)
        self.ui.ShortBreakSlider.setValue(self.state.short_break // 60)
        self.ui.LongBreakSlider.setValue(self.state.long_break // 60)
        self.ui.CyclesSlider.setValue(self.state.cycles)

        self._connect_signals()
        self.update_labels()

    def _connect_signals(self):
        self.ui.TimerButton.clicked.connect(self.toggle_timer)
        self.ui.ApplyButton.clicked.connect(self.apply_settings_and_return)
        self.ui.actionThemes.triggered.connect(self.open_settings_page)
        self.ui.WorkTimeSlider.valueChanged.connect(self.update_labels)
        self.ui.ShortBreakSlider.valueChanged.connect(self.update_labels)
        self.ui.LongBreakSlider.valueChanged.connect(self.update_labels)
        self.ui.CyclesSlider.valueChanged.connect(self.update_labels)

    def open_settings_page(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def apply_settings_and_return(self):
        self.state.work_time = self.ui.WorkTimeSlider.value() * 60
        self.state.short_break = self.ui.ShortBreakSlider.value() * 60
        self.state.long_break = self.ui.LongBreakSlider.value() * 60
        self.state.cycles = self.ui.CyclesSlider.value()
        self.timer_widget.total_time = self.state.work_time
        self.reset_timer()
        self.ui.stackedWidget.setCurrentIndex(0)

    def update_labels(self):
        self.ui.WorkTimeLabel.setText(f"Work: {self.ui.WorkTimeSlider.value()} min")
        self.ui.ShortBreakLabel.setText(f"Short Break: {self.ui.ShortBreakSlider.value()} min")
        self.ui.LongBreakLabel.setText(f"Long Break: {self.ui.LongBreakSlider.value()} min")
        self.ui.CyclesLabel.setText(f"Cycles: {self.ui.CyclesSlider.value()}")
        self.update_timer_display()

    def update_timer_display(self):
        """Обновляет отображение таймера"""
        self.timer_widget.set_time(self.state.remaining)

    def toggle_timer(self):
        if not self.timer_active:
            self.start_timer()
        else:
            self.stop_timer()

    def start_timer(self):
        self.timer_active = True
        self.ui.TimerButton.setText("Stop")
        self.qtimer.start(1000)

    def stop_timer(self):
        self.timer_active = False
        self.ui.TimerButton.setText("Start")
        self.qtimer.stop()
        self.reset_timer()

    def reset_timer(self):
        if self.state.current_mode == "work":
            self.state.remaining = self.state.work_time
            self.timer_widget.total_time = self.state.work_time
        elif self.state.current_mode == "short_break":
            self.state.remaining = self.state.short_break
            self.timer_widget.total_time = self.state.short_break
        elif self.state.current_mode == "long_break":
            self.state.remaining = self.state.long_break
            self.timer_widget.total_time = self.state.long_break
        self.timer_widget.set_mode(self.state.current_mode)
        self.update_labels()
        self.timer_widget.set_time(self.state.remaining)

    def update_timer(self):
        self.state.remaining -= 1
        if self.state.remaining <= 0:
            self.next_phase()
        self.update_labels()

    def next_phase(self):
        if self.state.current_mode == "work":
            self.state.current_cycle += 1
            if self.state.current_cycle < self.state.cycles:
                self.state.current_mode = "short_break"
                self.state.remaining = self.state.short_break
            else:
                self.state.current_mode = "long_break"
                self.state.remaining = self.state.long_break
                self.state.current_cycle = 0
        elif self.state.current_mode in ["short_break", "long_break"]:
            self.state.current_mode = "work"
            self.state.remaining = self.state.work_time

        self.timer_widget.set_mode(self.state.current_mode)
        self.update_timer_display()
