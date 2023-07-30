import numpy as np
from src.model.model import Model
import copy
from src.data_generator.data_generator_listener import DataGeneratorListener

class Client(DataGeneratorListener):
    def __init__(self, bcfl_connector, data_generator):
        self.bcfl_connector = bcfl_connector
        self.data_generator = data_generator

        self.local_model = None
        self.data_threshold = -1
        self.node_list = []

        self.data_points = []

        self.sync_client_bcfl_state()
        self.data_generator.add_listener(self)

    def add_node(self, new_node):
        if new_node not in self.node_list:
            self.node_list.append(new_node)

    def notify_new_data_point(self, new_data_point):
        self.data_points.append(new_data_point)

        if len(self.data_points) % self.data_threshold == 0:
            self.retrain_model()

    def sync_client_bcfl_state(self):
        self.bcfl_connector.add_new_client(self)
        for node in self.bcfl_connector.get_node_list():
            self.add_node(node)

        self.local_model = self.bcfl_connector.get_model_class()()
        client_config = self.bcfl_connector.get_client_config()
        self.data_threshold = client_config.get_data_threshold()
        
        if len(self.node_list) > 0:
            self.local_model = self.node_list[0].get_curr_blockchain_model()
            client_config = self.node_list[0].get_client_config()
            self.data_threshold = client_config.get_data_threshold()

    def run_score(self, data_points):
        return self.local_model.get_score(data_points)

    def get_local_model(self):
        return self.local_model

    def retrain_model(self):
        train_percent = 0.80

        test_start_ind = int(len(self.data_points) * train_percent)

        train_data_points = self.data_points[:test_start_ind]
        test_data_points = self.data_points[test_start_ind:]

        self.local_model.train(train_data_points)

        score = self.local_model.get_score(test_data_points)
        if score > -1.0:
            self.send_validated_model(self.local_model, test_data_points)

    def send_validated_model(self, model, validation_data_points):
        for node in self.node_list:
            node.receive_candidate_model(model, validation_data_points)

    def notify_new_global_model(self, new_block):
        self.local_model.set_from_block(new_block)

