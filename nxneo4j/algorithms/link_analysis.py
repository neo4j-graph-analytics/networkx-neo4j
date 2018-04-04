def pagerank(G, alpha=0.85, personalization=None,
             max_iter=100, tol=1.0e-8, nstart=None, weight='weight'):
    # doesn't currently supported `personalization`, `tol`, `nstart`, `weight`
    return G.pagerank(alpha, max_iter)
