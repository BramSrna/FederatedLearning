class Block(object):
    def __init__(self, model, data_point_pool):
        self.model = model
        self.data_point_pool = data_point_pool

    def run_proof_of_validation(self):
        score = self.model.get_score(self.data_point_pool)
        return score > -1.0

    def set_data_point_pool(self, new_data_point_pool):
        self.data_point_pool = new_data_point_pool

    def get_model(self):
        return self.model
    
    def get_data_point_pool(self):
        return self.data_point_pool
    
    def __eq__(self, second_block):
        if second_block.get_model() != self.model:
            return False
        
        if second_block.get_data_point_pool() != self.data_point_pool:
            return False
        
        print("ICI")
        return True