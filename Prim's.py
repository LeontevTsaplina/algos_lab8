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


def from_graph_to_adjacency_list(graph: nx.Graph) -> dict:
    """
    Function that translate nx.Graph into adjacency list elements like edge1: [(edge1, edgen, weigth), ...]

    :param graph: input graph
    :type graph: nx.Graph
    :return: adjacency list of input graph
    :rtype: dict
    """

    result = {}
    edges = graph.edges(data=True)

    for edge in edges:
        e1 = edge[0]
        e2 = edge[1]
        w = edge[2]['weight']

        result[e1] = result.get(e1, [])
        result[e2] = result.get(e2, [])

        result[e1].append((e1, e2, w))
        result[e2].append((e2, e1, w))

    return result


def prims(graph: nx.Graph, root: int = 0) -> tuple:
    """
    Function of using Prim's method to find Minimum Spanning Trees

    :param graph: input graph
    :param root: root of tree
    :type graph: nx.Graph
    :type root: int
    :return: weights sum of Minimum Spanning Trees, list of edges of Minimum Spanning Trees
    :rtype: tuple
    """

    result = []
    weights_sum = 0
    visited = [root]
    adjacency_list = from_graph_to_adjacency_list(graph)

    adjacent_vertexs_edges = adjacency_list[root]

    while adjacent_vertexs_edges:
        e1, e2, w = min(adjacent_vertexs_edges, key=lambda el: el[2])
        adjacent_vertexs_edges.remove((e1, e2, w))

        if e2 not in visited:
            visited.append(e2)
            result.append((e1, e2))
            weights_sum = w

            for next_edge in adjacency_list[e2]:
                if next_edge[2] not in visited:
                    adjacent_vertexs_edges.append(next_edge)

    return weights_sum, result


# Graph generating
my_vertices_count = 20
my_edges_count = 37

my_graph = random_graph(my_vertices_count, my_edges_count)

# Example of using method
edge_labels = dict([((u, v,), d['weight'])for u, v, d in my_graph.edges(data=True)])
nx.draw(my_graph, pos=nx.shell_layout(my_graph), with_labels=True, font_size=10, font_color='white',
        node_size=600)
nx.draw_networkx_edge_labels(my_graph, pos=nx.shell_layout(my_graph), edge_labels=edge_labels, font_size=5)
plt.show()

weight_sum, min_tree_edges = prims(my_graph)
print(f"Weights sum of Minimum Spanning Trees of my graph: {weight_sum}")
edges = my_graph.edges

print(f"Minimum Spanning Trees of my graph: {min_tree_edges}", '\n')

edges_colors = []

for edge in edges:
    if edge in min_tree_edges or (edge[1], edge[0]) in min_tree_edges:
        edges_colors.append('red')
    else:
        edges_colors.append((0, 0, 0, 0.1))

nx.draw(my_graph, pos=nx.shell_layout(my_graph), with_labels=True, font_size=10, font_color='white',
        node_size=600, edge_color=edges_colors)
nx.draw_networkx_edge_labels(my_graph, pos=nx.shell_layout(my_graph), edge_labels=edge_labels, font_size=5)
plt.show()


# Algorithm researching
prims_times = []

for _ in range(10):
    current_root = random.randint(0, my_vertices_count - 1)

    start_time = time.perf_counter()
    prims(my_graph, current_root)
    end_time = time.perf_counter()

    prims_times.append(end_time - start_time)

print(f"Average method's time: {mean(prims_times)}s")
