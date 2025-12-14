
import math

# Haversine formula
def haversine(coord1, coord2):
    R = 6371.0
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Build distance matrix
def build_distance_matrix(coords):
    n = len(coords)
    dist_matrix = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dist_matrix[i][j] = haversine(coords[i], coords[j])
    return dist_matrix

# Nearest Neighbor heuristic
def tsp_nearest_neighbor(coords):
    n = len(coords)
    dist_matrix = build_distance_matrix(coords)
    visited = [False]*n
    path = [0]
    visited[0] = True
    total_distance = 0.0

    for _ in range(n-1):
        last = path[-1]
        next_city = None
        min_dist = float('inf')
        for j in range(n):
            if not visited[j] and dist_matrix[last][j] < min_dist:
                min_dist = dist_matrix[last][j]
                next_city = j
        path.append(next_city)
        visited[next_city] = True
        total_distance += min_dist

    total_distance += dist_matrix[path[-1]][path[0]]
    path.append(0)
    return path, total_distance

# Read coordinates and city names
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

# Write optimized route back to file
def write_optimized_route(filename, route, coords, names):
    with open(filename, 'w') as file:
        file.write("#longitude   latitude    City\n")
        for idx in route[:-1]:  # skip the last return-to-start index
            lat, lon = coords[idx]
            city = names[idx]
            file.write(f"{lon:.2f}\t{lat:.2f}\t{city}\n")

# Main
if __name__ == "__main__":
    filename = "cities2k.dat"
    coords, names = read_coordinates_and_names(filename)

    if len(coords) < 2:
        raise ValueError("Error: Not enough cities to compute TSP.")

    route, distance = tsp_nearest_neighbor(coords)
    print("Optimal route (approx):", [names[i] for i in route])
    print("Total distance (km):", round(distance, 2))

    write_optimized_route(filename, route, coords, names)
    print(f"Optimized route written to {filename}")