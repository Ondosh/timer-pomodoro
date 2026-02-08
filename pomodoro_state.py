from dataclasses import dataclass


@dataclass
class PomodoroState:
    work_time: int
    short_break: int
    long_break: int
    cycles: int
    current_cycle: int = 0
    current_mode: str = "work"
    remaining: int = 0
