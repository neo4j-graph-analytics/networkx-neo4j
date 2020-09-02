def betweenness_centrality(G, k=None, normalized=True, weight=None, endpoints=False, seed=None):
    # doesn't currently support `weight`, `k`, `endpoints`, `seed`

    query = """\
    CALL gds.betweenness.stream({
        nodeProjection: $node_label,
        relationshipProjection: {
            relType: {
                type: $relationship_type,
                orientation: $direction,
                properties: {}
                }
            }
        })
    YIELD nodeId, score
    RETURN gds.util.asNode(nodeId).%s AS node, score
    ORDER BY node ASC
    """ % G.identifier_property

    params = G.base_params()

    with G.driver.session() as session:
        result = {row["node"]: row["score"] for row in session.run(query, params)}
    return result



def closeness_centrality(G, u=None, distance=None, wf_improved=True, reverse=False):
    # doesn't currently supported `distance`, `reverse`, `wf_improved`

    query = """\
    CALL gds.alpha.closeness.stream({
        nodeProjection: $node_label,
        relationshipProjection: {
            relType: {
            type: $relationship_type,
            orientation: $direction,
            properties: {}
        }
    }})
    YIELD nodeId, centrality
    RETURN gds.util.asNode(nodeId).%s AS node, centrality
    ORDER BY node ASC
    """ % G.identifier_property

    params = G.base_params()

    with G.driver.session() as session:
        result = {row["node"]: row["centrality"] for row in session.run(query, params)}
    if u:
        return result[u]
    return result



def pagerank(G, alpha=0.85, personalization=None,  max_iter=100, tol=1.0e-8, nstart=None, weight='weight'):
    # doesn't currently supported `personalization`, `tol`, `nstart`, `weight`

    query = """\
        CALL gds.pageRank.stream({
          nodeProjection: $node_label,
          relationshipProjection: {
            relType: {
              type: $relationship_type,
              orientation: $direction,
              properties: {}
            }
          },
          relationshipWeightProperty: null,
          dampingFactor: $dampingFactor,
          maxIterations: $iterations
        }) YIELD nodeId, score
        WITH gds.util.asNode(nodeId).%s AS node, score
        RETURN node, score
        """ % G.identifier_property


    params = G.base_params()
    params["iterations"] = max_iter
    params["dampingFactor"] = alpha

    with G.driver.session() as session:
        result = {row["node"]: row["score"] for row in session.run(query, params)}
    return result
