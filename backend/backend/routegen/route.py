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
            self.pool = []
            while self.pool == []:
                pool = nx.cycle_basis(self.map.to_undirected(), startnode)
            
                for path in pool:
                    if (startnode in path):
                        self.pool.append(path)
        else:
            raise Exception('Startnode is not in the set of nodes')


    """
        Random neighbor
    """
    def get_random_neighbor(self, start, path):
        start_index = path.index(start)
        # find random neighbor of start as end node
        if start_index == 0 or start_index == len(path) -1:
            start_neighbors = [path[1], path[len(path) - 2]]
        else:
            start_neighbors = [path[start_index-1], path[start_index+1]]

        return random.choice(start_neighbors)

    """
        add some randomness
    """
    def add_random_cycles(self, startnode):
        pool = []
        pool = nx.cycle_basis(self.map.to_undirected(), startnode)
        for path in pool:
            if (startnode in path):
                self.pool.append(path)

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

            while new_path == path and nr_of_attempts < self.NR_OF_ATTEMPTS:
                # init
                start = random.choice(path)
                
                # print cycle
                # coords = osmgraph.tools.coordinates(self.map.to_undirected(), cycle[0])
                # geojsonio.display(json.dumps({'type': 'LineString', 'coordinates': coords}))
                end = random.choice(path)
                temp = start
                new_path = []
                length_new_path = 0
                try_once = False
                # we stop when we have a path between start or end, or if we exceed a certain MAX_LENGTH_PATH
                if start == end:
                    try_once = True
                while (temp != end or try_once):
                    # init
                    neighbor = start
                    neighbor_visited = []
                    try_once = False
    
                    # find a random neighbour that hasn't been visited yet. If no such neighbour, then find new random path, otherwise it gets stuck)
                    while (neighbor in new_path or neighbor == start)  and sorted(list(set(neighbor_visited))) != sorted(list(self.map.neighbors(temp))):
                        neighbor = random.choice(list(self.map.neighbors(temp)))
                        neighbor_visited.append(neighbor)

                    # good path
                    if neighbor not in new_path and length_new_path < self.MAX_LENGTH_PATH:
                        new_path.append(neighbor)
                        temp = neighbor
                        length_new_path += 1
                    
                    # not a neighbouring node was found, do shortest_path
                    else:
                        test = nx.astar_path(self.map, new_path[len(new_path)-1], end)
                        temp = end
                        new_path = new_path + test

                # you've tried to find a path
                nr_of_attempts += 1

                # add path to cycle
                new_path = path[0:path.index(start)-1] + new_path + path[path.index(end)+1:]


                
            # add new path to the pool
            if nr_of_attempts < self.NR_OF_ATTEMPTS:
                new_pool.append(new_path)

                
        
        # we have a new pool
        self.pool = new_pool
        # print len([list(x) for x in set(tuple(x) for x in self.pool)])



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
        Crossover function
    """
    def crossover(self):
        new_pool = self.pool # the new pool will be the old pool plus NR_MUTANTS newly generated paths

        # Generate NR_MUTANTS new path and add it to the pool
        for i in xrange(0, self.NR_MUTANTS):
            cycle1 = random.choice(self.pool)
            retry_not_unique = True
            nr_of_attempts = 0

            while retry_not_unique and nr_of_attempts < self.NR_OF_ATTEMPTS:
                # select random node from cycle1 that is not the startnode, unless path = [startnode,startnode]
                if cycle1 != [cycle1[0],cycle1[0]]: # 1. What if it is????
                    random_node = cycle1[0] # startnode
                    while random_node == cycle1[0]:
                        random_node = random.choice(cycle1)

                    cycle2 = self.find_random_cycle_with_node(random_node)

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
        fitness function
    """
    def fitness(self, cycle):
        total_dist = 0
        for idx in xrange(1,len(cycle)):
            total_dist += self.map[cycle[idx-1]][cycle[idx]]['length']
        return 1/math.pow(total_dist-self.PREF_DIST, 2)
        

    """
        Cut to original POOL_SIZE
    """
    def cut_pool_size(self):        
        # Helper function for choice() - see stackoverflow
        def cdf(weights):
            total = sum(weights)
            result = []
            cumsum = 0
            for w in weights:
                cumsum += w
                result.append(cumsum / total)
            return result
        
        # Helper function for deleting cycles with specific probabilities
        def choice(population, weights):
            assert len(population) == len(weights)
            cdf_vals = cdf(weights)
            x = random.random()
            idx = bisect.bisect(cdf_vals, x)
            return idx
        
        # Normalize fitness to sum up to one
        def normalize(list):
            return [l/sum(list) for l in list]
        
        while len(self.pool) > self.POOL_SIZE:
            pool_fitness = normalize([self.fitness(c) for c in self.pool])
            del_idx = choice(self.pool, pool_fitness)
            del self.pool

            
    """
        Init
    """
    def __init__(self, pool_size, nr_mutants, nr_of_attempts, max_length_path, pref_dist):
        self.POOL_SIZE = pool_size
        self.pool = []

        self.NR_MUTANTS = nr_mutants
        self.NR_OF_ATTEMPTS = nr_of_attempts
        self.MAX_LENGTH_PATH = max_length_path
        self.PREF_DIST = pref_dist
        


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
