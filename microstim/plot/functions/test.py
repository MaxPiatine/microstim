import matplotlib.pylab as plt
import matplotlib.animation as animation
import numpy as np

from microstim.globals import T_RANGE, X_RANGE, intensity, sigma, weights, sigma, gamma
from microstim.main import model
from microstim.utils import rect, sigmoid

from PIL import Image
import glob
import os

# Call your model function to ensure other computations complete if necessary
v_e, v_i, rho_e, rho_i, nu_e, nu_i = model(intensity, weights, sigma, rect, gamma, is_depolarized=False)

# Get all image files sorted by modification time
files = sorted(glob.glob("./microstim/plot/results/*.png"), key=os.path.getmtime)

# Load images as numpy arrays
images = [np.array(Image.open(file)) for file in files]

# Ensure results directory exists
os.makedirs("results", exist_ok=True)

# Set up the figure and axis
fig, ax = plt.subplots()
im = ax.imshow(images[0], animated=True)
plt.axis("off")  # Turn off the axis for clean visuals

# Define the update function for animation
def update(i):
    im.set_array(images[i])
    return [im]

# Create the animation
animated = animation.FuncAnimation(
    fig, update, frames=len(images), interval=150, blit=True, repeat_delay=10
)

# Save the animation as a GIF
animated.save("./microstim/plot/animations/Vi_e180_i1.gif", writer="pillow", fps=30)
plt.show()