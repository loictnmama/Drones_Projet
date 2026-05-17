import numpy as np
import matplotlib.pyplot as plt

R = 1.0
N = 3
theta = np.linspace(0, 2*np.pi, N, endpoint=False)

x_clients = R * np.cos(theta)
y_clients = R * np.sin(theta)

x_depot, y_depot = 0, 0

plt.figure(figsize=(5, 4))

plt.arrow(x_depot, y_depot, (x_clients[0] - x_depot) * 0.7, (y_clients[0] - y_depot) * 0.7,
          color='r', alpha=0.7, length_includes_head=True,
          head_width=0.05, head_length=0.1, label='Trajet véhicule')

for i in range((N-1)):
    x_start = x_clients[i]
    y_start = y_clients[i]
    x_end = x_clients[(i + 1) % N]
    y_end = y_clients[(i + 1) % N]
    plt.arrow(x_start, y_start, (x_end - x_start) * 0.7, (y_end - y_start) * 0.7,
              color='r', alpha=0.7, length_includes_head=True,
              head_width=0.05, head_length=0.1)

plt.arrow(x_clients[N-1], y_clients[N-1], (x_depot - x_clients[N-1]) * 0.7, (y_depot - y_clients[N-1]) * 0.7,
          color='r', alpha=0.7, length_includes_head=True,
          head_width=0.05, head_length=0.1)

x_vehicule = np.array([x_depot] + list(x_clients) + [x_depot])
y_vehicule = np.array([y_depot] + list(y_clients) + [y_depot])
plt.plot(x_vehicule, y_vehicule, 'r-', alpha=0.3)
    
    
plt.plot(x_depot, y_depot, 'go', markersize=10, label='Dépôt')
plt.plot(x_clients, y_clients, 'ro', markersize=8, label='Clients')

circle = plt.Circle((0, 0), R, fill=False, color='k', linestyle='dotted')
plt.gca().add_artist(circle)

plt.axis('equal')
plt.xlim(-R * 1.3, R * 1.3)
plt.ylim(-R * 1.3, R * 1.3)
plt.grid(True, alpha=0.3)
plt.legend()
plt.title(f"Figure 2 : Trajet d'un véhicule pour N={N} clients\nRayon = {R} km")
plt.xlabel('Distance (km)')
plt.ylabel('Distance (km)')

plt.show()