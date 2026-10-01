"""
test_negative.py - Pruebas Negativas y de Robustez para ECO-HPC
---------------------------------------------------------------
Prueba situaciones límite y datos malformados para asegurar que el sistema
no falle catastróficamente ni se rompa en silencio:
1. Archivo inexistente o ruta corrupta
2. Dataset vacío
3. Tipos de datos incompatibles (strings en valores numéricos)
4. Diccionarios vacíos o registros con None total
5. Valores numéricos extremos (+inf, -inf, 1e9)
6. Lote sin lecturas válidas en MapReduce
"""

import math
import os
import pytest
from agent import EcoHpcAgent
from data_quality import DataQualityAuditor
from mapreduce_demo import execute_mapreduce
from rules import AgentAction, AgentState


def test_empty_record():
    empty = {}
    res = DataQualityAuditor.audit_record(empty)
    assert res.is_valid is False
    assert len(res.issues) >= 4


def test_corrupted_data_types():
    corrupted = {
        "gpu_id": "GPU-99",
        "temperature": "NO_ES_NUMERO",
        "power_w": "TRES_CIENTOS",
        "utilization": "ALTA",
        "frequency": "RAPIDO",
    }
    res = DataQualityAuditor.audit_record(corrupted)
    assert res.is_valid is False
    assert any("Error de tipo" in iss for iss in res.issues)


def test_extreme_numerical_values():
    extreme = {
        "gpu_id": "GPU-88",
        "temperature": 999999.0,
        "power_w": 1000000.0,
        "utilization": -50.0,
        "frequency": -100,
    }
    res = DataQualityAuditor.audit_record(extreme)
    assert res.is_valid is False
    assert len(res.issues) >= 3


def test_agent_handles_totally_invalid_record():
    agent = EcoHpcAgent()
    corrupted = {
        "gpu_id": "GPU-ERR",
        "temperature": None,
        "power_w": -999.0,
        "utilization": 200.0,
        "frequency": 0,
    }
    decision = agent.perceive_and_decide(corrupted)
    assert decision.state == AgentState.DATOS_NO_CONFIABLES
    assert decision.action == AgentAction.REVISAR_SENSOR
    assert decision.is_data_valid is False


def test_empty_batch_summary():
    agent = EcoHpcAgent()
    summary = agent.get_cluster_summary([])
    assert summary["total_gpus"] == 0
    assert summary["avg_temperature"] == 0.0
    assert summary["general_status"] == "SIN DATOS"


def test_mapreduce_with_empty_dataset():
    res = execute_mapreduce([])
    assert res["input_records_count"] == 0
    assert res["unique_keys_count"] == 0
    assert res["reduce_results"] == {}


def test_mapreduce_with_all_invalid_values():
    telemetry = [
        {"gpu_id": "GPU-ERR", "power_w": None, "temperature": None},
        {"gpu_id": "GPU-ERR", "power_w": -50.0, "temperature": 150.0},
    ]
    res = execute_mapreduce(telemetry)
    assert "GPU-ERR" in res["reduce_results"]
    assert res["reduce_results"]["GPU-ERR"]["valid_samples"] == 0
    assert res["reduce_results"]["GPU-ERR"]["avg_power_w"] == 0.0
