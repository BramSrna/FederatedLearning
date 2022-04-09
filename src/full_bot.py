
from src.client import Client
from src.node import Node
from src.aggregator import Aggregator

class FullBot(Client, Node, Aggregator):
    def __init__(self, central_connector, data_threshold, aggregation_threshold):
        self.bot_list = []
        self.node_list = []
        self.aggregator_list = []
        self.client_list = []

        self.central_connector = central_connector
        self.central_connector.add_bot(self)

        Aggregator.__init__(self, self.node_list, self.aggregator_list, aggregation_threshold)
        Node.__init__(self, self.node_list, self.aggregator_list, self.client_list)
        Client.__init__(self, self.get_curr_blockchain_model(), data_threshold, self.node_list)

    def get_bot_list(self):
        return self.bot_list

    def add_new_bot(self, new_bot):
        if new_bot not in self.bot_list:
            self.bot_list.append(new_bot)
            if isinstance(new_bot, Node):
                self.node_list.append(new_bot)
            if isinstance(new_bot, Aggregator):
                self.aggregator_list.append(new_bot)
            if isinstance(new_bot, Client):
                self.client_list.append(new_bot)