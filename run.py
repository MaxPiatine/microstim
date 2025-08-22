import argparse
import importlib
import yaml
import sys

# Load config.yaml
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Run microstim cell/axon functions")
parser.add_argument("function", help="Function to run (e.g. heatmap, radii, maxpotDistance)")
parser.add_argument("--is_depol", action="store_true", help="Use depolarization model")
parser.add_argument("--is_prod", action="store_true", help="Production mode")
args = parser.parse_args()

# Map function names to module paths
functions = {
    "heatmap": "microstim.plot.functions.cell.heatmap",
    "radii": "microstim.plot.functions.cell.radii",
    "maxpotDistance": "microstim.plot.functions.cell.maxpotDistance",
}

if args.function not in functions:
    print(f"Function '{args.function}' not recognized.")
    sys.exit(1)

module_path = functions[args.function]
module = importlib.import_module(module_path)

# config and flags as globals in the module
setattr(module, "config", config)
setattr(module, "is_depol", args.is_depol)
setattr(module, "is_prod", args.is_prod)

if hasattr(module, "main"):
    module.main()
else:
    print(f"Module '{module_path}' does not have a main() function.")