def closeness_centrality(G, u=None, distance=None,
                         wf_improved=True, reverse=False):
    closeness_centralities = G.closeness_centrality(wf_improved)

    if u:
        return closeness_centralities[u]

    return closeness_centralities


def betweenness_centrality(G):
    return G.betweenness_centrality()
