def betweenness_centrality(G, k=None, normalized=True, weight=None,
                           endpoints=False, seed=None):
    # doesn't currently support `weight`, `k`, `endpoints`, `seed`
    return G.betweenness_centrality()


def closeness_centrality(G, u=None, distance=None,
                         wf_improved=True, reverse=False):
    # doesn't currently supported `distance`, `reverse`
    centralities = G.closeness_centrality(wf_improved)

    if u:
        return centralities[u]

    return centralities


def harmonic_centrality(G, nbunch=None, distance=None):
    # doesn't currently support `distance`
    centralities = G.harmonic_centrality()

    if nbunch:
        return {k: v for k, v in centralities.items() if k in nbunch}

    return centralities


def pagerank(G, alpha=0.85, personalization=None,
             max_iter=100, tol=1.0e-8, nstart=None, weight='weight'):
    # doesn't currently supported `personalization`, `tol`, `nstart`, `weight`
    return G.pagerank(alpha, max_iter)
