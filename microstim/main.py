import torch.nn.functional as F
import torch
import numpy as np
import time

from microstim.config import config, DEVICE
from microstim.utils import maxRadius, normal, plot_tn, zeros, make_kernel

import matplotlib.pylab as plt

usingFFT = False
gif = False

N = config["N"]
X = config["distance"]
P = config["P"]
R = config["R"]
rates = config["rates"]
Rm = config["Rm"]
DT = config["dt"]
DX = config["dx"]
TAU = config["TAU"]
ALPHA = config["ALPHA"]
THRESHOLD = config["THRESHOLD"]
DISTANCE_RANGE = torch.tensor(np.arange(0, X, DX), dtype=torch.float32, device=DEVICE)
L = DISTANCE_RANGE.shape[0]

def model(intensity, weights, sigma, rate, boost, radius_only=False):
    start = time.time()
    is_transient = 0
    rho_e, rho_i = zeros(N), zeros(N) # radii
    nu_e, nu_i = zeros((N, L)), zeros((N, L)) # firing rates
    v_e, v_i = zeros((N, L)), zeros((N, L)) # membrane potentials
    
    wee = make_kernel(sigma["ee"], weights["ee"]).to(dtype=torch.float32, device=DEVICE).contiguous()
    wie = make_kernel(sigma["ie"], weights["ie"]).to(dtype=torch.float32, device=DEVICE).contiguous()
    wei = make_kernel(sigma["ei"], weights["ei"]).to(dtype=torch.float32, device=DEVICE).contiguous()
    wii = make_kernel(sigma["ii"], weights["ii"]).to(dtype=torch.float32, device=DEVICE).contiguous()
    
    nu_e[0] = np.log(intensity) * boost["exc"] * normal(DISTANCE_RANGE, 120)
    nu_i[0] = np.log(intensity) * boost["inh"] * normal(DISTANCE_RANGE, 120)

    plt.plot(DISTANCE_RANGE.cpu().numpy(), nu_e[0].cpu().numpy(), label="exc")
    plt.plot(DISTANCE_RANGE.cpu().numpy(), nu_i[0].cpu().numpy(), label="inh")
    plt.legend()
    plt.show()

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

        plt.plot(DISTANCE_RANGE.cpu().numpy(), v_e[i+1].cpu().numpy(), label="exc")
        plt.plot(DISTANCE_RANGE.cpu().numpy(), v_i[i+1].cpu().numpy(), label="inh")
        plt.legend()
        plt.show()
        
        # Update rates
        nu_e[i+1] = rates["exc"] * rate(v_e[i+1])
        nu_i[i+1] = rates["inh"] * rate(v_i[i+1])
        
        # Compute maxRadius
        if radius_only:
            rho_e[i+1] = maxRadius(v_e[i+1], DISTANCE_RANGE, THRESHOLD)
            rho_i[i+1] = maxRadius(v_i[i+1], DISTANCE_RANGE, THRESHOLD)

            if rho_e[i+1] >  rho_i[i+1] and not is_transient:
                is_transient += 1

            if rho_e[i+1] <  rho_i[i+1] and is_transient == 1:
                is_transient += 1

            if rho_e[i+1] == 0 and rho_i[i] == 0:
                print("break pad")
                break
        
        if gif:
            plot_tn([v_e[i].cpu().numpy(), v_i[i].cpu().numpy()], i*DT, DISTANCE_RANGE.cpu().numpy())
        

    end = time.time()
    print(f"Total time: {end - start} seconds")

    # Convert results back to numpy arrays
    return (v_e.cpu().numpy(), v_i.cpu().numpy(), 
            rho_e.cpu().numpy(), rho_i.cpu().numpy(), 
            nu_e.cpu().numpy(), nu_i.cpu().numpy(), is_transient)