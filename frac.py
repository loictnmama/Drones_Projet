import numpy as np
import matplotlib.pyplot as plt

# Canvas size
width, height = 1000, 1000
zoom = 1.5
max_iter = 300

# Complex plane
x = np.linspace(-zoom, zoom, width)
y = np.linspace(-zoom, zoom, height)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y

# Fractal equation parameters
c = complex(-0.30176, -0.8842)  # tweak for variety
div_time = np.zeros(Z.shape, dtype=int)

# Iterate fractal function
for i in range(max_iter):
    Z = Z**2 + c
    diverged = np.abs(Z) > 4
    mask = (div_time == 0) & diverged
    div_time[mask] = i
    Z[diverged] = 0  # avoid overflow

# Plot
plt.figure(figsize=(10, 10))
plt.imshow(div_time, cmap='magma', extent=(-zoom, zoom, -zoom, zoom))
plt.axis('off')
plt.title("Fractal Field - Complex Bloom", fontsize=18, color='white', pad=20)
plt.gca().set_facecolor('black')
plt.tight_layout()
plt.show()
