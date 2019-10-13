import pandas as pd

class DataManipulator:

    def filtrar_alumnos_de_materia(self, df, materia):
        """
            Quiero obtener los alumnos de una materia
            :return Dataframe
        """
        df = df.loc[df['materia.codigo'] == materia] #Por ahora lo hago por nombre
        return df

    def filtrar_alumnos_de_materia_periodo(self, df, materia, fecha_inicio, fecha_fin):
        """
            Quiero obtener los alumnos de una materia en un período determinado
            :return Dataframe
        """
        df = self.filtrar_alumnos_de_materia(df, materia)
        df = df.loc[(df.fecha >= fecha_inicio) & (df.fecha <= fecha_fin)]
        return df

    def aprobados(self, df, materia):
        """
            Obtengo los aprobados en base al resultado, no a la nota
            :return Dataframe
        """
        df = self.filtrar_alumnos_de_materia(df, materia)
        df = df.loc[(df.resultado == 'A') | (df.resultado == 'P')] #A: Regular | P: Acredito
        return df

    def pendientes(self, df, materia):
        """
            Obtengo los pendientes en base al resultado, no a la nota
            :return Dataframe
        """
        df = self.filtrar_alumnos_de_materia(df, materia)
        df = df.loc[(df.resultado == 'E')] #A: Regular | P: Acredito
        return df

    def desaprobados(self, df, materia):
        """
            Obtengo los desaprobados en base al resultado, no a la nota
            No tiene en cuenta los ausentes
            :return Dataframe
        """
        df = self.filtrar_alumnos_de_materia(df, materia)
        df = df.loc[(df.resultado == 'R')] #R: Reprobado
        return df

    def ausentes(self, df, materia):
        """
            Obtengo los ausentes en base al resultado
            :return Dataframe
        """
        df = self.filtrar_alumnos_de_materia(df, materia)
        df = df.loc[(df.resultado == 'U')] #U: Ausente/Libre
        return df

    def alumnos_aprobados_materia_series(self, df, materia):
        """
            Obtengo los alumnos aprobados de una materia
            :return Series
        """
        aprobados = self.aprobados(df, materia)
        return pd.Series(pd.unique(aprobados['alumno']))

    def alumnos_totales_materia_series(self, df, materia):
        """
            Obtengo los alumnos totales de una materia
            :return Series
        """
        alumnos = pd.unique(df['alumno'])
        return pd.Series(alumnos)

    def alumnos_falta_aprobar_materia_series(self, df, materia):
        """
            Obtengo los alumnos que aun no aprobaron esta materia
        """
        aprobados = self.alumnos_aprobados_materia_series(df, materia)
        totales = self.alumnos_totales_materia_series(df, materia)
        #Hago la resta 
        #Me quedo con aquellos que estan como desaprobados/ausentes y no estan en aprobados
        resultado = totales[~totales.isin(aprobados)]
        return resultado

    def cantidad_alumnos_falta_aprobar(self, df, materia):
        return len(self.alumnos_falta_aprobar_materia_series(df, materia))

    def cantidad_alumnos_aprobados(self, df, materia):
        return len(self.aprobados(df, materia))

    def cantidad_alumnos_desaprobados(self, df, materia):
        return len(self.desaprobados(df, materia))

    def cantidad_alumnos_ausentes(self, df, materia):
        return len(self.ausentes(df, materia))

    def cantidad_alumnos_pendientes(self, df, materia):
        return len(self.pendientes(df, materia))