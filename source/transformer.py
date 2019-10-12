from pandas.io.json import json_normalize

class DataTransformer:

    def __init__(self, data):
        """
            :data is a json
        """
        self.data = data

    def transform_to_dataframe(self):
        return json_normalize(self.data)