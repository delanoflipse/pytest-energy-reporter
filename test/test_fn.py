from time import sleep
import pytest
from pytest_energy_reporter.measurement import measure, measure_energy

def fib(n):
  if n == 0:
    return 0
  elif n == 1:
    return 1
  else:
    return fib(n-1) + fib(n-2)

@pytest.mark.energy(n=20)
def test_fib_35_n20():
  fib(35)

@pytest.mark.energy(n=10)
def test_fib_35_n10():
  fib(35)
  
@pytest.mark.energy(n=5)
def test_fib_35_n5():
  fib(35)
  
@pytest.mark.energy(n=3)
def test_fib_35_n3():
  fib(35)
  
@pytest.mark.energy(n=1)
def test_fib_35_n1():
  fib(35)

@pytest.mark.energy
def test_fib_35_2x():
  fib(35)
  fib(35)

@pytest.mark.energy
def test_fib_34():
  fib(34)

@pytest.mark.energy
def test_fib_34_2x():
  fib(34)
  fib(34)

@pytest.mark.energy
def test_fib_34_3x():
  fib(34)
  fib(34)
  fib(34)

@pytest.mark.energy
def test_sleep_2s():
  sleep(2)

@pytest.mark.energy
def test_sleep_5s():
  sleep(5)

def test_fib_assert_w():
  energy, res, err = measure(lambda: fib(34), n=3)
  assert res == 5702887
  assert err == None
  assert energy.power_w < 200

def test_fib_assert_j():
  energy = measure_energy(lambda: fib(34), n=2)
  assert energy.energy_j < 1000
