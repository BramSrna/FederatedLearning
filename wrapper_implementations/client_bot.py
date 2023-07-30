from src.client.client import Client
from src.node.node import Node
from src.aggregator.aggregator import Aggregator

class ClientBot(Client):
    def __init__(self, bcfl_connector, data_generator):
        Client.__init__(self, bcfl_connector, data_generator)