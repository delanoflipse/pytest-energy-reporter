import pytest

from .measurement import EnergyMeasurement, energy_model, get_measurement
from .energy_consumption_reporter.plugin.energy_test import EnergyTest

energy_metrics: list[EnergyMeasurement] = []

def pytest_addoption(parser):
    parser.addoption("--energy-runs", action="store", default=3, type=int,
                     help="Number of runs for tests marked as 'energy'")

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
    energy_test = EnergyTest(test_id=item.nodeid, energy_model=energy_model)
    
    # run tests and collect metrics
    try:
        measurement = get_measurement(energy_test, item.runtest, energy_runs)
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
    ordered_measurements = sorted(energy_metrics, key=lambda x: x.power_w)
    
    # report the energy metrics as a table
    table_strings = print_table_str(['Test', 'Time (ms)', 'Energy (J)', 'Power (W)'],
                                    [[m.name, f"{m.time_ms:.2f}", f"{m.energy_j:.2f}", f"{m.power_w:.2f}"] for m in ordered_measurements])
    for line in table_strings:
        terminalreporter.write_line(line)
