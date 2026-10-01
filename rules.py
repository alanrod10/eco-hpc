"""
rules.py - Motor de Reglas y Parámetros del Agente ECO-HPC
---------------------------------------------------------
Define los estados, acciones simuladas, umbrales y reglas deterministas
del Agente Basado en Reglas.

Aclaración de Arquitectura:
- Los umbrales aquí definidos son PARÁMETROS DEL PROTOTIPO y no representan
  límites universales de cualquier arquitectura de GPU.
- Las acciones son SIMULADAS: el agente calcula y emite la recomendación
  operativa, pero no ejecuta llamadas de bajo nivel a hardware físico real.
"""

from enum import Enum
from typing import Any, Dict, NamedTuple
from data_quality import QualityResult


class AgentState(str, Enum):
    """Estados canónicos del Agente ECO-HPC."""
    NORMAL = "NORMAL"
    AHORRO = "AHORRO"
    PROTECCION = "PROTECCION"
    DATOS_NO_CONFIABLES = "DATOS NO CONFIABLES"


class AgentAction(str, Enum):
    """Acciones operativas (simuladas) recomendadas por el agente."""
    MANTENER = "MANTENER"
    AHORRAR = "AHORRAR"
    REFRIGERAR = "REFRIGERAR"
    PROTEGER = "PROTEGER"
    REVISAR_SENSOR = "REVISAR SENSOR"


class RuleThresholds:
    """
    Parámetros configurables de simulación para el prototipo.
    Representan valores típicos de operación para aceleradores de cómputo HPC.
    """
    TEMP_CRITICAL: float = 85.0     # °C - Umbral de protección configurado para el prototipo/simulación (no es límite universal de toda GPU)
    TEMP_WARNING: float = 75.0      # °C - Alerta preventiva de temperatura elevada
    TEMP_SAFE: float = 70.0         # °C - Límite superior para operar con seguridad en perfiles de ahorro
    POWER_HIGH: float = 650.0       # W  - Umbral de consumo elevado (parámetro de simulación inspirado en aceleradores como H100 SXM con hasta 700 W configurables; no es límite universal de toda GPU)
    POWER_SAVING_TRIGGER: float = 300.0  # W - Consumo mínimo para considerar que hay derroche evitable
    UTIL_LOW: float = 30.0          # %  - Límite inferior de uso computacional para modo de ahorro
    UTIL_HIGH: float = 85.0         # %  - Carga computacional pesada (entrenamiento intensivo de IA)


class RuleEvaluationResult(NamedTuple):
    """Resultado de la evaluación de reglas sobre una percepción."""
    state: AgentState
    action: AgentAction
    reason: str
    action_details: str
    applied_rule_id: str


