import matplotlib.pylab as plt
import seaborn as sns
import numpy as np
from scipy.integrate import simps
from scipy.integrate import quad

from microstim.utils import lognormal, lognormalIntensity, diameterCurrentThreshold
from microstim.globals import X_RANGE

mu_e, mu_i = 0.712, 0.465
sigma_e, sigma_i = 0.292, 0.114

sns.set_theme(style="ticks")
palette = sns.color_palette("mako_r", n_colors=3) 

ax = plt.subplot(111) 
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# samples1 = np.random.normal(loc=mu_e, scale=sigma_e, size=10000)
# samples2 = np.random.normal(loc=mu_i, scale=sigma_i, size=10000)
# bins1 = np.linspace(0, max(samples1), 30)
# bins2 = np.linspace(0, max(samples2), 30)
# plt.hist(samples1, bins=bins1, density=True, alpha=0.5, color=palette[0], label="exc")
# plt.hist(samples2, bins=bins2, density=True, alpha=0.4, color=palette[1], label="inh")
# plt.plot(np.linspace(0, max(samples), 30), 1/(sigma_e * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu_e)**2 / (2 * sigma_e**2) ), linewidth=2, color="k")


# samples1 = np.random.lognormal(mean=mu_e, sigma=sigma_e, size=10000)
# samples2 = np.random.lognormal(mean=mu_i, sigma=sigma_i, size=10000)
# bins1 = np.linspace(0, max(samples1), 30)
# bins2 = np.linspace(0, max(samples2), 30)
# plt.hist(samples1, bins=bins1, density=True, alpha=0.5, color=palette[0], label="exc")
# plt.hist(samples2, bins=bins2, density=True, alpha=0.4, color=palette[1], label="inh")
# plt.plot(np.linspace(0, max(samples), 30), 1/(sigma_e * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu_e)**2 / (2 * sigma_e**2) ), linewidth=2, color="k")

a = diameterCurrentThreshold(diameter=12)
print(a)
x_linspace = np.linspace(0, 5, len(X_RANGE))
lognrml_e = lognormalIntensity(x_linspace, mu=0.712, sigma=0.292)
lognrml_i = lognormalIntensity(x_linspace, mu=0.465, sigma=0.114)

integral_a = 0
for x in x_linspace:
    print(integral_a)
    integral_a += lognormalIntensity(x, mu=0.712, sigma=0.292)

print("Integral from 0 to a: ", integral_a)

plt.plot(x_linspace, lognrml_e, color=palette[0], label="exc")
plt.plot(x_linspace, lognrml_i, color=palette[1], label="inh")
plt.fill_between(x_linspace, lognrml_e, where=(x_linspace < a), color='grey', alpha=0.3)
plt.axvline(a, color='black', linestyle='--', label=r"$I_T$")
plt.xlabel("intensity threshold [μA]")
plt.ylabel("probability density")
plt.legend(loc="best")
plt.show()
