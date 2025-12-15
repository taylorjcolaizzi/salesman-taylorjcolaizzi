
import math
import random
import sys

# -------------------------------
# Haversine formula
# -------------------------------
def haversine(coord1, coord2):
    R = 6371.0
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# -------------------------------
# Compute route distance
# -------------------------------
def route_distance(route, coords):
    dist = 0.0
    for i in range(len(route) - 1):
        dist += haversine(coords[route[i]], coords[route[i+1]])
    return dist

# -------------------------------
# Generate neighbor by swapping two cities
# -------------------------------
def swap_two(route):
    i, j = random.sample(range(1, len(route)-1), 2)
    new_route = route[:]
    new_route[i], new_route[j] = new_route[j], new_route[i]
    return new_route

# -------------------------------
# Simulated Annealing
# -------------------------------
def tsp_simulated_annealing(coords, initial_temp=10000, cooling_rate=0.995, max_iter=100000):
    n = len(coords)
    current_route = list(range(n)) + [0]
    current_distance = route_distance(current_route, coords)
    best_route = current_route[:]
    best_distance = current_distance
    T = initial_temp

    for _ in range(max_iter):
        new_route = swap_two(current_route)
        new_distance = route_distance(new_route, coords)
        delta = new_distance - current_distance

        if delta < 0 or random.random() < math.exp(-delta / T):
            current_route = new_route
            current_distance = new_distance
            if current_distance < best_distance:
                best_route = current_route[:]
                best_distance = current_distance

        T *= cooling_rate
        if T < 1e-8:
            break

    return best_route, best_distance

# -------------------------------
# Read coordinates and names
# -------------------------------
def read_coordinates_and_names(filename):
    coords = []
    names = []
    with open(filename, 'r') as file:
        next(file)  # Skip header
        for line in file:
            parts = line.strip().split(maxsplit=2)
            if len(parts) >= 2:
                try:
                    lon = float(parts[0])
                    lat = float(parts[1])
                    city = parts[2] if len(parts) == 3 else ""
                    coords.append((lat, lon))
                    names.append(city)
                except ValueError:
                    print(f"Skipping invalid line: {line.strip()}")
    return coords, names

# -------------------------------
# Write optimized route
# -------------------------------
def write_optimized_route(filename, route, coords, names):
    with open(filename, 'w') as file:
        file.write("#longitude   latitude    City\n")
        for idx in route[:-1]:
            lat, lon = coords[idx]
            city = names[idx]
            file.write(f"{lon:.2f}\t{lat:.2f}\t{city}\n")

# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sales.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    coords, names = read_coordinates_and_names(filename)

    if len(coords) < 2:
        raise ValueError("Error: Not enough cities to compute TSP.")

    print(f"Running Simulated Annealing on {len(coords)} cities...")
    route, distance = tsp_simulated_anne    route, distance = tsp_simulated_annealing(coords)
    print("Optimized route:", [names[i] for i in route])
    print("Total distance (km):", round(distance, 2))

    write_optimized_route(filename, route, coords, names)
