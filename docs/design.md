# Design Notes — OOP Vehicle Diagnostic Simulator

## UML Class Diagram (text representation)

```
Vehicle (ABC)
├── get_engine_type() [abstract]
├── log_fault(code, description)
├── fault_codes: list[str]
├── rpm_min, rpm_max, max_temp
│
├── FourCylinderEngine  (rpm 600–6500, max_temp 105°C)
├── V6Engine            (rpm 600–7000, max_temp 110°C)
└── V8Engine            (rpm 700–7500, max_temp 115°C)

Battery
├── vehicle: Vehicle
├── voltage: float
└── update() → checks P0562 / P0563

Sensors
├── vehicle: Vehicle
├── mode: str
├── scenario: str
├── update() → updates rpm, coolant_temp, oil_pressure, fuel_level, o2_voltage
└── _check_faults() → checks P0217, P0524, P0087

Dashboard
├── vehicle: Vehicle
├── sensors: Sensors
├── battery: Battery
├── report: DiagnosticReport
└── run() → launches Matplotlib animation

DiagnosticReport
└── display() → prints fault summary
```

## OOP Principles Applied

- **Encapsulation**: Each class manages its own state (e.g., `Battery` owns voltage logic).
- **Inheritance**: `FourCylinderEngine`, `V6Engine`, `V8Engine` all extend `Vehicle`.
- **Polymorphism**: `get_engine_type()` returns different values per subclass; sensor thresholds adapt via `vehicle.max_temp`.
- **Abstraction**: `Vehicle` is an ABC; callers don't need to know engine-specific internals.

## Driving Modes

| Mode         | RPM Range    | Temp Range  |
|--------------|--------------|-------------|
| Idle         | 600–900      | 85–92°C     |
| City Driving | 1000–3000    | 90–100°C    |
| Highway      | 2500–4000    | 95–105°C    |
| Heavy Load   | 3000–5500    | 100–115°C   |

## Fault Codes

| Code  | Trigger                       |
|-------|-------------------------------|
| P0217 | coolant_temp > engine max_temp |
| P0563 | battery voltage > 15V         |
| P0562 | battery voltage < 11.5V       |
| P0087 | fuel_level < 10%              |
| P0524 | oil_pressure < 20 PSI         |
