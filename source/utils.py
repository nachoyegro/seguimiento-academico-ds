def calcular_score_materia(obligatorias, indice_aprobacion):
    return float(obligatorias) * (1 - float(indice_aprobacion / 100))
