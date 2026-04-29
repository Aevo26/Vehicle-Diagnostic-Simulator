import random
from src.vehicle import Vehicle

VOLTAGE_HIGH = 15.0
VOLTAGE_LOW = 11.5

# Below this RPM the alternator can't fully compensate for electrical load.
_CHARGE_RPM = 2000.0
_CHARGE_RATE = 0.003    # V/tick gained when RPM is at _CHARGE_RPM
_DISCHARGE_RATE = 0.002  # V/tick lost at idle/low RPM


class Battery:
    def __init__(self, vehicle: Vehicle, scenario: str = "normal"):
        self.vehicle = vehicle
        self.scenario = scenario
        self.voltage = 12.6

    def update(self, rpm: float = None):
        if self.scenario == "failing_battery":
            self.voltage = max(self.voltage - 0.05, 9.0)
        else:
            if rpm is not None and rpm >= _CHARGE_RPM:
                # Higher RPM → more alternator output → net charge
                delta = _CHARGE_RATE * (rpm / _CHARGE_RPM)
            else:
                # Idle / low RPM → slight drain from electrical loads
                delta = -_DISCHARGE_RATE
            delta += random.gauss(0, 0.005)
            self.voltage = max(11.0, min(15.5, self.voltage + delta))

        if self.voltage > VOLTAGE_HIGH:
            self.vehicle.log_fault("P0563", "Battery Voltage High")
        elif self.voltage < VOLTAGE_LOW:
            self.vehicle.log_fault("P0562", "Battery Voltage Low")

    def get_voltage(self) -> float:
        return round(self.voltage, 2)
