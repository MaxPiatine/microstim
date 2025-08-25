import argparse
import importlib
import yaml
import sys
import seaborn as sns

# Load config.yaml
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Run microstim cell/axon functions")
parser.add_argument("function", help="Function to run (e.g. heatmap, radii, maxpotDistance)")
parser.add_argument("--is_depol", action="store_true", help="Use depolarization model")
parser.add_argument("--is_prod", action="store_true", help="Production mode")
parser.add_argument("--position", type=int, default=250, help="Position index (default: 250 microns)")
args = parser.parse_args()

# Map function names to module paths
functions = {
    "heatmap": "microstim.plot.cell.heatmap",
    "radii": "microstim.plot.cell.radii",
    "boostHeatmap": "microstim.plot.cell.boostHeatmap",
    "gif": "microstim.plot.cell.gif",
    "heatmapRadiusPot": "microstim.plot.cell.heatmapRadiusPot",
    "intensityPotential": "microstim.plot.cell.intensityPotential",
    "intensityRadius": "microstim.plot.cell.intensityRadius",
    "maxpotPosition": "microstim.plot.cell.maxpotPosition",
    "maxpotDistance": "microstim.plot.cell.maxpotDistance",
    "weightsHeatmap": "microstim.plot.cell.weightsHeatmap",

    "ratios": "microstim.plot.axon.ratios",
    "distributions": "microstim.plot.axon.distributions",
    "EI": "microstim.plot.axon.EI",
    "intensity": "microstim.plot.axon.intensity",
    "map": "microstim.plot.axon.map",
    "mapintensity": "microstim.plot.axon.mapintensity",
    "intensitygif": "microstim.plot.axon.intensitygif",
    "mapgif": "microstim.plot.axon.mapgif",
}

if args.function not in functions:
    print(f"Function '{args.function}' not recognized.")
    sys.exit(1)

module_path = functions[args.function]
module = importlib.import_module(module_path)

palette = sns.color_palette("mako_r", n_colors=3) 

# config and flags as globals in the module
setattr(module, "config", config)
setattr(module, "is_depol", args.is_depol)
setattr(module, "is_prod", args.is_prod)
setattr(module, "position", args.position)
setattr(module, "palette", palette)

if hasattr(module, "main"):
    module.main()
else:
    print(f"Module '{module_path}' does not have a main() function.")