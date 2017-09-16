import route
import random
import geog
import networkx as nx
import osmgraph
import itertools
import geojsonio
import json

routeGen = route.Route(pool_size=10, nr_mutants=10, nr_of_attempts=100, max_length_path=100)
routeGen.import_file('../../maps/waterloo_small.osm')
print 'file imported'

start_node = random.choice(list(routeGen.map.nodes()))
print('initial start node: '+str(start_node))
routeGen.setup_initial_pool(start_node)
print(routeGen.pool)

routeGen.mutation()
# routeGen.mutation()
# routeGen.mutation()
# routeGen.mutation()


for route in routeGen.pool:
    coords = osmgraph.tools.coordinates(routeGen.map, route)
    geojsonio.display(json.dumps({'type': 'LineString', 'coordinates': coords}))
# print(routeGen.pool)
