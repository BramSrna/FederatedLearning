import logging
import unittest

from src.node import Node
from src.aggregator import Aggregator
import numpy as np
from src.model import Model


class TestNodeAggregatorInterop(unittest.TestCase):
    def test_nodes_forward_validated_models_to_aggregators(self):
        test_node = Node([], [], [])

        test_aggregator = Aggregator([], [], 3)

        test_node.add_aggregator(test_aggregator)

        test_aggregator.add_node(test_node)

        n_samples, n_features = 10, 5

        test_targets = np.random.randn(n_samples)
        test_data = np.random.randn(n_samples, n_features)
        test_model = Model()
        test_model.train(test_data, test_targets)

        self.assertFalse(test_aggregator.isModelInPool(test_model))

        test_node.receive_candidate_model(test_model, test_data, test_targets)

        self.assertTrue(test_aggregator.isModelInPool(test_model))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
