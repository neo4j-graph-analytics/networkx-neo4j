__all__ = ['betweenness_centrality']


def betweenness_centrality(G, k=None, normalized=True, weight=None,
                           endpoints=False, seed=None):
    # doesn't currently support `weight`, `k`, `endpoints`, `seed`
    return G.betweenness_centrality()
