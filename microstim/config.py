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
