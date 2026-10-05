"""Trajectory graph representation."""

import networkx as nx


class Graph:
    """Stores estimated camera poses and relative transformations.

    This class is a data structure only. It does not perform graph
    optimization or loop-closure correction.
    """

    def __init__(self):
        self.graph = nx.Graph()

    @property
    def nodes(self):
        return self.graph.nodes

    @property
    def edges(self):
        return self.graph.edges

    def add_node(self, index, pose):
        self.graph.add_node(index, pose=pose)

    def add_edge(self, start, end, transformation):
        self.graph.add_edge(start, end, transformation=transformation)

    def optimize_graph(self):
        """Reserved for a future optimization implementation.

        The current project intentionally does not claim to optimize the
        trajectory graph.
        """
        raise NotImplementedError(
            "Graph optimization is not implemented in this prototype."
        )
