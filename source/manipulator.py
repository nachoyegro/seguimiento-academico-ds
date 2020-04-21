#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

class DataManipulator:

    ########################################### Filtrado ###############################################

    def filtrar_carreras(self, df, *carreras):
        """
            Quiero obtener las materias cursadas de carreras
            :return Dataframe
        """
        return df.loc[df['carrera'].isin(*carreras)]

    def filtrar_alumnos_de_materia(self, df, materia):
        """
            Quiero obtener los alumnos de una materia
            :return Dataframe
        """
        df = df.loc[df['codigo'] ==
                    materia]
        return df

    def filtrar_periodo(self, df, fecha_inicio, fecha_fin):
        """
            Se filtra por periodo seleccionado separando los casos correspondientes.
            Se puede querer filtrar solo "fecha mayor a" o "fecha menor a"
        """
        # Si hay fecha de inicio y fecha de fin, se filtra por gte & lte
        if fecha_inicio and fecha_fin:
            return df.loc[(df.fecha >= fecha_inicio) & (df.fecha <= fecha_fin)]
        # Si solo hay fecha de inicio, se filtra por gte
        elif fecha_inicio:
            return df.loc[(df.fecha >= fecha_inicio)]
        # Si solo hay fecha de fin, se filtra por lte
        elif fecha_fin:
            return df.loc[(df.fecha <= fecha_fin)]
        # Si no hay ni fecha de inicio ni fecha de fin, se retorna todo
        else:
            return df

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
        return df.loc[df['area'] == area]

    def filtrar_nucleo(self, df, nucleo):
        return df.loc[df['nucleo'] == nucleo]

    def filtrar_materias_obligatorias(self, df):
        return df.loc[df['nucleo'] != 'C']

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

    def cantidad_creditos(self, df):
        return int(df['creditos'].sum())

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

    def cantidad_materias_distintas(self, df):
        return len(pd.unique(df['codigo']))

    # TODO: esto hay que sacarlo del plan
    def get_nombre_materia(self, df, cod_materia):
        try:
            return df.loc[df['codigo'] == cod_materia]['materia'].iloc[0]
        except:
            return ''

    def areas_unicas(self, df):
        return pd.unique(df['area'])

    def nucleos_unicos(self, df):
        return pd.unique(df['nucleo'])

    def filtrar_materias_obligatorias_area(self, df, area):
        areas_filtradas = self.filtrar_area(df, area)
        obligatorias = self.filtrar_materias_obligatorias(areas_filtradas)
        return obligatorias

    def total_materias_obligatorias_area(self, df, area):
        obligatorias = self.filtrar_materias_obligatorias_area(df, area)
        total_materias_area = self.cantidad_materias_distintas(obligatorias)
        return total_materias_area

    def porcentaje_aprobadas_area(self, plan_data, cursadas, area):
        # Calculo el total de materias de un area, en base al plan
        total_area = self.total_materias_obligatorias_area(plan_data, area)

        # Si tiene materias esa area
        if total_area:
            # Filtro las materias aprobadas del alumno dentro de esa area
            materias_obligatorias_area = self.filtrar_materias_obligatorias_area(
                cursadas, area)

            # De las materias del alumno, quiero solo las que aprobo
            materias_obligatorias_area_alumno_aprobadas = self.filtrar_aprobados(
                materias_obligatorias_area)

            # Obtengo el total de materias del area aprobadas por el alumno
            total_materias_obligatorias_area_alumno = self.cantidad_materias_distintas(
                materias_obligatorias_area_alumno_aprobadas)

            return (float(total_materias_obligatorias_area_alumno) / total_area) * 100
        else:
            return 0

    def porcentaje_aprobadas_nucleo(self, plan_data, cursadas, nucleo):
        # Filtro ambos DataFrames por nucleo
        nucleo_data = self.filtrar_nucleo(plan_data, nucleo)
        alumno_nucleo_data = self.filtrar_nucleo(
            cursadas, nucleo)

        # Filtro solo las aprobadas del alumno
        aprobadas_alumno = self.filtrar_aprobados(alumno_nucleo_data)

        # Calculo las materias distintas de ambos DataFrames
        cantidad_materias_nucleo = self.cantidad_materias_distintas(
            nucleo_data)
        cantidad_materias_aprobadas = self.cantidad_materias_distintas(
            aprobadas_alumno)

        # Calculo el porcentaje
        if cantidad_materias_nucleo:
            return (float(cantidad_materias_aprobadas) / cantidad_materias_nucleo) * 100
        else:
            return 0

    def cantidad_aprobadas(self, cursadas):
        """
            Retorna la cantidad de materias aprobadas
        """
        # Filtro solo las aprobadas del alumno
        aprobadas_alumno = self.filtrar_aprobados(cursadas)

        # Calculo las materias distintas
        cantidad_materias_aprobadas = self.cantidad_materias_distintas(
            aprobadas_alumno)
        return cantidad_materias_aprobadas

    def porcentaje_aprobadas(self, aprobadas, total):
        return (float(aprobadas) / total) * 100

    def porcentajes_aprobadas_areas(self, plan_data, cursadas_data):
        """
            Precondicion: se asume que las materias ya vienen filtradas por alumno/s
        """
        areas = self.areas_unicas(plan_data)
        result = {}
        for area in areas:
            # Si no tiene seteada el Área, no me interesa
            if area:
                result[area] = self.porcentaje_aprobadas_area(
                    plan_data, cursadas_data, area)
        return result

    def porcentajes_aprobadas_nucleos(self, plan_data, cursadas_data):
        """
            Precondicion: se asume que las materias ya vienen filtradas por alumno/s
        """
        nucleos = self.nucleos_unicos(plan_data)
        result = {}
        for nucleo in nucleos:
            # Si no tiene seteada el Área, no me interesa
            if nucleo:
                result[nucleo] = self.porcentaje_aprobadas_nucleo(
                    plan_data, cursadas_data, nucleo)
        return result

    def porcentaje_creditos(self, total_creditos, df):
        if total_creditos:
            return (float(self.cantidad_creditos(df)) / total_creditos) * 100
        else:
            return 0

    def cantidad_creditos_nucleo(self, data, nucleo):
        nucleo_data = self.filtrar_nucleo(data, nucleo)
        return self.cantidad_creditos(nucleo_data)

    def cantidades_creditos_nucleos(self, data, nucleos):
        result = {}
        for nucleo in nucleos:
            # Filtro los nucleos
            result[nucleo] = self.cantidad_creditos_nucleo(data, nucleo)
        return result

    def cantidad_creditos_area(self, data, area):
        area_data = self.filtrar_area(data, area)
        return self.cantidad_creditos(area_data)

    def cantidades_creditos_areas(self, data, areas):
        result = {}
        for area in areas:
            # Filtro las areas
            result[area] = self.cantidad_creditos_area(data, area)
        return result

    def porcentajes_creditos_areas(self, plan_data, cursadas_data):
        """
            Precondicion: se asume que las cursadas ya estan filtradas por el alumno
        """
        result = {}
        areas = self.areas_unicas(plan_data)
        for area in areas:
            area_data = self.filtrar_materias_obligatorias_area(
                plan_data, area)
            creditos_area = self.cantidad_creditos(area_data)

            alumno_area_data = self.filtrar_materias_obligatorias_area(
                cursadas_data, area)
            result[area] = self.porcentaje_creditos(
                creditos_area, alumno_area_data)
        return result

    def porcentajes_creditos_nucleos(self, plan_data, cursadas_data):
        """
            Precondicion: se asume que las cursadas ya estan filtradas por el alumno
        """
        result = {}
        nucleos = self.nucleos_unicos(plan_data)
        for nucleo in nucleos:
            if nucleo:
                nucleo_data = self.filtrar_nucleo(
                    plan_data, nucleo)
                creditos_nucleo = self.cantidad_creditos(nucleo_data)

                alumno_nucleo_data = self.filtrar_nucleo(
                    cursadas_data, nucleo)
                result[nucleo] = self.porcentaje_creditos(
                    creditos_nucleo, alumno_nucleo_data)
        return result

    def cantidades_formas_aprobacion(self, df):
        return df['forma_aprobacion'].value_counts()

    def agrupar_periodo(self, df, fecha, periodo):
        #Saco los que no tienen fecha de inscripcion
        df = df.dropna(subset=[fecha])
        #Transformo la columna en date
        df[fecha] = pd.to_datetime(df[fecha])
        #Agrupo por fechas cada 6 meses
        df = df.groupby(pd.Grouper(key=fecha, freq=periodo)).count()
        return df

    def inscriptos_por_carrera(self, dataframe):
        df = self.agrupar_periodo(dataframe, 'fecha_inscripcion', '6MS')
        #Saco la columna plan
        df = df.drop(['plan'], axis=1)
        return df

    def fecha_anterior(self, fecha):
        """
            Dada una fecha, retorno la misma fecha del año anterior
        """
        from datetime import datetime, timedelta
        return (datetime.strptime(fecha, '%Y-%m-%d') - timedelta(days=365)).strftime('%Y-%m-%d')

    def materias_alumno_hasta(self, df, alumno, fecha):
        df = df.loc[df.alumno == str(alumno)] #Obtengo los resultados del alumno
        df = df.loc[df.fecha < fecha] #Obtengo las materias hasta la fecha
        return df

    def materias_alumno_fecha(self, df, alumno, fecha):
        df = df.loc[df.alumno == str(alumno)] #Obtengo los resultados del alumno
        df = df.loc[df.fecha == fecha] #Obtengo las materias de una determinada fecha
        return df

    def score_alumno_hasta(self, df, alumno, fecha):
        df = self.materias_alumno_hasta(df, alumno, fecha)
        df = df.loc[df.fecha > self.fecha_anterior(fecha)] #Filtro las materias del ultimo año anterior a "fecha"
        df.loc[df.nota == 'A', 'nota'] = 7 #Pongo las aprobadas como si fuese un 7
        df = df.loc[df.nota != 'PA'] #No me interesan los pendientes de aprobacion
        df = df.fillna(value=1) #Lleno los austenes con un 1
        df.nota=df.nota.astype(float)
        return df.nota.mean()

    def score_alumno_periodo(self, df, alumno, fecha):
        df = self.materias_alumno_periodo(df, alumno, fecha)
        return df.nota.mean()

    def materias_alumno_periodo(self, df, alumno, fecha):
        df = df.loc[df.alumno == str(alumno)] #Obtengo los resultados del alumno
        df = df.loc[df.fecha_periodo == fecha] #Obtengo las materias de una determinada fecha
        return df

    def row_periodos(self, row):
        row['fecha_periodo'] = self.fecha_periodo(row.fecha)
        row['periodo_semestre'] = self.periodo_semestre(row['fecha_periodo'])
        return row

    def row_score_periodo(self, row, df, x):
        row['score_periodo'] = self.score_alumno_periodo(df, row.alumno, row.fecha_periodo)
        return row

    def aplicar_periodos(self, df):
        return df.apply(self.row_periodos, axis=1)

    def aplicar_scores(self, df):
        return df.apply(self.row_score_periodo, args=(df, 2), axis=1)

    def recalcular_notas_faltantes(self, df):
        df.loc[df.nota == 'A', 'nota'] = 7
        df = df.loc[df.nota != 'PA'] #No me interesan los pendientes de aprobacion
        df['nota'] = df.nota.replace("", np.nan)
        df = df.fillna(value=1) #Lleno los austenes con un 1
        df.nota=df.nota.astype(float)
        return df

    def scores_periodos(self, df):
        """
            Se asume que ya se calcularon los scores por periodo
            Es recomendable que ya se haya filtrado por alumno tambien
        """
        scores = df[['periodo_semestre', 'score_periodo']].drop_duplicates()
        return scores.sort_values(['periodo_semestre'], ascending=[1])

    def promedio_alumno_fecha(self, df, alumno, fecha):
        """
            Quiero calcular el promedio del alumno en una fecha determinada
            Se asume que la columna nota del dataframe ya es de tipo float
            Retorna un numero, que representa el promedio

        """
        df = self.materias_alumno_fecha(df, alumno, fecha) #Obtengo las materias del alumno hasta la fecha
        df.nota=df.nota.astype(float)
        return df.nota.mean()
    
    def promedio_hasta(self, df, alumno, fecha):
        """
            Quiero calcular el promedio del alumno hasta una determinada fecha
            Retorna un numero, que representa el promedio

        """
        df = self.materias_alumno_hasta(df, alumno, fecha) #Obtengo las materias del alumno hasta la fecha
        df.nota=df.nota.astype(float)
        return df.nota.mean()

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

    #fecha_periodo('2019-02-10') == '2018-12-31'

    def periodo_semestre(self, periodo):
        from datetime import datetime
        fecha = datetime.strptime(str(periodo), '%Y-%m-%d')
        if fecha.month == 12:
            return '{}-S2'.format(fecha.year)
        else:
            return '{}-S1'.format(fecha.year)
        return periodo