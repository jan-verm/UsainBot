import route
import random

routeGen = route.Route(pool_size=5, nr_mutants=1, nr_of_attempts=1000, max_length_path=10)
routeGen.import_file('../../maps/waterloo_small.osm')

start_node = random.choice(list(routeGen.map.nodes()))
print('initial start node: '+str(start_node))
routeGen.setup_initial_pool(start_node)
print(routeGen.pool)

routeGen.mutation()
print(routeGen.pool)