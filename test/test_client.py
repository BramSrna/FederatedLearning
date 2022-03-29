import logging
import unittest

from src.client import Client
import numpy as np
from sklearn import linear_model
from src.model import Model


class TestClient(unittest.TestCase):
    def test_basic_sgd_regression_client_can_initialize_from_empty(self):
        n_samples, n_features = 10, 5

        data_threshold = 10

        np.random.seed(0)

        test_model = Model()
        test_client = Client(test_model, data_threshold, [])

        new_x = []
        new_y = []

        for _ in range(data_threshold):
            curr_x = np.random.randn(1, n_features)[0]
            curr_y = np.random.randn(1)[0]

            new_x.append(curr_x)
            new_y.append(curr_y)

            test_client.add_data_point(curr_x, curr_y)

        new_x = np.array(new_x)
        new_y = np.array(new_y)

        score = test_client.run_score(new_x, new_y)

        self.assertGreater(score, 0)

    def test_basic_sgd_regression_client_loads_model_properly(self):
        n_samples, n_features = 10, 5

        np.random.seed(0)

        test_model = Model()
        test_targets = np.random.randn(n_samples)
        test_data = np.random.randn(n_samples, n_features)
        test_model.train(test_data, test_targets)

        expected_score = test_model.get_score(test_data, test_targets)

        test_client = Client(test_model, 0, [])

        actual_score = test_client.run_score(test_data, test_targets)

        self.assertEqual(expected_score, actual_score)

    def test_basic_sgd_regression_client_can_continue_learning(self):
        n_samples, n_features = 10, 5

        np.random.seed(0)

        test_model = Model()
        test_targets = np.random.randn(n_samples)
        test_data = np.random.randn(n_samples, n_features)
        test_model.train(test_data, test_targets)

        data_threshold = 10

        test_client = Client(test_model, data_threshold, [])

        new_x = []
        new_y = []

        for _ in range(data_threshold):
            curr_x = np.random.randn(1, n_features)[0]
            curr_y = np.random.randn(1)[0]

            new_x.append(curr_x)
            new_y.append(curr_y)

            test_client.add_data_point(curr_x, curr_y)

        new_x = np.array(new_x)
        new_y = np.array(new_y)

        old_score = test_model.get_score(new_x, new_y)
        new_score = test_client.run_score(new_x, new_y)

        self.assertGreater(new_score, old_score)

    def test_initializing_coefs_and_intercept_results_in_different_model(self):
        n_samples, n_features = 10, 5

        np.random.seed(0)

        data_threshold = 10

        test_init_model = Model()
        test_targets = np.random.randn(n_samples)
        test_data = np.random.randn(n_samples, n_features)
        test_init_model.train(test_data, test_targets)

        test_uninit_model = Model()

        test_uninit_client = Client(test_uninit_model, data_threshold, [])
        test_init_client = Client(test_init_model, data_threshold, [])

        new_x = []
        new_y = []

        for _ in range(10):
            curr_x = np.random.randn(1, n_features)[0]
            curr_y = np.random.randn(1)[0]

            new_x.append(curr_x)
            new_y.append(curr_y)

            test_init_client.add_data_point(curr_x, curr_y)
            test_uninit_client.add_data_point(curr_x, curr_y)

        new_x = np.array(new_x)
        new_y = np.array(new_y)

        init_score = test_init_client.run_score(new_x, new_y)
        uninit_score = test_uninit_client.run_score(new_x, new_y)

        self.assertNotEqual(init_score, uninit_score)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
