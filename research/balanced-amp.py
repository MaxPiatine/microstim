# Generate the sample correlation data for evoked map and control pattern
import numpy as np
import matplotlib.pyplot as plt

# Set random seed for reproducibility
np.random.seed(42)

# Simulating a wider distribution for the evoked map
evoked_map_correlations = np.random.normal(0, 0.5, 1000)  # mean=0, wider std dev
# Simulating a narrower distribution for the control pattern
control_pattern_correlations = np.random.normal(0, 0.2, 1000)  # mean=0, narrower std dev

# Create the histogram to show the distributions
plt.figure(figsize=(12, 6))

# Plot histograms of the two distributions
plt.hist(evoked_map_correlations, bins=30, alpha=0.7, label='Evoked Map Correlation', color='blue', density=True)
plt.hist(control_pattern_correlations, bins=30, alpha=0.7, label='Control Pattern Correlation', color='red', density=True)

# Add labels and title
plt.title('Distribution of Correlation Coefficients: Evoked Map vs Control Pattern', fontsize=16)
plt.xlabel('Correlation Coefficient', fontsize=14)
plt.ylabel('Density', fontsize=14)
plt.axvline(x=0, color='black', linestyle='--', label='Average Correlation = 0')  # Line for average correlation
plt.legend(loc='upper left')

# Show the plot
plt.show()
