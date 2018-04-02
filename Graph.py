class Graph:
    def __init__(self, driver):
        self.driver = driver
        self.direction = "BOTH"

    add_node_query = """\
    MERGE (:Node {value: {value} })
    """

    def add_node(self, value):
        with self.driver.session() as session:
            session.run(self.add_node_query, {"value": value})

    add_nodes_query = """\
    UNWIND {values} AS value
    MERGE (:Node {value: value })
    """

    def add_nodes_from(self, values):
        with self.driver.session() as session:
            session.run(self.add_nodes_query, {"values": values})

    add_edge_query = """\
    MERGE (node1:Node {value: {node1} })
    MERGE (node2:Node {value: {node2} })
    MERGE (node1)-[:CONNECTED]->(node2)
    """

    def add_edge(self, node1, node2):
        with self.driver.session() as session:
            session.run(self.add_edge_query, {"node1": node1, "node2": node2})

    add_edges_query = """\
    UNWIND {edges} AS edge
    MERGE (node1:Node {value: edge[0] })
    MERGE (node2:Node {value: edge[1] })
    MERGE (node1)-[:CONNECTED]->(node2)
    """

    def add_edges_from(self, edges):
        with self.driver.session() as session:
            session.run(self.add_edges_query, {"edges": [list(edge) for edge in edges]})

    number_of_nodes_query = """\
    MATCH (:Node)
    RETURN count(*) AS numberOfNodes
    """

    def number_of_nodes(self):
        with self.driver.session() as session:
            return session.run(self.number_of_nodes_query).peek()["numberOfNodes"]

    betweenness_centrality_query = """\
    CALL algo.betweenness.stream("Node", "CONNECTED", {direction: {direction} })
    YIELD nodeId, centrality
    MATCH (n:Node) WHERE id(n) = nodeId
    RETURN n.value AS node, centrality
    """

    def betweenness_centrality(self):
        with self.driver.session() as session:
            result = session.run(self.betweenness_centrality_query, {"direction": self.direction})
            result = {row["node"]: row["centrality"] for row in result}
        return result

    closeness_centrality_query = """\
    CALL algo.closeness.stream("Node", "CONNECTED", {direction: {direction} })
    YIELD nodeId, centrality
    MATCH (n:Node) WHERE id(n) = nodeId
    RETURN n.value AS node, centrality
    """

    def closeness_centrality(self):
        with self.driver.session() as session:
            result = session.run(self.closeness_centrality_query, {"direction": self.direction})
            result = {row["node"]: row["centrality"] for row in result}
        return result