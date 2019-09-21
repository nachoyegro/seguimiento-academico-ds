import pandas as pd

class DataManipulator:

    def __init__(self, data):
        """
            data: Dataframe
        """
        self.data = data

    def filtrar_alumnos_de_materia(self, materia):
        """
            Quiero obtener los alumnos de una materia
            :return Dataframe
        """
        df = self.data
        df = df.loc[df.nota != 'PA'] #No me interesan los Pendientes de Aprobacion
        df = df.loc[df.materia == materia] #Por ahora lo hago por nombre
        return df

    def filtrar_alumnos_de_materia_periodo(self, materia, fecha_inicio, fecha_fin):
        """
            Quiero obtener los alumnos de una materia en un período determinado
            :return Dataframe
        """
        df = self.filtrar_alumnos_de_materia(materia)
        df = df.loc[(df.fecha >= fecha_inicio) & (df.fecha <= fecha_fin)]
        return df

    def aprobados(self, materia):
        """
            Obtengo los aprobados en base al resultado, no a la nota
            :return Dataframe
        """
        df = self.filtrar_alumnos_de_materia(materia)
        df = df.loc[(df.resultado == 'A') | (df.resultado == 'P')] #A: Regular | P: Acredito
        return df

    def desaprobados(self, materia):
        """
            Obtengo los desaprobados en base al resultado, no a la nota
            No tiene en cuenta los ausentes
            :return Dataframe
        """
        df = self.filtrar_alumnos_de_materia(materia)
        df = df.loc[(df.resultado == 'R')] #R: Reprobado
        return df

    def ausentes(self, materia):
        """
            Obtengo los ausentes en base al resultado
            :return Dataframe
        """
        df = self.filtrar_alumnos_de_materia(materia)
        df = df.loc[(df.resultado == 'U')] #U: Ausente/Libre
        return df


    def alumnos_aprobados_materia_series(self, materia):
        """
            Obtengo los alumnos aprobados de una materia
            :return Series
        """
        aprobados = self.aprobados(materia)
        return pd.Series(pd.unique(aprobados['alumno']))

    def alumnos_totales_materia_series(self, materia):
        """
            Obtengo los alumnos totales de una materia
            :return Series
        """
        alumnos = pd.unique(self.data['alumno'])
        return pd.Series(alumnos)

    def alumnos_falta_aprobar_materia_series(self, materia):
        """
            Obtengo los alumnos que aun no aprobaron esta materia
        """
        aprobados = self.alumnos_aprobados_materia_series(materia)
        totales = self.alumnos_totales_materia_series(materia)
        resultado = totales[~totales.isin(aprobados)]
        return resultado