import torch
import torch.nn.functional as F
import numpy as np
import time

from microstim.globals import N, i_RANGE, X_RANGE, ALPHA, R, P, DT, TAU, SYN, THRESHOLD
from microstim.utils import maxRadius, normal, plot_tn, k_e, k_i, spectral_convolution, KernelConvolution

import matplotlib.pylab as plt

usingFFT = False
gif = False

def model(intensity, weights, sigma, rate, boost, is_depolarized=True, radius_only=False):
    start = time.time()

    # Set device to MPS (Metal Performance Shaders) for Apple Silicon
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    
    # Convert arrays to PyTorch tensors
    X_RANGE_tensor = torch.tensor(X_RANGE, dtype=torch.float32, device=device)
    
    # Pre-allocate tensors on GPU
    rho_e = torch.zeros(N, dtype=torch.float32, device=device)
    rho_i = torch.zeros(N, dtype=torch.float32, device=device)
    nu_e = torch.zeros((len(i_RANGE), len(X_RANGE_tensor)), dtype=torch.float32, device=device)
    nu_i = torch.zeros((len(i_RANGE), len(X_RANGE_tensor)), dtype=torch.float32, device=device)
    v_e = torch.zeros((len(i_RANGE), len(X_RANGE_tensor)), dtype=torch.float32, device=device)
    v_i = torch.zeros((len(i_RANGE), len(X_RANGE_tensor)), dtype=torch.float32, device=device)
    
    # Pre-compute synaptic weights and kernels
    ee_linspace = np.linspace(-4*sigma["ee"], 4*sigma["ee"], len(X_RANGE)) 
    ie_linspace = np.linspace(-4*sigma["ee"], 4*sigma["ee"], len(X_RANGE)) 
    ei_linspace = np.linspace(-4*sigma["ee"], 4*sigma["ee"], len(X_RANGE)) 
    ii_linspace = np.linspace(-4*sigma["ii"], 4*sigma["ii"], len(X_RANGE))

    ee_linspace_tensor = torch.tensor(ee_linspace, dtype=torch.float32, device=device)
    ie_linspace_tensor = torch.tensor(ie_linspace, dtype=torch.float32, device=device)
    ei_linspace_tensor = torch.tensor(ei_linspace, dtype=torch.float32, device=device)
    ii_linspace_tensor = torch.tensor(ii_linspace, dtype=torch.float32, device=device)

    wee = weights["ee"] * normal(ee_linspace_tensor, sigma["ee"])
    wie = weights["ie"] * normal(ie_linspace_tensor, sigma["ie"])
    wei = weights["ei"] * normal(ei_linspace_tensor, sigma["ei"])
    wii = weights["ii"] * normal(ii_linspace_tensor, sigma["ii"])
    
    if usingFFT:
        # Pre-compute FFTs of kernels
        wee_fft = torch.fft.fft(wee)
        wie_fft = torch.fft.fft(wie)
        wei_fft = torch.fft.fft(wei)
        wii_fft = torch.fft.fft(wii)
    else:
        # Reshape the weights for convolution
        wee = wee.unsqueeze(0).unsqueeze(0)  # Shape: (1, 1, len(X_RANGE))
        wie = wie.unsqueeze(0).unsqueeze(0)
        wei = wei.unsqueeze(0).unsqueeze(0)
        wii = wii.unsqueeze(0).unsqueeze(0)
    
    # Initialize first step
    if is_depolarized:
        """
        depolarized model
        """
        v_e[0] = R*intensity/(X_RANGE_tensor + ALPHA)**P * boost["exc"]
        v_i[0] = R*intensity/(X_RANGE_tensor + ALPHA)**P * boost["inh"]
        
        nu_e[0] = rate(v_e[0])
        nu_i[0] = rate(v_i[0])
        
        if radius_only:
            rho_e[0] = maxRadius(v_e[0], X_RANGE_tensor, THRESHOLD)
            rho_i[0] = maxRadius(v_i[0], X_RANGE_tensor, THRESHOLD)
    else:
        """
        activation model
        """
        nu_e[0] = torch.log(intensity) * boost["exc"] * normal(X_RANGE_tensor, sigma["ee"])
        nu_i[0] = torch.log(intensity) * boost["inh"] * normal(X_RANGE_tensor, sigma["ii"])

    for i in range(0, len(i_RANGE)-1):
        if i % 100 == 0:
            print("i: ", i, ", time: ", time.time() - start)

        if usingFFT:
            nu_e_fft = torch.fft.fft(nu_e[i])
            nu_i_fft = torch.fft.fft(nu_i[i])
            
            # Time convolution operations
            conv_wee = torch.fft.ifft(nu_e_fft * wee_fft).real
            conv_wie = torch.fft.ifft(nu_i_fft * wie_fft).real
            conv_wei = torch.fft.ifft(nu_e_fft * wei_fft).real
            conv_wii = torch.fft.ifft(nu_i_fft * wii_fft).real
        else:

            nu_e_current = nu_e[i].unsqueeze(0).unsqueeze(0)  # Shape: (1, 1, len(X_RANGE))
            nu_i_current = nu_i[i].unsqueeze(0).unsqueeze(0)

            # Convolutions
            conv_wee = F.conv1d(nu_e_current, wee, padding='same').squeeze()
            conv_wie = F.conv1d(nu_i_current, wie, padding='same').squeeze()
            conv_wei = F.conv1d(nu_e_current, wei, padding='same').squeeze()
            conv_wii = F.conv1d(nu_i_current, wii, padding='same').squeeze()
        
        # Update voltages
        v_e[i+1] = v_e[i] + DT * (-1/TAU * v_e[i] + (conv_wee - conv_wie)/SYN)
        v_i[i+1] = v_i[i] + DT * (-1/TAU * v_i[i] + (conv_wei - conv_wii)/SYN)
        
        # Update rates
        nu_e[i+1] = rate(v_e[i+1])
        nu_i[i+1] = rate(v_i[i+1])
        
        # Compute maxRadius
        if radius_only:
            # 0.26 seconds
            # radius_start = time.time()
            rho_e[i+1] = maxRadius(v_e[i+1], X_RANGE_tensor, THRESHOLD)
            rho_i[i+1] = maxRadius(v_i[i+1], X_RANGE_tensor, THRESHOLD)
            # print(f"MaxRadius time: {time.time() - radius_start} seconds")
        
        if gif:
            plot_tn([v_e[i].cpu().numpy(), v_i[i].cpu().numpy()], i)
        

    end = time.time()
    print(f"Total time: {end - start} seconds")

    # Convert results back to numpy arrays
    return (v_e.cpu().numpy(), v_i.cpu().numpy(), 
            rho_e.cpu().numpy(), rho_i.cpu().numpy(), 
            nu_e.cpu().numpy(), nu_i.cpu().numpy())