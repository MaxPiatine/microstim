import matplotlib.pylab as plt
import matplotlib.animation as animation
import numpy as np
import argparse

from microstim.globals import intensity, act_sigma, act_weights, depol_sigma, depol_weights, gamma, start_boost, current_dir
from microstim.main import model
from microstim.utils import rect

from PIL import Image
import glob
import os

files_path = current_dir + "/plot/results/"

parser = argparse.ArgumentParser(description="potential for distance gif")
parser.add_argument("--is_depol", action="store_true", help="Run model with depolarization")

args = parser.parse_args()

is_depolarized = args.is_depol
typeModel = ""

if is_depolarized:
    boost = start_boost.copy()
    weights = depol_weights.copy()
    sigma = depol_sigma.copy()
    typeModel += "Stoney"
else:
    boost = gamma.copy()
    weights = act_weights.copy()
    sigma = act_sigma.copy()
    typeModel += "Histed"
    

v_e, v_i, rho_e, rho_i, nu_e, nu_i = model(intensity, weights, sigma, rect, boost, is_depolarized=is_depolarized)


files = sorted(glob.glob("./microstim/plot/results/*.png"), key=os.path.getmtime)
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

animated.save(f"results/{typeModel}/newgif.gif", writer="pillow", fps=30)
    
list(map(os.remove, glob.glob(os.path.join(files_path, "*.png"))))
plt.show()