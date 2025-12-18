
import numpy as np
import random
import math
import matplotlib.pyplot as plt
import argparse
from numba import njit, prange
from multiprocessing import Pool, cpu_count
import time

# --- Step 1: Read .dat file ---
def read_coordinates(filename):
    data = np.loadtxt(filename, skiprows=1, usecols=(0, 1))  # First two columns only
    coords = data[:, [1, 0]]  # Convert to (lat, lon)
    return coords

# --- Step 2: Numba-optimized Haversine distance matrix ---
@njit(parallel=True)
def haversine_distance_matrix(coords):
    R = 6371.0
    n = coords.shape[0]
    lat = np.radians(coords[:, 0])
    lon = np.radians(coords[:, 1])
    dist_matrix = np.zeros((n, n), dtype=np.float64)

    for i in prange(n):
        for j in range(n):
            dlat = lat[j] - lat[i]
            dlon = lon[j] - lon[i]
            a = math.sin(dlat / 2)**2 + math.cos(lat[i]) * math.cos(lat[j]) * math.sin(dlon / 2)**2
            c = 2 * math.asin(math.sqrt(a))
            dist_matrix[i, j] = R * c
    return dist_matrix

# --- Step 3: Numba-optimized total distance ---
@njit
def total_distance(tour, dist_matrix):
    n = len(tour)
    dist = 0.0
    for i in range(n):
        dist += dist_matrix[tour[i], tour[(i + 1) % n]]
    return dist

# just to get a general idea of benchmarking
def nearest_neighbor(dist_matrix, start = 0):
    n = dist_matrix.shape[0]
    unvisited = set(range(n))
    tour = [start]
    unvisited.remove(start)

    current = start
    while unvisited:
        next_city = min(unvisited, key=lambda city: dist_matrix[current, city])
        tour.append(next_city)
        unvisited.remove(next_city)
        current = next_city

    return np.array(tour)

# --- Step 4: Simulated Annealing worker (returns schedule) ---
def simulated_annealing_worker(args):
    coords, dist_matrix, initial_temp, cooling_rate, max_iter = args
    n = len(coords)
    current_tour = np.arange(n)
    np.random.shuffle(current_tour)
    current_distance = total_distance(current_tour, dist_matrix)
    best_tour = current_tour.copy()
    best_distance = current_distance
    temp = initial_temp

    # print("original distance is:", best_distance)

    # print("simulated annealing of original:")

    temperature_history = []
    distance_history = []

    # Before annealing, try nearest neighbor heuristic to get a good state

    for _ in range(max_iter):
        temperature_history.append(temp)
        distance_history.append(best_distance)

        a, b = np.random.choice(n, 2, replace=False)
        if a > b:
            a, b = b, a
        new_tour = current_tour.copy()
        new_tour[a:b+1] = new_tour[a:b+1][::-1]
        # new_tour[a], new_tour[b] = new_tour[b], new_tour[a]

        new_distance = total_distance(new_tour, dist_matrix)
        delta = new_distance - current_distance

        if delta < 0 or np.random.rand() < math.exp(-delta / temp):
            current_tour = new_tour
            current_distance = new_distance
            if current_distance < best_distance:
                best_tour = current_tour.copy()
                best_distance = current_distance

        if temp > 100:
            temp *= cooling_rate
        else:
            temp *= 0.9995

        # if temp > 1000:
        #     temp *= 0.995
        # else:
        #     temp *= 0.999

        # if temp < 1e-8:
        #     break

    return best_tour, best_distance, temperature_history, distance_history

# --- Step 5: Save best route ---
def save_route(filename, best_tour, coords, best_distance):
    with open(filename, 'w') as f:
        # f.write("Best TSP Route:\n")
        # f.write(f"Total Distance (km): {best_distance:.3f}\n\n")
        # f.write("Index\tLatitude\tLongitude\n")
        f.write("#longitude\tlatitude\tcity\n")
        for idx in best_tour:
            lat, lon = coords[idx]
            # f.write(f"{idx}\t{lat:.6f}\t{lon:.6f}\n")
            f.write(f"{lon:.6f}\t{lat:.6f}\t{idx}\n")
        lat, lon = coords[best_tour[0]]
        # f.write(f"{best_tour[0]}\t{lat:.6f}\t{lon:.6f} (Return)\n")

# --- Main ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve TSP using Simulated Annealing with Numba and multiprocessing.")
    parser.add_argument("input_file", help="Path to the .dat file containing city coordinates")
    parser.add_argument("output_file", help="Path to save the best route")
    parser.add_argument("--runs", type=int, default=cpu_count(), help="Number of parallel SA runs")
    # parser.add_argument("--runs", type=int, default=1, help="Number of parallel SA runs")
    parser.add_argument("--initial_temp", type=float, default=200000, help="Initial temperature")
    parser.add_argument("--cooling_rate", type=float, default=0.996, help="Cooling rate")
    parser.add_argument("--max_iter", type=int, default=4000000, help="Maximum iterations per run")
    args = parser.parse_args()

    coords = read_coordinates(args.input_file)
    dist_matrix = haversine_distance_matrix(coords)

    # Prepare arguments for each run
    run_args = [(coords, dist_matrix, args.initial_temp, args.cooling_rate, args.max_iter) for _ in range(args.runs)]

    # Original length

    n = len(coords)
    current_tour = np.arange(n)
    np.random.shuffle(current_tour)
    current_distance = total_distance(current_tour, dist_matrix)
    best_tour = current_tour.copy()
    best_distance = current_distance

    print("original distance is:", best_distance)

    # what would nearest neighbor look like?
    #_________________________
    start_city = 0
    nearest_tour = nearest_neighbor(dist_matrix, start=start_city)

    nearest_distance = total_distance(nearest_tour, dist_matrix)
    nearest_tour = nearest_tour.copy()
    nearest_distance = nearest_distance

    print("using nearest neighbor:", nearest_distance)
    #_________________________

    # Run SA in parallel
    print("now, simulated annealing of original route:")
    print("multithreading for number of runs =", args.runs)
    print("starting timer for simulated annealing:")

    start_time = time.perf_counter()
    with Pool(processes=args.runs) as pool:
        results = pool.map(simulated_annealing_worker, run_args)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.4f} seconds")

    print("annealing finished, looking for best run")

    # Find best result among all runs
    best_run = min(results, key=lambda x: x[1])
    best_tour, best_distance, temperature_history, distance_history = best_run

    print(f"Best distance (km): {best_distance}")
    print(f"Best tour: {best_tour}")

    save_route(args.output_file, best_tour, coords, best_distance)
    print(f"Best route saved to {args.output_file}")

    # --- Plot Annealing Schedule for Best Run ---
    plt.figure(figsize=(8, 5))
    plt.plot(temperature_history, distance_history, color='blue')
    plt.xlabel("Temperature")
    plt.xscale('log')
    plt.ylabel("Best Distance So Far")
    plt.title("Annealing Schedule (Best Run)")
    plt.grid(True)
    plot_name = 'an' + args.output_file[6:-4] + '.png'# skip cities, skip .dat
    plt.savefig(plot_name)
    print('saves plot as:', plot_name)
    plt.show()