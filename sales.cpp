// from copilot

#include <bits/stdc++.h>
using namespace std;

const double R = 6371.0; // Earth's radius in km
const double PI = 3.14159265358979323846;

// Convert degrees to radians
inline double toRadians(double deg) {
    return deg * PI / 180.0;
}

// Haversine distance between two points
double haversine(pair<double,double> a, pair<double,double> b) {
    double lon1 = toRadians(a.first), lat1 = toRadians(a.second);
    double lon2 = toRadians(b.first), lat2 = toRadians(b.second);
    double dlon = lon2 - lon1;
    double dlat = lat2 - lat1;
    double h = sin(dlat/2)*sin(dlat/2) +
               cos(lat1)*cos(lat2)*sin(dlon/2)*sin(dlon/2);
    double c = 2 * atan2(sqrt(h), sqrt(1-h));
    return R * c;
}

// Compute total route distance
double totalDistance(const vector<int>& route, const vector<pair<double,double>>& coords) {
    double dist = 0.0;
    int n = route.size();
    for (int i = 0; i < n; i++) {
        dist += haversine(coords[route[i]], coords[route[(i+1)%n]]);
    }
    return dist;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cerr << "Usage: " << argv[0] << " <input_file>\n";
        return 1;
    }

    // Read city coordinates
    vector<pair<double,double>> coords;
    ifstream fin(argv[1]);
    double lon, lat;
    string city;
    while (fin >> lon >> lat) {
        getline(fin, city); // skip city name
        coords.push_back({lon, lat});
    }
    fin.close();

    int n = coords.size();
    vector<int> route(n);
    iota(route.begin(), route.end(), 0);
    random_shuffle(route.begin(), route.end());

    double initialDist = totalDistance(route, coords);
    cout << "Initial distance: " << initialDist << " km\n";

    // Simulated Annealing parameters
    double T = 10000.0;
    double alpha = 0.9995;
    int steps = 1000000;

    vector<int> bestRoute = route;
    double bestDist = initialDist;

    mt19937 rng(time(0));
    uniform_real_distribution<double> urand(0.0, 1.0);

    for (int step = 0; step < steps; step++) {
        // Swap two cities
        int i = rng() % n;
        int j = rng() % n;
        if (i == j) continue;

        swap(route[i], route[j]);
        double newDist = totalDistance(route, coords);
        double delta = newDist - bestDist;

        if (delta < 0 || urand(rng) < exp(-delta / T)) {
            if (newDist < bestDist) {
                bestDist = newDist;
                bestRoute = route;
            }
        } else {
            swap(route[i], route[j]); // revert
        }

        T *= alpha;
        if (T < 1e-8) break;
    }

    cout << "Optimized distance: " << bestDist << " km\n";

    // Output optimized route
    ofstream fout("optimized_route.dat");
    for (int idx : bestRoute) {
        fout << coords[idx].first << " " << coords[idx].second << "\n";
    }
    fout.close();

    return 0;
}
