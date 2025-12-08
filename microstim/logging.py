import os
import json
import csv
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def _timestamp():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def log_run(config, stats=None, filename_prefix="run"):
    """
    Save full run JSON and append a CSV summary line.

    - config: dict (your config.yaml loaded to microstim.config.config)
    - is_transient: int (0 stable, 1 unstable, 2 transient) or bool-like
    - stats: optional dict with numeric summaries (total_time, max_rho_e, ...)
    """
    stats = stats or {}
    ts = _timestamp()
    json_name = f"{filename_prefix}_{ts}.json"
    json_path = os.path.join(LOG_DIR, json_name)

    payload = {
        "timestamp": ts,
        "config": config,
        "stats": stats
    }

    # write full json
    with open(json_path, "w") as f:
        json.dump(payload, f, indent=2, default=str)

    # append summary CSV
    csv_path = os.path.join(LOG_DIR, "runs.csv")
    header = ["timestamp", "total_time", "transient", "weights", "sigmas", "boosts", "max_rho_e", "max_rho_i", "config_json"]

    row = {
        "timestamp": ts,
        "total_time": stats.get("total_time", ""),
        "transient": stats.get("transient", ""),
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

    return json_path, csv_path