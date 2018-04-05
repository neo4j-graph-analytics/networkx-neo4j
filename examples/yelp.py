from neo4j.v1 import GraphDatabase, basic_auth

import nxneo4j


def cypher():
    driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo"))

    config = {
        "node_label": """\
        MATCH (c:Category) RETURN id(c) AS id
        """,
        "relationship_type": """\
        MATCH (c1:Category)<-[:IN_CATEGORY]-()-[:IN_CATEGORY]->(c2:Category)
        RETURN id(c1) AS source, id(c2) AS target, count(*) AS weight
        """,
        "identifier_property": "name",
        "graph": "cypher"
    }

    G = nxneo4j.Graph(driver, config)

    for community in nxneo4j.label_propagation_communities(G):
        print(community)


if __name__ == '__main__':
    cypher()
