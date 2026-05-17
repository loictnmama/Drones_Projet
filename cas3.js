const { sin, cos, PI, sqrt } = Math;

//generate a randome polar coordonate in the range of 0 to 2*PI, with a radius between 0 and 1, that return {angle, radius, x, y}
function randomPolar() {
    const angle = Math.random() * 2 * PI;
    const radius = Math.random();
    const x = radius * cos(angle);
    const y = radius * sin(angle);
    return { angle, radius, x, y };
}

let points = [];

let numPoints = 10; // Number of points to generate

for (let i = 0; i < numPoints; i++) {
    let point = randomPolar();
    points.push(point);
}

// Sort points by angle
points.sort((a, b) => a.angle - b.angle);

let droneCumulativeDistance = 0; // Cumulative distance from the center of the drone

let truckCumulativeDistance = 0; // Cumulative distance from the center of the truck

let truckLastPoint = {
    radius: 0,
    angle: 0,
    x: 0,
    y: 0,
}

for (let i = 0; i < points.length; i++) {
    let droneDistance = 2*points[i].radius; // Distance from the center of the drone
    droneCumulativeDistance += droneDistance; // Cumulative distance from the center of the drone
    points[i].droneDistance = droneDistance; // Add distance to point
    points[i].droneEnergy = droneDistance * PDrone; // Add energy consumption to point
    
    let truckDistance = sqrt((points[i].x - truckLastPoint.x) ** 2 + (points[i].y - truckLastPoint.y) ** 2); // Distance from the center of the truck
    truckCumulativeDistance += truckDistance; // Cumulative distance from the center of the truck
    points[i].truckDistance = truckDistance; // Add distance to point
    truckLastPoint = points[i]; // Update last point
}

console.log(points)