"""Get Community related metrics
TEST SETUP
from neo4j import GraphDatabase
import nxneo4j as nx

driver = GraphDatabase.driver(uri="bolt://localhost",auth=("neo4j","neo"))
G = nx.Graph(driver)

G.delete_all()

data = [(1, 2),(2, 3),(3, 4)]
G.add_edges_from(data)
"""

def triangles(G, nodes=None):
    query = """\
    CALL gds.alpha.triangleCount.stream({
        nodeProjection: $nodeLabel,
        relationshipProjection: {
            relType: {
            type: $relationshipType,
            orientation: $direction,
            properties: {}
            }
    }})
    YIELD nodeId, triangles, coefficient
    RETURN gds.util.asNode(nodeId).%s AS node, triangles, coefficient
    ORDER BY node ASC""" % G.identifier_property

    params = G.base_params()

    with G.driver.session() as session:
        result = {row["node"]: row["triangles"] for row in session.run(query, params)}

    if nodes:
        return {k: v for k, v in result.items() if k in nodes}
    return result

    """TEST OUTPUT
    nx.triangles(G)
    networkx.triangles(_G)
    """

def clustering(G, nodes=None, weight=None):
    # doesn't currently support `weight`
    query = """\
    CALL gds.alpha.triangleCount.stream({
        nodeProjection: $nodeLabel,
        relationshipProjection: {
            relType: {
            type: $relationshipType,
            orientation: $direction,
            properties: {}
            }
    }})
    YIELD nodeId, triangles, coefficient
    RETURN gds.util.asNode(nodeId).%s AS node, triangles, coefficient
    ORDER BY coefficient DESC""" % G.identifier_property

    params = G.base_params()

    with G.driver.session() as session:
        result = {row["node"]: row["coefficient"] for row in session.run(query, params)}
    return result

    """TEST OUTPUT
    nx.clustering(G)
    networkx.clustering(_G)
    """


def label_propagation_communities(G):

    query = """\
    CALL gds.labelPropagation.stream({
        nodeProjection: $nodeLabel,
        relationshipProjection: {
            relType: {
                type: $relationshipType,
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

    """TEST OUTPUT
    nx.label_propagation_communities(G)
    networkx.networkx.algorithms.community.label_propagation.label_propagation_communities(_G)
    """


def connected_components(G):

    query = """\
    CALL gds.wcc.stream({
        nodeProjection: 'Node',
        relationshipProjection: {
            relType: {
            type: 'CONNECTED',
            orientation: 'UNDIRECTED',
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

    """TEST OUTPUT
    nx.connected_components(G)
    nx.number_connected_components(G)
    """
