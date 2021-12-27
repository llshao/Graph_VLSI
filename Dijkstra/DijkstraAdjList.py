from builtins import staticmethod
from collections import defaultdict, OrderedDict
#  from queue import PriorityQueue
from heapq import heappush, heappop

IDX_X, IDX_Y, IDX_SEG, IDX_TOP, IDX_BOT = 0, 1, 2, 3, 4

class Graph:
    def __init__(self, num_of_vertices):
        self.v = num_of_vertices
        #   adjacency list
        self.adjlist = defaultdict(dict)
        self.visited = []

    def add_edge(self, u, v, weight=1, directed=True):  # default directed & unweighted
        self.adjlist[u][v] = weight
        if not directed:
            self.adjlist[v][u] = weight

    @staticmethod
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

    @staticmethod
    def build_vcg(vcg, segs):  # build vertical constraint graph based on given list of segs
        #   segs =[(x1,y1,idx1), (x2,y1,idx1)]
        segs_sorted = sorted(segs, key=lambda x: x[IDX_X])  # sort the dict by the x coord
        scan_dict = {}
        scan_list_sorted = []
        # add top & bottom
        bx, by = segs_sorted[0][IDX_X]-1, min([i[IDX_Y] for i in segs_sorted])-1
        bx1, by = segs_sorted[-1][IDX_X]+1, min([i[IDX_Y] for i in segs_sorted])-1
        tx, ty = bx, max([i[IDX_Y] for i in segs_sorted])+1
        tx1, ty = bx1, max([i[IDX_Y] for i in segs_sorted])+1
        # put the start point of bottom and top in to a scan_dict
        scan_dict.update({'bottom': [bx, by, 'bottom', 'top', None], 'top': [tx, ty, 'top', None, 'bottom']})
        scan_list_sorted += [(bx, by, 'bottom'), (tx, ty, 'top')]
        # append end points of bottom and top to the sorted list
        segs_sorted.append((bx1, by, 'bottom'))
        segs_sorted.append((tx1, ty, 'top'))
        #   init idx and curr_x
        curr_idx = 0
        while curr_idx < len(segs_sorted):  # get next curr_x & idx
            curr_seg = segs_sorted[curr_idx]  # get a tuple(x,y,seg_name)
            if curr_seg[IDX_SEG] not in scan_dict:  # start point
                # locating curr_seg's neighbor based on y coord
                scan_list_sorted, t, b = vcg.get_neighbors(scan_list_sorted, curr_seg)
                # update the top & bot neighbor of current seg
                scan_dict.update({curr_seg[IDX_SEG]: [curr_seg[IDX_X], curr_seg[IDX_Y], curr_seg[IDX_SEG],
                                                      scan_list_sorted[t][IDX_SEG], scan_list_sorted[b][IDX_SEG]]})
                # update the bot of the top neighbor
                top_key, top_value = scan_list_sorted[t][IDX_SEG], scan_dict[scan_list_sorted[t][IDX_SEG]]
                top_value[IDX_BOT] = curr_seg[IDX_SEG]
                scan_dict.update({top_key: top_value})
                # update the top of the bot neighbor
                bot_key, bot_value = scan_list_sorted[b][IDX_SEG], scan_dict[scan_list_sorted[b][IDX_SEG]]
                bot_value[IDX_TOP] = curr_seg[IDX_SEG]
                scan_dict.update({bot_key: bot_value})
            else:  # end point
                # check the existence of top & bottom
                if scan_dict[curr_seg[IDX_SEG]][IDX_TOP] in scan_dict:
                    vcg.add_edge(scan_dict[curr_seg[IDX_SEG]][IDX_TOP], curr_seg[IDX_SEG])
                if scan_dict[curr_seg[IDX_SEG]][IDX_BOT] in scan_dict:
                    vcg.add_edge(curr_seg[IDX_SEG], scan_dict[curr_seg[IDX_SEG]][IDX_BOT])
                # remove from scan_dict & scan_list_sorted
                scan_dict.pop(curr_seg[IDX_SEG], None)
                scan_list_sorted = [i for i in scan_list_sorted if i[IDX_SEG] != curr_seg[IDX_SEG]]
            # update index
            curr_idx += 1
        return vcg

    @staticmethod
    def get_neighbors(scan_list_sorted: list, curr_seg: tuple) -> (list, int):
        #   get neighbors for current seg and get the index for it
        #  because we use the scanline + jump(start & end points), only 1 bot & 1 top
        scan_list_sorted.append(curr_seg)
        index = -1
        while curr_seg[IDX_Y] < scan_list_sorted[index-1][IDX_Y]:  # find top
            scan_list_sorted[index] = scan_list_sorted[index-1]
            index -= 1
        scan_list_sorted[index] = curr_seg
        top = index + 1
        while curr_seg[IDX_Y] <= scan_list_sorted[index][IDX_Y]:  # find bot
            index -= 1
        bot = index
        return scan_list_sorted, top, bot


