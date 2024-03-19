from setuptools import setup

setup(
    name="pytest-energy-reporter",
    packages=["pytest-energy-reporter"],
    # the following makes a plugin available to pytest
    entry_points={"pytest11": ["pytest_energy_reporter = pytest-energy-reporter.plugin"]},
    # custom PyPI classifier for pytest plugins
    classifiers=["Framework :: Pytest"],
)
