import unittest
from src.engine import FourCylinderEngine, V6Engine, V8Engine
from src.battery import Battery
from src.sensors import Sensors


class TestEngineTypes(unittest.TestCase):
    def test_four_cylinder(self):
        engine = FourCylinderEngine()
        self.assertEqual(engine.get_engine_type(), "4-Cylinder")
        self.assertEqual(engine.max_temp, 105.0)

    def test_v6(self):
        engine = V6Engine()
        self.assertEqual(engine.get_engine_type(), "V6")
        self.assertEqual(engine.max_temp, 110.0)

    def test_v8(self):
        engine = V8Engine()
        self.assertEqual(engine.get_engine_type(), "V8")
        self.assertEqual(engine.max_temp, 115.0)


class TestBattery(unittest.TestCase):
    def test_normal_voltage_range(self):
        engine = FourCylinderEngine()
        battery = Battery(engine, scenario="normal")
        for _ in range(20):
            battery.update()
        self.assertGreaterEqual(battery.get_voltage(), 11.0)

    def test_failing_battery_triggers_fault(self):
        engine = FourCylinderEngine()
        battery = Battery(engine, scenario="failing_battery")
        battery.voltage = 11.6
        for _ in range(5):
            battery.update()
        self.assertIn("P0562: Battery Voltage Low", engine.fault_codes)


class TestSensors(unittest.TestCase):
    def test_overheating_triggers_fault(self):
        engine = FourCylinderEngine()
        sensors = Sensors(engine, mode="highway", scenario="overheating")
        sensors.coolant_temp = engine.max_temp + 0.5
        sensors.update()
        self.assertIn("P0217: Engine Overheating", engine.fault_codes)

    def test_low_oil_triggers_fault(self):
        engine = FourCylinderEngine()
        sensors = Sensors(engine, mode="idle", scenario="low_oil")
        sensors.oil_pressure = 19.0
        sensors._check_faults()
        self.assertIn("P0524: Oil Pressure Too Low", engine.fault_codes)
    def test_low_fuel_triggers_fault(self):
        engine = FourCylinderEngine()
        sensors = Sensors(engine, mode="city", scenario="normal")
        sensors.fuel_level = 5.0
        sensors.update()
        self.assertIn("P0087: Low Fuel Pressure", engine.fault_codes)

if __name__ == "__main__":
    unittest.main()