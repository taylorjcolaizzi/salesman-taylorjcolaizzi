
import math
import random
import matplotlib.pyplot as plt
import argparse

# --- Step 1: Read .dat file ---
def read_coordinates(filename):
    coords = []
    with open(filename, 'r') as f:
        next(f)  # Skip the first line (header)
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                lon, lat = map(float, parts[:2])
                coords.append((lat, lon))  # Store as (latitude, longitude)
    return coords

# --- Step 2: Haversine distance ---
def haversine_distance(p1, p2):
    R = 6371.0  # Earth radius in km
    lat1, lon1 = math.radians(p1[0]), math.radians(p1[1])
    lat2, lon2 = math.radians(p2[0]), math.radians(p2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))

    return R * c

def total_distance(tour, coords):
    # Includes return to starting point
    return sum(haversine_distance(coords[tour[i]], coords[tour[(i+1) % len(tour)]]) for i in range(len(tour)))

# --- Step 3: Simulated Annealing with tracking ---
def simulated_annealing(coords, initial_temp=10000, cooling_rate=0.9999, max_iter=200000):
    n = len(coords)
    current_tour = list(range(n))
    random.shuffle(current_tour)
    current_distance = total_distance(current_tour, coords)
    best_tour = current_tour[:]
    best_distance = current_distance
    temp = initial_temp

    temperature_history = []
    distance_history = []
    all_distance_history = []

    for i in range(max_iter):
        temperature_history.append(temp)
        distance_history.append(best_distance)
        all_distance_history.append(current_distance)

        a, b = random.sample(range(n), 2)
        new_tour = current_tour[:]
        new_tour[a], new_tour[b] = new_tour[b], new_tour[a]
        new_distance = total_distance(new_tour, coords)

        delta = new_distance - current_distance
        if delta < 0 or random.random() < math.exp(-delta / temp):
            current_tour = new_tour
            current_distance = new_distance
            if current_distance < best_distance:
                best_tour = current_tour[:]
                best_distance = current_distance

        temp *= cooling_rate
        # temp -= cooling_rate
        # if temp < 1e-8:
        #     break

    return best_tour, best_distance, temperature_history, distance_history, all_distance_history

# --- Step 4: Save best route to file ---
def save_route(filename, best_tour, coords, best_distance):
    with open(filename, 'w') as f:
        # f.write("Best TSP Route:\n")
        # f.write(f"Total Distance (km): {best_distance:.3f}\n\n")
        f.write("#Longitude\tLatitude\tCity\n")
        for idx in best_tour:
            lat, lon = coords[idx]
            f.write(f"{lon:.6f}\t{lat:.6f}\t{idx}\n")
        # Add return to start
        lat, lon = coords[best_tour[0]]
        f.write(f"{lon:.6f}\t{lat:.6f}\t{best_tour[0]}\n")

# --- Main ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve TSP using Simulated Annealing with Haversine distance.")
    parser.add_argument("input_file", help="Path to the .dat file containing city coordinates")
    parser.add_argument("output_file", help="Path to save the best route")
    args = parser.parse_args()

    coords = read_coordinates(args.input_file)
    best_tour, best_distance, temperature_history, distance_history, all_distance_history = simulated_annealing(coords)

    print("Best tour:", best_tour)
    print("Best distance (km):", best_distance)

    # Save route to output file
    save_route(args.output_file, best_tour, coords, best_distance)
    print(f"Best route saved to {args.output_file}")

    # Plot Distance vs Temperature
    plt.figure(figsize=(8, 5))
    plt.plot(temperature_history, distance_history, color='blue')
    plt.plot(temperature_history, all_distance_history, color='red')
    plt.xlabel("Temperature")
    plt.ylabel("Best Distance (km)")
    plt.title("Distance vs Temperature during Simulated Annealing")
    plt.grid(True)
    plt.show()
