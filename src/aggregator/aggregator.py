import random
from src.model.model import Model
import numpy as np
from src.blockchain.block import Block
from src.aggregator.data_point_pool import DataPointPool
from src.aggregator.model_pool import ModelPool


class Aggregator(object):
    def __init__(self, bcfl_connector):
        self.bcfl_connector = bcfl_connector
        
        self.node_list = []
        self.aggregation_threshold = -1
        self.aggregated_model = None

        self.model_pool = ModelPool()
        self.data_point_pool = DataPointPool()

        self.sync_aggregator_bcfl_state()

    def sync_aggregator_bcfl_state(self):
        self.bcfl_connector.add_new_aggregator(self)
        for node in self.bcfl_connector.get_node_list():
            self.add_node(node)

        self.aggregated_model = self.bcfl_connector.get_model_class()
        aggregator_config = self.bcfl_connector.get_aggregator_config()
        self.aggregation_threshold = aggregator_config.get_aggregation_threshold()
        
        if len(self.node_list) > 0:
            self.aggregated_model = self.node_list[0].get_curr_blockchain_model()
            aggregator_config = self.node_list[0].get_aggregator_config()
            self.aggregation_threshold = aggregator_config.get_aggregation_threshold()

    def get_model_pool(self):
        return self.model_pool

    def add_node(self, new_node):
        if new_node not in self.node_list:
            self.node_list.append(new_node)

    def get_aggregated_model(self):
        return self.model_pool.get_aggregated_model()

    def notify_new_aggregation(self, new_block):
        self.data_point_pool.notify_new_block(new_block)
        self.model_pool.notify_new_block(new_block)

    def aggregate_received_information(self):
        aggregated_model = self.model_pool.get_aggregated_model()
        aggregated_data_point_pool = self.data_point_pool.get_data_points()

        # Update notify_new_block_aggregated_model to determine the changes and create the new block
        # The node then notifies the clients, other nodes, and the aggregators about the new block
        if len(self.node_list) > 0:
            random_node_ind = random.randint(0, len(self.node_list) - 1)
            self.node_list[random_node_ind].notify_new_block_info(aggregated_model, aggregated_data_point_pool)
        
        return aggregated_model

    def receive_valid_model(self, new_model, validation_data_points):
        self.model_pool.add_model_candidate(new_model)     
        self.data_point_pool.add_new_points(validation_data_points)
        if self.model_pool.get_size() >= self.aggregation_threshold:
            self.aggregate_received_information()



