import logging
import unittest

from src.central_connector import CentralConnector
from src.full_bot import FullBot
import numpy as np


class TestE2eFullyCoupledBcfl(unittest.TestCase):
    def test_fully_coupled_bcfl_bots_will_connect_to_each_other_on_creation(self):
        test_central_connector = CentralConnector()

        test_bot_1 = FullBot(test_central_connector, 1, 1)

        self.assertEqual([], test_bot_1.get_bot_list())

        test_bot_2 = FullBot(test_central_connector, 1, 1)

        self.assertIn(test_bot_2, test_bot_1.get_bot_list())
        self.assertIn(test_bot_1, test_bot_2.get_bot_list())

        test_bot_3 = FullBot(test_central_connector, 1, 1)

        self.assertIn(test_bot_2, test_bot_1.get_bot_list())
        self.assertIn(test_bot_3, test_bot_1.get_bot_list())
        self.assertIn(test_bot_1, test_bot_2.get_bot_list())
        self.assertIn(test_bot_3, test_bot_2.get_bot_list())
        self.assertIn(test_bot_1, test_bot_3.get_bot_list())
        self.assertIn(test_bot_2, test_bot_3.get_bot_list())

    def test_clients_receive_aggregated_model_at_the_end_of_the_cycle(self):
        # Client will make a new local model every 100 data points
        test_data_threshold = 100

        # Change nodes to forward models to aggregators right after validation

        # Aggregator will aggregate model after receiveing 3 models
        aggregation_threshold = 3

        # Change aggregator to notify other aggregators once a new model has been created

        test_central_connector = CentralConnector()

        test_bot_1 = FullBot(test_central_connector, test_data_threshold, aggregation_threshold)
        test_bot_2 = FullBot(test_central_connector, test_data_threshold, aggregation_threshold)
        test_bot_3 = FullBot(test_central_connector, test_data_threshold, aggregation_threshold)

        n_samples, n_features = 10, 5

        np.random.seed(0)

        for _ in range(test_data_threshold):
            curr_x = np.random.randn(1, n_features)[0]
            curr_y = np.random.randn(1)[0]

            test_bot_1.add_data_point(curr_x, curr_y)

        old_test_bot_1_model = test_bot_1.get_local_model()
        print(old_test_bot_1_model)

        for _ in range(test_data_threshold):
            curr_x = np.random.randn(1, n_features)[0]
            curr_y = np.random.randn(1)[0]

            test_bot_2.add_data_point(curr_x, curr_y)
        print(old_test_bot_1_model)

        old_test_bot_2_model = test_bot_2.get_local_model()

        print(old_test_bot_2_model)

        self.assertNotEqual(old_test_bot_1_model, old_test_bot_2_model)

        for _ in range(test_data_threshold):
            curr_x = np.random.randn(1, n_features)[0]
            curr_y = np.random.randn(1)[0]

            test_bot_3.add_data_point(curr_x, curr_y)

        new_test_bot_1_model = test_bot_1.get_local_model()
        new_test_bot_2_model = test_bot_2.get_local_model()
        new_test_bot_3_model = test_bot_3.get_local_model()

        self.assertEqual(new_test_bot_1_model, new_test_bot_2_model)
        self.assertEqual(new_test_bot_2_model, new_test_bot_3_model)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
