import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Paramètres constants
R = 1  # Rayon en km
P_drone = 0.08  # Consommation énergétique drone en MJ/km
P_vehicles = {
    'Camion Diesel Medium': 11.00,
    'Petite Van Diesel': 4.90,
    'Camion Électrique Medium': 3.80,
    'Petite Van Électrique': 1.65
}

# Fonctions pour calculer les distances et énergies
def D_drone(N, R):
    return 2 * N * R

def D_vehicule(N, R):
    return 2 * R * ((N-1) * np.sin(np.pi/N) + 1)

def E_drone(N, R, P_drone):
    return P_drone * D_drone(N, R)

def E_vehicule(N, R, P_vehicule):
    return P_vehicule * D_vehicule(N, R)

# Valeurs de N (de 2 à 650, pas 0 car sin(π/1) est indéfini, mais axe à 0-650)
N_values = np.arange(2, 651)

# Calcul des énergies
E_drone_values = [E_drone(N, R, P_drone) for N in N_values]
E_vehicle_values = {name: [E_vehicule(N, R, P) for N in N_values] for name, P in P_vehicles.items()}

# Trouver les points d'intersection (où E_drone ≈ E_vehicule)
intersections = {}
for name, P in P_vehicles.items():
    E_vals = E_vehicle_values[name]
    for N, Ed, Ev in zip(N_values, E_drone_values, E_vals):
        if abs(Ed - Ev) < 0.1:  # Tolérance pour intersection
            intersections[name] = (N, Ed)
            break

# Création du graphique
plt.figure(figsize=(8.4, 4.8))
plt.plot(N_values, E_drone_values, 'b-', label=f'Drone (P={P_drone} MJ/km)')
colors = {
    'Camion Diesel Medium': 'r',
    'Petite Van Diesel': 'g',
    'Camion Électrique Medium': 'm',
    'Petite Van Électrique': 'c'
}
for name, E_vals in E_vehicle_values.items():
    plt.plot(N_values, E_vals, f'{colors[name]}-', label=f'{name} (P={P_vehicles[name]} MJ/km)')
    if name in intersections:
        N_int, E_int = intersections[name]
        plt.plot(N_int, E_int, 'ko', markersize=6)  # Smaller markers
        # Adjust annotation positions
        offset = 15 if name == 'Camion Diesel Medium' else 10  # Extra space for Camion Diesel Medium
        ha = 'center' if name != 'Petit Van Électrique' else 'right'  # Avoid edge overlap
        plt.annotate(f'N={N_int}', (N_int, E_int), textcoords="offset points", xytext=(0, offset), ha=ha, fontsize=9)

plt.grid(True)
plt.xlabel('Nombre de clients (N)')
plt.ylabel('Énergie consommée (MJ)')
plt.title('Figure 3 : Comparaison de l\'énergie consommée : Drone vs Véhicules\n(R = 1 km, N de 2 à 650)')
plt.legend()
plt.ylim(0, 100)  # Y-axis from 0 to 100 MJ as requested
plt.xlim(0, 650)  # X-axis from 0 to 650 as requested
plt.xticks(np.arange(0, 651, 100))
plt.show()

# # Création du DataFrame pour toutes les données
# data = {
#     'N': N_values,
#     'Drone': E_drone_values,
#     'Camion Diesel Medium': E_vehicle_values['Camion Diesel Medium'],
#     'Petit Van Diesel': E_vehicle_values['Petit Van Diesel'],
#     'Camion Électrique Medium': E_vehicle_values['Camion Électrique Medium'],
#     'Petit Van Électrique': E_vehicle_values['Petit Van Électrique']
# }
# df = pd.DataFrame(data)

# # Exportation vers un fichier CSV
# df.to_csv('energy_consumption_data.csv', index=False)
# print("\nDonnées exportées vers 'energy_consumption_data.csv'")