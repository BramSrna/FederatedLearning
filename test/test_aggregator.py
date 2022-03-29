import logging
import unittest

from src.model import Model
from src.aggregator import Aggregator
import numpy as np
from sklearn import linear_model

class TestAggregator(unittest.TestCase):
    def test_empty_model_returned_when_no_models_passed_into_aggregator(self):
        test_aggregator = Aggregator([], [], 1)
        aggregated_model = test_aggregator.handle_aggregation_selection_victory()
        self.assertEqual(Model(), aggregated_model)

    def test_aggregator_averages_the_intercept_values(self):
        test_aggregator = Aggregator([], [], 3)

        n_samples, n_features = 10, 5

        np.random.seed(0)

        targets = np.random.randn(n_samples)
        data = np.random.randn(n_samples, n_features)
        test_model_1 = Model()
        test_model_1.train(data, targets)
        test_aggregator.receive_valid_model(test_model_1, data, targets)

        targets = np.random.randn(n_samples)
        data = np.random.randn(n_samples, n_features)
        test_model_2 = Model()
        test_model_2.train(data, targets)
        test_aggregator.receive_valid_model(test_model_2, data, targets)

        targets = np.random.randn(n_samples)
        data = np.random.randn(n_samples, n_features)
        test_model_3 = Model()
        test_model_3.train(data, targets)
        test_aggregator.receive_valid_model(test_model_3, data, targets)

        min_intercept = min([test_model_1.get_intercept(), test_model_2.get_intercept(), test_model_3.get_intercept()])
        max_intercept = max([test_model_1.get_intercept(), test_model_2.get_intercept(), test_model_3.get_intercept()])

        aggregated_intercept = test_aggregator.get_aggregated_model().get_intercept()

        self.assertGreater(aggregated_intercept, min_intercept)
        self.assertLess(aggregated_intercept, max_intercept)

    def test_aggregator_averages_the_coef_values(self):
        test_aggregator = Aggregator([], [], 3)
        
        n_samples, n_features = 10, 5

        np.random.seed(0)

        targets = np.random.randn(n_samples)
        data = np.random.randn(n_samples, n_features)
        test_model_1 = Model()
        test_model_1.train(data, targets)
        test_aggregator.receive_valid_model(test_model_1, data, targets)

        targets = np.random.randn(n_samples)
        data = np.random.randn(n_samples, n_features)
        test_model_2 = Model()
        test_model_2.train(data, targets)
        test_aggregator.receive_valid_model(test_model_2, data, targets)

        targets = np.random.randn(n_samples)
        data = np.random.randn(n_samples, n_features)
        test_model_3 = Model()
        test_model_3.train(data, targets)
        test_aggregator.receive_valid_model(test_model_3, data, targets)

        aggregated_coefs = test_aggregator.get_aggregated_model().get_coef()

        for i in range(len(test_model_1.get_coef())):
            min_coef = min([test_model_1.get_coef()[i], test_model_2.get_coef()[i], test_model_3.get_coef()[i]])
            max_coef = max([test_model_1.get_coef()[i], test_model_2.get_coef()[i], test_model_3.get_coef()[i]])

            agg_coef = aggregated_coefs[i]

            self.assertGreater(agg_coef, min_coef)
            self.assertLess(agg_coef, max_coef)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
