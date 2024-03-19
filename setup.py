from setuptools import setup

setup(
    name="pytest-energy-reporter",
    version='0.1.0',
    description='A energy estimation reporter for pytest',
    url='https://github.com/delanoflipse/pytest-energy-reporter',
    packages=["pytest-energy-reporter"],
    # the following makes a plugin available to pytest
    entry_points={"pytest11": ["pytest_energy_reporter = pytest-energy-reporter.plugin"]},
    # custom PyPI classifier for pytest plugins
    classifiers=["Framework :: Pytest"],
)
