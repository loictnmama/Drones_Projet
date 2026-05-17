import numpy as np
from math import sqrt, sin, cos, acos, asin, atan2


exemple = [
    {
        "drone": {
            "poids": 490, # grams
            "vitesse": 5, # m/s
            "chargeMax": 200, # grams
            "puissance": 7000, # watts
            "tauxEnergie": 0.5, # kWh/km·kg
        },
        "env": {
            "vitesseVent": 2, # m/s
            "directionVent": 0, # radians
            "K": 0.1, # coefficient de résistance de l'air
            "G": 9.81, # m/s^2
        },
        "clients": [
            {
                "x": 0, # m (dépôt)
                "y": 0, # m
                "poids": 0 # grams
            },
            {
                "x": 50, # (client 1)
                "y": 30,
                "poids": 80
            },
            {
                "x": 80, # (client 2)
                "y": 10,
                "poids": 50
            },
            {
                "x": 20, # (client 3)
                "y": 70,
                "poids": 60
            }
        ]
    }, 
    # met l'exemple suivant ici
]


# Distance function
def distance(p1, p2):
    return sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


def speed_with_load(e):
    total_weight = e.drone.poid + load
    arg = total_weight * G / LIFT_POWER
    if arg > 1:
        arg = 1
    theta = acos(arg)
    return BASE_SPEED * sin(theta) / sin(acos(DRONE_WEIGHT * G / LIFT_POWER))