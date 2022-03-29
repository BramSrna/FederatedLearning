from src.model import Model

# https://www.oreilly.com/library/view/mastering-bitcoin/9781491902639/ch08.html
class Node(object):
    def __init__(self, node_list, aggregator_list, client_list):
        self.node_list = node_list
        self.aggregator_list = aggregator_list
        self.client_list = client_list

        self.blockchain = []
        self.download_blockchain()

    def add_node(self, new_node):
        self.node_list.append(new_node)

    def add_aggregator(self, new_aggregator):
        self.aggregator_list.append(new_aggregator)

    def download_blockchain(self):
        if len(self.node_list) > 0:
            # TODO: Download blocks from connected nodes
            # Validate blocks as they come in
            # Keep track of latest block
            self.node_list[0].request_blockchain_transfer(self)

    def get_curr_blockchain_model(self):
        curr_model = Model()
        if len(self.blockchain) > 0:
            curr_model.set_from_block(self.blockchain[len(self.blockchain) - 1])
        return curr_model

    def receive_candidate_model(self, new_model, new_validation_data, new_validation_targets):
        test_score = new_model.get_score(new_validation_data, new_validation_targets)
        if test_score > -100:
            for aggregator in self.aggregator_list:
                aggregator.receive_valid_model(new_model, new_validation_data, new_validation_targets)

    def request_blockchain_transfer(self, requester_bot):
        for block in self.blockchain:
            requester_bot.notify_new_block(block, False)

    def notify_new_block(self, new_block, notify_clients):
        if new_block.run_proof_of_validation():
            self.blockchain.append(new_block)
            if notify_clients:
                for client in self.client_list:
                    client.notify_new_global_model(new_block)
