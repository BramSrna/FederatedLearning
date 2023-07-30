class BcflConnector(object):
    def __init__(self, model_class, client_config, node_config, aggregator_config):
        self.model_class = model_class
        self.client_config = client_config
        self.node_config = node_config
        self.aggregator_config = aggregator_config

        self.client_list = []
        self.node_list = []
        self.aggregator_list = []

    def add_new_client(self, new_client):
        self.client_list.append(new_client)
        for node in self.node_list:
            node.add_node(new_client)

    def add_new_node(self, new_node):
        self.node_list.append(new_node)
        for client in self.client_list:
            client.add_node(new_node)
        for node in self.node_list:
            node.add_node(new_node)
        for aggregator in self.aggregator_list:
            aggregator.add_node(new_node)

    def add_new_aggregator(self, new_aggregator):
        self.aggregator_list.append(new_aggregator)
        for node in self.node_list:
            node.add_aggregator(new_aggregator)

    def get_node_list(self):
        return self.node_list
    
    def get_model_class(self):
        return self.model_class
    
    def get_client_config(self):
        return self.client_config
    
    def get_aggregator_config(self):
        return self.aggregator_config

    def get_aggregator_list(self):
        return self.aggregator_list
    
    def get_client_list(self):
        return self.client_list