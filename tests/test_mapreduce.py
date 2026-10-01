"""
test_mapreduce.py - Pruebas Unitarias de la Demostración de MapReduce
---------------------------------------------------------------------
Verifica la ejecución exacta de las fases:
1. Map: emisión de pares clave-valor
2. Shuffle: agrupamiento por clave
3. Reduce: agregación matemática de consumo y temperatura
"""

from mapreduce_demo import execute_mapreduce, map_function, reduce_function, shuffle_function


def test_map_function():
    record = {
        "gpu_id": "GPU-01",
        "power_w": 300.0,
        "temperature": 62.0,
        "utilization": 70.0,
    }
    key, val = map_function(record)
    assert key == "GPU-01"
    assert val["power_w"] == 300.0
    assert val["temperature"] == 62.0
    assert val["count"] == 1


def test_shuffle_function():
    mapped_pairs = [
        ("GPU-01", {"power_w": 300.0, "temperature": 60.0, "count": 1}),
        ("GPU-01", {"power_w": 320.0, "temperature": 64.0, "count": 1}),
        ("GPU-02", {"power_w": 500.0, "temperature": 75.0, "count": 1}),
        ("GPU-02", {"power_w": 520.0, "temperature": 77.0, "count": 1}),
    ]
    shuffled = shuffle_function(mapped_pairs)
    assert "GPU-01" in shuffled
    assert "GPU-02" in shuffled
    assert len(shuffled["GPU-01"]) == 2
    assert len(shuffled["GPU-02"]) == 2


def test_reduce_function_averaging():
    values_gpu01 = [
        {"power_w": 300.0, "temperature": 60.0, "utilization": 70.0, "count": 1},
        {"power_w": 320.0, "temperature": 64.0, "utilization": 72.0, "count": 1},
    ]
    reduced = reduce_function("GPU-01", values_gpu01)
    assert reduced["gpu_id"] == "GPU-01"
    assert reduced["records_processed"] == 2
    assert reduced["avg_power_w"] == 310.0  # (300 + 320) / 2 = 310.0
    assert reduced["max_temperature_c"] == 64.0
    assert reduced["total_energy_kwh"] > 0


def test_full_mapreduce_pipeline():
    telemetry = [
        {"gpu_id": "GPU-01", "power_w": 300.0, "temperature": 60.0, "utilization": 70.0},
        {"gpu_id": "GPU-01", "power_w": 320.0, "temperature": 62.0, "utilization": 72.0},
        {"gpu_id": "GPU-02", "power_w": 500.0, "temperature": 70.0, "utilization": 80.0},
        {"gpu_id": "GPU-02", "power_w": 520.0, "temperature": 72.0, "utilization": 82.0},
    ]
    res = execute_mapreduce(telemetry)
    assert res["input_records_count"] == 4
    assert res["unique_keys_count"] == 2
    assert res["reduce_results"]["GPU-01"]["avg_power_w"] == 310.0
    assert res["reduce_results"]["GPU-02"]["avg_power_w"] == 510.0
