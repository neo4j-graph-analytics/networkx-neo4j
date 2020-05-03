from nxneo4j.base_graph import BaseGraph


class DiGraph(BaseGraph):
    def __init__(self, driver, config=None):
        super().__init__(driver, "NATURAL", config)
