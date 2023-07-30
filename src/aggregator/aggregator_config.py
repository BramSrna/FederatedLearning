class AggregatorConfig(object):
    def __init__(self, aggregation_threshold):
        self.aggregation_threshold = aggregation_threshold

    def get_aggregation_threshold(self):
        return self.aggregation_threshold