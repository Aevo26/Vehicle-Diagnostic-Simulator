import random
from src.vehicle import Vehicle

OIL_PRESSURE_MIN = 20.0
FUEL_LOW_PCT = 10.0

DRIVING_MODE_PARAMS = {
    "idle":       {"rpm": (600, 900),   "temp": (85, 92)},
    "city":       {"rpm": (1000, 3000), "temp": (90, 100)},
    "highway":    {"rpm": (2500, 4000), "temp": (95, 105)},
    "heavy_load": {"rpm": (3000, 5500), "temp": (100, 115)},
}

_O2_RICH = 0.75   # volts — rich mixture ceiling
_O2_LEAN = 0.15   # volts — lean mixture floor
_O2_STEP = 0.04   # volts per tick


class Sensors:
    def __init__(self, vehicle: Vehicle, mode: str = "city", scenario: str = "normal"):
        self.vehicle = vehicle
        self.mode = mode
        self.scenario = scenario

        params = DRIVING_MODE_PARAMS.get(mode, DRIVING_MODE_PARAMS["city"])
        self.rpm = float(params["rpm"][0])
        self.coolant_temp = float(params["temp"][0])
        self.oil_pressure = 45.0
        self.fuel_level = 80.0
        self.o2_voltage = 0.45
        self._o2_going_rich = True

    def update(self):
        params = DRIVING_MODE_PARAMS.get(self.mode, DRIVING_MODE_PARAMS["city"])
        rpm_lo, rpm_hi = params["rpm"]
        temp_lo, temp_hi = params["temp"]

        # Smooth RPM: Gaussian delta + weak mean-reversion toward mode midpoint
        rpm_mid = (rpm_lo + rpm_hi) / 2.0
        rpm_delta = random.gauss(0, (rpm_hi - rpm_lo) * 0.03)
        rpm_delta += (rpm_mid - self.rpm) * 0.05
        self.rpm = max(rpm_lo, min(rpm_hi, self.rpm + rpm_delta))

        # Smooth coolant temp: same delta approach, except overheating scenario
        if self.scenario == "overheating":
            self.coolant_temp = min(self.coolant_temp + 0.3, self.vehicle.max_temp + 10)
        else:
            temp_mid = (temp_lo + temp_hi) / 2.0
            temp_delta = random.gauss(0, (temp_hi - temp_lo) * 0.03)
            temp_delta += (temp_mid - self.coolant_temp) * 0.05
            self.coolant_temp = max(temp_lo, min(temp_hi, self.coolant_temp + temp_delta))

        # Oil pressure: gradual drift with noise, or failing scenario
        if self.scenario == "low_oil":
            self.oil_pressure = max(self.oil_pressure - 0.2, 10.0)
        else:
            self.oil_pressure = max(10.0, min(80.0, self.oil_pressure + random.gauss(0, 1.0)))

        self.fuel_level = max(self.fuel_level - 0.01, 0.0)

        # O2 voltage: square-ish oscillation between lean (~0.15 V) and rich (~0.75 V)
        # with small Gaussian noise on each step — matches real closed-loop lambda behavior
        step = _O2_STEP if self._o2_going_rich else -_O2_STEP
        self.o2_voltage += step + random.gauss(0, 0.01)
        if self.o2_voltage >= _O2_RICH:
            self.o2_voltage = _O2_RICH
            self._o2_going_rich = False
        elif self.o2_voltage <= _O2_LEAN:
            self.o2_voltage = _O2_LEAN
            self._o2_going_rich = True

        self._check_faults()

    def _check_faults(self):
        if self.coolant_temp > self.vehicle.max_temp:
            self.vehicle.log_fault("P0217", "Engine Overheating")
        if self.oil_pressure < OIL_PRESSURE_MIN:
            self.vehicle.log_fault("P0524", "Oil Pressure Too Low")
        if self.fuel_level < FUEL_LOW_PCT:
            self.vehicle.log_fault("P0087", "Low Fuel Pressure")

    def get_readings(self) -> dict:
        return {
            "rpm": round(self.rpm),
            "coolant_temp": round(self.coolant_temp, 1),
            "oil_pressure": round(self.oil_pressure, 1),
            "fuel_level": round(self.fuel_level, 1),
            "o2_voltage": round(self.o2_voltage, 3),
        }
