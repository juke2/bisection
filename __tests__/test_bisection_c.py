from src.bisection import bisection, DEFAULT_FTOL, MaxIterException
import math
import pytest
import sys
import subprocess


subprocess.run(
    "gcc src/bisection.c -lm -o ./src/main.exe", stdout=sys.stdout, shell=True
)
SMALL_FTOL = 1e-10
FTOL_FOR_EXPECTED = 1e-3


f_ex = lambda x: math.pow((x - math.sqrt(2)), 3)
f_x = lambda x: (1 - x) * math.sin(math.exp(-math.pow(x, 2))) - x * math.cos(
    0.5 * math.pow(x, 2)
)
g_x = lambda x: (math.pow(x, 2) - 7 / 2 * x - 15 / 2) * (
    (8 * math.pow(x, 2) - 10 * x - 3) / 100
)
h_x = lambda x: sum([math.sin(n * math.pi * x) for n in range(1, 4)])
v_x = lambda x: h_x(x) - g_x(x)


def read_output() -> float:
    with open("src/output/output_c.txt", "r") as file:
        output = file.read()
        return float(output)


def test_f_ex():

    a, b = 1.0, 2.0
    iter_limit = 300
    expected = math.sqrt(2)
    assert f_ex(expected) == 0
    subprocess.run(
        f"src/main.exe FE_x {a} {b} {iter_limit} {DEFAULT_FTOL}",
        stdout=sys.stdout,
        shell=True,
    )
    result = read_output()
    assert -DEFAULT_FTOL < f_ex(result) and f_ex(result) < DEFAULT_FTOL


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (1.0, 2, 1.78274),
        (3.0, 3.5, 3.06996),
    ],
)
def test_f_x(a, b, expected):

    iter_limit = 300
    subprocess.run(
        f"src/main.exe F_x {a} {b} {iter_limit} {SMALL_FTOL}",
        stdout=sys.stdout,
        shell=True,
    )
    result = read_output()
    assert -FTOL_FOR_EXPECTED < f_x(expected) and f_x(expected) < FTOL_FOR_EXPECTED
    assert -SMALL_FTOL < f_x(result) and f_x(result) < SMALL_FTOL


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (-3.0, 1.3, -3 / 2),
        (-2.0, 1.2, -1 / 4),
        (0.0, 2.0, 3 / 2),
        (3.2, 6.0, 5.0),
    ],
)
def test_g_x(a, b, expected):
    iter_limit = 300
    subprocess.run(
        f"src/main.exe G_x {a} {b} {iter_limit} {DEFAULT_FTOL}",
        stdout=sys.stdout,
        shell=True,
    )
    result = read_output()
    assert g_x(expected) == 0
    assert -DEFAULT_FTOL < g_x(result) and g_x(result) < DEFAULT_FTOL


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (
            1,
            2,
            2,
        ),  # technically this isn't within the function but using it to test this case
        (1.25, 1.7, 1.5),
        (0.0, 2.0, 4 / 3),
        (0.7, 1.45, 1.0),
        (0.4, 0.82, 2 / 3),
        (0.21, 0.56, 0.5),
        (-0.5, 1.5, 0),
        (-0.7, 0.63, -0.5),
        (-0.7, 0.42, -2 / 3),
        (-1.0, 0.0, -1.0),  # same as 1st
    ],
)
def test_h_x(a, b, expected):
    iter_limit = 1000
    subprocess.run(
        f"src/main.exe H_x {a} {b} {iter_limit} {SMALL_FTOL}",
        stdout=sys.stdout,
        shell=True,
    )
    result = read_output()
    assert -FTOL_FOR_EXPECTED < h_x(expected) and h_x(expected) < FTOL_FOR_EXPECTED
    assert -SMALL_FTOL < h_x(result) and h_x(result) < SMALL_FTOL


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (
            -0.95,
            -0.7,
            -0.92133,
        ),  # no clue why my formatter hates me
        (-0.85, 0.2, -0.743531),
        (-1.0, 0, -0.472956),
        (0, 0.1, 0.012522),
        (0.2, 0.73, 0.438926),
        (0, 1.0, 0.792559),
        (0.7, 1.0, 0.895689),
        (0.98, 1.5, 1.375805),
        (-0.43, 1.98, 1.5),
        (1.0, 2.0, 1.954348),
    ],
)
def test_v_x(a, b, expected):

    iter_limit = 1000
    subprocess.run(
        f"src/main.exe V_x {a} {b} {iter_limit} {SMALL_FTOL}",
        stdout=sys.stdout,
        shell=True,
    )
    result = read_output()
    assert -FTOL_FOR_EXPECTED < v_x(expected) and v_x(expected) < FTOL_FOR_EXPECTED
    assert -SMALL_FTOL < v_x(result) and v_x(result) < SMALL_FTOL


@pytest.mark.parametrize(
    "function, a, b, maxiter, ftol, expect_nan",
    [
        ("FE_x", 5.0, 6.0, 100, DEFAULT_FTOL, True),
        ("FE_x", 1.0, 2.0, 20, DEFAULT_FTOL, True),
        ("F_x", 0.7, 0.9, 100, DEFAULT_FTOL, True),
        ("F_x", 1.1, 1.9, 1000, SMALL_FTOL, False),
        ("G_x", 1.0, 2.0, 1, DEFAULT_FTOL, False),
        ("G_x", 4.0, 6.0, 1, DEFAULT_FTOL, False),
        ("G_x", 2.0, 3.0, 10000, DEFAULT_FTOL, True),
        ("H_x", 1.5, 1.5, 1, SMALL_FTOL, False),
        ("H_x", -0.5, -0.5, 1, SMALL_FTOL, False),
        ("H_x", 0.0, 0.0, 1, DEFAULT_FTOL, False),
        ("H_x", -0.1, -0.05, 1, DEFAULT_FTOL, True),
        ("H_x", -1.0, -2 / 3, 1000, SMALL_FTOL, False),
        ("V_x", 0.0, 0.3, 1000, SMALL_FTOL, False),
        ("V_x", 0.0, 0.0, 10000, 0.1, True),
        ("V_x", 3.0, 5.0, 1000, 100, False),
        ("V_x", 0.3, 0.4, 100, DEFAULT_FTOL, True),
    ],
)
def test_max_iter_exception(function, a, b, maxiter, ftol, expect_nan):
    subprocess.run(
        f"src/main.exe {function} {a} {b} {maxiter} {ftol}",
        stdout=sys.stdout,
        shell=True,
    )
    result = read_output()
    if expect_nan:
        assert math.isnan(result)
    else:
        assert not math.isnan(result)
