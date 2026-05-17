import random
from math import pi, sin, cos, sqrt
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import euclidean
from itertools import permutations
from scipy.spatial import distance_matrix
from scipy.optimize import linear_sum_assignment

# Drone energy consumption in MJ/km
P_drone = 0.08

# Truck energy consumption in MJ/km
# Camion Diesel Medium
P_cdm = 11.00
# Petite Van Diesel,
P_pvd = 4.90
# Camion Électrique Medium
P_cem = 3.80
# Petite Van Électrique
P_pve = 1.65

class Point:
    def __init__(self, angle, radius, x, y):
        self.angle = angle
        self.radius = radius
        self.x = x
        self.y = y
        self.drone_distance = 0
        self.drone_energy = 0
        self.truck_distance = 0
        self.truck_energy_cdm = 0
        self.truck_energy_pvd = 0
        self.truck_energy_cem = 0
        self.truck_energy_pve = 0

# Generate a random polar coordinate
def random_polar():
    angle = random.uniform(0, 2 * pi)
    radius = random.uniform(1,1)
    x = radius * cos(angle)
    y = radius * sin(angle)
    return Point(angle, radius, x, y)

# Generate and sort points
num_points = 650 
points = [random_polar() for _ in range(num_points)]
points.sort(key=lambda p: p.angle)
# Plot the points and paths for vehicles and drones
plt.figure(figsize=(8, 8))

# Initialize cumulative distances
drone_cumulative_distance = 0
truck_cumulative_distance = 0
truck_last_point = Point(0, 0, 0, 0)  # Starting point for the truck

# Calculate distances and energies
for point in points:
    drone_distance = 2 * point.radius + drone_cumulative_distance
    drone_cumulative_distance += 2 * point.radius
    point.drone_distance = drone_distance
    point.drone_energy = drone_distance * P_drone

    truck_distance = sqrt((point.x - truck_last_point.x) ** 2 + (point.y - truck_last_point.y) ** 2) + truck_cumulative_distance
    truck_cumulative_distance += sqrt((point.x - truck_last_point.x) ** 2 + (point.y - truck_last_point.y) ** 2)
    point.truck_distance = truck_distance
    point.truck_energy_cdm = truck_distance * P_cdm
    point.truck_energy_pvd = truck_distance * P_pvd
    point.truck_energy_cem = truck_distance * P_cem
    point.truck_energy_pve = truck_distance * P_pve
    truck_last_point = point

# Plot the points
for point in points:
    plt.plot(point.x, point.y, 'bo')  # Points as blue circles
    plt.text(point.x, point.y, f'({point.x:.2f}, {point.y:.2f})', fontsize=8, ha='right')

# Plot the drone paths (round trip to each point)
for point in points:
    plt.plot([0, point.x], [0, point.y], 'g--', alpha=0.6)  # Drone outgoing path
    plt.plot([point.x, 0], [point.y, 0], 'g--', alpha=0.6)  # Drone return path

# Plot the truck path
truck_path_x = [0] + [point.x for point in points] + [0]
truck_path_y = [0] + [point.y for point in points] + [0]
plt.plot(truck_path_x, truck_path_y, 'r-', label='Truck Path')  # Truck path as red line

# Add labels and legend
plt.title('Paths of Vehicles and Drones')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.legend(['Drone Path', 'Truck Path'])
plt.grid(True)
plt.axis('equal')  # Equal scaling for x and y axes
plt.show()

# # Création du graphique
plt.figure(figsize=(8.4, 4.8))
drone_energies = [point.drone_energy for point in points]
plt.plot(range(1, num_points + 1), drone_energies, 'b-', label=f'Drone (P={P_drone} MJ/km)')
colors = {
    'Camion Diesel Medium': 'r',
    'Petite Van Diesel': 'g',
    'Camion Électrique Medium': 'm',
    'Petite Van Électrique': 'c'
}

# Define missing variables
P_vehicles = {
    'Camion Diesel Medium': P_cdm,
    'Petite Van Diesel': P_pvd,
    'Camion Électrique Medium': P_cem,
    'Petite Van Électrique': P_pve
}

E_vehicle_values = {
    'Camion Diesel Medium': [point.truck_energy_cdm for point in points],
    'Petite Van Diesel': [point.truck_energy_pvd for point in points],
    'Camion Électrique Medium': [point.truck_energy_cem for point in points],
    'Petite Van Électrique': [point.truck_energy_pve for point in points]
}

intersections = {}  # Define intersections as an empty dictionary or populate it with actual data if needed

for name, E_vals in E_vehicle_values.items():
    plt.plot(range(1, num_points + 1), E_vals, f'{colors[name]}-', label=f'{name} (P={P_vehicles[name]} MJ/km)')
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
plt.xlim(0, num_points)  # X-axis from 0 to 650 as requested
plt.xticks(np.arange(0, num_points+1, 100))
plt.show()