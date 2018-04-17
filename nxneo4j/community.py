def triangles(G, nodes=None):
    triangles = G.triangles()

    if nodes:
        return {k: v for k, v in triangles.items() if k in nodes}

    return triangles


def clustering(G, nodes=None, weight=None):
    # doesn't currently support `weight`
    triangles = G.triangles()

    if nodes:
        return {k: v for k, v in triangles.items() if k in nodes}

    return G.clustering()


def average_clustering(G, nodes=None, weight=None, count_zeros=True):
    # doesn't currently support `nodes`, `weight`, `count_zeros`
    return G.average_clustering()


def label_propagation_communities(G):
    return G.label_propagation()


def connected_components(G):
    return G.connected_components()


def number_connected_components(G):
    return sum(1 for cc in connected_components(G))
