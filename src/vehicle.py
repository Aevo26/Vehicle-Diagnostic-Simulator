from abc import ABC, abstractmethod


class Vehicle(ABC):
    def __init__(self, rpm_min: int, rpm_max: int, max_temp: float):
        self.rpm_min = rpm_min
        self.rpm_max = rpm_max
        self.max_temp = max_temp
        self.fault_codes: list[str] = []

    @abstractmethod
    def get_engine_type(self) -> str:
        pass

    def log_fault(self, code: str, description: str):
        entry = f"{code}: {description}"
        if entry not in self.fault_codes:
            self.fault_codes.append(entry)
            print(f"[FAULT] {entry}")
