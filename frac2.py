import numpy as np
import matplotlib.pyplot as plt

# Canvas size and parameters
width, height = 1000, 1000
zoom = 1.5
max_iter = 500  # Increased iterations for more detail
c = complex(-0.30176, -0.8842)  # Fractal equation constant (tweak for variation)

# Complex plane setup
x = np.linspace(-zoom, zoom, width)
y = np.linspace(-zoom, zoom, height)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y  # Complex plane

# Divergence time array
div_time = np.zeros(Z.shape, dtype=int)

# Iterate fractal equation
for i in range(max_iter):
    Z = Z**2 + c  # Fractal function: Z = Z^2 + c
    diverged = np.abs(Z) > 4  # Divergence condition
    mask = (div_time == 0) & diverged
    div_time[mask] = i  # Record the iteration when divergence happens
    Z[diverged] = 0  # Reset points that have diverged to avoid overflow

# Apply log scaling for smoother gradients (no blur)
div_time = np.log(div_time + 1)  # Log scaling to smooth the divergence effect

# Plot the fractal with a galaxy-inspired colormap
plt.figure(figsize=(10, 10), dpi=300)
plt.imshow(div_time, cmap='inferno', extent=(-zoom, zoom, -zoom, zoom))
plt.axis('off')  # Turn off axis to enhance the visual experience

# Title and background settings
plt.title("Sharp Galactic Fractal Bloom", fontsize=20, color='white', pad=20)
plt.gca().set_facecolor('black')
plt.tight_layout()
plt.show()


