class Graph:
    def __init__(self, driver, config=None):
        if config is None:
            config = {}

        self.driver = driver
        self.direction = "BOTH"
        self.node_label = config.get("node_label", "Node")
        self.relationship_type = config.get("relationship_type", "CONNECTED")
        self.graph = config.get("graph", "heavy")

    add_node_query = """\
    MERGE (:%s {value: {value} })
    """

    def add_node(self, value):
        with self.driver.session() as session:
            query = self.add_node_query % self.node_label
            session.run(query, {"value": value})

    add_nodes_query = """\
    UNWIND {values} AS value
    MERGE (:`%s` {value: value })
    """

    def add_nodes_from(self, values):
        with self.driver.session() as session:
            query = self.add_nodes_query % self.node_label
            session.run(query, {"values": values})

    add_edge_query = """\
    MERGE (node1:`%s` {value: {node1} })
    MERGE (node2:`%s` {value: {node2} })
    MERGE (node1)-[:`%s`]->(node2)
    """

    def add_edge(self, node1, node2):
        with self.driver.session() as session:
            query = self.add_edge_query % (
                self.node_label,
                self.node_label,
                self.relationship_type
            )
            session.run(query, {"node1": node1, "node2": node2})

    add_edges_query = """\
    UNWIND {edges} AS edge
    MERGE (node1:`%s` {value: edge[0] })
    MERGE (node2:`%s` {value: edge[1] })
    MERGE (node1)-[:`%s`]->(node2)
    """

    def add_edges_from(self, edges):
        with self.driver.session() as session:
            query = self.add_edges_query % (
                self.node_label,
                self.node_label,
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

    betweenness_centrality_query = """\
    CALL algo.betweenness.stream({nodeLabel}, {relationshipType}, {
        direction: {direction},
        graph: {graph}
    })
    YIELD nodeId, centrality
    MATCH (n) WHERE id(n) = nodeId
    RETURN n.value AS node, centrality
    """

    def betweenness_centrality(self):
        with self.driver.session() as session:
            query = self.betweenness_centrality_query
            params = self.base_params()
            result = {row["node"]: row["centrality"] for row in session.run(query, params)}
        return result

    closeness_centrality_query = """\
    CALL algo.closeness.stream({nodeLabel}, {relationshipType}, {
      direction: {direction},
      improved: {wfImproved},
      graph: {graph}
    })
    YIELD nodeId, centrality
    MATCH (n) WHERE id(n) = nodeId
    RETURN n.value AS node, centrality
    """

    def closeness_centrality(self, wf_improved=True):
        with self.driver.session() as session:
            params = self.base_params()
            params["wfImproved"] = wf_improved
            query = self.closeness_centrality_query
            result = {row["node"]: row["centrality"] for row in session.run(query, params)}
        return result

    harmonic_centrality_query = """\
    CALL algo.closeness.harmonic.stream({nodeLabel}, {relationshipType}, {
      direction: {direction},
      graph: {graph}
    })
    YIELD nodeId, centrality
    MATCH (n) WHERE id(n) = nodeId
    RETURN n.value AS node, centrality
    """

    def harmonic_centrality(self):
        with self.driver.session() as session:
            params = self.base_params()
            query = self.harmonic_centrality_query
            result = {row["node"]: row["centrality"] for row in session.run(query, params)}
        return result

    pagerank_query = """\
    CALL algo.pageRank.stream({nodeLabel}, {relationshipType}, {
      direction: {direction},
      graph: {graph},
      iterations: {iterations},
      dampingFactor: {dampingFactor}
    })
    YIELD nodeId, score
    MATCH (n:`%s`) WHERE id(n) = nodeId
    RETURN n.value AS node, score
    """

    def pagerank(self, alpha, max_iter):
        with self.driver.session() as session:
            params = self.base_params()
            params["iterations"] = max_iter
            params["dampingFactor"] = alpha

            query = self.pagerank_query % self.node_label
            result = {row["node"]: row["score"] for row in session.run(query, params)}
        return result

    triangle_count_query = """\
    CALL algo.triangleCount.stream({nodeLabel}, {relationshipType}, {
      direction: {direction},
      graph: {graph}
    })
    YIELD nodeId, triangles, coefficient
    MATCH (n) WHERE id(n) = nodeId
    RETURN n.value AS node, triangles, coefficient
    """

    def triangles(self):
        with self.driver.session() as session:
            params = self.base_params()
            query = self.triangle_count_query
            result = {row["node"]: row["triangles"] for row in session.run(query, params)}
        return result

    def clustering(self):
        with self.driver.session() as session:
            params = self.base_params()
            query = self.triangle_count_query
            result = {row["node"]: row["coefficient"] for row in session.run(query, params)}
        return result

    triangle_query = """\
    CALL algo.triangleCount({nodeLabel}, {relationshipType}, {
      direction: {direction},
      graph: {graph},
      write: false
    })
    """

    def average_clustering(self):
        with self.driver.session() as session:
            params = self.base_params()
            query = self.triangle_query
            result = session.run(query, params)
            return result.peek()["averageClusteringCoefficient"]

    lpa_query = """\
    CALL algo.labelPropagation.stream({nodeLabel}, {relationshipType}, {
      direction: {direction},
      graph: {graph}
    })
    YIELD nodeId, label
    MATCH (n) WHERE id(n) = nodeId
    RETURN label, collect(n.value) AS nodes
    """

    def label_propagation(self):
        with self.driver.session() as session:
            params = self.base_params()
            query = self.lpa_query

            for row in session.run(query, params):
                yield set(row["nodes"])

    def base_params(self):
        return {
            "direction": self.direction,
            "nodeLabel": self.node_label,
            "relationshipType": self.relationship_type,
            "graph": self.graph
        }
