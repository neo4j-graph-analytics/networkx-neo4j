import networkx as nx
from neo4j import GraphDatabase

import nxneo4j

networkx_functions = {
    "betweenness_centrality": nx.betweenness_centrality,
    "closeness_centrality": nx.closeness_centrality,
    "pagerank": nx.pagerank,
    "triangles": nx.triangles,
    "clustering": nx.clustering,
    "label_propagation_communities": nx.algorithms.community.label_propagation_communities,
    "shortest_path": nx.shortest_path,
}

neo4j_functions = {
    "betweenness_centrality": nxneo4j.betweenness_centrality,
    "closeness_centrality": nxneo4j.closeness_centrality,
    "pagerank": nxneo4j.pagerank,
    "triangles": nxneo4j.triangles,
    "clustering": nxneo4j.clustering,
    "label_propagation_communities": nxneo4j.community.label_propagation_communities,
    "shortest_path": nxneo4j.shortest_path,
}

driver = GraphDatabase.driver(uri="bolt://localhost",auth=("neo4j","neo"))
G = nxneo4j.Graph(driver)
functions = neo4j_functions
def execute_graph(G, functions):
    G.add_node(1)
    G.add_nodes_from([2, 3])

    G.add_edge(1, 2)
    G.add_edge(4, 5)
    G.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4), (4, 5)])

    print("Number of nodes: {0}".format(G.number_of_nodes()))

    between = functions["betweenness_centrality"]
    print("Betweenness (default): {0}".format(between(G)))

    closeness = functions["closeness_centrality"]

    print("Closeness (WF): {0}".format(closeness(G, wf_improved=True)))
    print("Closeness (no WF): {0}".format(closeness(G, wf_improved=False)))
    print("Closeness (one node): {0}".format(closeness(G, 1, wf_improved=False)))

    pagerank = functions["pagerank"]
    print("PageRank: {0}".format(pagerank(G)))

    triangles = functions["triangles"]
    print("Triangles: {0}".format(triangles(G)))

    clustering = functions["clustering"]
    print("Clustering Coefficient: {0}".format(clustering(G)))

    lpa = functions["label_propagation_communities"]
    print("Label Propagation: {0}".format(list(lpa(G))))

    shortest_path = functions["shortest_path"]
    print("Single Shortest Path: {0}".format(shortest_path(G, 1)))

if __name__ == '__main__':
    print("Neo4j")
    execute_graph(nxneo4j.Graph(GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo"))),
                  neo4j_functions)

    print()

    print("networkx")
    execute_graph(nx.Graph(), networkx_functions)
