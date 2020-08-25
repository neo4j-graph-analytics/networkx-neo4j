from neo4j import GraphDatabase
import nxneo4j as nx

driver = GraphDatabase.driver(uri="bolt://localhost:11003",auth=("neo4j","neo"))
G = nx.DiGraph(driver)


G.add_node(1)
G.add_nodes_from([2,3,4])
G.add_edge(1,2)
G.add_edges_from([(2,3),(3,4)])

nx.betweenness_centrality(G)
nx.closeness_centrality(G)
nx.pagerank(G)
nx.triangles(G)
nx.clustering(G)
list(nx.community.label_propagation_communities(G))
nx.shortest_path(G, source=1, target=4)
