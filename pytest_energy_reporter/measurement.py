
from .energy_consumption_reporter.plugin.energy_test import EnergyModel, EnergyTest
import numpy as np

energy_model = EnergyModel()
energy_model.setup()

class EnergyMeasurement:
    def __init__(self, name: str, time: float, energy: float, power: float):
        self.name = name
        # Average time in seconds
        self.time = time
        # Energy in Joules
        self.energy = energy
        # Energy in Watts
        self.power = power

    def __str__(self):
        return f"Name: {self.name}\tTime: {self.time:.2f} s\tEnergy: {self.energy:.2f} J\tPower: {self.power:.2f} W"
      
def measure(func, n: int = 3):
    energy_test = EnergyTest(energy_model=energy_model, test_id=func.__name__)
    measurement = get_measurement(energy_test, func, n)
    return measurement

def get_measurement(e: EnergyTest, func, n: int = 3):
    metrics = e.test(func, n)
    measurement = EnergyMeasurement(e.test_id,
                                    np.mean(metrics['time']),
                                    np.mean(metrics['energy']),
                                    np.mean(metrics['power'])
                                    )
    return measurement