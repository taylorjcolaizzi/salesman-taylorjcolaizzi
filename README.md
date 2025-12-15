Starter code and data for traveling salesman problem


Files in this directory:

* datareader.cpp : example code to read in the data files (use Makefile)
* datareader.py  : example code to read in the data files
* cities23.dat : list of coordinates for 23 cities in North America
* cities150.dat : 150 cities in North America
* cities1k.dat : 1207 cities in North America
* cities2k.dat : 2063 cities around the world
* routeplot.py : code to plot the globe and salesman's path<br>
usage:<br>
python routeplot.py cities.dat [cities2.dat] -r [="NA"],"World"'<br>
NA = North America, World = Mercator projection of the whole earth
* earth.C : (just for fun) plotting the globe in ROOT

HOW TO USE THIS INSANE PROGRAM

All my simulated annealing code is in the file sales.py. This is all just AI code. It does simulated annealing like asked. It prints the old distance and the new distance. It also prints the time to execute. For fun, I also found out another algorithm called the nearest neighbor heuristic that is very fast, but it doesn't necessarily seek the global minimum.

How to run my code:
First, make sure you're on the phys56xx environment.

Second, make sure you have all the original .dat files for the city locations.

Third, run the sales.py program with the following structure:

python sales.py old_route.dat new_route.dat

This will run sales.py in python with the old_route.dat as the original route. Then it will save the new route to location new_route.dat.

An example is the following:

python sales.py original_cities23.dat cities23.dat

Please check out files citiesxx.pdf to see my world plots.

Honestly, it looks like nearest neighbor heuristic is doing better than simulated annealing for me. Maybe that's because my simulated annealing is just doing "swap two" instead of something more complex. It also might just not be running long enough, since I just run it for less than a minute each time.

Current best results with simulated annealing:

file, original length, simulated annealing, nearest neighbor, sim. ann. time
cities23, 38 963, 14 098, 13 859, .7

cities150, 317 298, 99 252, 56 179, 3.8

cities1k, 732 177, 731 965, 119 212, 29

cities2k, 10 187 617, 5 179 440, 355 493, 50

Clearly, my simulated annealing isn't really working that great. I want it to be at least at the length of nearest neighbor, but even less is better.