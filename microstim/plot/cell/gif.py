from PIL import Image
import matplotlib.pylab as plt
import matplotlib.animation as animation
import numpy as np
import glob
import os

from microstim.config import current_dir
from microstim.main import model
from microstim.utils import rect, sigmoid
from microstim.plot.cell.utils import setup

files_path = current_dir + "/plot/results/"

def main():
    global config, is_prod
    weights, boost, sigma = setup(config)
    
    v_e, v_i, rho_e, rho_i, nu_e, nu_i = model(config["intensity"], weights, sigma, sigmoid, boost)

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

    animated.save(f"results/new/v_i.gif", writer="pillow", fps=30)
        
    list(map(os.remove, glob.glob(os.path.join(files_path, "*.png"))))
    plt.show()