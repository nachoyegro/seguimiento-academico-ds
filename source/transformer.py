from pandas.io.json import json_normalize


class DataTransformer:

    def transform_to_dataframe(self, data):
        return json_normalize(data)
