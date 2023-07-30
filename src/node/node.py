from src.model.model import Model
from src.blockchain.blockchain import Blockchain
from src.blockchain.block import Block

# https://www.oreilly.com/library/view/mastering-bitcoin/9781491902639/ch08.html
class Node(object):
    def __init__(self, bcfl_connector):
        self.bcfl_connector = bcfl_connector

        self.node_list = []
        self.aggregator_list = []
        self.client_list = []
        
        self.blockchain = Blockchain()

        self.sync_node_bcfl_state()
        self.clone_blockchain()

    def sync_node_bcfl_state(self):
        self.bcfl_connector.add_new_node(self)

        for node in self.bcfl_connector.get_node_list():
            self.add_node(node)
        for aggregator in self.bcfl_connector.get_aggregator_list():
            self.add_aggregator(aggregator)
        for client in self.bcfl_connector.get_client_list():
            self.add_client(client)

    def add_client(self, new_client):
        if (new_client not in self.client_list):
            self.client_list.append(new_client)

    def add_node(self, new_node):
        if (new_node not in self.node_list) and (new_node is not self):
            self.node_list.append(new_node)

    def add_aggregator(self, new_aggregator):
        if (new_aggregator not in self.aggregator_list):
            self.aggregator_list.append(new_aggregator)

    def clone_blockchain(self):
        if len(self.node_list) > 0:
            blockchain_to_copy = self.node_list[0].get_blockchain()
            for block in blockchain_to_copy.get_blocks():
                self.notify_new_block(block, False)

    def get_curr_blockchain_model(self):
        curr_model = self.bcfl_connector.get_model_class()()
        if not self.blockchain.is_empty():
            curr_model = self.blockchain.get_newest_block().get_model()
        return curr_model

    def receive_candidate_model(self, new_model, validation_data_points):
        test_score = new_model.get_score(validation_data_points)
        curr_model = self.get_curr_blockchain_model()
        if (curr_model is not None) or (test_score > curr_model.get_score(validation_data_points)):
            for aggregator in self.aggregator_list:
                aggregator.receive_valid_model(new_model, validation_data_points)

    def notify_new_block_info(self, aggregated_model, data_point_pool):
        new_block = Block(aggregated_model, data_point_pool)
        self.blockchain.add_block(new_block)
        for client in self.client_list:
            client.notify_new_global_model(new_block)
        for node in self.node_list:
            node.notify_new_block(new_block, True)
        for aggregator in self.aggregator_list:
            aggregator.notify_new_aggregation(new_block)
            
    def notify_new_block(self, new_block, notify_clients):
        if new_block.run_proof_of_validation():
            self.blockchain.add_block(new_block)
            if notify_clients:
                for client in self.client_list:
                    client.notify_new_global_model(new_block)

    def get_aggregator_config(self):
        if not self.blockchain.is_empty():
            return self.blockchain.get_newest_block().get_aggregator_config()
        else:
            return self.bcfl_connector.get_aggregator_config()
        
    def get_blockchain(self):
        return self.blockchain
    
    def get_client_config(self):
        if not self.blockchain.is_empty():
            return self.blockchain.get_newest_block().get_client_config()
        else:
            return self.bcfl_connector.get_client_config()

