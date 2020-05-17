"""TEST SETUP
import sys
sys.path.append("../")  #included to reach to the parent directory

from neo4j import GraphDatabase
import nxneo4j as nx

# to fix the default port run $kill $(lsof -ti:7687) OR

driver = GraphDatabase.driver(uri="bolt://localhost",auth=("neo4j","neo"))
G = nx.Graph(driver)

G.delete_all()

data = [(1, 2),(2, 3),(3, 4)]
G.add_edges_from(data)

import networkx
_G = networkx.Graph()
_G.add_edges_from(data)
"""

def shortest_weighted_path(G,source, target, weight):
    if source is None:
        if target is None:
            # Find paths between all pairs.
            if weight is None:
                # paths = dict(nx.all_pairs_shortest_path(G))
                paths = {}
            else:
                # paths = dict(nx.all_pairs_dijkstra_path(G, weight=weight))
                paths = {}
        else:
            # Find paths from all nodes co-accessible to the target.
            if weight is None:
                # paths = nx.single_source_shortest_path(G, target)
                # paths = G.single_source_shortest_path(target)
                paths = []
            else:
                # paths = nx.single_source_dijkstra_path(G, target,
                #                                        weight=weight)
                paths = []
    else:
        if target is None:
            # Find paths to all nodes accessible from the source.
            if weight is None:
                # paths = nx.single_source_shortest_path(G, source)
                paths = []
                # paths = G.single_source_shortest_path(source)
            else:
                # paths = nx.single_source_dijkstra_path(G, source,
                #                                        weight=weight)
                paths = []
        else:

            query = """\
            MATCH (source:%s   {%s: $source })
            MATCH (target:%s   {%s: $target })

            CALL gds.alpha.shortestPath.stream({
                nodeProjection: $nodeLabel,
                relationshipProjection: {
                    relType: {
                        type: $relationshipType,
                        orientation: $direction,
                        properties: {}
                    }
                },
                startNode: source,
                endNode: target,
                relationshipWeightProperty: $propertyName
            })
            YIELD nodeId, cost
            RETURN gds.util.asNode(nodeId).%s AS node, cost
            """ % (
                G.node_label,
                G.identifier_property,
                G.node_label,
                G.identifier_property,
                G.identifier_property
            )

            with G.driver.session() as session:
                params = G.base_params()
                params["source"] = source
                params["target"] = target
                params["propertyName"] = weight

                paths = [row["node"] for row in session.run(query, params)]
    return paths

def shortest_path(G,source, target):
    return shortest_weighted_path(G,source, target, weight='')
"""TEST OUTPUT
nx.shortest_weighted_path(G, source=1, target=3, weight='')
nx.shortest_path(G, source=1, target=3)
"""
