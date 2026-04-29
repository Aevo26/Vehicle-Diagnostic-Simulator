import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

from src.vehicle import Vehicle
from src.sensors import Sensors
from src.battery import Battery
from src.diagnostic_report import DiagnosticReport

MAX_POINTS = 60


class Dashboard:
    def __init__(self, vehicle: Vehicle, mode: str = "city", scenario: str = "normal"):
        self.vehicle = vehicle
        self.sensors = Sensors(vehicle, mode=mode, scenario=scenario)
        self.battery = Battery(vehicle, scenario=scenario)
        self.report = DiagnosticReport(vehicle)

        self.history = {key: deque(maxlen=MAX_POINTS) for key in
                        ["rpm", "coolant_temp", "oil_pressure", "fuel_level", "battery", "o2_voltage"]}

    def run(self):
        fig, axes = plt.subplots(3, 2, figsize=(12, 8))
        fig.suptitle(f"Vehicle Diagnostic — {self.vehicle.get_engine_type()}", fontsize=14)

        keys = ["rpm", "coolant_temp", "oil_pressure", "fuel_level", "battery", "o2_voltage"]
        labels = ["RPM", "Coolant Temp (°C)", "Oil Pressure (PSI)", "Fuel Level (%)", "Battery Voltage (V)", "O2 Voltage (V)"]
        plot_axes = [axes[0][0], axes[0][1], axes[1][0], axes[1][1], axes[2][0], axes[2][1]]
        lines = [ax.plot([], [])[0] for ax in plot_axes]

        for ax, label in zip(plot_axes, labels):
            ax.set_title(label)
            ax.set_xlim(0, MAX_POINTS)

        def update(_frame):
            self.sensors.update()
            readings = self.sensors.get_readings()
            self.battery.update(rpm=readings["rpm"])
            readings["battery"] = self.battery.get_voltage()

            for key, value in readings.items():
                self.history[key].append(value)

            for line, key, ax in zip(lines, keys, plot_axes):
                data = list(self.history[key])
                line.set_data(range(len(data)), data)
                if data:
                    margin = (max(data) - min(data)) * 0.1 or 1
                    ax.set_ylim(min(data) - margin, max(data) + margin)

            return lines

        ani = animation.FuncAnimation(fig, update, interval=500, blit=False, cache_frame_data=False)
        plt.tight_layout()
        plt.show()

        self.report.display()
