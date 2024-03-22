
from .energy_consumption_reporter.plugin.energy_test import EnergyModel, EnergyTest
import numpy as np

energy_model = EnergyModel()
energy_model.setup()

class EnergyMeasurement:
    def __init__(self, name: str, time_ms: float, energy_j: float, power_w: float):
        self.name = name
        # Average time in mili sceonds
        self.time_ms = time_ms
        # Energy in Joules
        self.energy_j = energy_j
        # Energy in Watts
        self.power_w = power_w

    def __str__(self):
        return f"Name: {self.name}\tTime: {self.time_ms:.2f} s\tEnergy: {self.energy_j:.2f} J\tPower: {self.power_w:.2f} W"
      
def measure(func, n: int = 3):
    energy_test = EnergyTest(energy_model)
    test_id = func.__name__
    measurement = get_measurement(energy_test, func, test_id, n)
    return measurement

def get_measurement(e: EnergyTest, func, test_id: str, n: int = 3):
    metrics = e.test(func, n, test_id=test_id)
    measurement = EnergyMeasurement(test_id,
                                    np.mean(metrics['time']),
                                    np.mean(metrics['energy']),
                                    np.mean(metrics['power'])
                                    )
    return measurement