def shortest_weighted_path(G,source, target, weight):
    if source is None:
        if target is None:
            # Find paths between all pairs.
            if weight is None:
                # paths = dict(nx.all_pairs_shortest_path(G))
                paths = {}
            else:
                # paths = dict(nx.all_pairs_dijkstra_path(G, weight=weight))
                paths = {}
        else:
            # Find paths from all nodes co-accessible to the target.
            if weight is None:
                # paths = nx.single_source_shortest_path(G, target)
                # paths = G.single_source_shortest_path(target)
                paths = []
            else:
                # paths = nx.single_source_dijkstra_path(G, target,
                #                                        weight=weight)
                paths = []
    else:
        if target is None:
            # Find paths to all nodes accessible from the source.
            if weight is None:
                # paths = nx.single_source_shortest_path(G, source)
                paths = []
                # paths = G.single_source_shortest_path(source)
            else:
                # paths = nx.single_source_dijkstra_path(G, source,
                #                                        weight=weight)
                paths = []
        else:

            query = """\
            MATCH (source:%s   {%s: $source })
            MATCH (target:%s   {%s: $target })

            CALL gds.alpha.shortestPath.stream({
                nodeProjection: $node_label,
                relationshipProjection: {
                    relType: {
                        type: $relationship_type,
                        orientation: $direction,
                        properties: {}
                    }
                },
                startNode: source,
                endNode: target,
                relationshipWeightProperty: $weight,
                relationshipProperties: [$weight]
            })
            YIELD nodeId, cost
            RETURN gds.util.asNode(nodeId).%s AS node, cost
            """ % (
                G.node_label,
                G.identifier_property,
                G.node_label,
                G.identifier_property,
                G.identifier_property
            )

            with G.driver.session() as session:
                params = G.base_params()
                params["source"] = source
                params["target"] = target
                params["weight"] = weight

                paths = [row["node"] for row in session.run(query, params)]
    return paths

def shortest_path(G,source, target):
    return shortest_weighted_path(G,source, target, weight='')
