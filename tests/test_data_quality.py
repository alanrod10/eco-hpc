"""
test_data_quality.py - Pruebas Unitarias del Filtro de Veracidad
----------------------------------------------------------------
Verifica que el DataQualityAuditor detecte correctamente datos válidos,
datos faltantes, datos fuera de rango e inconsistencias físicas cruzadas.
"""

import pytest
from data_quality import DataQualityAuditor


def test_valid_record():
    valid = {
        "gpu_id": "GPU-01",
        "temperature": 62.5,
        "power_w": 350.0,
        "utilization": 75.0,
        "frequency": 1800,
        "cooling": 55.0,
        "job_status": "AI_TRAINING",
    }
    res = DataQualityAuditor.audit_record(valid)
    assert res.is_valid is True
    assert len(res.issues) == 0
    assert res.status_label == "VÁLIDO"
    assert res.cleaned_record is not None


def test_missing_mandatory_field():
    missing = {
        "gpu_id": "GPU-02",
        "temperature": 60.0,
        "power_w": 300.0,
        # falta utilization y frequency
    }
    res = DataQualityAuditor.audit_record(missing)
    assert res.is_valid is False
    assert any("utilization" in iss for iss in res.issues)
    assert any("frequency" in iss for iss in res.issues)


def test_null_value_detected():
    null_record = {
        "gpu_id": "GPU-03",
        "temperature": None,
        "power_w": 320.0,
        "utilization": 50.0,
        "frequency": 1700,
    }
    res = DataQualityAuditor.audit_record(null_record)
    assert res.is_valid is False
    assert any("Temperatura es nula" in iss for iss in res.issues)


def test_out_of_bounds_temperature():
    extreme_hot = {
        "gpu_id": "GPU-04",
        "temperature": 150.0,  # Excede límite físico de silicio
        "power_w": 400.0,
        "utilization": 80.0,
        "frequency": 1800,
    }
    res = DataQualityAuditor.audit_record(extreme_hot)
    assert res.is_valid is False
    assert any("fuera de rango admisible" in iss for iss in res.issues)


def test_out_of_bounds_negative_power():
    neg_power = {
        "gpu_id": "GPU-05",
        "temperature": 60.0,
        "power_w": -45.0,  # Violación física en sensor eléctrico
        "utilization": 80.0,
        "frequency": 1800,
    }
    res = DataQualityAuditor.audit_record(neg_power)
    assert res.is_valid is False
    assert any("Potencia" in iss and "fuera de rango" in iss for iss in res.issues)


def test_cross_variable_contradiction():
    # Temp de fundición (120°C) con potencia casi nula (15W) y sin carga (0%)
    contradiction = {
        "gpu_id": "GPU-12",
        "temperature": 102.0,
        "power_w": 25.0,
        "utilization": 0.0,
        "frequency": 1200,
    }
    res = DataQualityAuditor.audit_record(contradiction)
    assert res.is_valid is False
    assert any("Inconsistencia física" in iss for iss in res.issues)


def test_batch_audit_statistics():
    batch = [
        {"gpu_id": "GPU-01", "temperature": 60.0, "power_w": 300.0, "utilization": 50.0, "frequency": 1700},
        {"gpu_id": "GPU-02", "temperature": None, "power_w": 300.0, "utilization": 50.0, "frequency": 1700},
        {"gpu_id": "GPU-03", "temperature": 150.0, "power_w": 10.0, "utilization": 0.0, "frequency": 1200},
    ]
    summary = DataQualityAuditor.audit_batch(batch)
    assert summary["total_records"] == 3
    assert summary["valid_records"] == 1
    assert summary["anomalous_records"] == 2
    assert summary["missing_records"] >= 1
    assert summary["veracity_rate_pct"] == 33.33
