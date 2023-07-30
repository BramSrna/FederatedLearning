
from src.client.client import Client
from src.node.node import Node
from src.aggregator.aggregator import Aggregator

class FullBot(Client, Node, Aggregator):
    def __init__(self, bcfl_connector, data_generator):
        Client.__init__(self, bcfl_connector, data_generator)
        Node.__init__(self, bcfl_connector)
        Aggregator.__init__(self, bcfl_connector)