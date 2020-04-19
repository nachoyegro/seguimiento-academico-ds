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
        if date.month >= 1 and date.month <= 6:
            # Como los datos se agrupan de a 6 meses, el primer semestre lo pone como mes 1
            return '{}-S1'.format(date.year)
        else:
            return '{}-S2'.format(date.year)

    def transform_timestamp_to_semester(self, timestamp):
        import datetime
        date = self.transform_timestamp_to_date(timestamp)
        semester = self.transform_date_to_semester(date)
        return semester

    #Dada una fecha, quiero saber a que período pertenece
    def fecha_periodo(self, fecha_str):
        """
            Si la fecha es mayor a octubre:
                periodo: anio-12-31
            Si la fecha es menor a Marzo:
                periodo: anioAnterior-12-31
            Si la fecha es mayor a marzo y menor a octubre
                periodo: anio-06-30
        """
        from datetime import datetime
        fecha = datetime.strptime(str(fecha_str), '%Y-%m-%d')
        if fecha.month > 10:
            return '{}-12-31'.format(fecha.year)
        elif fecha.month <= 3:
            return '{}-12-31'.format(fecha.year - 1)
        else:
            return '{}-06-30'.format(fecha.year)
        return periodo

    def periodo_semestre(self, periodo):
        from datetime import datetime
        fecha = datetime.strptime(str(periodo), '%Y-%m-%d')
        if fecha.month == 12:
            return '{}-S2'.format(fecha.year)
        else:
            return '{}-S1'.format(fecha.year)
        return periodo