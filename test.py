import matplotlib.pyplot as plt

fig = plt.figure(num=8,figsize = (4.5,3), facecolor = 'w', dpi = 150, edgecolor = 'w')
plt.figure(figsize=(10, 6))
plt.xlabel(r"distance [$\mu$m]")
plt.ylabel(r"distance to electrode [$\mu$m]")
plt.savefig("ink.svg", format="svg", bbox_inches="tight")