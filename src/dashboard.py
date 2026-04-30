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

    def run(self, block: bool = True, show_report: bool = True):
        plt.style.use("dark_background")

        line_colors = ["#00d4ff", "#ff6b6b", "#6bff6b", "#ffd700", "#ff9f43", "#c56bff"]

        fig, axes = plt.subplots(3, 2, figsize=(12, 8))
        fig.patch.set_facecolor("#0d0d0d")
        fig.suptitle(f"Vehicle Diagnostic — {self.vehicle.get_engine_type()}", fontsize=14, color="white")

        keys = ["rpm", "coolant_temp", "oil_pressure", "fuel_level", "battery", "o2_voltage"]
        labels = ["RPM", "Coolant Temp (°C)", "Oil Pressure (PSI)", "Fuel Level (%)", "Battery Voltage (V)", "O2 Voltage (V)"]
        plot_axes = [axes[0][0], axes[0][1], axes[1][0], axes[1][1], axes[2][0], axes[2][1]]
        lines = [ax.plot([], [], color=color, linewidth=1.5)[0] for ax, color in zip(plot_axes, line_colors)]

        for ax, label, color in zip(plot_axes, labels, line_colors):
            ax.set_facecolor("#1a1a1a")
            ax.set_title(label, color=color, fontsize=10)
            ax.set_xlim(0, MAX_POINTS)
            ax.tick_params(colors="#aaaaaa")
            ax.grid(True, color="#333333", linewidth=0.5)
            for spine in ax.spines.values():
                spine.set_edgecolor("#333333")

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

        self.ani = animation.FuncAnimation(fig, update, interval=500, blit=False, cache_frame_data=False)
        plt.tight_layout()
        plt.show(block=block)

        if show_report:
            self.report.display()
