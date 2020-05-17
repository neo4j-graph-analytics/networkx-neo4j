class BaseGraph:
    def __init__(self, driver, direction, config=None):
        if config is None:
            config = {}

        self.driver = driver
        self.direction = direction
        self.node_label = config.get("node_label", "Node")
        self.relationship_type = config.get("relationship_type", "CONNECTED")
        self.graph = config.get("graph", "heavy")
        self.identifier_property = config.get("identifier_property", "id")

    def base_params(self):
        return {
            "direction": self.direction,
            "nodeLabel": self.node_label,
            "relationshipType": self.relationship_type,
            "graph": self.graph
        }

    add_node_query = """\
    MERGE (:`%s` {`%s`:  $node })
    """

    def add_node(self, node):
        with self.driver.session() as session:
            query = self.add_node_query % (self.node_label, self.identifier_property)
            session.run(query, {"node": node})

    add_nodes_query = """\
    UNWIND $values AS value
    MERGE (:`%s` {`%s`: value })
    """

    def add_nodes_from(self, values):
        with self.driver.session() as session:
            query = self.add_nodes_query % (self.node_label, self.identifier_property)
            session.run(query, {"values": values})

    add_edge_query = """\
    MERGE (node1:`%s` {`%s`: $node1 })
    MERGE (node2:`%s` {`%s`: $node2 })
    MERGE (node1)-[:`%s`]->(node2)
    """

    def add_edge(self, node1, node2):
        with self.driver.session() as session:
            query = self.add_edge_query % (
                self.node_label,
                self.identifier_property,
                self.node_label,
                self.identifier_property,
                self.relationship_type
            )
            session.run(query, {"node1": node1, "node2": node2})

    add_edges_query = """\
    UNWIND $edges AS edge
    MERGE (node1:`%s` {`%s`: edge[0] })
    MERGE (node2:`%s` {`%s`: edge[1] })
    MERGE (node1)-[:`%s`]->(node2)
    """

    def add_edges_from(self, edges):
        with self.driver.session() as session:
            query = self.add_edges_query % (
                self.node_label,
                self.identifier_property,
                self.node_label,
                self.identifier_property,
                self.relationship_type
            )
            session.run(query, {"edges": [list(edge) for edge in edges]})

    number_of_nodes_query = """\
    MATCH (:`%s`)
    RETURN count(*) AS numberOfNodes
    """

    def number_of_nodes(self):
        with self.driver.session() as session:
            query = self.number_of_nodes_query % self.node_label
            return session.run(query).peek()["numberOfNodes"]


    def delete_all(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def load_got(self):
        """
        Author: Andrew Beveridge
        https://twitter.com/mathbeveridge
        """
        with self.driver.session() as session:
            session.run("""\
            CREATE CONSTRAINT ON (c:Character)
            ASSERT c.name IS UNIQUE
            """)

            session.run("""\
            LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/mathbeveridge/asoiaf/master/data/asoiaf-book1-edges.csv" AS row
            MERGE (src:Character {name: row.Source})
            MERGE (tgt:Character {name: row.Target})
            // relationship for the book
            MERGE (src)-[r:INTERACTS1]->(tgt)
            ON CREATE SET r.weight = toInt(row.weight), r.book=1
            """)

            session.run("""\
            LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/mathbeveridge/asoiaf/master/data/asoiaf-book2-edges.csv" AS row
            MERGE (src:Character {name: row.Source})
            MERGE (tgt:Character {name: row.Target})
            // relationship for the book
            MERGE (src)-[r:INTERACTS2]->(tgt)
            ON CREATE SET r.weight = toInt(row.weight), r.book=2
            """)

            session.run("""\
            LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/mathbeveridge/asoiaf/master/data/asoiaf-book3-edges.csv" AS row
            MERGE (src:Character {name: row.Source})
            MERGE (tgt:Character {name: row.Target})
            // relationship for the book
            MERGE (src)-[r:INTERACTS3]->(tgt)
            ON CREATE SET r.weight = toInt(row.weight), r.book=3
            """)

            session.run("""\
            LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/mathbeveridge/asoiaf/master/data/asoiaf-book45-edges.csv" AS row
            MERGE (src:Character {name: row.Source})
            MERGE (tgt:Character {name: row.Target})
            // relationship for the book
            MERGE (src)-[r:INTERACTS45]->(tgt)
            ON CREATE SET r.weight = toInt(row.weight), r.book=45
            """)

    def load_euroads(self):
        with self.driver.session() as session:
            session.run("""\
            CREATE CONSTRAINT ON (p:Place) ASSERT p.name IS UNIQUE
            """)

            session.run("""\
            USING PERIODIC COMMIT 1000
            LOAD CSV WITH HEADERS FROM "https://github.com/neo4j-apps/neuler/raw/master/sample-data/eroads/roads.csv"
            AS row

            MERGE (origin:Place {name: row.origin_reference_place})
            SET origin.countryCode = row.origin_country_code

            MERGE (destination:Place {name: row.destination_reference_place})
            SET destination.countryCode = row.destination_country_code

            MERGE (origin)-[eroad:EROAD {road_number: row.road_number}]->(destination)
            SET eroad.distance = toInteger(row.distance), eroad.watercrossing = row.watercrossing
            """)

    def load_twitter(self):
        with self.driver.session() as session:
            session.run("""\
            CREATE CONSTRAINT ON(u:User) ASSERT u.id IS unique
            """)

            session.run("""\
            CALL apoc.load.json("https://github.com/neo4j-apps/neuler/raw/master/sample-data/twitter/users.json")
            YIELD value
            MERGE (u:User {id: value.user.id })
            SET u += value.user
            FOREACH (following IN value.following |
              MERGE (f1:User {id: following})
              MERGE (u)-[:FOLLOWS]->(f1))
            FOREACH (follower IN value.followers |
              MERGE(f2:User {id: follower})
              MERGE (u)<-[:FOLLOWS]-(f2));
            """)
