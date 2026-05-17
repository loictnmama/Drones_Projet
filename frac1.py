import numpy as np
import matplotlib.pyplot as plt

width, height = 1000, 1000
zoom = 1.5
max_iter = 500
c = complex(-0.30176, -0.8842)
glow_factor = 0.2

x = np.linspace(-zoom, zoom, width)
y = np.linspace(-zoom, zoom, height)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y 

div_time = np.zeros(Z.shape, dtype=int)

for i in range(max_iter):
    Z = Z**2 + c
    diverged = np.abs(Z) > 4
    mask = (div_time == 0) & diverged
    div_time[mask] = i
    Z[diverged] = 0

div_time = np.log(div_time + 1)

plt.figure(figsize=(10, 10), dpi=300)
plt.imshow(div_time, cmap='inferno', extent=(-zoom, zoom, -zoom, zoom))
plt.axis('off')

noise = np.random.normal(0, glow_factor, (height, width))
glow = np.clip(div_time + noise, 0, np.max(div_time))

plt.imshow(glow, cmap='inferno', alpha=0.7, extent=(-zoom, zoom, -zoom, zoom))

plt.title("Galactic Fractal Bloom", fontsize=20, color='white', pad=20)
plt.gca().set_facecolor('black')
plt.tight_layout()
plt.show()
