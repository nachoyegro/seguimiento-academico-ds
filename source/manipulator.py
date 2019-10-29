import pandas as pd


class DataManipulator:

    ########################################### Filtrado ###############################################
    def filtrar_alumnos_de_materia(self, df, materia):
        """
            Quiero obtener los alumnos de una materia
            :return Dataframe
        """
        df = df.loc[df['materia.codigo'] ==
                    materia]  # Por ahora lo hago por nombre
        return df

    def filtrar_periodo(self, df, fecha_inicio, fecha_fin):
        return df.loc[(df.fecha >= fecha_inicio) & (df.fecha <= fecha_fin)]

    def filtrar_alumnos_de_materia_periodo(self, df, materia, fecha_inicio, fecha_fin):
        """
            Quiero obtener los alumnos de una materia en un período determinado
            :return Dataframe
        """
        df = self.filtrar_alumnos_de_materia(df, materia)
        df = self.filtrar_periodo(df, fecha_inicio, fecha_fin)
        return df

    def filtrar_aprobados(self, df):
        # A: Regular | P: Acredito
        return df.loc[(df.resultado == 'A') | (df.resultado == 'P')]

    def filtrar_ausentes(self, df):
        return df.loc[(df.resultado == 'U')]  # U: Ausente/Libre

    def filtrar_desaprobados(self, df):
        return df.loc[(df.resultado == 'R')]  # R: Reprobado

    def filtrar_pendientes(self, df):
        return df.loc[(df.resultado == 'E')]  # A: Regular | P: Acredito

    def filtrar_area(self, df, area):
        return df.loc[df['materia.area'] == area]

    def filtrar_nucleo(self, df, nucleo):
        return df.loc[df['materia.nucleo'] == nucleo]

    def filtrar_materias_obligatorias(self, df):
        return df.loc[df['materia.nucleo'] != 'C']

    def filtrar_materias_obligatorias(self, df):
        return df.loc[df['materia.nucleo'] != 'C']

    def filtrar_materias_de_alumno(self, df, legajo_alumno):
        return df.loc[df['alumno'] == legajo_alumno]

    def aprobados_de_materia(self, df, materia):
        """
            Obtengo los aprobados en base al resultado, no a la nota
            :return Dataframe
        """
        df = self.filtrar_alumnos_de_materia(df, materia)
        df = self.filtrar_aprobados(df)
        return df

    def pendientes_de_materia(self, df, materia):
        """
            Obtengo los pendientes en base al resultado, no a la nota
            :return Dataframe
        """
        df = self.filtrar_alumnos_de_materia(df, materia)
        df = self.filtrar_pendientes(df)
        return df

    def desaprobados_de_materia(self, df, materia):
        """
            Obtengo los desaprobados en base al resultado, no a la nota
            No tiene en cuenta los ausentes
            :return Dataframe
        """
        df = self.filtrar_alumnos_de_materia(df, materia)
        df = self.filtrar_desaprobados(df)
        return df

    def ausentes_de_materia(self, df, materia):
        """
            Obtengo los ausentes en base al resultado
            :return Dataframe
        """
        df = self.filtrar_alumnos_de_materia(df, materia)
        df = self.filtrar_ausentes(df)
        return df

    def alumnos_aprobados_materia_series(self, df, materia):
        """
            Obtengo los alumnos aprobados de una materia
            :return Series
        """
        aprobados = self.aprobados_de_materia(df, materia)
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
        # Hago la resta
        # Me quedo con aquellos que estan como desaprobados/ausentes y no estan en aprobados
        resultado = totales[~totales.isin(aprobados)]
        return resultado

    def cantidad_alumnos_falta_aprobar(self, df, materia):
        return len(self.alumnos_falta_aprobar_materia_series(df, materia))

    def cantidad_alumnos_aprobados(self, df, materia):
        return len(self.aprobados_de_materia(df, materia))

    def cantidad_alumnos_desaprobados(self, df, materia):
        return len(self.desaprobados_de_materia(df, materia))

    def cantidad_alumnos_ausentes(self, df, materia):
        return len(self.ausentes_de_materia(df, materia))

    def cantidad_alumnos_pendientes(self, df, materia):
        return len(self.pendientes_de_materia(df, materia))

    def total_materias_distintas(self, df):
        return len(pd.unique(df['materia.codigo']))

    def get_nombre_materia(self, df, cod_materia):
        try:
            return df.loc[df['materia.codigo'] == cod_materia.zfill(5)]['materia.materia'].iloc[0]
        except:
            return ''

    def filtrar_materias_obligatorias_area(self, df, area):
        areas_filtradas = self.filtrar_area(df, area)
        obligatorias = self.filtrar_materias_obligatorias(areas_filtradas)
        return obligatorias

    def total_materias_obligatorias_area(self, df, area):
        obligatorias = self.filtrar_materias_obligatorias_area(df, area)
        total_materias_area = self.total_materias_distintas(obligatorias)
        return total_materias_area

    def porcentaje_aprobadas_area(self, df, area, legajo_alumno):
        # Filtro las materias obligatorias de un area
        materias_obligatorias_area = self.filtrar_materias_obligatorias_area(
            df, area)
        # De esas materias, quiero solo las del alumno actual
        materias_obligatorias_area_alumno = self.filtrar_materias_de_alumno(
            materias_obligatorias_area, legajo_alumno)
        # De las materias del alumno, quiero solo las que aprobo
        materias_obligatorias_area_alumno_aprobadas = self.filtrar_aprobados(
            materias_obligatorias_area_alumno)
        # Obtengo el total de materias del area (obligatorias, y no tiene en cuenta las que nunca fueron cursadas)
        total_materias_obligatorias_area = self.total_materias_distintas(
            materias_obligatorias_area)
        # Obtengo el total de materias del area aprobadas por el alumno
        total_materias_obligatorias_area_alumno = self.total_materias_distintas(
            materias_obligatorias_area_alumno_aprobadas)

        if total_materias_obligatorias_area:
            return (float(total_materias_obligatorias_area_alumno) / total_materias_obligatorias_area) * 100
        else:
            return 0

    def areas_unicas(self, df):
        return pd.unique(df['materia.area'])

    def porcentajes_aprobadas_por_area(self, df, legajo_alumno):
        areas = self.areas_unicas(df)
        result = {}
        for area in areas:
            # Si no tiene seteada el Área, no me interesa
            if area:
                result[area] = self.porcentaje_aprobadas_area(
                    df, area, legajo_alumno)
        return result
