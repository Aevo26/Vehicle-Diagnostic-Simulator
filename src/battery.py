from src.vehicle import Vehicle

VOLTAGE_HIGH = 15.0
VOLTAGE_LOW = 11.5


class Battery:
    def __init__(self, vehicle: Vehicle, scenario: str = "normal"):
        self.vehicle = vehicle
        self.scenario = scenario
        self.voltage = 12.6

    def update(self):
        if self.scenario == "failing_battery":
            self.voltage = max(self.voltage - 0.05, 9.0)
        else:
            import random
            self.voltage += random.uniform(-0.05, 0.05)
            self.voltage = max(11.0, min(15.5, self.voltage))

        if self.voltage > VOLTAGE_HIGH:
            self.vehicle.log_fault("P0563", "Battery Voltage High")
        elif self.voltage < VOLTAGE_LOW:
            self.vehicle.log_fault("P0562", "Battery Voltage Low")

    def get_voltage(self) -> float:
        return round(self.voltage, 2)
