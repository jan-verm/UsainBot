import geog
import networkx as nx
import osmgraph
import random
import itertools
import geojsonio
import json
import math
import bisect
import numpy as np

class Route2:

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
    # def setup_initial_pool(self, startnode):
    #     if (startnode in self.map.nodes()):
    #         # set up an initial pool of POOL_SIZE
    #         self.pool = []
    #         while self.pool == []:
    #             pool = nx.cycle_basis(self.map.to_undirected(), startnode)
            
    #             for path in pool:
    #                 if (startnode in path):
    #                     self.pool.append(path)
    #     else:
    #         raise Exception('Startnode is not in the set of nodes')
    # def setup_initial_pool(self, startnode):
    #     self.pool = []
    #     for i in range(0,100):
    #         self.pool.append([startnode,startnode])


    """
        Find a random direction to go to
    """
    def DFS(self, preferred_distance, v, target, path, margin):
        if self.found_paths > 10:
            return

        if (-margin < preferred_distance < margin and v == target): # stop clause for successful branch
            print 'yes'
            path.append(v)
            print path
            self.pool.append(path)
            print self.pool
            self.found_paths += 1
        elif (preferred_distance < -margin): # stop clause for non successful branch
            # print 'no'
            return
        for u in list(self.map.neighbors(v)):
            # print u, list(self.map.neighbors(v))
            margin = np.random.uniform(low=0, high=1, size=1)
            if v not in path and margin[0] > self.LEAVE_PATH_MARGIN:
                new_path = path[:]
                new_path.append(v) # add current vertex to path
                self.DFS(preferred_distance-self.map[v][u]['length'], u, target, new_path, margin)


    # def greedy(self, preferred_distance, v, target, path, margin):
    #     print preferred_distance
    #     if self.found_paths > 10:
    #         return

    #     if (-margin < preferred_distance < margin and v == target): # stop clause for successful branch
    #         print 'yes'
    #         path.append(v)
    #         print path
    #         self.pool.append(path)
    #         print self.pool
    #         self.found_paths += 1
    #     elif (preferred_distance < -margin): # stop clause for non successful branch
    #         # print 'no'
    #         return

    #     print path
    #     neighbors = list(self.map.neighbors(v))
    #     neighbor_lengths = [self.map[v][t]['length'] for t in neighbors]
    #     index = neighbor_lengths.index(max(neighbor_lengths))
    #     highest_neighbor = neighbors[index]
    #     print highest_neighbor
    #     if highest_neighbor not in path:
    #         new_path = path[:]
    #         new_path.append(v) # add current vertex to path
    #         self.greedy(preferred_distance-self.map[v][highest_neighbor]['length'], highest_neighbor, target, new_path, margin)
                


    def get_pool(self):
        return pool

    """
        Init
    """
    def __init__(self, pref_dist):
        self.PREF_DIST = pref_dist
        self.pool = []
        self.found_paths = 0
        self.LEAVE_PATH_MARGIN = 0.9

