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
    G.add_edges_from([(1, 2), (1, 3)])

    print(G.number_of_nodes())

    print(functions["betweenness_centrality"](G))
    print(functions["closeness_centrality"](G))


execute_graph(Graph(GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo"))), neo4j_functions)

execute_graph(nx.Graph(), networkx_functions)
