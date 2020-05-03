from nxneo4j.base_graph import BaseGraph


class Graph(BaseGraph):
    def __init__(self, driver, config=None):
        super().__init__(driver, "UNDIRECTED", config)
