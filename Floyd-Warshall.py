import random
import networkx as nx
import matplotlib.pyplot as plt
import time
from statistics import mean


def random_graph(vertices_count: int, edges_count: int) -> nx.Graph:
    """
    Function that generate random weighted graph with input count of vertices and edges

    :param vertices_count: vertices count
    :param edges_count: edges count
    :type vertices_count: int
    :type edges_count: int
    :return: generated weighted graph
    :rtype: nx.Graph
    """

    if edges_count > vertices_count ** 2 / 2:
        raise ValueError("Edges count must be less then vertices count ^ 2 / 2")

    if edges_count < vertices_count:
        raise ValueError("Vertices count must be bigger then edges count")

    result = nx.Graph()

    for i in range(vertices_count):
        result.add_node(i)

    possible_vertices_in_matrix = [elem for elem in range(vertices_count ** 2) if elem // vertices_count < elem % vertices_count]

    for row in range(vertices_count - 1):
        column = random.randint(row + 1, vertices_count - 1)

        result.add_edge(row, column, weight=random.randint(1, 100))

        possible_vertices_in_matrix.remove(row * vertices_count + column)

    edges_left = edges_count - vertices_count

    random_vertices = random.sample(possible_vertices_in_matrix, edges_left)

    for elem in random_vertices:
        result.add_edge(elem // vertices_count, elem % vertices_count, weight=random.randint(1, 100))

    return result


# Graph generating
my_vertices_count = 20
my_edges_count = 74

my_graph = random_graph(my_vertices_count, my_edges_count)

# Example of using method
results = {a: dict(b) for a, b in nx.floyd_warshall(my_graph).items()}
for key, value in results.items():
    print(f"{key}: {dict(sorted(value.items(), key=lambda elem: elem[0]))}")
print()

edge_labels = dict([((u, v,), d['weight'])for u, v, d in my_graph.edges(data=True)])
nx.draw(my_graph, pos=nx.shell_layout(my_graph), with_labels=True, font_size=10, font_color='white',
        node_size=600)
nx.draw_networkx_edge_labels(my_graph, pos=nx.shell_layout(my_graph), edge_labels=edge_labels, font_size=5)
plt.show()

# Algorithm researching
prims_times = []

for _ in range(10):
    current_root = random.randint(0, my_vertices_count - 1)
    start_time = time.perf_counter()
    nx.floyd_warshall(my_graph)
    end_time = time.perf_counter()
    prims_times.append(end_time - start_time)

print(f"Average method's time: {mean(prims_times)}s")