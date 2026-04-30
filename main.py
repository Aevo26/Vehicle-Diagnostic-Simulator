import matplotlib.pyplot as plt

from src.engine import FourCylinderEngine, V6Engine, V8Engine
from src.dashboard import Dashboard
from src.tkinter_dashboard import TkinterDashboard


def select_engine():
    print("Select Engine Type:")
    print("  1. 4-Cylinder")
    print("  2. V6")
    print("  3. V8")
    choice = input("Enter choice (1-3): ").strip()
    if choice == "1":
        return FourCylinderEngine()
    elif choice == "2":
        return V6Engine()
    elif choice == "3":
        return V8Engine()
    else:
        print("Invalid choice, defaulting to 4-Cylinder.")
        return FourCylinderEngine()


def select_mode():
    print("\nSelect Driving Mode:")
    print("  1. Idle")
    print("  2. City Driving")
    print("  3. Highway")
    print("  4. Heavy Load")
    choice = input("Enter choice (1-4): ").strip()
    modes = {"1": "idle", "2": "city", "3": "highway", "4": "heavy_load"}
    return modes.get(choice, "idle")


def select_scenario():
    print("\nSelect Scenario:")
    print("  1. Normal Drive")
    print("  2. Overheating Engine")
    print("  3. Failing Battery")
    print("  4. Low Oil Pressure")
    choice = input("Enter choice (1-4): ").strip()
    scenarios = {
        "1": "normal",
        "2": "overheating",
        "3": "failing_battery",
        "4": "low_oil",
    }
    return scenarios.get(choice, "normal")


def main():
    print("=== OOP Vehicle Diagnostic Simulator ===\n")
    engine = select_engine()
    mode = select_mode()
    scenario = select_scenario()

    use_tkinter = input("\nEnable Tkinter dashboard? (y/n): ").strip().lower() == "y"

    dashboard = Dashboard(engine, mode=mode, scenario=scenario)

    if use_tkinter:
        dashboard.run(block=False, show_report=False)
        mpl_root = plt.get_current_fig_manager().window
        tkinter_dashboard = TkinterDashboard(
            dashboard.sensors, dashboard.battery, dashboard.vehicle,
            owns_update=False, master=mpl_root,
        )
        tkinter_dashboard.run()
        dashboard.report.display()
    else:
        dashboard.run()


if __name__ == "__main__":
    main()
