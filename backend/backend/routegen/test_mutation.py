import route
import random
import geog
import networkx as nx
import osmgraph
import itertools
import geojsonio
import json

routeGen = route.Route(pool_size=10, nr_mutants=10, nr_of_attempts=100, max_length_path=100, pref_dist=2000)
routeGen.import_file('../../maps/brussels.osm.pbf')
print 'file imported'


start_node = random.choice(list(routeGen.map.nodes()))
routeGen.nature_or_monuments(True,start_node)
# print('initial start node: '+str(start_node))
# routeGen.setup_initial_pool(start_node)
# # print(routeGen.pool)

# for i in range(0,20):
#     routeGen.mutation()
#     routeGen.mutation()
#     # routeGen.add_random_cycles(start_node)
#     if i % 2 == 0:
#         routeGen.cut_pool_size2()


# routeGen.final_cut()
# for i in range(0,20):
#     route = random.choice(routeGen.pool)
#     coords = osmgraph.tools.coordinates(routeGen.map, route)
#     geojsonio.display(json.dumps({'type': 'LineString', 'coordinates': coords}))