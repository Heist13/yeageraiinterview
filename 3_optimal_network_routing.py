import heapq
from typing import Dict, List, Tuple

# I will implement Dijkstra for getting lowest cost path from source to target, using the latency as distance
# Time complexity: O( (E+V) * logV) - E number of connections between routers, V - number of routers
# Space: O(V)

Graph = Dict[str, List[Tuple[str, int]]]
LatencyMap = Dict[str, Tuple[int, int]]


def calculate_new_latency(current_latency: int, edge_latency: int, compression_used: bool, compressible: bool) -> Tuple[
    int, bool]:
    if compressible and not compression_used:
        return current_latency + edge_latency // 2, True
    return current_latency + edge_latency, compression_used


def initialize_min_latency(graph: Graph) -> LatencyMap:
    inf = float('inf')
    return {node: (inf, inf) for node in graph}


def update_priority_queue(
        pq: list[tuple], min_latency: LatencyMap,
        neighbor: str, new_latency: int, compression_used: bool) -> None:
    if new_latency < min_latency[neighbor][compression_used]:
        if compression_used:
            min_latency[neighbor] = (min_latency[neighbor][0], new_latency)
        else:
            min_latency[neighbor] = (new_latency, min_latency[neighbor][1])
        heapq.heappush(pq, (new_latency, neighbor, compression_used))


def find_minimum_latency_path(graph: Graph, compression_nodes: List[str], source: str, destination: str) -> int:
    pq: list[tuple] = [(0, source, False)]
    min_latency = initialize_min_latency(graph)
    min_latency[source] = 0

    while pq:
        current_latency, current_node, compression_used = heapq.heappop(pq)
        if current_node == destination:
            return min(current_latency, min_latency[destination][1])

        for neighbor, latency in graph[current_node]:
            compressible = current_node in compression_nodes
            for apply_compression in [False, True]:
                if apply_compression and compression_used:
                    # Compression is already applied
                    continue

                new_latency, new_compression_used = calculate_new_latency(
                    current_latency, latency, compression_used, compressible and apply_compression
                )
                update_priority_queue(pq, min_latency, neighbor, new_latency, new_compression_used)

    min_latency_val = min(min_latency[destination])
    if min_latency_val == float("inf"):
        raise ValueError("No path available")

    return min_latency_val


graph = {
    'A': [('B', 10), ('C', 20)],
    'B': [('D', 15)],
    'C': [('D', 30)],
    'D': []
}
compression_nodes = ['B', 'C']
source, destination = 'A', 'D'
min_latency = find_minimum_latency_path(graph, compression_nodes, source, destination)
assert 17 == min_latency

# No compression nodes
graph = {
    'A': [('B', 10), ('C', 20)],
    'B': [('D', 15)],
    'C': [('D', 30)],
    'D': []
}
compression_nodes = []
source, destination = 'A', 'D'
min_latency = find_minimum_latency_path(graph, compression_nodes, source, destination)
assert 25 == min_latency

# No path
graph = {
    'A': [('B', 10)],
    'B': [],
    'C': [('D', 10)],
    'D': []
}
compression_nodes = ['B', 'C']
source, destination = 'A', 'D'
try:
    min_latency = find_minimum_latency_path(graph, compression_nodes, source, destination)
except ValueError as e:
    assert str(e) == "No path available"

# Ignore destination for compression (Destination is the only compression node)
graph = {
    'A': [('B', 10)],
    'B': [('C', 10)],
    'C': []
}
compression_nodes = ['C']
source, destination = 'A', 'C'
min_latency = find_minimum_latency_path(graph, compression_nodes, source, destination)
assert 20 == min_latency

print("Test passed")
