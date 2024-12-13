"""
Descrete Math Laboratory Work №2
"""

import time


def read_file(filename: str) -> list[tuple]:
    """
    Function reads .dot file with graph
    and returns it as a list of edges.

    :param filename: str, name of .dot file
    :return: list[tuple], list of edges for the given graph
    >>> read_file('input.dot')
    [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]
    """
    with open(filename, "r", encoding="utf-8") as file:
        edges_list = []
        for line in file.readlines()[1:-1]:
            line = line.strip().split("->")
            edges_list.append((int(line[0].strip()), int(line[1].strip(";"))))
    return edges_list


def read_incidence_matrix(filename: str) -> list[list]:
    """
    :param str filename: path to file
    :returns list[list]: the incidence matrix of a given graph
    >>> read_incidence_matrix('input.dot')
    [[-1, 0, 1, 1, 0, -1], [0, -1, 0, -1, 1, 1], [1, 1, -1, 0, -1, 0]]
    """
    graph = read_file(filename)

    all_vertices = set()
    for v1, v2 in graph:
        all_vertices.add(v1)
        all_vertices.add(v2)
    matrix = [len(graph) * [0 * (len(graph))] for _ in range(1, len(all_vertices) + 1)]

    for i, edge in enumerate(graph):
        if edge[0] == edge[1]:
            matrix[edge[0] - 1][i] = 2
        else:
            matrix[edge[0] - 1][i] = 1
            matrix[edge[1] - 1][i] = -1

    return matrix


def read_adjacency_matrix(filename: str) -> list[list]:
    """
    :param str filename: path to file
    :returns list[list]: the adjacency matrix of a given graph
    >>> read_adjacency_matrix('input.dot')
    [[0, 1, 0], [1, 0, 0], [0, 0, 0]]
    """
    graph = read_file(filename)
    all_vertices = set()
    for v1, v2 in graph:
        all_vertices.add(v1)
        all_vertices.add(v2)

    matrix = [
        len(all_vertices) * [0 * (len(all_vertices))]
        for _ in range(1, len(all_vertices) + 1)
    ]

    for i, _ in enumerate(matrix):
        for j in range(len(matrix[i])):
            if (i + 1, j + 1) in graph:
                matrix[i][j] = 1
    return matrix


def read_adjacency_dict(filename: str) -> dict[int, list[int]]:
    """
    :param str filename: path to file
    :returns dict: the adjacency dict of a given graph
    >>> read_adjacency_dict('input.dot')
    {0: {1, 2}, 1: {0, 2}, 2: {0, 1}}
    """
    edges_list = read_file(filename)

    neighbour_vertex = {}
    for v1, v2 in edges_list:
        if v1 not in neighbour_vertex:
            neighbour_vertex.setdefault(v1, set())
        if v2 not in neighbour_vertex:
            neighbour_vertex.setdefault(v2, set())

        neighbour_vertex[v1].add(v2)
        neighbour_vertex[v2].add(v1)
    return neighbour_vertex


def iterative_adjacency_dict_dfs(graph: dict[int, list[int]], start: int) -> list[int]:
    """
    :param list[list] graph: the adjacency list of a given graph
    :param int start: start vertex of search
    :returns list[int]: the dfs traversal of the graph
    >>> iterative_adjacency_dict_dfs({0: [1, 2], 1: [0, 2], 2: [0, 1]}, 0)
    [0, 1, 2]
    >>> iterative_adjacency_dict_dfs({0: [1, 2], 1: [0, 2, 3], 2: [0, 1], 3: []}, 0)
    [0, 1, 2, 3]
    """
    visited = [False] * len(graph)
    component = []
    stack = [start]

    while stack:
        curr_vertice = stack.pop()
        visited[curr_vertice] = True
        if curr_vertice not in component:
            component.append(curr_vertice)
        for neighbour in reversed(list(graph.get(curr_vertice))):
            if visited[neighbour] is False:
                stack.append(neighbour)

    return component


def iterative_adjacency_matrix_dfs(graph: list[list], start: int) -> list[int]:
    """
    :param dict graph: the adjacency matrix of a given graph
    :param int start: start vertex of search
    :returns list[int]: the dfs traversal of the graph
    >>> iterative_adjacency_matrix_dfs([[0, 1, 1], [1, 0, 1], [1, 1, 0]], 0)
    [0, 1, 2]
    >>> iterative_adjacency_matrix_dfs([[0, 1, 1, 0], [1, 0, 1, 1], [1, 1, 0, 0], [0, 0, 0, 0]], 0)
    [0, 1, 2, 3]
    """
    vertices = [start]
    res = []
    visited = set()
    while vertices:
        curr_vertice = vertices.pop()
        if curr_vertice not in visited:
            visited.add(curr_vertice)
            res.append(curr_vertice)
            for i in range(len(graph[curr_vertice]) - 1, -1, -1):
                if graph[curr_vertice][i] == 1 and i not in visited:
                    vertices.append(i)
    return res


def recursive_adjacency_dict_dfs(graph: dict[int, list[int]], start: int) -> list[int]:
    """
    :param list[list] graph: the adjacency list of a given graph
    :param int start: start vertex of search
    :returns list[int]: the dfs traversal of the graph
    >>> recursive_adjacency_dict_dfs({0: [1, 2], 1: [0, 2], 2: [0, 1]}, 0)
    [0, 1, 2]
    >>> recursive_adjacency_dict_dfs({0: [1, 2], 1: [0, 2, 3], 2: [0, 1], 3: []}, 0)
    [0, 1, 2, 3]
    """
    visited = [False] * len(graph)
    res = []

    def dfs(node):
        visited[node] = True
        res.append(node)
        for neighbour in graph.get(node, []):
            if not visited[neighbour]:
                dfs(neighbour)

    dfs(start)
    return res


