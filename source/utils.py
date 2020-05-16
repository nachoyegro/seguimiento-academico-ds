def calcular_score_materia(obligatorias, indice_aprobacion):
    return float(obligatorias) * float(1 - indice_aprobacion)
