from builtins import staticmethod
from collections import defaultdict, OrderedDict
#  from queue import PriorityQueue
from heapq import heappush, heappop


class Graph:
    def __init__(self, num_of_vertices):
        self.v = num_of_vertices
        #   adjacency list
        self.adjlist = defaultdict(dict)
        self.visited = []

    def add_edge(self, u, v, weight):  # directed
        self.adjlist[u][v] = weight
        # self.adjlist[v][u] = weight

    @staticmethod  # Static method can be called without creating an object or instance.
    def dijkstra(graph, start_vertex):
        key_list = [k for k in graph.adjlist.keys()]
        value_list = [j for v in graph.adjlist.values() for j in v.keys()]
        d = {v: float('inf') for v in (set(key_list) | set(value_list))}  # Union keys & values
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


def build_vcg(vcg: Graph, segs: list) -> Graph:  # build vertical constraint graph based on given list of segs
    #   segs =[(x1,y1,idx1),(x2,y1,idx1)}
    segs_sorted = sorted(segs, key=lambda x: x[0])  # sort the dict by the x coord
    scan_list = {}
    # add top & bottom
    bx, by = segs_sorted[0][0]-1, min([i[1] for i in segs_sorted])-1
    bx1, by = segs_sorted[-1][0]+1, min([i[1] for i in segs_sorted])-1
    tx, ty = bx, max([i[1] for i in segs_sorted])+1
    tx1, ty = bx1, max([i[1] for i in segs_sorted])+1
    # put the start point of bottom and top in to a scan_list
    scan_list.update({'bottom': (bx, by), 'top': (tx, ty)})
    # append end points of bottom and top to the sorted list
    segs_sorted.append((bx1, by, 'bottom'))
    segs_sorted.append((tx1, ty, 'top'))
    #   init idx and curr_x
    curr_idx = 0
    while curr_idx < len(segs_sorted):  # get next curr_x & idx
        curr_seg = segs_sorted[curr_idx]  # get a tuple(x,y,seg_name)
        if curr_seg[2] not in scan_list:  # start point
            # add constraints / edges by locating curr_seg's neighbor based on y coord
            i = 0
            scan_list_sorted = sorted(scan_list.items(), key=lambda x: x[1][1])  # sort by y ascending
            while scan_list_sorted[i][1][1] < curr_seg[1]:  # find bottom neighbor
                i += 1
            b = i - 1
            while scan_list_sorted[i][1][1] <= curr_seg[1]:  # find top neighbor
                i += 1
            t = i
            vcg.add_edge(curr_seg[2], scan_list_sorted[b][0], 1)  # add bottom
            vcg.add_edge(scan_list_sorted[t][0], curr_seg[2], 1)  # add top
            # put into a y-sorted dict
            scan_list.update({curr_seg[2]: (curr_seg[0], curr_seg[1])})
        else:  # end point
            # remove from scan_list
            scan_list.pop(curr_seg[2], None)
        # update index
        curr_idx += 1
    return vcg

