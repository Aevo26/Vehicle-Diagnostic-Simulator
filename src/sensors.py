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

    def update(self):
        params = DRIVING_MODE_PARAMS.get(self.mode, DRIVING_MODE_PARAMS["city"])
        rpm_lo, rpm_hi = params["rpm"]
        temp_lo, temp_hi = params["temp"]

        self.rpm = random.uniform(rpm_lo, rpm_hi)

        if self.scenario == "overheating":
            self.coolant_temp = min(self.coolant_temp + 0.3, self.vehicle.max_temp + 10)
        else:
            self.coolant_temp = random.uniform(temp_lo, temp_hi)

        if self.scenario == "low_oil":
            self.oil_pressure = max(self.oil_pressure - 0.2, 10.0)
        else:
            self.oil_pressure = random.uniform(25.0, 65.0)

        self.fuel_level = max(self.fuel_level - 0.01, 0.0)
        self.o2_voltage = random.uniform(0.1, 0.9)

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
