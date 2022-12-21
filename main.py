import matplotlib.pyplot as plt
from expand_spline import *
import math as m
import numpy as np
from MathFun import MathFun as mf


def f(x: float):
    return x * x - m.sin(m.pi * x)


def plot_graphic():
    plt.grid(True)
    plt.title("График зависимости ∆Sn(n)")
    plt.plot(counts_of_nodes, errors, color="orange")
    plt.show()


counts_of_nodes = [i for i in range(10, 100 + 1, 10)]
errors = []
print(f'n       ∆fn{" " * 25}  δfn{" " * 25} ')
for n in counts_of_nodes:
    xn = np.linspace(0.4, 0.9, n)
    yn = [f(xi) for xi in xn]
    spline = compute_spline(xn, yn)
    between_nodes = np.linspace(0.4, 0.9, n * 5)
    splines = [spline(xi) for xi in between_nodes]
    exact_y = [f(xi) for xi in between_nodes]
    remainder = mf.rn(exact_y, splines)
    percent_err = remainder / mf.norm(exact_y) * 100
    errors.append(remainder)

    print(f'{n:^3}| {remainder:^25}| {percent_err:^25}|')

plot_graphic()
