class ClientConfig(object):
    def __init__(self, data_threshold):
        self.data_threshold = data_threshold

    def get_data_threshold(self):
        return self.data_threshold