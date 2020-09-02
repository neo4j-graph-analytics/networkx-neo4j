from .exceptions import *

class NodeView:
    def __init__(self, graph):
        self.graph = graph

    def __iter__(self):
        return iter(self.__call__())

    number_of_nodes_query = """\
    MATCH (:`%s`)
    RETURN count(*) AS numberOfNodes
    """

    def __len__(self):
        with self.graph.driver.session() as session:
            query = self.number_of_nodes_query % self.graph.node_label
            return session.run(query).peek()["numberOfNodes"]

    get_node_attributes_query = """\
    MATCH (node:`%s` {`%s`: $value })
    RETURN node
    """

    def __getitem__(self, index):
        with self.graph.driver.session() as session:
            query = self.get_node_attributes_query % (
                self.graph.node_label,
                self.graph.identifier_property
            )
            key = self.graph.identifier_property
            n = session.run(query, {"value": index}).single()["node"]
            data = {k: n[k] for k in n.keys() if k!=key}
            return data

    get_nodes_query = """\
    MATCH (node:`%s`)
    RETURN node
    """

    def __call__(self, data=False, default=None):
        with self.graph.driver.session() as session:
            query = self.get_nodes_query % (self.graph.node_label)
            nodes = [r["node"] for r in session.run(query).data()]
            key = self.graph.identifier_property
            if not data:
                for n in nodes:
                    yield n[key]
            elif isinstance(data, bool):
                for n in nodes:
                    rdata = {k: n[k] for k in n.keys() if k!=key}
                    yield (n[key], rdata)
            else:
                for n in nodes:
                    yield n[key], n.get(data, default)

