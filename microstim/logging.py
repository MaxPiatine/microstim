import os
import json
import csv
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def _timestamp():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def log_run(config, stats=None, filename_prefix="run"):
    csv_path = os.path.join(LOG_DIR, "runs.csv")
    header = ["timestamp", "total_time", "transient", "intensity", "weights", "sigmas", "boosts", "max_rho_e", "max_rho_i", "config_json"]

    row = {
        "timestamp": _timestamp(),
        "total_time": stats.get("total_time", ""),
        "transient": stats.get("transient", ""),
        "intensity": stats.get("intensity", ""),
        "weights": stats.get("weights", ""),
        "sigmas": stats.get("sigmas", ""),
        "boosts": stats.get("boosts", ""),
        "max_rho_e": stats.get("max_rho_e", ""),
        "max_rho_i": stats.get("max_rho_i", ""),
        "config_json": json.dumps(config)
    }

    write_header = not os.path.exists(csv_path)
    with open(csv_path, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        if write_header:
            writer.writeheader()
        writer.writerow(row)

    return csv_path