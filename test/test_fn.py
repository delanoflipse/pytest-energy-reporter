import pytest

pytest_plugins = ("pytester", "pytest_energy_reporter.plugin")

def fib(n):
  if n == 0:
    return 0
  elif n == 1:
    return 1
  else:
    return fib(n-1) + fib(n-2)

@pytest.mark.energy(n=5)
def test_fib():
  fib(35)

@pytest.mark.energy
def test_fib_2():
  fib(39)
  
@pytest.mark.energy
def test_fib_2x():
  fib(39)
  fib(39)