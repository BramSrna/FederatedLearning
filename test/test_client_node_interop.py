import logging
import unittest

from unittest.mock import patch
from src.client import Client
from src.node import Node
import numpy as np
from src.model import Model


class TestClientNodeInterop(unittest.TestCase):
    def test_new_local_models_are_propagated_from_clients_to_all_nodes(self):
        test_node = Node([], [], [])

        test_model = Model()
        test_data_threshold = 100
        test_client = Client(test_model, test_data_threshold, [test_node])

        old_model = test_client.get_local_model()

        with patch.object(test_node, 'receive_candidate_model') as mock:
            for _ in range(test_data_threshold):
                curr_x = np.random.randn(1, 5)[0]
                curr_y = np.random.randn(1)[0]

                test_client.add_data_point(curr_x, curr_y)

            mock.assert_called()

        new_model = test_client.get_local_model()

        self.assertNotEqual(test_model, new_model)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
