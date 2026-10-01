"""
simulator.py - ECO-HPC Telemetry & Scenario Generator
-----------------------------------------------------
Genera datos de telemetría simulada para un conjunto representativo de GPUs
en un entorno HPC (Computación de Alto Rendimiento) para Inteligencia Artificial.

Aclaración de Escala:
- Escala conceptual de referencia: Cluster HPC de hasta 1.024 GPUs.
- Escala del prototipo funcional: 16 GPUs simuladas (GPU-01 a GPU-16).
- Tipo de hardware: SIMULADO (ningún comando actúa sobre hardware físico real).
"""

import json
import os
import random
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple


# Definición de GPUs del cluster simulado (16 GPUs distribuidas en 4 nodos)
GPU_CLUSTER_CONFIG = [
    {"gpu_id": f"GPU-{i:02d}", "node": f"node-{((i-1)//4)+1:02d}", "model": "NVIDIA H100 PCIe (Simulada)"}
    for i in range(1, 17)
]

# Umbrales base para la generación de escenarios representativos
DEFAULT_SEED = 42


def generate_baseline_telemetry(
    timestamp: Optional[str] = None, seed: Optional[int] = DEFAULT_SEED
) -> List[Dict]:
    """
    Genera una lectura instantánea de telemetría para las 16 GPUs del cluster,
    cubriendo deliberadamente los 4 estados canónicos del trabajo práctico:
    - NORMAL (condiciones estándar de trabajo seguro)
    - AHORRO (baja utilización pero consumo/frecuencia elevados innecesariamente)
    - PROTECCIÓN (temperatura crítica o potencia al límite de diseño térmico TDP)
    - ANOMALÍA / DATOS NO CONFIABLES (inconsistencias físicas, datos fuera de rango o nulos)
    """
    if seed is not None:
        random.seed(seed)

    if timestamp is None:
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    telemetry = []

    for cfg in GPU_CLUSTER_CONFIG:
        gpu_id = cfg["gpu_id"]
        node = cfg["node"]
        model = cfg["model"]

        # Escenario Canónico 1: ANOMALÍAS CONTROLADAS DE VERACIDAD
        if gpu_id == "GPU-12":
            # Lectura físicamente contradictoria (temp extrema con consumo casi nulo)
            record = {
                "timestamp": timestamp,
                "gpu_id": gpu_id,
                "node": node,
                "model": model,
                "temperature": 150.0,
                "power_w": 10.0,
                "utilization": 0.0,
                "frequency": 1200,
                "cooling": 0.0,
                "job_status": "ANOMALOUS_SENSOR",
                "energy_efficiency_gflops_w": 0.0,
                "scenario_tag": "ANOMALIA",
            }
        elif gpu_id == "GPU-13":
            # Lectura con valor nulo / potencia negativa / utilización > 100%
            record = {
                "timestamp": timestamp,
                "gpu_id": gpu_id,
                "node": node,
                "model": model,
                "temperature": None,
                "power_w": -45.0,
                "utilization": 108.0,
                "frequency": 1400,
                "cooling": 50.0,
                "job_status": "CORRUPTED_STREAM",
                "energy_efficiency_gflops_w": 0.0,
                "scenario_tag": "ANOMALIA",
            }

        # Escenario Canónico 2: PROTECCIÓN TÉRMICA Y ENERGÉTICA
        elif gpu_id in ("GPU-07", "GPU-14"):
            # Alta temperatura (>85°C), alto consumo (>700W), altísima utilización
            temp = 89.0 if gpu_id == "GPU-07" else 92.5
            pwr = 720.0 if gpu_id == "GPU-07" else 745.0
            util = 97.0 if gpu_id == "GPU-07" else 99.0
            freq = 2100 if gpu_id == "GPU-07" else 2150
            record = {
                "timestamp": timestamp,
                "gpu_id": gpu_id,
                "node": node,
                "model": model,
                "temperature": temp,
                "power_w": pwr,
                "utilization": util,
                "frequency": freq,
                "cooling": 95.0,
                "job_status": "TRAINING_AI_LLM",
                "energy_efficiency_gflops_w": round(util * 15.0 / pwr, 2),
                "scenario_tag": "PROTECCION",
            }

        # Escenario Canónico 3: OPORTUNIDAD DE AHORRO ENERGÉTICO (ENERGY SAVING)
        elif gpu_id in ("GPU-04", "GPU-11"):
            # Potencia y frecuencia elevadas para una utilización muy baja (GPU subutilizada/idle)
            temp = 58.0 if gpu_id == "GPU-04" else 55.0
            pwr = 380.0 if gpu_id == "GPU-04" else 360.0
            util = 14.0 if gpu_id == "GPU-04" else 18.0
            freq = 1950 if gpu_id == "GPU-04" else 1900
            record = {
                "timestamp": timestamp,
                "gpu_id": gpu_id,
                "node": node,
                "model": model,
                "temperature": temp,
                "power_w": pwr,
                "utilization": util,
                "frequency": freq,
                "cooling": 42.0,
                "job_status": "IDLE_STALLED",
                "energy_efficiency_gflops_w": round(util * 15.0 / pwr, 2),
                "scenario_tag": "AHORRO",
            }

        # Escenario Canónico 4: OPERACIÓN NORMAL
        else:
            # Rango seguro de operación: temp 58-68°C, pwr 320-450W, util 60-80%
            temp = round(random.uniform(59.0, 67.0), 1)
            pwr = round(random.uniform(330.0, 440.0), 1)
            util = round(random.uniform(62.0, 82.0), 1)
            freq = random.randint(1700, 1850)
            cooling = round(random.uniform(48.0, 62.0), 1)
            record = {
                "timestamp": timestamp,
                "gpu_id": gpu_id,
                "node": node,
                "model": model,
                "temperature": temp,
                "power_w": pwr,
                "utilization": util,
                "frequency": freq,
                "cooling": cooling,
                "job_status": "AI_INFERENCE_BATCH",
                "energy_efficiency_gflops_w": round(util * 15.0 / pwr, 2),
                "scenario_tag": "NORMAL",
            }

        telemetry.append(record)

    return telemetry


