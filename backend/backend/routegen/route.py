import geog
import networkx as nx
import osmgraph
import random
import itertools
import geojsonio
import json


def import_file(self, path):
"""
    import file with relative path 'path' and stores the map data in self.map
"""
    self.map = osmgraph.parse_file(path)
    for n1, n2 in self.map.edges():
        c1, c2 = osmgraph.tools.coordinates(self.map, (n1, n2))   
        self.map[n1][n2]['length'] = geog.distance(c1, c2)

# # By default any way with a highway tag will be loaded
# g = osmgraph.parse_file('boston_massachusetts.osm.bz2')  # or .osm or .pbf
# for n1, n2 in g.edges_iter():
#     c1, c2 = osmgraph.tools.coordinates(g, (n1, n2))   
#     g[n1][n2]['length'] = geog.distance(c1, c2)

# start = random.choice(g.nodes())
# end = random.choice(g.nodes())
# path = nx.shortest_path(g, start, end, 'length')
# coords = osmgraph.tools.coordinates(g, path)

# # Find the sequence of roads to get from start to end
# edge_names = [g[n1][n2].get('name') for n1, n2 in osmgraph.tools.pairwise(path)]
# names = [k for k, v in itertools.groupby(edge_names)]
# print(names)
#     #  ['North Harvard Street',
#     #   'Franklin Street',
#     #   'Lincoln Street',
#     #   None,
#     #   'Cambridge Street',
#     #   'Gordon Street',
#     #   'Warren Street',
#     #   'Commonwealth Avenue']

# # Visualize the path using geojsonio.py
# geojsonio.display(json.dumps({'type': 'LineString', 'coordinates': coords}))