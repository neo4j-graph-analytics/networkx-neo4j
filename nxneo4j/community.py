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
