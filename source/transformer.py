from pandas.io.json import json_normalize
import pandas as pd


class DataTransformer:

    def transform_to_dataframe(self, data):
        return json_normalize(data)

    def transform_materiascursadas_to_dataframe(self, data):
        materias = json_normalize(data)
        materias.rename(columns={'materia': 'codigo'}, inplace=True)
        return materias

    def merge_materias_con_plan(self, materias, plan):
        return pd.merge(materias, plan, on=['codigo'])

    def transform_timestamp_to_date(self, timestamp):
        from datetime import datetime
        return datetime.strptime(str(timestamp), '%Y-%m-%d %H:%M:%S')

    def transform_date_to_semester(self, date):
        """
            Las fechas que pueden venir son julio o diciembre
        """
        if date.month == 1:
            # Como los datos se agrupan de a 6 meses, el primer semestre lo pone como mes 1
            return '{}-S1'.format(date.year)
        else:
            return '{}-S2'.format(date.year)

    def transform_timestamp_to_semester(self, timestamp):
        import datetime
        date = self.transform_timestamp_to_date(timestamp)
        semester = self.transform_date_to_semester(date)
        return semester