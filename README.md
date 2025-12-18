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

All my simulated annealing code is in the file sales.py. This is all just AI code. It does simulated annealing, prints the old and new distances, and the time to execute. For fun, I also found out another algorithm called the nearest neighbor heuristic that is very fast, but it doesn't necessarily seek the global minimum. Finally, the code produces a plot of the annealing schedule and saves the new cities file.

How to run my code:
First, make sure you're on the phys56xx environment.

Second, make sure you have all the original .dat files for the city locations.

Third, run the sales.py program with the following structure:

python sales.py old_route.dat new_route.dat

This will run sales.py in python with the old_route.dat as the original route. Then it will save the new route to the location new_route.dat.

An example is the following:

python sales.py original_cities23.dat cities23.dat

Please check out files citiesxx.pdf to see my world plots and files anxx.png to see my annealing schedules.

Current best results with simulated annealing: I'm just running this on Rivanna with 16 Gb of memory and 10 CPU cores. However, Rivanna says it has access to 40 cores when I only specified 10 in the open on demand.

For some reason, Rivanna takes longer to run than my humble $1000 MacBook Air, but I don't know why.

| filename | original length (km) | nearest neighbor (km) | simulated annealing (km) | time (s) |
| --- | --- | --- | --- | --- |
| cities23 | 46 112 | 13 859 | 13 487 | 68.5 |
| cities150 | 316 803 | 56 179 | 50 160 | 78.1 |
| cities1k | 2 780 334 | 119 212 | 106 549 | 148.4 |
| cities2k | 12 141 639 | 355 493 | 354 308 | 192.3 |

So, it looks like compared to nearest neighbor, my simulated annealing was able to shave off a little bit of distance for every data file; however, I needed to run this a couple times until I got satisfactory results.