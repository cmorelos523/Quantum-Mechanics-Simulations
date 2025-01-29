import numpy as np
import matplotlib.pyplot as plt

L = 0.000000005
n = 2
x = np.linspace(0, L, 1000)  # Position values in the box

# Wavefunction ψ(x)
def wavefunction(x, n, L):
    return np.sqrt(2 / L) * np.sin(n * np.pi * x / L)

# Probability Density |ψ(x)|^2
def probability_density(x, n, L):
    return wavefunction(x, n, L) ** 2

# Calculate wavefunction and probability density
psi = wavefunction(x, n, L)
prob_density = probability_density(x, n, L)

# Plotting
plt.figure(figsize=(10, 6))

# Plot wavefunction
plt.plot(x, psi, label=r'Wavefunction $\psi(x)$', color='blue')

# Plot probability density
plt.plot(x, prob_density, label=r'Probability Density $|\psi(x)|^2$', color='red')

# Labels and legend
plt.title(f"Particle in a Box: n={n}, L={L}", fontsize=14)
plt.xlabel("Position (x)", fontsize=12)
plt.ylabel("Amplitude / Probability", fontsize=12)
plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
plt.legend(fontsize=12)
plt.grid()

# Show the plot
plt.show()
