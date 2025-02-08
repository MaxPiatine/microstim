from math import sqrt
import numpy as np
import matplotlib.pylab as plt

def f(x):
    return np.exp(-x**2/2)*1/sqrt(2*np.pi)


x = np.arange(0, 4, 0.1)

plt.plot(x, f(x))
plt.show()