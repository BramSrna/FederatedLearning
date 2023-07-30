class DataPointPool(object):
    def __init__(self):
        self.data_points = []

    def notify_new_block(self, new_block):
        self.data_points = []

    def add_new_points(self, new_data_points):
        for data_point in new_data_points:
            if data_point not in self.data_points:
                self.data_points.append(data_point)

    def get_data_points(self):
        return self.data_points

    def convert_current_state_to_block_savable_obj(self):
       return self.data_points