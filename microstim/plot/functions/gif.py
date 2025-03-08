import matplotlib.pylab as plt
import matplotlib.animation as animation
import numpy as np

from microstim.globals import intensity, sigma, weights, sigma, gamma, start_boost
from microstim.main import model
from microstim.utils import rect, sigmoid, sigmoidalRect

from PIL import Image
import glob
import os

boost = start_boost.copy()
v_e, v_i, rho_e, rho_i, nu_e, nu_i = model(intensity, weights, sigma, rect, boost, is_depolarized=True)


files = sorted(glob.glob("./microstim/plot/results2/*.png"), key=os.path.getmtime)
images = [np.array(Image.open(file)) for file in files]
os.makedirs("results", exist_ok=True)

fig, ax = plt.subplots()
im = ax.imshow(images[0], animated=True)
plt.axis("off") 

def update(i):
    im.set_array(images[i])
    return [im]

# Create the animation
animated = animation.FuncAnimation(
    fig, update, frames=len(images), interval=150, blit=True, repeat_delay=10
)

# Save the animation as a GIF
animated.save("./microstim/plot/animations/sigmoid.gif", writer="pillow", fps=30)
os.system('say "Potential GIF finished"')
plt.show()