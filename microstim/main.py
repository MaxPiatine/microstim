import torch.nn.functional as F
import torch
import numpy as np
import time
import glob
import os
import matplotlib.animation as animation
from PIL import Image
from datetime import datetime
import json
import gc

from microstim.config import config, DEVICE, current_dir
from microstim.utils import maxRadius, normal, plot_tn, zeros, make_kernel, V_eph, x0s, classify_behavior
from microstim.logging import log_run

import matplotlib.pylab as plt

N = config["N"]
X = config["distance"]
P = config["P"]
R = config["R"]
rates = config["rates"]
d_axon = config["d_axon"]
Rm = config["Rm"]
DT = config["dt"]
DX = config["dx"]
TAU = config["TAU"]
ALPHA = config["ALPHA"]
THRESHOLD = config["THRESHOLD"]
DISTANCE_RANGE = torch.tensor(np.arange(0, X, DX), dtype=torch.float32, device=DEVICE)
L = DISTANCE_RANGE.shape[0]

def model(intensity, weights, sigma, rate, boost, radius_only=False, is_gif=False):
    start = time.time()
    nu_e, nu_i = zeros((N, L)), zeros((N, L)) # firing rates
    v_e, v_i = zeros((N, L)), zeros((N, L)) # membrane potentials
    
    wee = make_kernel(sigma["ee"], weights["ee"]).to(dtype=torch.float32, device=DEVICE).contiguous()
    wie = make_kernel(sigma["ie"], weights["ie"]).to(dtype=torch.float32, device=DEVICE).contiguous()
    wei = make_kernel(sigma["ei"], weights["ei"]).to(dtype=torch.float32, device=DEVICE).contiguous()
    wii = make_kernel(sigma["ii"], weights["ii"]).to(dtype=torch.float32, device=DEVICE).contiguous()

    v_e[0] = V_eph(DISTANCE_RANGE, R, intensity, ALPHA) * d_axon["exc"] * boost["exc"] 
    v_i[0] = V_eph(DISTANCE_RANGE, R, intensity, ALPHA) * d_axon["inh"] * boost["inh"]

    # v_e[0] *= normal(DISTANCE_RANGE, 113)
    # v_i[0] *= normal(DISTANCE_RANGE, 113)

    nu_e[0] = torch.exp(-DISTANCE_RANGE**2/(100+(1*intensity)**(2/(P+2))))
    nu_i[0] = torch.exp(-DISTANCE_RANGE**2/(100+(0.2*intensity)**(2/(P+2))))

    if radius_only:
        rho_e, rho_i = zeros(N), zeros(N) # radii
        rho_e[0] = maxRadius(v_e[0], DISTANCE_RANGE, THRESHOLD)
        rho_i[0] = maxRadius(v_i[0], DISTANCE_RANGE, THRESHOLD)

    for i in range(N-1):
        if i / 100 == 1.0:
            print(f" time: {(time.time() - start) * (N - 100)//100 }")

        nu_e_current = nu_e[i].unsqueeze(0).unsqueeze(0) 
        nu_i_current = nu_i[i].unsqueeze(0).unsqueeze(0)

        # Convolutions
        conv_wee = F.conv1d(nu_e_current, wee, padding='same').squeeze()
        conv_wie = F.conv1d(nu_i_current, wie, padding='same').squeeze()
        conv_wei = F.conv1d(nu_e_current, wei, padding='same').squeeze()
        conv_wii = F.conv1d(nu_i_current, wii, padding='same').squeeze()
        
        # Update voltages
        v_e[i+1] = v_e[i] + DT * (-v_e[i] + Rm*(conv_wee - conv_wie))/TAU
        v_i[i+1] = v_i[i] + DT * (-v_i[i] + Rm*(conv_wei - conv_wii))/TAU
    
        # Update rates
        nu_e[i+1] = rate(DISTANCE_RANGE, v_e[i+1], x0s(v_e[i+1]))
        nu_i[i+1] = rate(DISTANCE_RANGE, v_i[i+1], x0s(v_i[i+1]))
        
        # Compute maxRadius
        if radius_only:
            rho_e[i+1] = maxRadius(v_e[i+1], DISTANCE_RANGE, THRESHOLD)
            rho_i[i+1] = maxRadius(v_i[i+1], DISTANCE_RANGE, THRESHOLD)

            if rho_e[i+1] == 0 and rho_i[i] == 0:
                print("break pad")
                break

        if is_gif:
            plot_tn([v_e[i].cpu().numpy(), v_i[i].cpu().numpy()], i*DT, DISTANCE_RANGE.cpu().numpy())
            plt.close("all")

        try:
            del conv_wee, conv_wie, conv_wei, conv_wii, nu_e_current, nu_i_current
        except NameError:
            pass
            

    end = time.time()
    print(f"Total time: {end - start} seconds")

    if is_gif:
        files_path = current_dir + "/plot/results/"
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

        animated.save(f"results/new/{datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}.gif", writer="pillow", fps=30)
            
        list(map(os.remove, glob.glob(os.path.join(files_path, "*.png"))))

    v_e_np = v_e.cpu().numpy()
    v_i_np = v_i.cpu().numpy()
    nu_e_np = nu_e.cpu().numpy()
    nu_i_np = nu_i.cpu().numpy()
    rho_e_np = rho_e.cpu().numpy() if radius_only else None
    rho_i_np = rho_i.cpu().numpy() if radius_only else None

    # logging 
    stats = {
        "total_time": round(end - start, 2),
        "transient": classify_behavior(rho_i, rho_e) if radius_only else None,
        "intensity": int(intensity),
        "max_rho_e": float(torch.max(rho_e).cpu().numpy()) if radius_only else None,
        "max_rho_i": float(torch.max(rho_i).cpu().numpy()) if radius_only else None,
        "weights": json.dumps(weights),
        "sigmas": json.dumps(sigma),
        "boosts": json.dumps(boost),
    }
    log_run(config, stats=stats)


    try:
        del v_e, v_i, nu_e, nu_i, rho_e, rho_i
        del wee, wie, wei, wii
    except NameError:
        pass

    plt.close('all')

    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    elif hasattr(torch, "mps"):
        try:
            torch.mps.empty_cache()
        except Exception:
            pass
    
    return (v_e_np, v_i_np, rho_e_np, rho_i_np, nu_e_np, nu_i_np)