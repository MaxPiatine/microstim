import torch.nn.functional as F
import torch
import numpy as np
import time

from microstim.config import config, DISTANCE_RANGE, TIME_RANGE, DEVICE
from microstim.utils import maxRadius, normal, plot_tn, zeros

usingFFT = False
gif = False
N = TIME_RANGE.shape[0]
X = DISTANCE_RANGE.shape[0]
P = config["P"]
R = config["R"]
Rm = config["Rm"]
DT = config["dt"]
TAU = config["TAU"]
ALPHA = config["ALPHA"]
THRESHOLD = config["THRESHOLD"]

def model(intensity, weights, sigma, rate, boost, is_depolarized=True, radius_only=False):
    start = time.time()

    rho_e, rho_i = zeros(N), zeros(N) # radii
    nu_e, nu_i = zeros((N, X)), zeros((N, X)) # firing rates
    v_e, v_i = zeros((N, X)), zeros((N, X)) # membrane potentials
    
    # Pre-compute synaptic weights and kernels
    ee_linspace = np.linspace(-4*sigma["ee"], 4*sigma["ee"], X) 
    ie_linspace = np.linspace(-4*sigma["ie"], 4*sigma["ie"], X) 
    ei_linspace = np.linspace(-4*sigma["ei"], 4*sigma["ei"], X) 
    ii_linspace = np.linspace(-4*sigma["ii"], 4*sigma["ii"], X)

    ee_linspace_tensor = torch.tensor(ee_linspace, dtype=torch.float32, device=DEVICE)
    ie_linspace_tensor = torch.tensor(ie_linspace, dtype=torch.float32, device=DEVICE)
    ei_linspace_tensor = torch.tensor(ei_linspace, dtype=torch.float32, device=DEVICE)
    ii_linspace_tensor = torch.tensor(ii_linspace, dtype=torch.float32, device=DEVICE)

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
            nu_e[i] = np.log(intensity) * boost["exc"] * normal(DISTANCE_RANGE, sigma["ee"])
            nu_i[i] = np.log(intensity) * boost["inh"] * normal(DISTANCE_RANGE, sigma["ii"])

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
        v_e[i+1] = v_e[i] + DT/TAU * (v_e[i] + Rm*(conv_wee - conv_wie))
        v_i[i+1] = v_i[i] + DT/TAU * (v_i[i] + Rm*(conv_wei - conv_wii))
        
        # Update rates
        nu_e[i+1] = rate(v_e[i+1])
        nu_i[i+1] = rate(v_i[i+1])
        
        # Compute maxRadius
        if radius_only:
            # 0.26 seconds 
            rho_e[i+1] = maxRadius(v_e[i+1], DISTANCE_RANGE, THRESHOLD)
            rho_i[i+1] = maxRadius(v_i[i+1], DISTANCE_RANGE, THRESHOLD)
        
        if gif:
            plot_tn([v_e[i].cpu().numpy(), v_i[i].cpu().numpy()], i*DT, DISTANCE_RANGE.cpu().numpy())
        

    end = time.time()
    print(f"Total time: {end - start} seconds")

    # Convert results back to numpy arrays
    return (v_e.cpu().numpy(), v_i.cpu().numpy(), 
            rho_e.cpu().numpy(), rho_i.cpu().numpy(), 
            nu_e.cpu().numpy(), nu_i.cpu().numpy())