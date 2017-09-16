import geog
import networkx as nx
import osmgraph
import random
import itertools
import geojsonio
import json


class Route:

    """
        import file with relative path 'path' and stores the map data in self.map
    """
    def import_file(self, path):
        self.map = osmgraph.parse_file(path)

        # add distances
        for n1, n2 in self.map.edges():
            c1, c2 = osmgraph.tools.coordinates(self.map, (n1, n2))   
            self.map[n1][n2]['length'] = geog.distance(c1, c2)


    """
        setup initial pool for generation process
    """
    def setup_initial_pool(self, startnode):
        if (startnode in self.map.nodes()):
            # set up an initial pool of POOL_SIZE
            for i in xrange(0, self.POOL_SIZE):
                self.pool.append([startnode,startnode])

        else
            raise Exception('Startnode is not in the set of nodes')


    """
        Mutation function
    """
    def mutation(self, startnode):
        new_pool = self.pool # the new pool will be the old pool plus NR_MUTANTS newly generated paths

        # Generate NR_MUTANTS new path and add it to the pool
        for i in xrange(0, self.NR_MUTANTS):
            # select random path from pool
            path = random.choice(self.pool)
            new_path = path
            nr_of_attempts = 0

            # see which nodes have already been visited
            visited = []
            for i in path:
                visited.append(i)
            
            while new_path == path && nr_of_attempts < self.NR_OF_ATTEMPTS:
                # init
                v = random.choice(path)
                
            





            
    """
        Init
    """
    def __init__(self, pool_size, nr_mutants, nr_of_attempts):
        self.POOL_SIZE = pool_size
        self.pool = []

        self.NR_MUTANTS = nr_mutants
        self.NR_OF_ATTEMPTS = nr_of_attempts


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