def generate_unstructured_logs(telemetry: List[Dict]) -> List[str]:
    """
    Genera logs textuales no estructurados (formato syslog/DCGM/IPMI)
    a partir del vector de telemetría para ilustrar la Variedad en Big Data.
    """
    logs = []
    for item in telemetry:
        ts = item["timestamp"]
        gid = item["gpu_id"]
        node = item["node"]
        tag = item.get("scenario_tag")

        if tag == "ANOMALIA":
            if item["temperature"] is None or item["power_w"] < 0:
                logs.append(
                    f"{ts} {node} kernel: [ERR] {gid}: Null pointer or parity mismatch in PCIe NVLINK telemetry buffer. PWR={item['power_w']}W, UTIL={item['utilization']}%"
                )
            else:
                logs.append(
                    f"{ts} {node} dcgm[1042]: [WARN] {gid}: Sensor thermistor #0 reported {item['temperature']}C while draw is {item['power_w']}W. Physical check required."
                )
        elif tag == "PROTECCION":
            logs.append(
                f"{ts} {node} dcgm[1042]: [ALERT] {gid}: Thermal junction limit approaching ({item['temperature']}C > 85.0C). High draw: {item['power_w']}W. Throttling flag set."
            )
        elif tag == "AHORRO":
            logs.append(
                f"{ts} {node} slurm_node[890]: [INFO] {gid}: Workload low activity ({item['utilization']}%). Clock lock at {item['frequency']}MHz. Inefficient power state."
            )
        else:
            logs.append(
                f"{ts} {node} dcgm[1042]: [INFO] {gid}: Telemetry normal. T={item['temperature']}C, P={item['power_w']}W, Util={item['utilization']}%, Freq={item['frequency']}MHz"
            )
    return logs


def generate_historical_batch(
    num_timestamps: int = 10, seed: int = DEFAULT_SEED
) -> Tuple[List[Dict], List[str]]:
    """
    Genera una serie temporal histórica con múltiples timestamps
    para alimentar los análisis Batch y la demostración MapReduce.
    """
    all_telemetry = []
    all_logs = []

    base_time = 1790856000  # Epoch representativo (año 2026)

    for step in range(num_timestamps):
        ts = datetime.fromtimestamp(base_time + (step * 60), timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        # Semilla variable suavemente por paso para generar variación histórica realista
        step_telemetry = generate_baseline_telemetry(timestamp=ts, seed=seed + step)
        all_telemetry.extend(step_telemetry)
        all_logs.extend(generate_unstructured_logs(step_telemetry))

    return all_telemetry, all_logs


def export_datasets(output_dir: str = "data") -> None:
    """
    Exporta los 3 formatos representativos de las 5 V (Variedad):
    - data/telemetry.csv (Estructurado)
    - data/telemetry.json (Semiestructurado)
    - data/logs.txt (No estructurado)
    """
    os.makedirs(output_dir, exist_ok=True)

    # Generar lote histórico consistente
    batch_telemetry, batch_logs = generate_historical_batch(num_timestamps=10)

    # 1. Guardar JSON (Semiestructurado)
    json_path = os.path.join(output_dir, "telemetry.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(batch_telemetry, f, indent=2, ensure_ascii=False)

    # 2. Guardar CSV (Estructurado)
    import pandas as pd

    df = pd.DataFrame(batch_telemetry)
    csv_path = os.path.join(output_dir, "telemetry.csv")
    df.to_csv(csv_path, index=False, encoding="utf-8")

    # 3. Guardar Logs (No estructurado)
    logs_path = os.path.join(output_dir, "logs.txt")
    with open(logs_path, "w", encoding="utf-8") as f:
        f.write("\n".join(batch_logs) + "\n")

    print(f"[OK] Datasets exportados exitosamente en: {output_dir}/")
    print(f"     - CSV:  {csv_path} ({len(df)} registros)")
    print(f"     - JSON: {json_path} ({len(batch_telemetry)} objetos)")
    print(f"     - LOGS: {logs_path} ({len(batch_logs)} líneas de eventos)")


if __name__ == "__main__":
    export_datasets()
