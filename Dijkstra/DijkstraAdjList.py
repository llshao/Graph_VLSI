from collections import defaultdict
#  from queue import PriorityQueue
from heapq import heappush, heappop

class Graph:
    def __init__(self, num_of_vertices):
        self.v = num_of_vertices
        #   adjacency list
        self.adjlist = defaultdict(dict)
        self.visited = []

    def add_edge(self, u, v, weight):
        self.adjlist[u][v] = weight
        self.adjlist[v][u] = weight

    @staticmethod  # Static method can be called without creating an object or instance.
    def dijkstra(graph, start_vertex):
        d = {v: float('inf') for v in range(graph.v)}
        d[start_vertex] = 0

        pq = []  # DFS search to go over all vertex
        heappush(pq, (0, start_vertex))  # dist, current_vertex

        while len(pq) != 0:   # have to go over all vertex to find the shortest path
            (dist, current_vertex) = heappop(pq)
            graph.visited.append(current_vertex)
            print(current_vertex)
            print('\n')
            for neighbor in graph.adjlist[current_vertex].keys():
                if neighbor not in graph.visited:  # avoid circle and self-loop; also because using priorityqueue
                    #  can avoid visiting neighbors have been visited
                    distance = graph.adjlist[current_vertex][neighbor]
                    old_cost = d[neighbor]
                    new_cost = d[current_vertex] + distance
                    if new_cost < old_cost:
                        heappush(pq, (new_cost, neighbor))
                        d[neighbor] = new_cost
        return d
