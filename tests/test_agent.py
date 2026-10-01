"""
test_agent.py - Pruebas Unitarias del Agente Supervisor ECO-HPC
--------------------------------------------------------------
Verifica los 4 escenarios obligatorios:
1. NORMAL -> NORMAL / MANTENER
2. AHORRO -> AHORRO / AHORRAR
3. PROTECCIÓN -> PROTECCION / PROTEGER
4. ANOMALÍA -> DATOS NO CONFIABLES / REVISAR SENSOR
Y las respuestas explicativas del ciclo cognitivo.
"""

import pytest
from agent import EcoHpcAgent
from rules import AgentAction, AgentState


@pytest.fixture
def agent():
    return EcoHpcAgent()


def test_scenario_normal(agent):
    reading = {
        "gpu_id": "GPU-01",
        "temperature": 60.0,
        "power_w": 350.0,
        "utilization": 70.0,
        "frequency": 1800,
        "cooling": 55.0,
        "job_status": "AI_INFERENCE",
    }
    decision = agent.perceive_and_decide(reading)

    assert decision.state == AgentState.NORMAL
    assert decision.action == AgentAction.MANTENER
    assert decision.is_data_valid is True
    assert "equilibrio" in decision.reason or "balanceada" in decision.reason
    assert "SIMULACIÓN" in decision.action_details
    assert "operación normal" in decision.what_is_happening().lower() or "nominal" in decision.what_is_happening().lower()


def test_scenario_ahorro(agent):
    reading = {
        "gpu_id": "GPU-04",
        "temperature": 58.0,
        "power_w": 380.0,
        "utilization": 15.0,
        "frequency": 1950,
        "cooling": 40.0,
        "job_status": "IDLE_STALLED",
    }
    decision = agent.perceive_and_decide(reading)

    assert decision.state == AgentState.AHORRO
    assert decision.action == AgentAction.AHORRAR
    assert decision.is_data_valid is True
    assert "ahorro" in decision.reason.lower()
    assert "reloj" in decision.action_details.lower() or "frecuencia" in decision.action_details.lower()
    assert agent.simulated_savings_kwh > 0


def test_scenario_proteccion(agent):
    reading = {
        "gpu_id": "GPU-07",
        "temperature": 89.0,
        "power_w": 720.0,
        "utilization": 97.0,
        "frequency": 2100,
        "cooling": 95.0,
        "job_status": "TRAINING_AI_LLM",
    }
    decision = agent.perceive_and_decide(reading)

    assert decision.state == AgentState.PROTECCION
    assert decision.action == AgentAction.PROTEGER
    assert decision.is_data_valid is True
    assert "térmica o eléctrica crítica" in decision.reason.lower() or "crítica" in decision.reason.lower()
    assert "refrigeración" in decision.action_details.lower() or "dvfs" in decision.action_details.lower()


def test_scenario_anomalia_sensor(agent):
    reading = {
        "gpu_id": "GPU-12",
        "temperature": 150.0,
        "power_w": 10.0,
        "utilization": 0.0,
        "frequency": 1200,
        "cooling": 0.0,
        "job_status": "ANOMALOUS_SENSOR",
    }
    decision = agent.perceive_and_decide(reading)

    assert decision.state == AgentState.DATOS_NO_CONFIABLES
    assert decision.action == AgentAction.REVISAR_SENSOR
    assert decision.is_data_valid is False
    assert len(decision.quality_issues) > 0
    assert "se rechaza decisión automática" in decision.reason.lower()
    assert "alerta de veracidad" in decision.what_is_happening().lower()


def test_cluster_processing_and_summary(agent):
    batch = [
        {"gpu_id": "GPU-01", "temperature": 60.0, "power_w": 350.0, "utilization": 70.0, "frequency": 1800, "cooling": 50.0},
        {"gpu_id": "GPU-04", "temperature": 58.0, "power_w": 380.0, "utilization": 15.0, "frequency": 1950, "cooling": 40.0},
        {"gpu_id": "GPU-07", "temperature": 89.0, "power_w": 720.0, "utilization": 97.0, "frequency": 2100, "cooling": 95.0},
        {"gpu_id": "GPU-12", "temperature": 150.0, "power_w": 10.0, "utilization": 0.0, "frequency": 1200, "cooling": 0.0},
    ]
    decisions = agent.process_cluster(batch)
    assert len(decisions) == 4

    summary = agent.get_cluster_summary(decisions)
    assert summary["total_gpus"] == 4
    assert summary["states_count"][AgentState.PROTECCION.value] == 1
    assert summary["states_count"][AgentState.AHORRO.value] == 1
    assert summary["states_count"][AgentState.DATOS_NO_CONFIABLES.value] == 1
    assert summary["states_count"][AgentState.NORMAL.value] == 1
    assert "PROTECCIÓN ACTIVA" in summary["general_status"]
