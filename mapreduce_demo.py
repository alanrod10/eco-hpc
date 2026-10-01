"""
mapreduce_demo.py - Demostración Didáctica del Paradigma MapReduce en ECO-HPC
----------------------------------------------------------------------------
Implementa en Python puro las etapas canónicas del paradigma MapReduce:
1. ENTRADA (Dataset histórico de telemetría de GPUs)
2. MAP (Emisión de pares clave-valor <gpu_id, métricas>)
3. SHUFFLE & SORT (Agrupamiento y particionamiento por clave)
4. REDUCE (Agregación matemática: promedio de potencia, temperatura máxima, energía)
5. SALIDA (Métricas consolidadas para análisis Batch)

Nota Académica Fundamental:
Esta implementación representa fielmente el PARADIGMA MapReduce (Dean & Ghemawat, 2004)
a nivel conceptual y algorítmico en memoria local. No requiere ni pretende ser un
clúster físico Hadoop/Spark en producción.
"""

from collections import defaultdict
from typing import Any, Dict, List, Tuple


def map_function(record: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    """
    Etapa MAP:
    Transforma un registro de telemetría en un par Clave-Valor.
    Clave: gpu_id
    Valor: {power_w, temperature, utilization, count}
    
    Ignora registros sin lectura válida de potencia para evitar contaminación.
    """
    gpu_id = record.get("gpu_id", "DESCONOCIDO")
    pwr = record.get("power_w")
    temp = record.get("temperature")
    util = record.get("utilization", 0.0)

    # Filtrado básico en etapa map para lecturas limpias
    pwr_val = float(pwr) if pwr is not None and pwr > 0 else 0.0
    temp_val = float(temp) if temp is not None else 0.0
    util_val = float(util) if util is not None else 0.0

    return (
        gpu_id,
        {
            "power_w": pwr_val,
            "temperature": temp_val,
            "utilization": util_val,
            "count": 1 if pwr_val > 0 else 0,
        },
    )


def shuffle_function(mapped_pairs: List[Tuple[str, Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Etapa SHUFFLE & SORT:
    Agrupa todos los valores emitidos por los Mappers que comparten la misma Clave (gpu_id).
    En un clúster distribuido real, esta etapa involucra transferencia de red
    entre nodos mappers y reducers.
    """
    grouped = defaultdict(list)
    for key, val in mapped_pairs:
        grouped[key].append(val)
    return dict(grouped)


def reduce_function(gpu_id: str, values: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Etapa REDUCE:
    Agrega la lista de valores asociados a una Clave única.
    Calcula:
    - Lecturas válidas procesadas
    - Consumo de potencia promedio (W)
    - Temperatura máxima registrada (°C)
    - Utilización promedio (%)
    - Energía total estimada consumida (kWh simulados, asumiendo muestras de 1 minuto)
    """
    valid_counts = [v["count"] for v in values if v["count"] > 0]
    total_valid = sum(valid_counts)

    if total_valid == 0:
        return {
            "gpu_id": gpu_id,
            "records_processed": len(values),
            "valid_samples": 0,
            "avg_power_w": 0.0,
            "max_temperature_c": 0.0,
            "avg_utilization_pct": 0.0,
            "total_energy_kwh": 0.0,
            "operational_profile": "DATOS INVÁLIDOS / SIN CONSUMO REGISTRADO",
        }

    powers = [v["power_w"] for v in values if v["count"] > 0]
    temps = [v["temperature"] for v in values if v["count"] > 0]
    utils = [v["utilization"] for v in values if v["count"] > 0]

    avg_power = sum(powers) / len(powers)
    max_temp = max(temps) if temps else 0.0
    avg_util = sum(utils) / len(utils)

    # Supuesto pedagógico: cada muestra representa un intervalo de 60 segundos
    # kWh = (avg_power * horas) / 1000 = (avg_power * (total_valid * 60 / 3600)) / 1000
    total_hours = (total_valid * 60.0) / 3600.0
    total_kwh = (avg_power * total_hours) / 1000.0

    # Perfil operativo deducido del histórico
    if max_temp >= 85.0 or avg_power >= 650.0:
        profile = "ALTO CONSUMO / RIESGO TÉRMICO FRECUENTE"
    elif avg_util < 30.0 and avg_power > 300.0:
        profile = "SUBUTILIZADA / CANDIDATA RECURRENTE A AHORRO"
    else:
        profile = "OPERACIÓN NOMINAL BALANCEADA"

    return {
        "gpu_id": gpu_id,
        "records_processed": len(values),
        "valid_samples": total_valid,
        "avg_power_w": round(avg_power, 2),
        "max_temperature_c": round(max_temp, 2),
        "avg_utilization_pct": round(avg_util, 2),
        "total_energy_kwh": round(total_kwh, 4),
        "operational_profile": profile,
    }


def execute_mapreduce(telemetry_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Ejecuta el pipeline completo de MapReduce y captura los estados intermedios
    para propósitos de demostración y visualización académica.
    """
    # 1. Entrada
    input_count = len(telemetry_records)

    # 2. Map
    mapped = [map_function(r) for r in telemetry_records]

    # 3. Shuffle
    shuffled = shuffle_function(mapped)

    # 4. Reduce
    reduced = {}
    for gpu_id, values in sorted(shuffled.items()):
        reduced[gpu_id] = reduce_function(gpu_id, values)

    return {
        "input_records_count": input_count,
        "map_output_count": len(mapped),
        "unique_keys_count": len(shuffled),
        "map_sample": mapped[:8],           # Muestra representativa de tuplas (k, v)
        "shuffle_sample": {k: shuffled[k][:2] for k in list(shuffled.keys())[:4]},
        "reduce_results": reduced,
    }
