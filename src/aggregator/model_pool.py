class ModelPool(object):
    def __init__(self):
        self.model_candidates = []
        self.aggregated_model = None

    def notify_new_block(self, new_block):
        self.model_candidates = []

    def add_model_candidate(self, new_candidate):
        self.model_candidates.append(new_candidate)

        self.aggregated_model = self.model_candidates[0]
        if len(self.model_candidates) > 1:
            self.aggregated_model.aggregate_models(self.model_candidates[1:])

    def get_size(self):
        return len(self.model_candidates)
    
    def get_aggregated_model(self):
        return self.aggregated_model