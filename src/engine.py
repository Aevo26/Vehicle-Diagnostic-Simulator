from src.vehicle import Vehicle


class FourCylinderEngine(Vehicle):
    def __init__(self):
        super().__init__(rpm_min=600, rpm_max=6500, max_temp=105.0)

    def get_engine_type(self) -> str:
        return "4-Cylinder"


class V6Engine(Vehicle):
    def __init__(self):
        super().__init__(rpm_min=600, rpm_max=7000, max_temp=110.0)

    def get_engine_type(self) -> str:
        return "V6"


class V8Engine(Vehicle):
    def __init__(self):
        super().__init__(rpm_min=700, rpm_max=7500, max_temp=115.0)

    def get_engine_type(self) -> str:
        return "V8"
