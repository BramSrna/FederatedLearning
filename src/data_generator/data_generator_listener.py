class DataGeneratorListener(object):
    def __init__(self):
        pass

    def notify_new_data_point(self, new_data_point):
        raise NotImplementedError("ERROR: The notify_new_data_point method must be implemented by the child class.")