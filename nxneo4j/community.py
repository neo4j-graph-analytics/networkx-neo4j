def triangles(G, nodes=None):
    query = """\
    CALL gds.triangleCount.stream({
        nodeProjection: $node_label,
        relationshipProjection: {
            relType: {
            type: $relationship_type,
            orientation: $direction,
            properties: {}
            }
    }})
    YIELD nodeId, triangleCount
    RETURN gds.util.asNode(nodeId).%s AS node, triangleCount
    ORDER BY node ASC""" % G.identifier_property

    params = G.base_params()

    with G.driver.session() as session:
        result = {row["node"]: row["triangleCount"] for row in session.run(query, params)}

    if nodes:
        return {k: v for k, v in result.items() if k in nodes}
    return result

def clustering(G, nodes=None, weight=None):
    # doesn't currently support `weight`
    query = """\
    CALL gds.localClusteringCoefficient.stream({
        nodeProjection: $node_label,
        relationshipProjection: {
            relType: {
            type: $relationship_type,
            orientation: $direction,
            properties: {}
            }
    }})
    YIELD nodeId, localClusteringCoefficient
    RETURN gds.util.asNode(nodeId).%s AS node, localClusteringCoefficient
    ORDER BY localClusteringCoefficient DESC""" % G.identifier_property

    params = G.base_params()

    with G.driver.session() as session:
        result = {row["node"]: row["localClusteringCoefficient"] for row in session.run(query, params)}
    return result

def label_propagation_communities(G):

    query = """\
    CALL gds.labelPropagation.stream({
        nodeProjection: $node_label,
        relationshipProjection: {
            relType: {
                type: $relationship_type,
                orientation: $direction,
                properties: {}
            }
        },
        relationshipWeightProperty: null
    })
    YIELD nodeId, communityId AS community
    MATCH (n) WHERE id(n) = nodeId
    RETURN community, collect(n.%s) AS nodes
    """ % G.identifier_property

    params = G.base_params()

    with G.driver.session() as session:
        for row in session.run(query, params):
            yield set(row["nodes"])

def connected_components(G):

    query = """\
    CALL gds.wcc.stream({
        nodeProjection: $node_label,
        relationshipProjection: {
            relType: {
            type: $relationship_type,
            orientation: $direction,
            properties: {}
        }
      }
    })
    YIELD nodeId, componentId AS community
    MATCH (n) WHERE id(n) = nodeId
    RETURN community, collect(n.%s) AS nodes
    ORDER BY community DESC
    """ % G.identifier_property

    params = G.base_params()

    with G.driver.session() as session:
        for row in session.run(query, params):
            yield set(row["nodes"])

def number_connected_components(G):
    return sum(1 for cc in connected_components(G))
