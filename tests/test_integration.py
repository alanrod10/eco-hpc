"""
test_integration.py - Pruebas de Integración y Única Fuente de Verdad
---------------------------------------------------------------------
Verifica la consistencia integral del flujo de datos:
Dataset CSV/JSON -> Control de Calidad -> Agente ECO-HPC -> Dashboard Summary.
Garantiza que no existan discrepancias entre las lecturas y las decisiones.
"""

import json
import os
import pandas as pd
import pytest
from agent import EcoHpcAgent
from rules import AgentState


def test_single_source_of_truth_consistency():
    # 1. Cargar fuentes de datos centralizadas
    csv_path = os.path.join("data", "telemetry.csv")
    json_path = os.path.join("data", "telemetry.json")
    logs_path = os.path.join("data", "logs.txt")

    assert os.path.exists(csv_path), "Falta data/telemetry.csv"
    assert os.path.exists(json_path), "Falta data/telemetry.json"
    assert os.path.exists(logs_path), "Falta data/logs.txt"

    df = pd.read_csv(csv_path)
    with open(json_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    assert len(df) == len(json_data), "Discrepancia de tamaño entre CSV y JSON"

    # 2. Aislar última instantánea temporal
    latest_ts = df["timestamp"].max()
    current_df = df[df["timestamp"] == latest_ts]
    assert len(current_df) == 16, f"Se esperaban 16 GPUs en el prototipo, encontradas: {len(current_df)}"

    # 3. Procesar mediante el Agente ECO-HPC
    agent = EcoHpcAgent()
    telemetry_records = current_df.to_dict(orient="records")
    decisions = agent.process_cluster(telemetry_records)

    assert len(decisions) == 16

    # 4. Validar consistencia valor por valor
    for dec in decisions:
        row = current_df[current_df["gpu_id"] == dec.gpu_id].iloc[0]

        # Comprobar que la percepción del agente coincide exactamente con la fila del dataset
        if dec.is_data_valid:
            assert float(dec.perceptions["power_w"]) == float(row["power_w"])
            assert float(dec.perceptions["temperature"]) == float(row["temperature"])
            assert float(dec.perceptions["utilization"]) == float(row["utilization"])
        else:
            assert dec.state == AgentState.DATOS_NO_CONFIABLES

    # 5. Comprobar resumen del clúster
    summary = agent.get_cluster_summary(decisions)
    assert summary["total_gpus"] == 16
    assert summary["states_count"][AgentState.NORMAL.value] >= 8
    assert summary["states_count"][AgentState.AHORRO.value] >= 2
    assert summary["states_count"][AgentState.PROTECCION.value] >= 2
    assert summary["states_count"][AgentState.DATOS_NO_CONFIABLES.value] >= 2