class EdgeView:
    def __init__(self, graph):
        self.graph = graph

    def __iter__(self):
        return iter(self.__call__())

    number_of_edges_query = """\
    MATCH (u:`%s`)-[edge:`%s`]->(v:`%s`)
    RETURN COUNT(edge) AS numberOfEdges
    """

    def __len__(self):
        with self.graph.driver.session() as session:
            query = self.number_of_edges_query % (
                self.graph.node_label,
                self.graph.relationship_type,
                self.graph.node_label
            )
            return session.run(query).peek()["numberOfEdges"]

    get_edges_query = """\
    MATCH (u:`%s`)-[edge:`%s`]->(v:`%s`)
    RETURN u.`%s` AS u, v.`%s` AS v, edge
    """

    def __call__(self, data=False, default=None):
        if self.graph.relationship_type is None:
            return # raises StopIteration

        with self.graph.driver.session() as session:
            query = self.get_edges_query % (
                self.graph.node_label,
                self.graph.relationship_type,
                self.graph.node_label,
                self.graph.identifier_property,
                self.graph.identifier_property
            )
            edges = [(r["u"], r["v"], r["edge"]._properties) for r in session.run(query)]
            if not data:
                for u, v, _ in edges:
                    yield (u, v)
            elif isinstance(data, bool):
                for u, v, d in edges:
                    yield (u, v, d)
            else:
                for u, v, d in edges:
                    yield (u, v, d.get(data, default))


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
            "node_label": self.node_label,
            "relationship_type": self.relationship_type,
            "identifier_property": self.identifier_property
    #        "graph": self.graph
        }

    add_node_query = """\
    MERGE (:`%s` {`%s`:  $node })
    """

    def __iter__(self):
        return iter(self.nodes)

    def __contains__(self, n):
        return n in self.nodes

    def __len__(self):
        return len(self.nodes)

    def number_of_nodes(self):
        return len(self.nodes)

    @property
    def nodes(self):
        # Lazy View creation, like in networkx
        nodes = NodeView(self)
        self.__dict__["nodes"] = nodes
        return nodes

    @property
    def edges(self):
        edges = EdgeView(self)
        self.__dict__["edges"] = edges
        return edges


    add_node_query = """\
    MERGE (:`%s` {`%s`: $value })
    """

    add_node_query_with_props = """\
    MERGE (n:`%s` {`%s`: $value })
    ON CREATE SET n+=$props
    """
    def add_node(self, value, attr_dict=dict(), **attr):
        with self.driver.session() as session:
            if len(attr_dict) == 0 and len(attr) == 0:
                query = self.add_node_query % (self.node_label, self.identifier_property)
                session.run(query, {"value": value})
            else:
                props = dict(attr_dict)
                for k, v in attr.items():
                    props[k] = v
                query = self.add_node_query_with_props % (self.node_label, self.identifier_property)
                session.run(query, {"value": value}, props=props)

    add_nodes_query = """\
    UNWIND $values AS value
    MERGE (:`%s` {`%s`: value })
    """

    add_nodes_query_with_attrdict = """\
    UNWIND $values AS props
    MERGE (n:`%s` {`%s`: props.`%s` })
    ON CREATE SET n=props
    """

    def add_nodes_from(self, values, **attr):
        are_node_attrdict_tuple = False
        try:
            for v in values:
                if isinstance(v[1], dict):
                    are_node_attrdict_tuple = True
                break
        except:
            pass

        if are_node_attrdict_tuple or len(attr) > 0:
            query = self.add_nodes_query_with_attrdict % (
                self.node_label,
                self.identifier_property,
                self.identifier_property
            )
            n_values = []
            for i in values:
                n_d = dict(attr)
                if are_node_attrdict_tuple:
                    n_d.update(i[1])
                    if self.identifier_property not in i[1]:
                        n_d[self.identifier_property] = i[0]
                else:
                    n_d[self.identifier_property] = i
                n_values.append(n_d)
            values = n_values
        else:
            query = self.add_nodes_query % (self.node_label, self.identifier_property)

        with self.driver.session() as session:
            session.run(query, {"values": values})

    add_edge_query = """\
    MERGE (node1:`%s` {`%s`: $node1 })
    MERGE (node2:`%s` {`%s`: $node2 })
    MERGE (node1)-[r:`%s`]->(node2)
    ON CREATE SET r=$props
    """

    def add_edge(self, node1, node2, **attr):
        with self.driver.session() as session:
            query = self.add_edge_query % (
                self.node_label,
                self.identifier_property,
                self.node_label,
                self.identifier_property,
                self.relationship_type
            )
            session.run(query, {"node1": node1, "node2": node2}, props=attr)

    add_edges_query = """\
    UNWIND $edges AS edge
    MERGE (node1:`%s` {`%s`: edge[0] })
    MERGE (node2:`%s` {`%s`: edge[1] })
    MERGE (node1)-[r:`%s`]->(node2)
    ON CREATE SET r=edge[2]
    """

    def add_edges_from(self, edges, **attr):
        with self.driver.session() as session:
            query = self.add_edges_query % (
                self.node_label,
                self.identifier_property,
                self.node_label,
                self.identifier_property,
                self.relationship_type
            )
            def fix_edge(edge):
                if len(edge) == 2:
                    edge.append({})
                return edge
            session.run(query, {"edges": [fix_edge(list(edge)) for edge in edges]})

    def add_path(self, path, **attr):
        for u, v in itertools.izip(path, path[1:]):
            self.add_edge(u, v, **attr)

    remove_node_query = """\
    MATCH (n:`%s` {`%s`: $value })
    DETACH DELETE n
    RETURN COUNT(*) AS deletedNodes;
    """

    def remove_node(self, n):
        with self.driver.session() as session:
            query = self.remove_node_query % (self.node_label, self.identifier_property)
            deleted_nodes = session.run(query, {"value": n}).peek()["deletedNodes"]
            if deleted_nodes < 1:
                raise NetworkXError("The node %s is not in the graph." % (n, ))

    remove_nodes_query = """\
    UNWIND $nodes as value
    MERGE (n:`%s` {`%s`: value })
    DETACH DELETE n
    """

    def remove_nodes_from(self, nodes):
        with self.driver.session() as session:
            query = self.remove_nodes_query % (self.node_label, self.identifier_property)
            session.run(query, {"nodes": nodes})

    def update(self, edges=None, nodes=None, graph_id_props=None):
        if edges is not None:
            if nodes is not None:
                self.add_nodes_from(edges)
                self.add_edges_from(nodes)
            else:
                try:
                    graph_nodes = edges.nodes
                    graph_edges = edges.edges
                except:
                    self.add_edges_from(edges)
                else:
                    graph_nodes_data = graph_nodes(data=True)
                    graph_edges_data = graph_edges(data=True)
                    adding_edges = []
                    for u, v, data in graph_edges_data:
                        try:
                            if self.identifier_property in graph_nodes[u]:
                                u = graph_nodes[u][self.identifier_property]
                        except:
                            pass
                        try:
                            if self.identifier_property in graph_nodes[v]:
                                v = graph_nodes[v][self.identifier_property]
                        except:
                            pass
                        adding_edges.append((u, v, data))
                    graph_nodes_data = graph_nodes(data=True)
                    graph_nodes_fixed_data = []
                    for n, d in graph_nodes_data:
                        if graph_id_props is not None:
                            if isinstance(graph_id_props, tuple) or isinstance(graph_id_props, list):
                                for value, v in zip(n, graph_id_props):
                                    d[v] = value
                            else:
                                d[graph_id_props] = n
                        graph_nodes_fixed_data.append((n, d))
                    self.add_nodes_from(graph_nodes_fixed_data)
                    self.add_edges_from(adding_edges)

    _clear_graph_nodes_query = """\
    MATCH (n:`%s`)
    DELETE n
    """

    _clear_graph_edges_query = """\
    MATCH (:`%s`)-[r:`%s`]-(:`%s`)
    DELETE r
    """

    def clear(self):
        with self.driver.session() as session:
            if self.relationship_type:
                query = self._clear_graph_edges_query % (
                    self.node_label,
                    self.relationship_type,
                    self.node_label
                )
                session.run(query)
            query = self._clear_graph_nodes_query % (self.node_label)
            session.run(query)
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
            CREATE CONSTRAINT ON (c:Character) ASSERT c.name IS UNIQUE;
            """)

            session.run("""\
            LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/mathbeveridge/asoiaf/master/data/asoiaf-book1-edges.csv" AS row
            MERGE (src:Character {name: row.Source})
            MERGE (tgt:Character {name: row.Target})
            // relationship for the book
            MERGE (src)-[r:INTERACTS1]->(tgt)
            ON CREATE SET r.weight = toInteger(row.weight), r.book=1
            """)

            session.run("""\
            LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/mathbeveridge/asoiaf/master/data/asoiaf-book2-edges.csv" AS row
            MERGE (src:Character {name: row.Source})
            MERGE (tgt:Character {name: row.Target})
            // relationship for the book
            MERGE (src)-[r:INTERACTS2]->(tgt)
            ON CREATE SET r.weight = toInteger(row.weight), r.book=2
            """)

            session.run("""\
            LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/mathbeveridge/asoiaf/master/data/asoiaf-book3-edges.csv" AS row
            MERGE (src:Character {name: row.Source})
            MERGE (tgt:Character {name: row.Target})
            // relationship for the book
            MERGE (src)-[r:INTERACTS3]->(tgt)
            ON CREATE SET r.weight = toInteger(row.weight), r.book=3
            """)

            session.run("""\
            LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/mathbeveridge/asoiaf/master/data/asoiaf-book45-edges.csv" AS row
            MERGE (src:Character {name: row.Source})
            MERGE (tgt:Character {name: row.Target})
            // relationship for the book
            MERGE (src)-[r:INTERACTS45]->(tgt)
            ON CREATE SET r.weight = toInteger(row.weight), r.book=45
            """)
        with self.driver.session() as session:
            session.run("""\
            DROP CONSTRAINT ON (c:Character) ASSERT c.name IS UNIQUE;
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
        with self.driver.session() as session:
            session.run("""\
            DROP CONSTRAINT ON (p:Place) ASSERT p.name IS UNIQUE
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
        with self.driver.session() as session:
            session.run("""\
            DROP CONSTRAINT ON(u:User) ASSERT u.id IS unique
            """)
