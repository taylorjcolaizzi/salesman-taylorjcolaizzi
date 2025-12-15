# all this code is ai code by the way
# only a small amount of human intervention
import math
import random
import sys

# -------------------------------
# Haversine formula
# -------------------------------
def haversine(coord1, coord2):
    '''
    Docstring for haversine
    Compute distance between two points on the surface of a sphere


    :param coord1: longitude and latitude of first city
    :param coord2: longitude and latitute of second city

    returns distance for the arc length of the great
    circle connecting those cities
    '''
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
    '''
    Docstring for route_distance
    For each stop on route, just add up the distance from one 
    stop to the next.
    
    :param route: just number of stops on route
    :param coords: longitude and latitude for each
    location on route
    '''
    dist = 0.0
    for i in range(len(route) - 1):
        dist += haversine(coords[route[i]], coords[route[i+1]])
    return dist

# -------------------------------
# Generate neighbor by swapping two cities
# -------------------------------
def swap_two(route):
    '''
    Docstring for swap_two
    Just pick two locations and swap them
    THIS IS THE ANNEALING RANDOMIZER
    
    :param route: Ordering of locations in the route
    '''
    i, j = random.sample(range(1, len(route)-1), 2)
    new_route = route[:]
    new_route[i], new_route[j] = new_route[j], new_route[i]
    return new_route

# -------------------------------
# Simulated Annealing
# -------------------------------
def tsp_simulated_annealing(coords, initial_temp=10000, cooling_rate=0.99, max_iter=1000000):
    '''
    Docstring for tsp_simulated_annealing
    Uses simulated annealing to reduce total path length of
    traveling salesman problem.
    Basically just do metropolis algorithm starting at really 
    high temperature and slowly reduce the temperature after
    each iteration.
    
    :param coords: longitude and latitude of each city
    :param initial_temp: higher means more likely to swap
    :param cooling_rate: rate of annealing. slowly reduce likelihood
    to swap cities
    :param max_iter: how many times to run the annealing
    before quitting
    '''
    n = len(coords)
    current_route = list(range(n)) + [0]
    current_distance = route_distance(current_route, coords)
    best_route = current_route[:]
    best_distance = current_distance
    T = initial_temp

    for _ in range(max_iter):
        '''
        each time through the loop, you
        swap two cities. Then check the 
        distance of the whole route

        if the new route is better than the old route, 
        take it!
        If not, only take it with a certain probability
        that decreases as temperature decreases.
        '''
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
    '''
    Docstring for read_coordinates_and_names
    
    :param filename: just the name and location of the
    .dat file that has your coordinates and city names
    '''
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
    '''
    Once you have the ideal route after simulated
    annealing, write this route to a new file, specified
    by the user
    
    :param filename: new name
    :param route: from code
    :param coords: from code
    :param names: from old route
    '''
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
    '''
    To use sales.py, here's what you gotta do

    make sure you're on the phys56xx environment

    usage is just to go
    python sales.py input.dat output.dat

    where input.dat is your original data file
    and output.dat is the name of the new file you 
    want the optimized route to be saved to

    example usage
    python sales.py original_cities23.dat new_cities23.dat


    finally, the program prints out the route and the 
    new length for you!
    '''
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python sales.py <input_file> [output_file]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) == 3 else input_file

    coords, names = read_coordinates_and_names(input_file)

    if len(coords) < 2:
        raise ValueError("Error: Not enough cities to compute TSP.")

    print(f"Running Simulated Annealing on {len(coords)} cities...")

    n = len(coords)
    current_route = list(range(n)) + [0]
    current_distance = route_distance(current_route, coords)
    print("Old route is this long (km):", round(current_distance, 2))

    route, distance = tsp_simulated_annealing(coords)
    print("Optimized route:", [names[i] for i in route])
    print("Total distance (km):", round(distance, 2))

    write_optimized_route(output_file, route, coords, names)