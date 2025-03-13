import numpy as np
import matplotlib.pyplot as plt

# Define the ODE
def dydt(y):
    return -2 * y

# Euler method
def euler_solve(y0, t_end, DT):
    t = np.arange(0, t_end + DT, DT)  # Time array
    y = np.zeros_like(t)              # Solution array
    y[0] = y0                         # Initial condition

    for i in range(1, len(t)):
        y[i] = y[i-1] + DT * dydt(y[i-1])  # Euler step

    return t, y

# Parameters
y0 = 1       # Initial condition
t_end = 5    # End time
DT1 = 0.1    # Large time step
DT2 = 0.01   # Small time step

# Solve with two different DeltaT values
t1, y1 = euler_solve(y0, t_end, DT1)
t2, y2 = euler_solve(y0, t_end, DT2)

# Exact solution
t_exact = np.linspace(0, t_end, 1000)
y_exact = np.exp(-2 * t_exact)

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(t_exact, y_exact, label="Exact Solution", color="black", linewidth=2)
plt.plot(t1, y1, label=f"Euler (DT = {DT1})", marker="o", linestyle="--")
plt.plot(t2, y2, label=f"Euler (DT = {DT2})", marker="x", linestyle="--")
plt.xlabel("Time (t)")
plt.ylabel("y(t)")
plt.title("Euler Method with Different DeltaT Values")
plt.legend()
plt.grid()
plt.show()