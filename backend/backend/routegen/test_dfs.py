import route2
import random
import geog
import networkx as nx
import osmgraph
import itertools
import geojsonio
import json

routeGen = route2.Route2(pref_dist=1000)
routeGen.import_file('../../maps/waterloo_small.osm')
print 'file imported'

start_node = random.choice(list(routeGen.map.nodes()))
print('initial start node: '+str(start_node))
# routeGen.setup_initial_pool(start_node)

while routeGen.pool == []:
    routeGen.DFS(routeGen.PREF_DIST, start_node, start_node, [], 50)

print routeGen.pool
for i in range(0,20):
    route = random.choice(routeGen.pool)
    coords = osmgraph.tools.coordinates(routeGen.map, route)
    geojsonio.display(json.dumps({'type': 'LineString', 'coordinates': coords}))