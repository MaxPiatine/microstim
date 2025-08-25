import numpy as np
import torch
import yaml
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

config = load_config()

DEVICE = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
DISTANCE_RANGE = torch.tensor(np.arange(0, config["distance"], config["dx"]), dtype=torch.float32, device=DEVICE)
TIME_RANGE = torch.tensor(np.arange(0, config["N"]), dtype=torch.float32, device=DEVICE)

AXON_LINSPACE = np.arange(config["RHEOBASE"], 20, float(config["STEP"]))

