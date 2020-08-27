# test only (import sys;sys.path.append("../"))  #the purpose is to reach to the parent directory
# to fix the default port run $kill $(lsof -ti:7687)
"""
known fails
G.add_node("Betul",age=4)
G.add_node("Betul",age=5) #this does not update the first one

G.nodes['Betul']['age'] = 5 #also does not work

list(G.edges(data=True)) it would be nice to display labels here

G.edges(['Betul','Nurgul']) #FAILS


"""


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
