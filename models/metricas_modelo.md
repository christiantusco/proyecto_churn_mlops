# Metricas del Modelo Churn v1.0

**Autor:** Christian Tusco
**Fecha de entrenamiento:** 2026-06-18T12:27:47.727300
**Version:** 1.0

## Variables de entrada

| Variable             | Tipo  | Rango    |
|----------------------|-------|----------|
| edad                 | int   | 18 - 90  |
| meses_contrato       | int   | 1 - 72   |
| llamadas_soporte     | int   | 0 - 20   |
| saldo_promedio       | float | 0 - 5000 |
| productos_contratados| int   | 1 - 5    |

## Resultados

| Metrica   | Valor              |
|-----------|--------------------|
| Accuracy  | 0.6650     |
| F1-Score  | 0.3964           |
| Precision | 0.4490    |
| Recall    | 0.3548       |

## Parametros del modelo

- Algoritmo: Random Forest Classifier
- Estimadores: 100
- Muestras de entrenamiento: 800
- Muestras de prueba: 200