def evaluate_rules(record: Dict[str, Any], quality: QualityResult) -> RuleEvaluationResult:
    """
    Evalúa el conjunto de reglas jerárquicas sobre la lectura de telemetría auditada.
    
    Jerarquía de Decisión:
    1. Regla 0: Veracidad de Datos -> Si la lectura es anómala o inconsistente,
       el agente pasa a DATOS NO CONFIABLES y no emite órdenes automáticas sobre el hardware.
    2. Regla 1: Protección Térmica y Eléctrica -> Si la temperatura alcanza el umbral de protección
       o existe sobreconsumo con alta utilización, prioriza la seguridad operativa del clúster.
    3. Regla 2: Oportunidad de Ahorro y Eficiencia -> Si el consumo/frecuencia es alto
       pero la GPU está subutilizada (idle/espera de I/O), reduce frecuencia (DVFS simulado).
    4. Regla 3: Régimen Normal -> Si opera dentro de los rangos equilibrados, mantiene
       los parámetros operativos vigentes.
    """
    # -------------------------------------------------------------
    # REGLA 0: FILTRO DE VERACIDAD (V DE VERACIDAD)
    # -------------------------------------------------------------
    if not quality.is_valid:
        issues_str = "; ".join(quality.issues)
        return RuleEvaluationResult(
            state=AgentState.DATOS_NO_CONFIABLES,
            action=AgentAction.REVISAR_SENSOR,
            reason=f"Anomalía en percepción de telemetría: {issues_str}. Se rechaza decisión automática.",
            action_details="SIMULACIÓN: Aislamiento del stream de telemetría y emisión de ticket de mantenimiento de hardware.",
            applied_rule_id="RULE-0_VERACITY_FILTER",
        )

    temp = float(record["temperature"])
    power = float(record["power_w"])
    util = float(record["utilization"])
    freq = float(record["frequency"])
    gid = record.get("gpu_id", "GPU")

    # -------------------------------------------------------------
    # REGLA 1: PROTECCIÓN TÉRMICA Y ENERGÉTICA
    # Condición: Temperatura crítica (>= 85°C) O combinación de temp de advertencia
    # con alta potencia (>= 650W) y alta utilización (>= 85%).
    # -------------------------------------------------------------
    if temp >= RuleThresholds.TEMP_CRITICAL or (
        temp >= RuleThresholds.TEMP_WARNING
        and power >= RuleThresholds.POWER_HIGH
        and util >= RuleThresholds.UTIL_HIGH
    ):
        return RuleEvaluationResult(
            state=AgentState.PROTECCION,
            action=AgentAction.PROTEGER,
            reason=(
                f"Condición térmica o eléctrica crítica detectada ({temp:.1f} °C, {power:.1f} W, {util:.1f}% util). "
                f"85 °C es un umbral de protección configurado para el prototipo/simulación. Se activa protocolo preventivo."
            ),
            action_details=(
                "SIMULACIÓN: [1] Reducción forzada de reloj (DVFS cap a 1400 MHz). "
                "[2] Incremento de ventiladores/bombas de refrigeración al 100% de ciclo de trabajo. "
                "[3] Señal de power-capping a 500W al scheduler SLURM."
            ),
            applied_rule_id="RULE-1_THERMAL_POWER_PROTECTION",
        )

    # -------------------------------------------------------------
    # REGLA 2: EFICIENCIA ENERGÉTICA Y AHORRO
    # Condición: Consumo elevado (> 300W) con utilización baja (< 30%)
    # en condiciones térmicas seguras (< 70°C).
    # -------------------------------------------------------------
    if (
        power > RuleThresholds.POWER_SAVING_TRIGGER
        and util < RuleThresholds.UTIL_LOW
        and temp < RuleThresholds.TEMP_SAFE
    ):
        potential_saving_w = round(power * 0.40, 1)  # Estimación didáctica de ahorro ~40%
        return RuleEvaluationResult(
            state=AgentState.AHORRO,
            action=AgentAction.AHORRAR,
            reason=(
                f"Oportunidad de ahorro energético detectada: {gid} disipa {power:.1f} W a {freq:.0f} MHz "
                f"con utilización de sólo {util:.1f}%. Temperatura segura ({temp:.1f} °C)."
            ),
            action_details=(
                f"SIMULACIÓN: Ajuste de frecuencia de reloj hacia P-State intermedio (1200 MHz). "
                f"Ahorro estimado proyectado: ~{potential_saving_w} W sin degradación de rendimiento."
            ),
            applied_rule_id="RULE-2_ENERGY_SAVING_IDLE",
        )

    # -------------------------------------------------------------
    # REGLA 3: RÉGIMEN NOMINAL / OPERACIÓN NORMAL
    # -------------------------------------------------------------
    return RuleEvaluationResult(
        state=AgentState.NORMAL,
        action=AgentAction.MANTENER,
        reason=(
            f"Operación balanceada y segura: Temp {temp:.1f} °C (<{RuleThresholds.TEMP_WARNING}°C), "
            f"Potencia {power:.1f} W, Utilización {util:.1f}%. El hardware opera dentro de la envolvente de diseño."
        ),
        action_details="SIMULACIÓN: Mantener frecuencia, curva de refrigeración y perfiles energéticos vigentes.",
        applied_rule_id="RULE-3_NOMINAL_OPERATION",
    )
