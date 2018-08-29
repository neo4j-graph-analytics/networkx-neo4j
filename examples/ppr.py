import operator

import networkx as nx

G = nx.Graph()

G.add_nodes_from(["John", "Mary", "Jill", "Todd",
                  "iPhone5", "Kindle Fire", "Fitbit Flex Wireless", "Harry Potter", "Hobbit"])

G.add_edges_from([
    ("John", "iPhone5"),
    ("John", "Kindle Fire"),
    ("Mary", "iPhone5"),
    ("Mary", "Kindle Fire"),
    ("Mary", "Fitbit Flex Wireless"),
    ("Jill", "iPhone5"),
    ("Jill", "Kindle Fire"),
    ("Jill", "Fitbit Flex Wireless"),
    ("Todd", "Fitbit Flex Wireless"),
    ("Todd", "Harry Potter"),
    ("Todd", "Hobbit"),
])

pr = nx.pagerank(G)
pr = sorted(pr.items(), key=operator.itemgetter(1), reverse=True)

print("PageRank")

for item, score in pr:
    print(item, score)

print("")
print("Personalised PageRank")

ppr = nx.pagerank(G, personalization={"Mary": 1})
ppr = sorted(ppr.items(), key=operator.itemgetter(1), reverse=True)

for item, score in ppr:
    print(item, "{0:.10f}".format(score))
