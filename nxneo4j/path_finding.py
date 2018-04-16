def shortest_path(G, source=None, target=None, weight=None):
    if source is None:
        if target is None:
            # Find paths between all pairs.
            if weight is None:
                # paths = dict(nx.all_pairs_shortest_path(G))
                paths = {}
            else:
                # paths = dict(nx.all_pairs_dijkstra_path(G, weight=weight))
                paths = {}
        else:
            # Find paths from all nodes co-accessible to the target.
            if weight is None:
                # paths = nx.single_source_shortest_path(G, target)
                # paths = G.single_source_shortest_path(target)
                paths = []
            else:
                # paths = nx.single_source_dijkstra_path(G, target,
                #                                        weight=weight)
                paths = []
    else:
        if target is None:
            # Find paths to all nodes accessible from the source.
            if weight is None:
                # paths = nx.single_source_shortest_path(G, source)
                paths = []
                # paths = G.single_source_shortest_path(source)
            else:
                # paths = nx.single_source_dijkstra_path(G, source,
                #                                        weight=weight)
                paths = []
        else:
            # Find shortest source-target path.
            if weight is None:
                paths = G.shortest_path(source, target)
            else:
                paths = G.shortest_weighted_path(source, target, weight)

    return paths
