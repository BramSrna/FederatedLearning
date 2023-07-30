from src.client.client import Client
from src.node.node import Node
from src.aggregator.aggregator import Aggregator

class AggregatorBot(Aggregator):
    def __init__(self, bcfl_connector):
        Aggregator.__init__(self, bcfl_connector)