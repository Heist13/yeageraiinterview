import heapq


# Used to sort data centers in heap
def calculate_data_center_risk(base_risk: int, num_fragments: int) -> int:
    return base_risk ** num_fragments


def init_risk_heap(risk_factors: list[int], default_num_fragments: int = 1) -> list[tuple]:
    heap = []
    for risk in risk_factors:
        pair = (calculate_data_center_risk(risk, default_num_fragments), default_num_fragments, risk)
        heapq.heappush(heap, pair)
    return heap


def distribute_fragment(risk_heap: list[tuple]):
    current_risk, num_fragments, base_risk = heapq.heappop(risk_heap)
    new_risk = calculate_data_center_risk(base_risk, num_fragments + 1)
    heapq.heappush(risk_heap, (new_risk, num_fragments + 1, base_risk))


# O(NlogM) , where N = number of fragments, M = number of data centers (risk_factors length) - time complexity
# O(N) - space complexity (N number of data centers)
def find_minimized_max_risk(risk_factors: list[int], fragments_num: int) -> int:
    # Initialize the heap with 1 fragment for each data center
    heap = init_risk_heap(risk_factors)

    # Distribute the remaining fragments
    for _ in range(fragments_num - len(risk_factors)):
        distribute_fragment(heap)

    # Maximum risk after distribution
    return max(heap)[0]


data_centers = [10, 20, 30]
fragments = 5
assert 400 == find_minimized_max_risk(data_centers, fragments)

data_centers = list(range(10, 5000, 10))
fragments = 15
assert 4990 == find_minimized_max_risk(data_centers, fragments)

data_centers = [1]
fragments = 3
assert 1 == find_minimized_max_risk(data_centers, fragments)