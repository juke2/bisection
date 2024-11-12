from typing import Callable, Optional
import math

DEFAULT_MAX_ITER = 50
DEFAULT_FTOL = 1e-50


class MaxIterException(Exception):
    """Raises in the event that the amount of iterations exceeds maxiter."""


def bisection(
    f: Callable,
    a: float,
    b: float,
    maxiter: Optional[int] = DEFAULT_MAX_ITER,
    ftol: Optional[float] = DEFAULT_FTOL,
) -> float:
    """
    performs the bisection method in order to apporimate the zeroes of a certain function.
    input:
    f - function being called
    a - x value before root
    b - x value after root
    maxiter - the maximum amount of iterations before the bisection method is abandonded and MaxIterException is thrown.
    Default maxiter = 50
    ftol - the tolerance for a root to be considered "found"
    Default ftol = 1e-50
    output:
    the root where f(root) is within the given tolerance.
    if the root is not found within the given amount of iterations, MaxIterException is thrown.
    """
    for _iter in range(maxiter):
        x_r = (a + b) / 2
        f_a = f(a)
        f_x_r = f(x_r)
        if abs(f_x_r) < ftol:
            return x_r
        if f_a * f_x_r < 0:
            b = x_r
        else:
            a = x_r
    raise MaxIterException
