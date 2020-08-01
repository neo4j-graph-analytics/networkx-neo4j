from neo4j import GraphDatabase

import nxneo4j as nx
import networkx as nx
nx.__file__

driver = GraphDatabase.driver(uri="bolt://localhost:11003",auth=("neo4j","neo"))
G = nx.Graph(driver)
G = nx.Graph()
G.delete_all()
G.add_node(1)
G.add_nodes_from([2,3,4])
G.add_edge(1,2)
G.add_edges_from([(2,3),(3,4)])

>>> nx.betweenness_centrality(G)
{1: 0.0, 2: 2.0, 3: 2.0, 4: 0.0}

>>> nx.closeness_centrality(G)
{1: 0.5, 2: 0.75, 3: 0.75, 4: 0.5}

>>> nx.pagerank(G)
{1: 0.7017541848906179,
 2: 1.298245213209345,
 3: 1.298245213209345,
 4: 0.7017541848906179}

>>> nx.triangles(G)
{1: 0, 2: 0, 3: 0, 4: 0}

>>> nx.clustering(G)
{1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0}

>>> list(nx.community.label_propagation_communities(G))
[{1, 2, 3, 4}]

>>> nx.shortest_path(G, source=1, target=4)
[1, 2, 3, 4]
