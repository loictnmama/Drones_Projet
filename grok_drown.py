import numpy as np
from math import sqrt, sin, cos, acos, asin, atan2
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection
import matplotlib.colors as mcolors

# Constants
DRONE_WEIGHT = 490  # grams
MAX_PAYLOAD = 200  # grams
BASE_SPEED = 5  # m/s
WIND_SPEED = 2  # m/s
WIND_DIR = 0  # radians
LIFT_POWER = 7000  # Adjusted lift power
K = 0.1  # air resistance coefficient
G = 9.81  # m/s^2
ANIMATION_SCALE = 0.5
ENERGY_RATE = 0.5 # kWh/km·kg (example value, adjustable)

# Customer data: [x, y, weight in grams]
customers = [
    (0, 0, 0),      # Depot
    (50, 30, 80),   # Customer 1
    (80, 10, 50),   # Customer 2
    (20, 70, 60)    # Customer 3
]
N = len(customers) - 1

# Distance function
def distance(p1, p2):
    return sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

# Speed with load
def speed_with_load(load):
    total_weight = DRONE_WEIGHT + load
    arg = total_weight * G / LIFT_POWER
    if arg > 1:
        arg = 1
    theta = acos(arg)
    return BASE_SPEED * sin(theta) / sin(acos(DRONE_WEIGHT * G / LIFT_POWER))

# Speed with load and wind
def speed_with_load_and_wind(load, p1, p2):
    v_l = speed_with_load(load)
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    if dx == 0 and dy == 0:
        return v_l
    flight_angle = atan2(dy, dx)
    theta_w = flight_angle - WIND_DIR
    v_w = WIND_SPEED
    theta_d = asin((v_w * sin(theta_w)) / v_l) if v_l != 0 else 0
    v_prime = v_w * cos(theta_w) + v_l * cos(theta_d)
    return max(v_prime, 0.1)

# Flight time
def flight_time(p1, p2, load):
    dist = distance(p1, p2)
    speed = speed_with_load_and_wind(load, p1, p2)
    return dist / speed if speed > 0 else float('inf')

# Energy consumption (kWh)
def energy_consumption(distance_m, load_g):
    dist_km = distance_m / 1000  # meters to kilometers
    load_kg = (DRONE_WEIGHT + load_g) / 1000  # grams to kilograms (include drone weight)
    return dist_km * load_kg * ENERGY_RATE

# Dynamic Programming Algorithm
def solve_fsvrplw(customers):
    N = len(customers) - 1
    total_payload = sum(c[2] for c in customers[1:])
    if total_payload > MAX_PAYLOAD:
        print("Total payload exceeds drone capacity!")
        return None, None, None, None, None

    FT = {}
    Payload = {}
    for next_c in range(1, N + 1):
        visited = 1 << (next_c - 1)
        FT[(visited, next_c)] = flight_time(customers[0], customers[next_c], total_payload)
        Payload[visited] = total_payload - customers[next_c][2]

    for size in range(2, N + 1):
        for visited in range(1, 1 << N):
            if bin(visited).count('1') != size - 1:
                continue
            for next_c in range(1, N + 1):
                if visited & (1 << (next_c - 1)):
                    continue
                new_visited = visited | (1 << (next_c - 1))
                min_time = float('inf')
                for prev in range(1, N + 1):
                    if not (visited & (1 << (prev - 1))):
                        continue
                    time = FT.get((visited, prev), float('inf')) + flight_time(
                        customers[prev], customers[next_c], Payload[visited]
                    )
                    min_time = min(min_time, time)
                FT[(new_visited, next_c)] = min_time
                Payload[new_visited] = Payload[visited] - customers[next_c][2]

    all_visited = (1 << N) - 1
    min_time = float('inf')
    optimal_last = None
    for last in range(1, N + 1):
        if (all_visited, last) in FT:
            total_time = FT[(all_visited, last)] + flight_time(customers[last], customers[0], 0)
            if total_time < min_time:
                min_time = total_time
                optimal_last = last

    route = [0]
    visited = all_visited
    last = optimal_last
    while visited:
        route.append(last)
        next_visited = visited & ~(1 << (last - 1))
        min_time = float('inf')
        prev_last = None
        for prev in range(1, N + 1):
            if next_visited & (1 << (prev - 1)):
                time = FT.get((next_visited, prev), float('inf'))
                if time < min_time:
                    min_time = time
                    prev_last = prev
        visited = next_visited
        last = prev_last
    route.append(0)

    segment_times = []
    segment_loads = []
    segment_energies = []
    current_load = total_payload
    for i in range(len(route) - 1):
        p1 = customers[route[i]]
        p2 = customers[route[i + 1]]
        time = flight_time(p1, p2, current_load)
        dist = distance(p1, p2)
        energy = energy_consumption(dist, current_load)
        segment_times.append(time if time != float('inf') else 0)
        segment_loads.append(current_load)
        segment_energies.append(energy)
        if i < len(route) - 2:
            current_load -= customers[route[i + 1]][2]
    
    return route, min_time, segment_times, segment_loads, segment_energies

if route:
    total_energy = sum(segment_energies)
    print("Optimal Route:", route)
    print(f"Total Flight Time: {total_time:.2f} seconds")
    print("Segment Times:", [f"{t:.2f}" for t in segment_times])
    print("Segment Loads:", segment_loads)
    print("Segment Energies (kWh):", [f"{e:.6f}" for e in segment_energies])
    print(f"Total Energy Consumption: {total_energy:.6f} kWh")
    print(f"Computation Time: {end_time - start_time:.4f} seconds")
    # animate_drone_movement(route, customers, segment_times, segment_loads, segment_energies)
else:
    print("No feasible solution found.")