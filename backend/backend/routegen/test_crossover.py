import route
import random
import geog
import networkx as nx
import osmgraph
import itertools
import geojsonio
import json


routeGen = route.Route(pool_size=10, nr_mutants=5, nr_of_attempts=100, max_length_path=5, pref_dist=5000)
routeGen.import_file('../../maps/waterloo_small.osm')
start_node = random.choice(list(routeGen.map.nodes()))
print('initial start node: '+str(start_node))
routeGen.setup_initial_pool(start_node)
print(routeGen.pool)

for i in range(0, 20):
    routeGen.mutation()
    #routeGen.crossover()
    routeGen.add_random_cycles(start_node)
    routeGen.cut_pool_size()

for i in range(0,10):
    route = random.choice(routeGen.pool)
    coords = osmgraph.tools.coordinates(routeGen.map, route)
    geojsonio.display(json.dumps({'type': 'LineString', 'coordinates': coords}))