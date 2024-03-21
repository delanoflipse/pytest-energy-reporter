import pytest
import logging
from .energy_consumption_reporter.plugin.energy_test import EnergyTest
import numpy as np

energy_metrics = []


class EnergyMeasurement:
    def __init__(self, name: str, time: float, energy: float, power: float):
        self.name = name
        self.time = time
        self.energy = energy
        self.power = power

    def __str__(self):
        return f"Name: {self.name}\tTime: {self.time:.2f} s\tEnergy: {self.energy:.2f} J\tPower: {self.power:.2f} W"


def pytest_addoption(parser):
    parser.addoption("--energy-runs", action="store", default=3, type=int,
                     help="Number of runs for tests marked as 'energy'")


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "energy(n): specify the number of iterations for energy analysis."
    )


@pytest.hookimpl
def pytest_runtest_call(item):
    # only run the tests marked for energy
    if not "energy" in item.keywords:
        return
    
    # define the number of runs for the energy test
    energy_marker = item.get_closest_marker("energy")
    if energy_marker and energy_marker.kwargs and "n" in energy_marker.kwargs:
        energy_runs = energy_marker.kwargs.get("n")
    else:
        energy_runs = item.session.config.getoption("--energy-runs")

    # intialize the energy test
    energy_test = EnergyTest(func_name=item.nodeid)
    
    # run tests and collect metrics
    try:
        metrics = energy_test.test(item.runtest, energy_runs)
        measurement = EnergyMeasurement(item.nodeid,
                                        np.mean(metrics['time']),
                                        np.mean(metrics['energy']),
                                        np.mean(metrics['power'])
                                        )
        energy_metrics.append(measurement)
    except Exception as e:
        raise e

def print_table_str(headers=list[str], values=list[list[str]]) -> list[str]:
    # Find the maximum width of the columns
    column_widths = [len(header) for header in headers]
    for row in values:
        for i, cell in enumerate(row):
            column_widths[i] = max(column_widths[i], len(str(cell)))

    # Create the table
    table = []
    table.append(" | ".join([header.ljust(column_widths[i]) for i, header in enumerate(headers)]))
    table.append("-" * (sum(column_widths) + len(headers) * 3 - 1))
    for row in values:
        table.append(" | ".join([str(cell).ljust(column_widths[i]) for i, cell in enumerate(row)]))

    return table

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    terminalreporter.write_sep('-', 'Energy Summary')
    
    # get the energy metrics sorted by power
    ordered_measurements = sorted(energy_metrics, key=lambda x: x.power)
    
    # report the energy metrics as a table
    table_strings = print_table_str(['Test', 'Time (s)', 'Energy (J)', 'Power (W)'],
                                    [[m.name, f"{m.time:.2f}", f"{m.energy:.2f}", f"{m.power:.2f}"] for m in ordered_measurements])
    for line in table_strings:
        terminalreporter.write_line(line)