def recursive_adjacency_matrix_dfs(graph: list[list[int]], start: int) -> list[int]:
    """
    :param dict graph: the adjacency matrix of a given graph
    :param int start: start vertex of search
    :returns list[int]: the dfs traversal of the graph
    >>> recursive_adjacency_matrix_dfs([[0, 1, 1], [1, 0, 1], [1, 1, 0]], 0)
    [0, 1, 2]
    >>> recursive_adjacency_matrix_dfs([[0, 1, 1, 0], [1, 0, 1, 1], [1, 1, 0, 0], [0, 0, 0, 0]], 0)
    [0, 1, 2, 3]
    """
    visited = [False] * len(graph)
    res = []

    def dfs(node):
        visited[node] = True
        res.append(node)
        for neighbor, connected in enumerate(graph[node]):
            if connected == 1 and not visited[neighbor]:
                dfs(neighbor)

    dfs(start)
    return res


def iterative_adjacency_dict_bfs(graph: dict[int, list[int]], start: int) -> list[int]:
    """
    :param list[list] graph: the adjacency list of a given graph
    :param int start: start vertex of search
    :returns list[int]: the bfs traversal of the graph
    >>> iterative_adjacency_dict_bfs({0: [1, 2], 1: [0, 2], 2: [0, 1]}, 0)
    [0, 1, 2]
    >>> iterative_adjacency_dict_bfs({0: [1, 2], 1: [0, 2, 3], 2: [0, 1], 3: []}, 0)
    [0, 1, 2, 3]
    """
    visited = set()
    not_visited = [start]

    while not_visited:
        vertice = not_visited[0]
        if vertice not in visited:
            visited.add(vertice)
            for neighbour in graph.get(vertice):
                if neighbour not in visited:
                    not_visited.append(neighbour)
        not_visited.remove(vertice)
    return sorted(list(visited))


def iterative_adjacency_matrix_bfs(graph: list[list[int]], start: int) -> list[int]:
    """
    :param dict graph: the adjacency matrix of a given graph
    :param int start: start vertex of search
    :returns list[int]: the bfs traversal of the graph
    >>> iterative_adjacency_matrix_bfs([[0, 1, 1], [1, 0, 1], [1, 1, 0]], 0)
    [0, 1, 2]
    >>> iterative_adjacency_matrix_bfs([[0, 1, 1, 0], [1, 0, 1, 1], [1, 1, 0, 0], [0, 0, 0, 0]], 0)
    [0, 1, 2, 3]
    """
    visited = set()
    not_visited = [start]

    while not_visited:
        vertice = not_visited[0]
        if vertice not in visited:
            visited.add(vertice)
            for neighbour in range(len(graph)):
                if graph[vertice][neighbour] == 1 and neighbour not in visited:
                    not_visited.append(neighbour)
        not_visited.remove(vertice)
    return sorted(list(visited))


def adjacency_matrix_radius(graph: list[list]) -> int:
    """
    :param list[list] graph: the adjacency matrix of a given graph
    :returns int: the radius of the graph
    >>> adjacency_matrix_radius([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
    1
    """
    distance = [[float("inf")] * len(graph) for _ in range(len(graph))]
    for i, row in enumerate(graph):
        for j, value in enumerate(row):
            if i == j:
                distance[i][j] = 0
            elif value == 1:
                distance[i][j] = 1

    for k in range(len(graph)):
        for i in range(len(graph)):
            for j in range(len(graph)):
                distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])

    eccentr = [max(row) for row in distance]
    radius = min(eccentr)
    return radius


def adjacency_dict_radius(graph: dict[int : list[int]]) -> int:
    """
    :param dict graph: the adjacency list of a given graph
    :returns int: the radius of the graph
    >>> adjacency_dict_radius({0: [1, 2], 1: [0, 2], 2: [0, 1]})
    1
    >>> adjacency_dict_radius({0: [1, 2], 1: [0, 2], 2: [0, 1], 3: [1]})
    2
    """
    distance = [[float("inf")] * len(graph) for _ in range(len(graph))]
    for vertice, neighbours in graph.items():
        distance[vertice][vertice] = 0
        for n in neighbours:
            distance[vertice][n] = 1

    for k in range(len(graph)):
        for i in range(len(graph)):
            for j in range(len(graph)):
                distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])

    eccentr = []
    for i in range(len(graph)):
        max_dist = max(distance[i])
        if max_dist != float("inf"):
            eccentr.append(max_dist)
    radius = min(eccentr)
    return radius


def find_function_runtime(
    func, path=None, matrix=None, start_point=0, dictionary=None
) -> float:
    """
    Returns the runtime of the function

    :param func: callable, The function to check
    :param graph: list, The graph that function will work with
    :return: float, The runtime of the function
    """
    begin = time.perf_counter()
    if path is not None:
        func(path)
    elif matrix is not None:
        func(matrix, start_point)
    elif dictionary is not None:
        func(dictionary, start_point)
    time.sleep(1)
    end = time.perf_counter()
    return end - begin


# print(find_function_runtime(read_incidence_matrix, path='input.dot'))
# print(find_function_runtime(read_adjacency_dict, path='input.dot'))
# print(find_function_runtime(read_adjacency_matrix, path='input.dot'))


if __name__ == "__main__":
    import doctest

    print(doctest.testmod())
