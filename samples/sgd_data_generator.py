import random

from src.data_generator.data_generator import DataGenerator
from src.data_generator.data_point import DataPoint

class SgdDataGenerator(DataGenerator):
    def __init__(self):
        super().__init__()

    def create_new_data_point(self):
        val_1 = random.randint(0, 9)
        val_2 = random.randint(0, 9)
        total = val_1 + val_2
        return DataPoint([val_1, val_2], total)