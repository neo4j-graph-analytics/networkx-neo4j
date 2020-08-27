"""Get Centrality related metrics
TEST SETUP
from neo4j import GraphDatabase
import nxneo4j as nx

driver = GraphDatabase.driver(uri="bolt://localhost",auth=("neo4j","neo"))
G = nx.Graph(driver)

G.delete_all()

data = [(1, 2),(2, 3),(3, 4)]
G.add_edges_from(data)
"""
# test only (import sys;sys.path.append("../"))  #the purpose is to reach to the parent directory
# to fix the default port run $kill $(lsof -ti:7687)
def betweenness_centrality(G, k=None, normalized=True, weight=None, endpoints=False, seed=None):
    # doesn't currently support `weight`, `k`, `endpoints`, `seed`

    """TEST OUTPUT
    nx.betweenness_centrality(G)
    networkx.betweenness_centrality(_G)
    """

    query = """\
    CALL gds.betweenness.stream({
        nodeProjection: $nodeLabel,
        relationshipProjection: {
            relType: {
                type: $relationshipType,
                orientation: $direction,
                properties: {}
                }
            }
        })
    YIELD nodeId, centrality
    RETURN gds.util.asNode(nodeId).%s AS node, centrality
    ORDER BY node ASC
    """ % G.identifier_property

    params = G.base_params()

    with G.driver.session() as session:
        result = {row["node"]: row["centrality"] for row in session.run(query, params)}
    return result



def closeness_centrality(G, u=None, distance=None, wf_improved=True, reverse=False):
    # doesn't currently supported `distance`, `reverse`, `wf_improved`
    """TEST OUTPUT
    nx.closeness_centrality(G)
    networkx.closeness_centrality(_G)
    """

    query = """\
    CALL gds.alpha.closeness.stream({
        nodeProjection: $nodeLabel,
        relationshipProjection: {
            relType: {
            type: $relationshipType,
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
    """TEST OUTPUT
    nx.pagerank(G)
    networkx.pagerank(_G)
    """

    query = """\
    CALL gds.pageRank.stream({
        nodeProjection: $nodeLabel,
        relationshipProjection: {
            relType: {
                type: $relationshipType,
                orientation: $direction,
                properties: {}
            }
        },
        relationshipWeightProperty: null,
        dampingFactor: $dampingFactor,
        maxIterations: $iterations
    })
    YIELD nodeId, score
    RETURN gds.util.asNode(nodeId).%s AS node, score
    ORDER BY node ASC
    """ % G.identifier_property

    params = G.base_params()
    params["iterations"] = max_iter
    params["dampingFactor"] = alpha

    with G.driver.session() as session:
        result = {row["node"]: row["score"] for row in session.run(query, params)}
    return result
