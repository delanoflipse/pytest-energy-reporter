import pytest
import logging

energy_metrics = {}

def pytest_addoption(parser):
    parser.addoption("--energy-runs", action="store", default=3, type=int,
                     help="Number of runs for tests marked as 'energy'")
    
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "energy: mark test to be run for energy consumption analysis"
    )

@pytest.hookimpl
def pytest_runtest_call(item):    
    if not "energy" in item.keywords:
        return
    
    energy_runs = item.session.config.getoption("--energy-runs")
    # TODO: run energy test
    logging.debug(f"Energy runs: {energy_runs}")
    metrics = None
    item.runtest()
    energy_metrics[item.nodeid] = metrics
    logging.debug(f"Energy: {metrics}")

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    terminalreporter.write_sep('-', 'Energy Summary')
    # all_items = terminalreporter.stats.get("passed", []) + terminalreporter.stats.get("failed", [])
    # energy_tests = [item for item in all_items if "energy" in getattr(item, "keywords", [])]
    terminalreporter.write_sep("=", "Average runtime for tests marked as 'energy'")
    for key in energy_metrics:
        metrics = energy_metrics[key]
        logging.debug(f"Energy test item({key}): {metrics}")
        avg_runtime = sum(metrics['energy']) / len(metrics['energy'])
        terminalreporter.write_line(f"{avg_runtime:.6f} seconds (average)")