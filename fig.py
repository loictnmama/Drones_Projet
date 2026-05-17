import numpy as np
import matplotlib.pyplot as plt

R = 1.0

fig, axes = plt.subplots(nrows=9, ncols=2, figsize=(8, 36), constrained_layout=True)

for idx, N in enumerate(range(2, 11)):
    theta = np.linspace(0, 2 * np.pi, N, endpoint=False)

    x_clients = R * np.cos(theta)
    y_clients = R * np.sin(theta)
    x_depot, y_depot = 0, 0

    # --- Trajet Drone ---
    ax_drone = axes[idx, 0]
    for i in range(N):
        ax_drone.arrow(x_depot, y_depot, x_clients[i] - x_depot, y_clients[i] - y_depot,
                       color='b', alpha=0.5, length_includes_head=True,
                       head_width=0.05, head_length=0.1)
        ax_drone.arrow(x_clients[i], y_clients[i], x_depot - x_clients[i], y_depot - y_clients[i],
                       color='b', alpha=0.5, length_includes_head=True,
                       head_width=0.05, head_length=0.1)

    ax_drone.plot(x_depot, y_depot, 'go', markersize=6)
    ax_drone.plot(x_clients, y_clients, 'ro', markersize=5)
    ax_drone.add_artist(plt.Circle((0, 0), R, fill=False, color='k', linestyle='dotted'))
    ax_drone.set_title(f"Drone - N={N}", fontsize=10)
    ax_drone.set_aspect('equal')
    ax_drone.set_xlim(-R * 1.3, R * 1.3)
    ax_drone.set_ylim(-R * 1.3, R * 1.3)
    ax_drone.axis('off')

    # --- Trajet Véhicule ---
    ax_veh = axes[idx, 1]
    ax_veh.arrow(x_depot, y_depot, (x_clients[0] - x_depot) * 0.7, (y_clients[0] - y_depot) * 0.7,
                 color='r', alpha=0.7, length_includes_head=True,
                 head_width=0.05, head_length=0.1)

    for i in range(N - 1):
        x_start, y_start = x_clients[i], y_clients[i]
        x_end, y_end = x_clients[(i + 1) % N], y_clients[(i + 1) % N]
        ax_veh.arrow(x_start, y_start, (x_end - x_start) * 0.7, (y_end - y_start) * 0.7,
                     color='r', alpha=0.7, length_includes_head=True,
                     head_width=0.05, head_length=0.1)

    ax_veh.arrow(x_clients[-1], y_clients[-1], (x_depot - x_clients[-1]) * 0.7, (y_depot - y_clients[-1]) * 0.7,
                 color='r', alpha=0.7, length_includes_head=True,
                 head_width=0.05, head_length=0.1)

    x_vehicule = np.array([x_depot] + list(x_clients) + [x_depot])
    y_vehicule = np.array([y_depot] + list(y_clients) + [y_depot])
    ax_veh.plot(x_vehicule, y_vehicule, 'r-', alpha=0.3)

    ax_veh.plot(x_depot, y_depot, 'go', markersize=6)
    ax_veh.plot(x_clients, y_clients, 'ro', markersize=5)
    ax_veh.add_artist(plt.Circle((0, 0), R, fill=False, color='k', linestyle='dotted'))
    ax_veh.set_title(f"Véhicule - N={N}", fontsize=10)
    ax_veh.set_aspect('equal')
    ax_veh.set_xlim(-R * 1.3, R * 1.3)
    ax_veh.set_ylim(-R * 1.3, R * 1.3)
    ax_veh.axis('off')

fig.suptitle("Comparaison des trajets Drone vs Véhicule pour N de 2 à 10", fontsize=14)
plt.show()