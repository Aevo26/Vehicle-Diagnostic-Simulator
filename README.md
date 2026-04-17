# Group 3 — OOP Vehicle Diagnostic Simulator
**Texas State University | Spring 2026**
 
---
 
## Project Overview
An Object-Oriented Vehicle Diagnostic Simulator built in Python. The program simulates real automotive sensor systems including engine temperature, RPM, battery voltage, fuel level, and oil pressure. Sensor readings fluctuate over time mimicking a real car running, and fault codes are triggered when values exceed safe thresholds — similar to how a real OBD-II scanner works.
 
The user selects an engine type at startup and the simulator adjusts its behavior accordingly. All data is visualized in real time using Matplotlib graphs and an optional Tkinter dashboard.
 
---
 
## Team Members
| Name | Role | TXST Email |
|------|------|------------|
| Aevin Tweedie | Project Manager | lav115@txstate.edu |
| Jesse Leavitt  | Developer       | dvu13@txstate.edu |
| [Member 3]  | Developer       | @txstate.edu |
 
---
 
## Engine Types Supported
| Engine Type | RPM Range    | Max Temp |
|-------------|--------------|----------|
| 4-Cylinder  | 600–6500 RPM | 105°C    |
| V6          | 600–7000 RPM | 110°C    |
| V8          | 700–7500 RPM | 115°C    |
 
All fault codes follow the universal OBD-II standard and apply across all engine types.
 
---
 
## Tech Stack
- **Language:** Python 3.x
- **Paradigm:** Object-Oriented Programming (OOP)
- **Visualization:** Matplotlib
- **GUI:** Tkinter (optional dashboard)
- **Tools:** Git, GitHub, VS Code / PyCharm
---
 
## OOP Concepts Demonstrated
- **Encapsulation** — each vehicle system manages its own data
- **Inheritance** — engine types inherit from a base Vehicle class
- **Polymorphism** — different engine types behave differently under load
- **Abstraction** — fault detection logic hidden inside each class
---
 
## Project Structure
```
EE-Group3/
├── README.md
├── main.py                  # Entry point, user selects engine type
├── src/
│   ├── __init__.py
│   ├── vehicle.py           # Base Vehicle class
│   ├── engine.py            # Engine class (4-cyl, V6, V8)
│   ├── battery.py           # Battery class
│   ├── sensors.py           # Sensor readings (oil, coolant, O2)
│   ├── dashboard.py         # Displays live readings
│   └── diagnostic_report.py # Generates fault code report
├── tests/
│   ├── __init__.py
│   └── test_systems.py      # Unit tests
└── docs/
    └── design.md            # UML class diagram & design notes
```
 
---
 
## Fault Codes (OBD-II Standard)
| Code  | Description           | Trigger Condition          |
|-------|-----------------------|----------------------------|
| P0217 | Engine Overheating    | Temp exceeds max threshold |
| P0563 | Battery Voltage High  | Voltage > 15V              |
| P0562 | Battery Voltage Low   | Voltage < 11.5V            |
| P0087 | Low Fuel Pressure     | Fuel level < 10%           |
| P0524 | Oil Pressure Too Low  | Oil pressure < 20 PSI      |
 
---
 
## Getting Started
 
### Clone the Repository
```bash
git clone https://github.com/lav115/EE-Group3.git
cd EE-Group3
```
 
### Install Dependencies
```bash
pip install matplotlib
```
 
### Run the Simulator
```bash
python main.py
```
 
---
 
## Project Timeline
| Milestone                  | Due Date |
|----------------------------|----------|
| Repo Setup & Planning      |          |
| Class Design & UML         |          |
| Core System Implementation |          |
| Visualization & Dashboard  |          |
| Testing & Bug Fixes        |          |
| Final Submission           |          |
 
---
 
## Info
- **Group:** 3
- **Project Option:** 9
 
