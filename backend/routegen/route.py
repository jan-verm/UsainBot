import geog
import networkx as nx
from backend.libraries import osmgraph

# By default any way with a highway tag will be loaded
g = osmgraph.parse_file('boston_massachusetts.osm.bz2')  # or .osm or .pbf
for n1, n2 in g.edges_iter():
    c1, c2 = osmgraph.tools.coordinates(g, (n1, n2))   
    g[n1][n2]['length'] = geog.distance(c1, c2)


import random
start = random.choice(g.nodes())
end = random.choice(g.nodes())
path = nx.shortest_path(g, start, end, 'length')
coords = osmgraph.tools.coordinates(g, path)

# Find the sequence of roads to get from start to end
edge_names = [g[n1][n2].get('name') for n1, n2 in osmgraph.tools.pairwise(path)]
import itertools
names = [k for k, v in itertools.groupby(edge_names)]
print(names)
     ['North Harvard Street',
      'Franklin Street',
      'Lincoln Street',
      None,
      'Cambridge Street',
      'Gordon Street',
      'Warren Street',
      'Commonwealth Avenue']

# Visualize the path using geojsonio.py
import geojsonio
import json
geojsonio.display(json.dumps({'type': 'LineString', 'coordinates': coords}))
