from pandas.io.json import json_normalize
import pandas as pd


class DataTransformer:

    def transform_to_dataframe(self, data):
        return json_normalize(data)

    def merge_materias_con_plan(self, materias, plan):
        materias.rename(columns={'materia': 'codigo'}, inplace=True)
        return pd.merge(materias, plan, on=['codigo'])
