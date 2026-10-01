"""
agent.py - Agente Supervisor de Eficiencia Energética (ECO-HPC)
--------------------------------------------------------------
Implementa el Agente Inteligente Reactivo Basado en Reglas con Estado Interno.

Cumple con el marco formal PEAS:
- Performance (Rendimiento): Maximizar la eficiencia energética (reducción de kWh y disipación)
  manteniendo las GPUs en régimen de temperatura seguro y cumpliendo los SLAs de cómputo.
- Environment (Entorno): Clúster HPC con aceleradores GPU para cargas de Inteligencia Artificial.
- Actuators (Actuadores): Ajuste de frecuencia (DVFS), escalado de refrigeración y limitación de potencia (SIMULADOS).
- Sensors (Sensores): Percepciones de telemetría de hardware (temperatura, potencia, utilización, frecuencia, cooling).

Flujo de Operación Fundamental:
SENSORES -> PERCEPCIONES -> CONTROL DE CALIDAD -> ESTADO INTERNO -> DECISIÓN -> ACCIÓN
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from data_quality import DataQualityAuditor, QualityResult
from rules import AgentAction, AgentState, RuleEvaluationResult, evaluate_rules


@dataclass
class AgentDecision:
    """
    Representa la resolución integral producida por el agente ECO-HPC ante una percepción.
    Responde directamente a las 5 preguntas canónicas requeridas:
    1. ¿Qué está ocurriendo?
    2. ¿En qué estado se encuentra la GPU?
    3. ¿Qué decisión corresponde?
    4. ¿Por qué?
    5. ¿Qué acción se recomienda o simula?
    """
    gpu_id: str
    timestamp: str
    state: AgentState
    action: AgentAction
    reason: str
    action_details: str
    rule_id: str
    is_data_valid: bool
    quality_issues: List[str]
    perceptions: Dict[str, Any]

    # Respuestas conceptuales explícitas para la defensa oral y la UI:
    def what_is_happening(self) -> str:
        """¿Qué está ocurriendo?"""
        if not self.is_data_valid:
            return f"Alerta de Veracidad: El sensor de {self.gpu_id} reportó valores fuera de límites físicos o inconsistentes."
        temp = self.perceptions.get("temperature", 0.0)
        pwr = self.perceptions.get("power_w", 0.0)
        util = self.perceptions.get("utilization", 0.0)
        job = self.perceptions.get("job_status", "DESCONOCIDO")

        if self.state == AgentState.PROTECCION:
            return f"{self.gpu_id} está bajo carga crítica ({job}) disipando {pwr:.0f} W con temperatura de {temp:.1f} °C y {util:.0f}% de carga."
        elif self.state == AgentState.AHORRO:
            return f"{self.gpu_id} está subutilizada ({util:.0f}% de uso) pero manteniendo un consumo elevado ({pwr:.0f} W) a alta frecuencia."
        else:
            return f"{self.gpu_id} opera en régimen nominal y equilibrado ({util:.0f}% uso, {temp:.1f} °C, {pwr:.0f} W)."

    def gpu_state_label(self) -> str:
        """¿En qué estado se encuentra la GPU?"""
        return self.state.value

    def decision_label(self) -> str:
        """¿Qué decisión corresponde?"""
        return self.action.value

    def why_label(self) -> str:
        """¿Por qué?"""
        return self.reason

    def simulated_action_label(self) -> str:
        """¿Qué acción se recomienda o simula?"""
        return self.action_details

    def to_dict(self) -> Dict[str, Any]:
        """Convierte la decisión a diccionario plano para dashboards y DataFrames."""
        return {
            "gpu_id": self.gpu_id,
            "timestamp": self.timestamp,
            "state": self.state.value,
            "action": self.action.value,
            "is_valid": self.is_data_valid,
            "temperature": self.perceptions.get("temperature"),
            "power_w": self.perceptions.get("power_w"),
            "utilization": self.perceptions.get("utilization"),
            "frequency": self.perceptions.get("frequency"),
            "cooling": self.perceptions.get("cooling"),
            "job_status": self.perceptions.get("job_status"),
            "reason": self.reason,
            "action_details": self.action_details,
            "rule_id": self.rule_id,
        }


class EcoHpcAgent:
    """
    Agente Supervisor de Eficiencia Energética y Seguridad Térmica para Clúster HPC.
    Mantiene estado interno entre ciclos de sensado.
    """

    def __init__(self, agent_name: str = "ECO-HPC-SUPERVISOR"):
        self.agent_name = agent_name
        self.state_history: List[AgentDecision] = []
        self.simulated_savings_kwh: float = 0.0
        self.interventions_counter: int = 0
        self.last_cluster_decisions: Dict[str, AgentDecision] = {}

    def reset_state(self) -> None:
        """Reinicia la memoria interna del agente."""
        self.state_history.clear()
        self.simulated_savings_kwh = 0.0
        self.interventions_counter = 0
        self.last_cluster_decisions.clear()

    def perceive_and_decide(self, sensor_reading: Dict[str, Any]) -> AgentDecision:
        """
        Ejecuta el ciclo cognitivo del agente ante una percepción individual:
        1. SENSORES: Lectura de la entrada cruda.
        2. PERCEPCIONES: Extracción y tipado de variables.
        3. CONTROL DE CALIDAD: Validación con DataQualityAuditor (V de Veracidad).
        4. ESTADO INTERNO: Actualización del estado interno según la regla disparada.
        5. DECISIÓN: Evaluación determinista de reglas jerárquicas.
        6. ACCIÓN SIMULADA: Formulación de la acción correctiva o de mantenimiento.
        """
        # Paso 1 y 2: Percepciones
        gpu_id = str(sensor_reading.get("gpu_id", "GPU-UNKNOWN"))
        ts = str(
            sensor_reading.get(
                "timestamp", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            )
        )

        # Paso 3: Control de Calidad y Veracidad
        quality_result = DataQualityAuditor.audit_record(sensor_reading)

        # Paso 4 y 5: Decisión mediante reglas deterministas
        rule_res: RuleEvaluationResult = evaluate_rules(sensor_reading, quality_result)

        # Actualizar métricas acumuladas de sostenibilidad en el estado interno
        if rule_res.state == AgentState.AHORRO:
            # Estimación pedagógica: ~150 W ahorrados por 1 hora = 0.15 kWh simulados
            self.simulated_savings_kwh += 0.025
            self.interventions_counter += 1
        elif rule_res.state == AgentState.PROTECCION:
            self.interventions_counter += 1

        decision = AgentDecision(
            gpu_id=gpu_id,
            timestamp=ts,
            state=rule_res.state,
            action=rule_res.action,
            reason=rule_res.reason,
            action_details=rule_res.action_details,
            rule_id=rule_res.applied_rule_id,
            is_data_valid=quality_result.is_valid,
            quality_issues=quality_result.issues,
            perceptions=dict(sensor_reading),
        )

        # Actualizar memoria del estado interno
        self.state_history.append(decision)
        self.last_cluster_decisions[gpu_id] = decision

        return decision

    def process_cluster(self, telemetry_batch: List[Dict[str, Any]]) -> List[AgentDecision]:
        """
        Procesa una ronda completa de telemetría para todas las GPUs del clúster.
        """
        decisions = []
        for item in telemetry_batch:
            dec = self.perceive_and_decide(item)
            decisions.append(dec)
        return decisions

    def get_cluster_summary(self, decisions: Optional[List[AgentDecision]] = None) -> Dict[str, Any]:
        """
        Calcula indicadores agregados para la pantalla de Dashboard y Telemetría.
        """
        target_decisions = decisions if decisions is not None else list(self.last_cluster_decisions.values())

        if not target_decisions:
            return {
                "total_gpus": 0,
                "avg_temperature": 0.0,
                "total_power_w": 0.0,
                "avg_utilization": 0.0,
                "states_count": {},
                "actions_count": {},
                "general_status": "SIN DATOS",
            }

        valid_temps = [
            float(d.perceptions["temperature"])
            for d in target_decisions
            if d.is_data_valid and d.perceptions.get("temperature") is not None
        ]
        valid_powers = [
            float(d.perceptions["power_w"])
            for d in target_decisions
            if d.is_data_valid and d.perceptions.get("power_w") is not None
        ]
        valid_utils = [
            float(d.perceptions["utilization"])
            for d in target_decisions
            if d.is_data_valid and d.perceptions.get("utilization") is not None
        ]

        states_count = {s.value: 0 for s in AgentState}
        actions_count = {a.value: 0 for a in AgentAction}

        for d in target_decisions:
            states_count[d.state.value] = states_count.get(d.state.value, 0) + 1
            actions_count[d.action.value] = actions_count.get(d.action.value, 0) + 1

        # Diagnóstico del estado general del cluster
        if states_count[AgentState.PROTECCION.value] > 0:
            general_status = "ALERTA TÉRMICA / PROTECCIÓN ACTIVA"
        elif states_count[AgentState.DATOS_NO_CONFIABLES.value] > 0:
            general_status = "ADVERTENCIA DE INTEGRIDAD DE SENSORES"
        elif states_count[AgentState.AHORRO.value] > 0:
            general_status = "OPORTUNIDAD DE OPTIMIZACIÓN ENERGÉTICA"
        else:
            general_status = "OPERACIÓN NORMAL Y BALANCEADA"

        return {
            "total_gpus": len(target_decisions),
            "avg_temperature": round(sum(valid_temps) / len(valid_temps), 1) if valid_temps else 0.0,
            "total_power_w": round(sum(valid_powers), 1),
            "avg_utilization": round(sum(valid_utils) / len(valid_utils), 1) if valid_utils else 0.0,
            "states_count": states_count,
            "actions_count": actions_count,
            "general_status": general_status,
            "simulated_savings_kwh": round(self.simulated_savings_kwh, 3),
            "interventions_count": self.interventions_counter,
        }
