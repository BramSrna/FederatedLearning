from src.client.client import Client
from src.node.node import Node
from src.aggregator.aggregator import Aggregator

class NodeBot(Node):
    def __init__(self, bcfl_connector):
        Node.__init__(self, bcfl_connector)