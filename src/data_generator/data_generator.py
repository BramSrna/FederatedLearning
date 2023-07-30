class DataGenerator(object):
    def __init__(self):
        self.listeners = []

    def add_listener(self, new_listener):
        self.listeners.append(new_listener)

    def generate_data_point(self):
        new_data_point = self.create_new_data_point()
        for listener in self.listeners:
            listener.notify_new_data_point(new_data_point)
        return new_data_point

    def create_new_data_point(self):
        raise NotImplementedError("ERROR: The create_new_data_point method must be implemented by the child class.")