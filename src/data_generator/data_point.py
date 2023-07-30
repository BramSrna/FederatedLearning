class DataPoint(object):
    def __init__(self, data, target):
        self.id = id(self)
        self.data = data
        self.target = target

    def get_id(self):
        return self.id

    def get_data(self):
        return self.data
    
    def get_target(self):
        return self.target
    
    def __eq__(self, second_data_point):
        if self.id != second_data_point.get_id():
            return False
        
        if self.data != second_data_point.get_data():
            return False
        
        if self.target != second_data_point.get_target():
            return False
        
        return True