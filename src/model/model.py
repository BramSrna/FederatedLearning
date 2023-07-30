from sklearn import linear_model
from src.blockchain.block import Block
import copy

# https://scikit-learn.org/0.15/modules/generated/sklearn.linear_model.SGDRegressor.html#sklearn.linear_model.SGDRegressor.partial_fit
# https://scikit-learn.org/0.15/modules/scaling_strategies.html

class Model(object):
    def __init__(self):
        pass

    def train(self, data, targets):
        raise NotImplementedError("ERROR: The train method must be implemented by the child class.")

    def get_score(self, datapoints):
        raise NotImplementedError("ERROR: The get_score method must be implemented by the child class.")

    def set_from_block(self, block):
        raise NotImplementedError("ERROR: The set_from_block method must be implemented by the child class.")
    
    def predict(self, data):
        raise NotImplementedError("ERROR: The predict method must be implemented by the child class.")

    def aggregate_models(self, model_list):
        raise NotImplementedError("ERROR: The aggregate_models method must be implemented by the child class.")