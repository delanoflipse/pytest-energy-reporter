import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

def pytest_configure(config):
  if config.pluginmanager.hasplugin("pytest_energy_reporter"):
    logger.debug("pytest_energy_reporter already registered")
  else:
    logger.debug("Registering pytest_energy_reporter")
    config.pluginmanager.register("pytest_energy_reporter")