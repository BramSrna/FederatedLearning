import logging
import unittest

from src.node import Node
from src.model import Model


class TestNode(unittest.TestCase):
    def test_blockchain_is_initialized_by_node_when_chain_does_not_exist(self):
        test_node = Node([], [], [])

        curr_model = test_node.get_curr_blockchain_model()

        empty_model = Model()

        self.assertEqual(empty_model, curr_model)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
