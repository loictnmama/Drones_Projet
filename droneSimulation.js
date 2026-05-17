import { sin, cos, sqrt, acos, max } from 'mathjs'

let exemples = [
    {
        drone: {
            poids: 490, // grams
            vitesse: 5, // m/s
            chargeMax: 200, // grams
            puissance: 7000, // watts
            tauxEnergie: 0.5, // kWh/km·kg
        },
        voiture: {
            tauxEnergie: 0.5, // kWh/km·kg
        },
        env: {
            vitesseVent: 2, // m/s
            directionVent: 0, // radians
            K: 0.1, // coefficient de résistance de l'air
            G: 9.81, // m/s^2
        },
        clients: [
            {
                x: 0, // m (dépôt)
                y: 0, // m
                poidsColis: 0 // grams
            },
            {
                x: 50, // (client 1)
                y: 30,
                poidsColis: 80
            },
            {
                x: 80, // (client 2)
                y: 10,
                poidsColis: 50
            },
            {
                x: 20, // (client 3)
                y: 70,
                poidsColis: 60
            }
        ]
    }, 
    // met l'exemple suivant ici
]

function distance (x1, y1, x2, y2) {
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)
}

function vitesseAvecPoidsColis (drone, env, client) {
    poidsTotal = drone.poids + client.poidsColis
    arg = poidsTotal * env.G / drone.puissance
    if (arg > 1) arg = 1;
    thetha = acos(arg)
    return drone.vitesse * sin(thetha) / sin(acos(drone.poids * env.G / drone.puissance))
    
function vitesseAvecPoidsColis_et_Vent(drone, env, client, p1, p2) {
    // Calcul de la vitesse avec le poids
    let v_l = vitesseAvecPoidsColis(drone, env, client);
    
    // Différence de coordonnées
    let dx = p2.x - p1.x;
    let dy = p2.y - p1.y;
    
    // Si le drone ne bouge pas
    if (dx === 0 && dy === 0) {
        return v_l;
    }
    
    // Calcul de l'angle de vol
    let angleVol = Math.atan2(dy, dx);
    
    // Différence entre l'angle de vol et la direction du vent
    let theta_w = angleVol - env.directionVent;
    
    // Vitesse du vent
    let v_w = env.vitesseVent;
    
    // Calcul de l'angle de dérivation
    let theta_d = v_l !== 0 ? Math.asin((v_w * Math.sin(theta_w)) / v_l) : 0;
    
    // Calcul de la vitesse résultante
    let v_prime = v_w * Math.cos(theta_w) + v_l * Math.cos(theta_d);
    
    // Retour de la vitesse minimale de 0.1 m/s
    return max(v_prime, 0.1);
}