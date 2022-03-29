from src.model import Model
import numpy as np


class Aggregator(object):
    def __init__(self, node_list, aggregator_list, aggregation_threshold):
        self.node_list = node_list
        self.aggregator_list = aggregator_list
        self.aggregation_threshold = aggregation_threshold

        self.aggregated_model = Model()
        self.model_calc_required = False

        self.model_pool = []

    def create_block(self, aggregated_model):
        new_block = aggregated_model.to_block()

        validation_data = None
        validation_targets = None
        if len(self.model_pool) > 0:
            validation_data = self.model_pool[0]["VALIDATION_DATA"]
            validation_targets = self.model_pool[0]["VALIDATION_TARGETS"]
        if len(self.model_pool) > 1:
            i = 1
            while i < len(self.model_pool):
                validation_data = np.concatenate((validation_data, self.model_pool[i]["VALIDATION_DATA"]), axis = 0)
                validation_targets = np.concatenate((validation_targets, self.model_pool[i]["VALIDATION_TARGETS"]), axis = 0)
                i += 1
        new_block.set_validation_data(validation_data)
        new_block.set_validation_targets(validation_targets)

        return new_block

    def get_model_pool(self):
        return self.model_pool

    def add_node(self, new_node):
        self.node_list.append(new_node)

    def get_aggregated_model(self):
        if self.model_calc_required:
            if len(self.model_pool) == 1:
                self.aggregated_model = self.model_pool[0]["MODEL"]
            elif len(self.model_pool) > 1:
                model_list = []
                i = 1
                while i < len(self.model_pool):
                    model_list.append(self.model_pool[i]["MODEL"])
                    i += 1
                self.aggregated_model = self.model_pool[0]["MODEL"].aggregate_models(model_list)

                self.model_calc_required = False
        return self.aggregated_model

    def notify_aggregation_victory(self, included_models):
        for included_model in included_models:
            for local_model in self.model_pool:
                if local_model == included_model:
                    self.model_pool.remove(local_model)

    def handle_aggregation_selection_victory(self):
        for aggregator in self.aggregator_list:
            aggregator.notify_aggregation_victory(self.model_pool)
        aggregated_model = self.get_aggregated_model()
        new_block = self.create_block(aggregated_model)
        for node in self.node_list:
            node.notify_new_block(new_block, True)
        self.model_pool = []
        return self.get_aggregated_model()

    def isModelInPool(self, model_to_check):
        for model in self.model_pool:
            if model["MODEL"] == model_to_check:
                return True
        return False

    def receive_valid_model(self, new_model, new_validation_data, new_validation_targets):
        if self.isModelInPool(new_model):
            return False
        self.model_pool.append({
            "MODEL": new_model,
            "VALIDATION_DATA": new_validation_data,
            "VALIDATION_TARGETS": new_validation_targets
        })
        print(id(self), len(self.model_pool))
        self.model_calc_required = True
        if len(self.model_pool) >= self.aggregation_threshold:
            self.handle_aggregation_selection_victory()



