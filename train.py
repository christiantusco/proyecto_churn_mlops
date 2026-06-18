import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import joblib
import json
import os
from datetime import datetime

AUTOR = "Christian Tusco"
VERSION = "1.0"
MODEL_NAME = "modelo_churn_v1"

os.makedirs("models", exist_ok=True)

np.random.seed(42)
n_samples = 1000

data = {
    "edad": np.random.randint(18, 90, n_samples),
    "meses_contrato": np.random.randint(1, 72, n_samples),
    "llamadas_soporte": np.random.randint(0, 20, n_samples),
    "saldo_promedio": np.round(np.random.uniform(0, 5000, n_samples), 2),
    "productos_contratados": np.random.randint(1, 5, n_samples),
}

df = pd.DataFrame(data)

prob_churn = (
    (df["meses_contrato"] < 12).astype(float) * 0.35 +
    (df["llamadas_soporte"] > 10).astype(float) * 0.40 +
    (df["saldo_promedio"] < 500).astype(float) * 0.15 +
    (df["productos_contratados"] == 1).astype(float) * 0.10
).clip(0, 1)

df["churn"] = (np.random.uniform(0, 1, n_samples) < prob_churn).astype(int)

X = df.drop("churn", axis=1)
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy  = accuracy_score(y_test, y_pred)
f1        = f1_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall    = recall_score(y_test, y_pred)

joblib.dump(model, f"models/{MODEL_NAME}.joblib")

metadata = {
    "modelo": MODEL_NAME,
    "version": VERSION,
    "autor": AUTOR,
    "fecha_entrenamiento": datetime.now().isoformat(),
    "algoritmo": "RandomForestClassifier",
    "n_estimadores": 100,
    "variables": list(X.columns),
    "n_muestras_entrenamiento": len(X_train),
    "n_muestras_prueba": len(X_test),
    "metricas": {
        "accuracy":  round(accuracy, 4),
        "f1_score":  round(f1, 4),
        "precision": round(precision, 4),
        "recall":    round(recall, 4),
    },
}

with open(f"models/{MODEL_NAME}_metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

metricas_md = f"""# Metricas del Modelo Churn v{VERSION}

**Autor:** {AUTOR}
**Fecha de entrenamiento:** {metadata['fecha_entrenamiento']}
**Version:** {VERSION}

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
| Accuracy  | {accuracy:.4f}     |
| F1-Score  | {f1:.4f}           |
| Precision | {precision:.4f}    |
| Recall    | {recall:.4f}       |

## Parametros del modelo

- Algoritmo: Random Forest Classifier
- Estimadores: 100
- Muestras de entrenamiento: {len(X_train)}
- Muestras de prueba: {len(X_test)}
"""

with open("models/metricas_modelo.md", "w", encoding="utf-8") as f:
    f.write(metricas_md)

print("=" * 45)
print(f"  Modelo: models/{MODEL_NAME}.joblib")
print(f"  Metadata: models/{MODEL_NAME}_metadata.json")
print(f"  Metricas: models/metricas_modelo.md")
print("=" * 45)
print(f"  Accuracy:  {accuracy:.4f}")
print(f"  F1-Score:  {f1:.4f}")
print(f"  Precision: {precision:.4f}")
print(f"  Recall:    {recall:.4f}")
print("=" * 45)
print("Entrenamiento completado exitosamente.")
