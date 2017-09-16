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
                self.pool.append([startnode, startnode])
        else:
            raise Exception('Startnode is not in the set of nodes')


    """
        Mutation function
    """
    def mutation(self):
        new_pool = self.pool # the new pool will be the old pool plus NR_MUTANTS newly generated paths

        # Generate NR_MUTANTS new path and add it to the pool
        for i in xrange(0, self.NR_MUTANTS):
            # select random path from pool
            path = random.choice(self.pool)
            new_path = path
            nr_of_attempts = 0

            retry_not_unique = True

            while new_path == path and nr_of_attempts < self.NR_OF_ATTEMPTS and retry_not_unique:
                # init
                start = random.choice(path)
                start_index = path.index(start)
                # find random neighbor of start as end node
                if start_index == 0 or start_index == len(path -1):
                    start_neighbors = [path[1], path[len(path) - 2]]
                else:
                    start_neighbors = [path[start_index-1], path[start_index+1]]

                end = random.choice(start_neighbors)
                temp = start
                new_path = [start]
                length_path = 0
                
                # we stop when we have a path between start or end, or if we exceed a certain MAX_LENGTH_PATH
                try_again = True
                while (temp != end or start==end) and length_path < self.MAX_LENGTH_PATH and try_again:
                    neighbors_checked = []
                    n = temp
                    while n in new_path and neighbors_checked.sort() != self.map(neighbors(temp)).sort():
                        n = random.choice(list(self.map.neighbors(temp)))
                        neighbors_checked.append(n)
                    
                    
                    if neighbors_checked.sort() != self.map(neighbors(temp)).sort():
                        temp=n
                        new_path.append(n)
                        length_path += 1
                    else:
                        try_again = False
                    
                new_path.append(end)

                # replace path in cycle with new_path
                new_path = path[0:path.index(new_path[0])] + new_path + path[path.index(new_path[len(new_path)-1])+2:]

                # check that a node is not visited twice
                if (all_nodes_unique(new_path)):
                    new_pool.append(new_path)
                    retry_not_unique = False
                else:
                    retry_not_unique = True
                    
                nr_of_attempts += 1
            
            # we have a new pool
            self.pool = new_pool
            
    """
        Crossover function
    """
    def crossover(self):
        # TODO
        new_pool = self.pool # the new pool will be the old pool plus NR_MUTANTS newly generated paths

        # Generate NR_MUTANTS new path and add it to the pool
        for i in xrange(0, self.NR_MUTANTS):
            cycle1 = random.choice(self.pool)
            retry_not_unique = True
            nr_of_attempts = 0

            while retry_not_unique and nr_of_attempts < self.NR_OF_ATTEMPTS:
                # select random node from cycle1 that is not the startnode, unless path = [startnode,startnode]
                if cycle1 != [cycle1[0],cycle1[0]]:
                    random_node = cycle1[0] # startnode
                    while random_node == cycle1[0]:
                        random_node = random.choice(cycle1)

                    cycle2 = find_random_cycle_with_node(random_node)

                    # make combination of the two cycles
                    new_path = cycle1[0:cycle1.index(random_node)] + cycle2[cycle2.index(random_node):]

                    # check that a node is not visited twice
                    if (all_nodes_unique(new_path)):
                        new_pool.append(new_path)
                        retry_not_unique = False
                    else:
                        nr_of_attempts += 1

         # we have a new pool
        self.pool = new_pool


    """
        Find a random cycle with node n from pool
    """
    def find_random_cycle_with_node(self, n):
        cycles = []

        # find all the cycles that contain the node
        for path in self.pool:
            if n in path:
                cycles.append(path)

        # return a random cycle
        return random.choice(cycles)

    """
        Assign fitness
    """
    def assign_fitness(self):
        pass
        # TODO

    """
        Cut to original POOL_SIZE
    """
    def cut_pool_size(self):
        pass
        # TODO

            
    """
        Init
    """
    def __init__(self, pool_size, nr_mutants, nr_of_attempts, max_length_path):
        self.POOL_SIZE = pool_size
        self.pool = []

        self.NR_MUTANTS = nr_mutants
        self.NR_OF_ATTEMPTS = nr_of_attempts
        self.MAX_LENGTH_PATH = max_length_path
        


"""
    Check if all nodes in a list are unique (check visited nodes)
"""
def all_nodes_unique(x):
    seen = set()
    return not any(i in seen or seen.add(i) for i in x)


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
