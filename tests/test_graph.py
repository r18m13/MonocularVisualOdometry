import unittest
import numpy as np

from src.map_software.graph import Graph


class GraphTests(unittest.TestCase):
    def test_node_and_edge_storage(self):
        graph = Graph()
        pose = np.eye(4)
        graph.add_node(0, pose)
        graph.add_node(1, pose)
        graph.add_edge(0, 1, pose)

        self.assertEqual(len(graph.nodes), 2)
        self.assertEqual(len(graph.edges), 1)
        np.testing.assert_array_equal(graph.nodes[0]["pose"], pose)


if __name__ == "__main__":
    unittest.main()
