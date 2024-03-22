import pytest

pytest_plugins = ("pytest_energy_reporter.plugin")

def fib(n):
  if n == 0:
    return 0
  elif n == 1:
    return 1
  else:
    return fib(n-1) + fib(n-2)

@pytest.mark.energy(n=5)
def test_fib_n():
  fib(35)

@pytest.mark.energy()
def test_fib_2x():
  fib(35)
  fib(35)

@pytest.mark.energy()
def test_fib_faster():
  fib(34)
