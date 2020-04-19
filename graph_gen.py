import random, sys

def generate_graph(num_vertices):
    print(num_vertices)
    for i in range(num_vertices - 1):
        print(i, i + 1, round(random.uniform(0, 100), 3))
    for i in range(random.randrange(0, num_vertices)):
    	vertex1, vertex2 = random.randrange(0, num_vertices), random.randrange(0, num_vertices)
    	if vertex1 != vertex2 or vertex1 == vertex2 + 1 or vertex1 + 1 == vertex2:
    		print(vertex1, vertex2, round(random.uniform(0, 100), 3))

generate_graph(int(sys.argv[1]))
