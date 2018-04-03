def closeness_centrality(G, u=None, distance=None,
                         wf_improved=True, reverse=False):
    # doesn't currently supported `distance` or `reverse`
    centralities = G.closeness_centrality(wf_improved)

    if u:
        return centralities[u]

    return centralities


def betweenness_centrality(G, k=None, normalized=True, weight=None,
                           endpoints=False, seed=None):
    # doesn't currently support `weight`
    return G.betweenness_centrality()
