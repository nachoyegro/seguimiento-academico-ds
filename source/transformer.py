import pandas as pd

class DataTransformer:

    def __init__(self, data):
        """
            :data is a json
        """
        self.data = data

    def transform_to_dataframe(self):
        return pd.read_json(self.data)