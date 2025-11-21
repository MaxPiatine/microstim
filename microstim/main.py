import torch.nn.functional as F
import torch
import numpy as np
import time

from microstim.config import config, DEVICE
from microstim.utils import maxRadius, normal, plot_tn, zeros

import matplotlib.pylab as plt

usingFFT = False
gif = False

N = config["N"]
X = config["distance"]
P = config["P"]
R = config["R"]
Rm = config["Rm"]
DT = config["dt"]
DX = config["dx"]
TAU = config["TAU"]
ALPHA = config["ALPHA"]
THRESHOLD = config["THRESHOLD"]
DISTANCE_RANGE = torch.tensor(np.arange(0, X, DX), dtype=torch.float32, device=DEVICE)
L = DISTANCE_RANGE.shape[0]

def model(intensity, weights, sigma, rate, boost, is_depolarized=True, radius_only=False):
    start = time.time()
    is_transient = 0
    rho_e, rho_i = zeros(N), zeros(N) # radii
    nu_e, nu_i = zeros((N, L)), zeros((N, L)) # firing rates
    v_e, v_i = zeros((N, L)), zeros((N, L)) # membrane potentials
    
    # Pre-compute synaptic weights and kernels
    # ee_linspace = np.linspace(-4*sigma["ee"], 4*sigma["ee"], L) 
    # ie_linspace = np.linspace(-4*sigma["ie"], 4*sigma["ie"], L) 
    # ei_linspace = np.linspace(-4*sigma["ei"], 4*sigma["ei"], L) 
    # ii_linspace = np.linspace(-4*sigma["ii"], 4*sigma["ii"], L)

    # ee_linspace_tensor = torch.tensor(ee_linspace, dtype=torch.float32, device=DEVICE)
    # ie_linspace_tensor = torch.tensor(ie_linspace, dtype=torch.float32, device=DEVICE)
    # ei_linspace_tensor = torch.tensor(ei_linspace, dtype=torch.float32, device=DEVICE)
    # ii_linspace_tensor = torch.tensor(ii_linspace, dtype=torch.float32, device=DEVICE)

    # wee = weights["ee"] * normal(ee_linspace_tensor, sigma["ee"])
    # wie = weights["ie"] * normal(ie_linspace_tensor, sigma["ie"])
    # wei = weights["ei"] * normal(ei_linspace_tensor, sigma["ei"])
    # wii = weights["ii"] * normal(ii_linspace_tensor, sigma["ii"])
    # Choose kernel support multiplier (4 or 5 recommended; increase for higher accuracy)
    K_FACTOR = 4.0

    def make_kernel(sigma_val, weight_val):
        # radius in samples (at spatial resolution DX)
        radius_samples = max(1, int(np.ceil((K_FACTOR * sigma_val) / DX)))
        # create coordinates in micrometers sampled at DX
        x = torch.linspace(-radius_samples * DX, radius_samples * DX,
                           2 * radius_samples + 1, dtype=torch.float32, device=DEVICE)
        k = normal(x, sigma_val)  # expected to return torch tensor
        k = k / k.sum()           # normalize kernel area to 1
        k = k * weight_val        # scale by synaptic weight
        # ensure odd kernel length so 'same' padding is symmetric
        return k.unsqueeze(0).unsqueeze(0)  # shape (1,1,klen)

    wee = make_kernel(sigma["ee"], weights["ee"])
    wie = make_kernel(sigma["ie"], weights["ie"])
    wei = make_kernel(sigma["ei"], weights["ei"])
    wii = make_kernel(sigma["ii"], weights["ii"])
    
    if usingFFT:
        # Pre-compute FFTs of kernels
        wee_fft = torch.fft.fft(wee)
        wie_fft = torch.fft.fft(wie)
        wei_fft = torch.fft.fft(wei)
        wii_fft = torch.fft.fft(wii)
    else:
        # make_kernel already returns shape (out_channels=1, in_channels=1, kernel_len)
        # ensure kernels are float32, on device and contiguous
        wee = wee.to(dtype=torch.float32, device=DEVICE).contiguous()
        wie = wie.to(dtype=torch.float32, device=DEVICE).contiguous()
        wei = wei.to(dtype=torch.float32, device=DEVICE).contiguous()
        wii = wii.to(dtype=torch.float32, device=DEVICE).contiguous()
    
    # Initialize first step
    if is_depolarized:
        """
        depolarized model
        """
        v_e[0] = R*intensity/(DISTANCE_RANGE + ALPHA)**P * boost["exc"]
        v_i[0] = R*intensity/(DISTANCE_RANGE + ALPHA)**P * boost["inh"]
        
        nu_e[0] = rate(v_e[0])
        nu_i[0] = rate(v_i[0])
        
        if radius_only:
            rho_e[0] = maxRadius(v_e[0], DISTANCE_RANGE, THRESHOLD)
            rho_i[0] = maxRadius(v_i[0], DISTANCE_RANGE, THRESHOLD)

    for i in range(0, N-1):
        if i % 100 == 0:
            print("i: ", i, ", time: ", time.time() - start)

        if not is_depolarized and i*DT < 2:
            continue
        elif not is_depolarized and i*DT==2:
            print(i, "2ms")
            nu_e[i] = np.log(intensity) * boost["exc"] * normal(DISTANCE_RANGE, 120)
            nu_i[i] = np.log(intensity) * boost["inh"] * normal(DISTANCE_RANGE, 120)

        if usingFFT:
            nu_e_fft = torch.fft.fft(nu_e[i])
            nu_i_fft = torch.fft.fft(nu_i[i])
            
            # Time convolution operations
            conv_wee = torch.fft.ifft(nu_e_fft * wee_fft).real
            conv_wie = torch.fft.ifft(nu_i_fft * wie_fft).real
            conv_wei = torch.fft.ifft(nu_e_fft * wei_fft).real
            conv_wii = torch.fft.ifft(nu_i_fft * wii_fft).real
        else:

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
        nu_e[i+1] = rate(v_e[i+1])
        nu_i[i+1] = rate(v_i[i+1])
        
        # Compute maxRadius
        if radius_only:
            rho_e[i+1] = maxRadius(v_e[i+1], DISTANCE_RANGE, THRESHOLD)
            rho_i[i+1] = maxRadius(v_i[i+1], DISTANCE_RANGE, THRESHOLD)

            if rho_e[i+1] >  rho_i[i+1] and not is_transient:
                is_transient += 1

            if rho_e[i+1] <  rho_i[i+1] and is_transient == 1:
                is_transient += 1
        
        if gif:
            plot_tn([v_e[i].cpu().numpy(), v_i[i].cpu().numpy()], i*DT, DISTANCE_RANGE.cpu().numpy())
        

    end = time.time()
    print(f"Total time: {end - start} seconds")

    # Convert results back to numpy arrays
    return (v_e.cpu().numpy(), v_i.cpu().numpy(), 
            rho_e.cpu().numpy(), rho_i.cpu().numpy(), 
            nu_e.cpu().numpy(), nu_i.cpu().numpy(), is_transient)