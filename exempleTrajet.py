import numpy as np
import matplotlib.pyplot as plt

# Paramètres
R = 1.0  # Rayon du cercle (en km)
N = 3    # Nombre de clients
theta = np.linspace(0, 2*np.pi, N, endpoint=False)  # Angles des clients

# Coordonnées des clients (sur la circonférence)
x_clients = R * np.cos(theta)
y_clients = R * np.sin(theta)

# Coordonnées du dépôt (centre)
x_depot, y_depot = 0, 0

# Création de la figure
plt.figure(figsize=(10, 8))

# # 1. Trajet du drone (aller-retour pour chaque client)
# for i in range(N):
#     plt.plot([x_depot, x_clients[i]], [y_depot, y_clients[i]], 
#              'b--', alpha=0.5, label='Trajet drone' if i==0 else "")
    
for i in range(N):
    # Aller (dépôt -> client)
    plt.arrow(x_depot, y_depot, x_clients[i]-x_depot, y_clients[i]-y_depot,
              color='b', alpha=0.5, length_includes_head=True,
              head_width=0.05, head_length=0.1, label='Trajet drone' if i==0 else "")
    # Retour (client -> dépôt)
    plt.arrow(x_clients[i], y_clients[i], x_depot-x_clients[i], y_depot-y_clients[i],
              color='b', alpha=0.5, length_includes_head=True,
              head_width=0.05, head_length=0.1)
    
# # 2. Trajet du véhicule (tour complet)
x_vehicule = np.append(x_clients, x_clients[0])
y_vehicule = np.append(y_clients, y_clients[0])
plt.plot(x_vehicule, y_vehicule, 'r-', label='Trajet véhicule')

# Points
plt.plot(x_depot, y_depot, 'go', markersize=10, label='Dépôt')
plt.plot(x_clients, y_clients, 'ro', markersize=8, label='Clients')

# Cercle de référence
circle = plt.Circle((0, 0), R, fill=False, color='k', linestyle='dotted')
plt.gca().add_artist(circle)

# Personnalisation
plt.axis('equal')
plt.xlim(-R * 1.3, R * 1.3)  # Limites x avec une marge de 30%
plt.ylim(-R * 1.3, R * 1.3)  # Limites y avec une marge de 30%
plt.grid(True, alpha=0.3)
plt.legend()
plt.title(f'Comparaison des trajets pour N={N} clients\nRayon = {R} km')
plt.xlabel('Distance (km)')
plt.ylabel('Distance (km)')

# # Calcul des distances totales
# distance_drone = 2 * R * N  # Aller-retour pour chaque client
# distance_vehicule = 2 * np.pi * R  # Circonférence approximative

# # Ajout des informations d'énergie (simplifiées)
# plt.text(0.05, 0.95, f'Distance drone: {distance_drone:.2f} km\n'
#                     f'Distance véhicule: {distance_vehicule:.2f} km',
#          transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.8))

plt.show()

# # Calcul de l'énergie (exemple simplifié)
# energie_par_km_drone = 0.5  # kWh/km (hypothétique)
# energie_par_km_vehicule = 1.0  # kWh/km (hypothétique)

# energie_drone = distance_drone * energie_par_km_drone
# energie_vehicule = distance_vehicule * energie_par_km_vehicule

# print(f"Énergie estimée drone: {energie_drone:.2f} kWh")
# print(f"Énergie estimée véhicule: {energie_vehicule:.2f} kWh")