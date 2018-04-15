from neo4j.v1 import GraphDatabase, basic_auth

import nxneo4j
import operator


def cypher():
    driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo"))

    nodes = """\
    MATCH (c:Category) 
    RETURN id(c) AS id
    """

    relationships = """\
    MATCH (c1:Category)<-[:IN_CATEGORY]-()-[:IN_CATEGORY]->(c2:Category)
    RETURN id(c1) AS source, id(c2) AS target, count(*) AS weight
    """

    config = {
        "node_label": nodes,
        "relationship_type": relationships,
        "identifier_property": "name",
        "graph": "cypher"
    }

    G = nxneo4j.Graph(driver, config)

    for community in nxneo4j.label_propagation_communities(G):
        print(community)

    pr = nxneo4j.pagerank(G)
    sorted_pr = sorted(pr.items(), key=operator.itemgetter(1), reverse=True)
    for category, score in sorted_pr[:10]:
        print(category, score)


if __name__ == '__main__':
    cypher()
