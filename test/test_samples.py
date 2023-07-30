import logging
import unittest

from wrapper_implementations.bcfl_connector import BcflConnector
from wrapper_implementations.full_bot import FullBot
import numpy as np
from samples.sgd_data_generator import SgdDataGenerator
from samples.sgd_model import SgdModel
from src.client.client_config import ClientConfig
from src.aggregator.aggregator_config import AggregatorConfig
from src.model.model import Model
from wrapper_implementations.node_bot import NodeBot
from wrapper_implementations.aggregator_bot import AggregatorBot
from wrapper_implementations.client_bot import ClientBot
from src.node.node_config import NodeConfig


class TestSamples(unittest.TestCase):
    def test_sgd_regressor_seperate_components(self):
        data_threshold = 100
        aggregation_threshold = 1
        client_config = ClientConfig(data_threshold)
        node_config = NodeConfig()
        aggregator_config = AggregatorConfig(aggregation_threshold)
        bcfl_connector = BcflConnector(SgdModel, client_config, node_config, aggregator_config)
        data_generator = SgdDataGenerator()
        test_client = ClientBot(bcfl_connector, data_generator)
        test_node = NodeBot(bcfl_connector)
        test_aggregator = AggregatorBot(bcfl_connector)
        num_blocks_to_gen = 3
        start_blockchain_len = test_node.get_blockchain().get_length()
        for _ in range(data_threshold * aggregation_threshold * num_blocks_to_gen):
            data_generator.generate_data_point()
        end_blockchain_len = test_node.get_blockchain().get_length()
        self.assertEqual(start_blockchain_len + num_blocks_to_gen, end_blockchain_len)
        generated_model = test_aggregator.get_aggregated_model()
        second_data_generator = SgdDataGenerator()
        for _ in range(10):
            data_point = second_data_generator.generate_data_point()
            expected_val = data_point.get_target()
            actual_val = generated_model.predict(data_point)[0]
            self.assertAlmostEqual(expected_val, actual_val, 0)

    def test_sgd_regressor_one_full_bot(self):
        data_threshold = 100
        aggregation_threshold = 1
        client_config = ClientConfig(data_threshold)
        node_config = NodeConfig()
        aggregator_config = AggregatorConfig(aggregation_threshold)
        bcfl_connector = BcflConnector(SgdModel, client_config, node_config, aggregator_config)
        data_generator = SgdDataGenerator()
        test_bot = FullBot(bcfl_connector, data_generator)
        num_blocks_to_gen = 3
        start_blockchain_len = test_bot.get_blockchain().get_length()
        for _ in range(data_threshold * aggregation_threshold * num_blocks_to_gen):
            data_generator.generate_data_point()
        end_blockchain_len = test_bot.get_blockchain().get_length()
        self.assertEqual(start_blockchain_len + num_blocks_to_gen, end_blockchain_len)
        generated_model = test_bot.get_aggregated_model()
        second_data_generator = SgdDataGenerator()
        for _ in range(10):
            data_point = second_data_generator.generate_data_point()
            expected_val = data_point.get_target()
            actual_val = generated_model.predict(data_point)[0]
            self.assertAlmostEqual(expected_val, actual_val, 0)

    def test_sgd_regressor_multiple_full_bots(self):
        data_threshold = 100
        aggregation_threshold = 1
        client_config = ClientConfig(data_threshold)
        node_config = NodeConfig()
        aggregator_config = AggregatorConfig(aggregation_threshold)
        bcfl_connector = BcflConnector(SgdModel, client_config, node_config, aggregator_config)
        data_generator_1 = SgdDataGenerator()
        data_generator_2 = SgdDataGenerator()
        data_generator_3 = SgdDataGenerator()
        test_bot_1 = FullBot(bcfl_connector, data_generator_1)
        test_bot_2 = FullBot(bcfl_connector, data_generator_2)
        test_bot_3 = FullBot(bcfl_connector, data_generator_3)
        start_blockchain_len = test_bot_1.get_blockchain().get_length()
        for _ in range(data_threshold * aggregation_threshold):
            data_generator_1.generate_data_point()
        for _ in range(data_threshold * aggregation_threshold):
            data_generator_2.generate_data_point()
        for _ in range(data_threshold * aggregation_threshold):
            data_generator_3.generate_data_point()
        end_blockchain_len = test_bot_3.get_blockchain().get_length()
        self.assertEqual(start_blockchain_len + 3, end_blockchain_len)
        generated_model = test_bot_2.get_aggregated_model()
        second_data_generator = SgdDataGenerator()
        for _ in range(10):
            data_point = second_data_generator.generate_data_point()
            expected_val = data_point.get_target()
            actual_val = generated_model.predict(data_point)[0]
            self.assertAlmostEqual(expected_val, actual_val, 0)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
