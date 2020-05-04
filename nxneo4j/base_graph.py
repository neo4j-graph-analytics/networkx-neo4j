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

    add_node_query = """\
    MERGE (:`%s` {`%s`: $value })
    """

    def base_params(self):
        return {
            "direction": self.direction,
            "nodeLabel": self.node_label,
            "relationshipType": self.relationship_type,
            "graph": self.graph
        }

    def add_node(self, value):
        with self.driver.session() as session:
            query = self.add_node_query % (self.node_label, self.identifier_property)
            session.run(query, {"value": value})

    add_nodes_query = """\
    UNWIND $value AS value
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

    betweenness_centrality_query = """\
    CALL gds.alpha.betweenness.stream({
          nodeProjection: $nodeLabel,
          relationshipProjection: $relationshipType
        })
    YIELD nodeId, centrality
    RETURN gds.util.asNode(nodeId).`%s` AS node, centrality
    ORDER BY centrality DESC, node ASC
    """

    def betweenness_centrality(self):
        with self.driver.session() as session:
            query = self.betweenness_centrality_query % self.identifier_property
            params = self.base_params()
            result = {row["node"]: row["centrality"] for row in session.run(query, params)}
        return result

    closeness_centrality_query = """\
    CALL gds.alpha.closeness.stream({
        nodeProjection: $nodeLabel,
        relationshipProjection: $relationshipType
    })
    YIELD nodeId, centrality
    RETURN gds.util.asNode(nodeId).`%s` AS node, centrality
    ORDER BY centrality DESC, node ASC
    """

    def closeness_centrality(self, wf_improved=True):
        with self.driver.session() as session:
            params = self.base_params()
            params["wfImproved"] = wf_improved
            query = self.closeness_centrality_query % self.identifier_property

            result = {row["node"]: row["centrality"] for row in session.run(query, params)}
        return result

    pagerank_query = """\
    CALL gds.pageRank.stream({
        nodeProjection: $nodeLabel,
        relationshipProjection: $relationshipType,
        maxIterations: $iterations,
        dampingFactor: $dampingFactor })
    YIELD nodeId, score
    RETURN gds.util.asNode(nodeId).`%s` AS node, score
    ORDER BY score DESC, node ASC
"""
    def pagerank(self, alpha, max_iter):
        with self.driver.session() as session:
            params = self.base_params()
            params["iterations"] = max_iter
            params["dampingFactor"] = alpha

            query = self.pagerank_query % self.identifier_property
            result = {row["node"]: row["score"] for row in session.run(query, params)}
        return result

    triangle_count_query = """\
    CALL gds.alpha.triangleCount.stream({
        nodeProjection: $nodeLabel,
        relationshipProjection: {
            %s: {
                orientation: 'UNDIRECTED'
        }
      }
    })
    YIELD nodeId, triangles, coefficient
    RETURN gds.util.asNode(nodeId).`%s` AS node, triangles, coefficient
    ORDER BY coefficient DESC"""

    def triangles(self):
        with self.driver.session() as session:
            params = self.base_params()
            query = self.triangle_count_query % (params['relationshipType'],identifier_property)
            query = self.triangle_count_query % self.identifier_property
            result = {row["node"]: row["triangles"] for row in session.run(query, params)}
        return result

    def clustering(self):
        with self.driver.session() as session:
            params = self.base_params()
            query = self.triangle_count_query % self.identifier_property
            result = {row["node"]: row["coefficient"] for row in session.run(query, params)}
        return result

    triangle_query = """\
    CALL gds.alpha.triangleCount.stream({
        nodeProjection: $nodeLabel,
        relationshipProjection: {
            %s: {
                orientation: 'UNDIRECTED'
        }
      }
    })
    YIELD coefficient
    RETURN avg(coefficient) as averageClusteringCoefficient
    """

    def average_clustering(self):
        with self.driver.session() as session:
            params = self.base_params()
            query = triangle_query % (params['relationshipType'])
            result = session.run(query,params)
            result.peek()["averageClusteringCoefficient"]

    lpa_query = """\
    CALL gds.labelPropagation.stream({
        nodeProjection: $nodeLabel,
        relationshipProjection: {
            %s: {
                orientation: $direction
        }
      }
    })
    YIELD nodeId, communityId AS community
    RETURN gds.util.asNode(nodeId).`%s` AS node, community
    """

    def label_propagation(self):
        with self.driver.session() as session:
            params = self.base_params()
            query = self.lpa_query % (params['relationshipType'],identifier_property)

            for row in session.run(query, params):
                yield set(row["nodes"])

    shortest_path_query = """\
    MATCH (source:`%s` {`%s`: $source })
    MATCH (target:`%s`   {`%s`: $target })

    CALL gds.alpha.shortestPath.stream({
        nodeProjection: $nodeLabel,
        relationshipProjection: {
            %s: {
                orientation: $direction,
                properties: $propertyName
                }
            },
        startNode: source,
        endNode: target,
        weightProperty: $propertyName
        })
    YIELD nodeId, cost
    RETURN gds.util.asNode(nodeId).`%s` AS node, cost
    """

    def shortest_weighted_path(self, source, target, weight):
        with self.driver.session() as session:
            params = self.base_params()
            params["source"] = source
            params["target"] = target
            params["propertyName"] = weight

            query = self.shortest_path_query % (
                self.node_label,
                self.identifier_property,
                self.node_label,
                self.identifier_property,
                self.relationshipType,
                self.identifier_property
            )

            result = [row["node"] for row in session.run(query, params)]
        return result

    def shortest_path(self, source, target):
        with self.driver.session() as session:
            params = self.base_params()
            params["source"] = source
            params["target"] = target
            params["propertyName"] = None

            query = self.shortest_path_query % (
                self.node_label,
                self.identifier_property,
                self.node_label,
                self.identifier_property,
                self.relationshipType,
                self.identifier_property
            )

            result = [row["node"] for row in session.run(query, params)]
        return result
