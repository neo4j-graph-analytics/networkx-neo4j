import networkx as nx
from neo4j.v1 import GraphDatabase, basic_auth

from Graph import Graph
import centrality

networkx_functions = {
    "betweenness_centrality": nx.centrality.betweenness_centrality,
    "closeness_centrality": nx.centrality.closeness_centrality
}

neo4j_functions = {
    "betweenness_centrality": centrality.betweenness_centrality,
    "closeness_centrality": centrality.closeness_centrality
}


def execute_graph(G, functions):
    G.add_node(1)
    G.add_nodes_from([2, 3])

    G.add_edge(1, 2)
    G.add_edge(4, 5)
    G.add_edges_from([(1, 2), (1, 3)])

    print("Number of nodes: {0}".format(G.number_of_nodes()))

    between = functions["betweenness_centrality"]
    print("Betweenness (default): {0}".format(between(G)))

    closeness = functions["closeness_centrality"]

    print("Closeness (WF): {0}".format(closeness(G, wf_improved=True)))
    print("Closeness (no WF): {0}".format(closeness(G, wf_improved=False)))
    print("Closeness (one node): {0}".format(closeness(G, 1, wf_improved=False)))

print("Neo4j")
execute_graph(Graph(GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo"))), neo4j_functions)

print()

print("networkx")
execute_graph(nx.Graph(), networkx_functions)
