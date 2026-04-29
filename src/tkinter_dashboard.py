import tkinter as tk

from src.sensors import Sensors
from src.battery import Battery
from src.vehicle import Vehicle

_FIELDS = [
    ("RPM",                 "rpm"),
    ("Coolant Temp (°C)",   "coolant_temp"),
    ("Oil Pressure (PSI)",  "oil_pressure"),
    ("Fuel Level (%)",      "fuel_level"),
    ("Battery Voltage (V)", "battery"),
    ("O2 Voltage (V)",      "o2_voltage"),
]


class TkinterDashboard:
    def __init__(self, sensors: Sensors, battery: Battery, vehicle: Vehicle,
                 owns_update: bool = True, master=None):
        self.sensors = sensors
        self.battery = battery
        self.vehicle = vehicle
        self._owns_update = owns_update

        if master is not None:
            self.root = tk.Toplevel(master)
            self._loop_root = master
        else:
            self.root = tk.Tk()
            self._loop_root = self.root
        self.root.title(f"Vehicle Diagnostic — {vehicle.get_engine_type()}")
        self.root.resizable(False, False)

        self._value_vars: dict[str, tk.StringVar] = {}
        for row, (label_text, key) in enumerate(_FIELDS):
            tk.Label(self.root, text=label_text, anchor="w", width=22).grid(
                row=row, column=0, padx=10, pady=4, sticky="w"
            )
            var = tk.StringVar(value="—")
            tk.Label(self.root, textvariable=var, anchor="e", width=12).grid(
                row=row, column=1, padx=10, pady=4, sticky="e"
            )
            self._value_vars[key] = var

        fault_row = len(_FIELDS)
        tk.Label(
            self.root, text="Active Fault Codes:",
            anchor="w", font=("TkDefaultFont", 9, "bold"),
        ).grid(row=fault_row, column=0, columnspan=2, padx=10, pady=(12, 2), sticky="w")
        self._fault_frame = tk.Frame(self.root)
        self._fault_frame.grid(
            row=fault_row + 1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="w"
        )

    def _update(self):
        if self._owns_update:
            self.sensors.update()
        readings = self.sensors.get_readings()
        if self._owns_update:
            self.battery.update(rpm=readings["rpm"])
        readings["battery"] = self.battery.get_voltage()

        for key, var in self._value_vars.items():
            var.set(str(readings[key]))

        for widget in self._fault_frame.winfo_children():
            widget.destroy()
        for fault in self.vehicle.fault_codes:
            tk.Label(self._fault_frame, text=fault, fg="red", anchor="w").pack(anchor="w")

        self.root.after(500, self._update)

    def run(self):
        self.root.after(500, self._update)
        self._loop_root.mainloop()
