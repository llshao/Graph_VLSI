from queue import PriorityQueue


class Graph:
    def __init__(self, num_of_vertices):
        self.v = num_of_vertices
        #   adjacency matrix
        self.edges = [[-1 for i in range(num_of_vertices)] for j in range(num_of_vertices)]
        self.visited = []

    def add_edge(self, u, v, weight): # undirected
        self.edges[u][v] = weight
        self.edges[v][u] = weight

    @staticmethod  # Static method can be called without creating an object or instance.
    def dijkstra(graph, start_vertex):
        d = {v: float('inf') for v in range(graph.v)}
        d[start_vertex] = 0

        pq = PriorityQueue() # DFS search to go over all vertex
        pq.put((0, start_vertex)) # dist, current_vertex

        while not pq.empty(): # have to go over all vertex to find the shortest path
            (dist, current_vertex) = pq.get()
            graph.visited.append(current_vertex)
            print(current_vertex)
            print('\n')
            for neighbor in range(graph.v):
                if graph.edges[current_vertex][neighbor] != -1:  # checking the existence of edge
                    distance = graph.edges[current_vertex][neighbor]
                    if neighbor not in graph.visited:  # avoid circle and self-loop; also because using priorityqueue
                        #  can avoid visiting neighbors have been visited
                        old_cost = d[neighbor]
                        new_cost = d[current_vertex] + distance
                        if new_cost < old_cost:
                            pq.put((new_cost, neighbor))
                            d[neighbor] = new_cost
        return d
