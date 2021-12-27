# This is a sample Python script.

# from DijkstraAdjMatrix import Graph
from DijkstraAdjList import Graph
# Press the green button in the gutter to run the script.
__name__ = '__test_vcg__'
# __name__ = '__test_Dijkstra__'

if __name__ == '__test_vcg__':
    input_tuple = [(1, 1, 'a'), (4, 1, 'a'), (2, 2, 'b'), (5, 2, 'b'),
                   (3, 3, 'c'), (6, 3, 'c'), (5, 4, 'd'), (7, 4, 'd'),
                   (1, 5, 'e'), (4, 5, 'e'), (7, 5, 'f'), (9, 5, 'f')]
    # --e--  --f--
    #    --d--
    #   --c--
    #  --b--
    # --a--
    vcg = Graph(len(input_tuple)//2+2)
    vcg = Graph.build_vcg(vcg, input_tuple)
    D = Graph.dijkstra(vcg, 'top')
    key_list = [k for k in vcg.adjlist.keys()]
    value_list = [j for v in vcg.adjlist.values() for j in v.keys()]
    for vertex in (set(key_list) | set(value_list)):
        print("Distance from vertex top to vertex", vertex, "is", D[vertex])
    print(vcg.adjlist)


if __name__ == '__test_Dijkstra__':
    #  CASE 1
    g = Graph(3)
    g.add_edge(0,1,1)
    g.add_edge(0,2,3)
    g.add_edge(1,2,1)
    #  CASE 2
    # g = Graph(9)
    # g.add_edge(0, 1, 4)
    # g.add_edge(0, 6, 7)
    # g.add_edge(1, 6, 11)
    # g.add_edge(1, 7, 20)
    # g.add_edge(1, 2, 9)
    # g.add_edge(2, 3, 6)
    # g.add_edge(2, 4, 2)
    # g.add_edge(3, 4, 10)
    # g.add_edge(3, 5, 5)
    # g.add_edge(4, 5, 15)
    # g.add_edge(4, 7, 1)
    # g.add_edge(4, 8, 5)
    # g.add_edge(5, 8, 12)
    # g.add_edge(6, 7, 1)
    # g.add_edge(7, 8, 3)
    D = Graph.dijkstra(g, 0)

    for vertex in range(len(D)):
        print("Distance from vertex 0 to vertex", vertex, "is", D[vertex])
    # {0: 0, 1: 4, 2: 11, 3: 17, 4: 9, 5: 22, 6: 7, 7: 8, 8: 11}

