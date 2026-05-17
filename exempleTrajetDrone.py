import numpy as np
import matplotlib.pyplot as plt

R = 1.0
N = 3
theta = np.linspace(0, 2*np.pi, N, endpoint=False)

x_clients = R * np.cos(theta)
y_clients = R * np.sin(theta)

x_depot, y_depot = 0, 0

plt.figure(figsize=(5, 4))
    
for i in range(N):
    plt.arrow(x_depot, y_depot, x_clients[i]-x_depot, y_clients[i]-y_depot,
              color='b', alpha=0.5, length_includes_head=True,
              head_width=0.05, head_length=0.1, label='Trajet drone' if i==0 else "")
    plt.arrow(x_clients[i], y_clients[i], x_depot-x_clients[i], y_depot-y_clients[i],
              color='b', alpha=0.5, length_includes_head=True,
              head_width=0.05, head_length=0.1)
    

plt.plot(x_depot, y_depot, 'go', markersize=10, label='Dépôt')
plt.plot(x_clients, y_clients, 'ro', markersize=8, label='Clients')

circle = plt.Circle((0, 0), R, fill=False, color='k', linestyle='dotted')
plt.gca().add_artist(circle)

plt.axis('equal')
plt.xlim(-R * 1.3, R * 1.3)
plt.ylim(-R * 1.3, R * 1.3)
plt.grid(True, alpha=0.3)
plt.legend()
plt.title(f"Figure 1 : Trajet d'un petit drone pour N={N} clients\nRayon = {R} km")
plt.xlabel('Distance (km)')
plt.ylabel('Distance (km)')

plt.show()