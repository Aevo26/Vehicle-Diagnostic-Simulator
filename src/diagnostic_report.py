from src.vehicle import Vehicle


class DiagnosticReport:
    def __init__(self, vehicle: Vehicle):
        self.vehicle = vehicle

    def display(self):
        print("\n=== Diagnostic Report ===")
        print(f"Engine: {self.vehicle.get_engine_type()}")
        if self.vehicle.fault_codes:
            print("Fault Codes Triggered:")
            for code in self.vehicle.fault_codes:
                print(f"  - {code}")
        else:
            print("No fault codes — all systems normal.")
        print("=========================\n")
