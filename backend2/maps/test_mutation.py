import route
import random
import geog
import networkx as nx
import osmgraph
import itertools
import geojsonio
import json
import numpy as np

routeGen = route.Route(pool_size=10, nr_mutants=10, nr_of_attempts=100, max_length_path=100, pref_dist=2000)
routeGen.import_file('./maps_osm/waterloo_small.osm')
print 'file imported'


start_node = random.choice(list(routeGen.map.nodes()))
start_node = 2147170547

print('initial start node: '+str(start_node))
routeGen.setup_initial_pool(start_node)
print routeGen.pool
# print(routeGen.pool)

for i in range(0,20):
    routeGen.mutation()
    routeGen.crossover()
    routeGen.mutation()
    routeGen.crossover()
    routeGen.add_random_cycles(start_node)
    if i % 2 == 0:
        routeGen.cut_pool_size2()


routeGen.final_cut()
fitness = [0] * len(list(routeGen.pool))
# for i in range(0,len(list(routeGen.pool))):
#     route = routeGen.pool[i]

#     # find fitness
#     for node in list(route):
#         print node
#         fitness[i] += routeGen.nature_or_monuments(True,node)

numb = max([10,len(list(routeGen.pool))])
ind = fitness.index(max(fitness))
print ind
coords = osmgraph.tools.coordinates(routeGen.map, routeGen.pool[ind])
geojsonio.display(json.dumps({'type': 'LineString', 'coordinates': coords}))
   