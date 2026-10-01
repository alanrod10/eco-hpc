"""
data_quality.py - Módulo de Veracidad y Calidad de Datos para ECO-HPC
--------------------------------------------------------------------
Implementa los controles de calidad de datos correspondientes a la V de
VERACIDAD del Big Data, antes de que las lecturas ingresen al agente.

Verifica:
1. Existencia y completitud de campos obligatorios.
2. Detección de valores nulos o tipos inválidos.
3. Validación de límites físicos admisibles para hardware GPU HPC.
4. Detección de inconsistencias lógicas (ej. temperatura extrema sin potencia).
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class QualityResult:
    """Resultado del control de calidad sobre una percepción de telemetría."""
    is_valid: bool
    issues: List[str] = field(default_factory=list)
    cleaned_record: Optional[Dict[str, Any]] = None

    @property
    def status_label(self) -> str:
        return "VÁLIDO" if self.is_valid else "ANOMALÍA DETECTADA"


class DataQualityAuditor:
    """
    Auditor de calidad y veracidad de datos de telemetría de hardware HPC.
    
    Límites físicos admisibles configurados como parámetros del prototipo:
    - Temperatura: 15.0 °C a 105.0 °C (bajo 15°C es anómalo en datacenter; sobre 105°C supera límite de apagado por hardware).
    - Potencia: 20.0 W a 900.0 W (valores negativos son errores eléctricos; >900 W supera el consumo de aceleradores como H100 SXM con hasta 700 W configurables según documentación de NVIDIA).
    - Utilización: 0.0 % a 100.0 %.
    - Frecuencia: 200 MHz a 2800 MHz.
    - Refrigeración (cooling): 0.0 % a 100.0 %.
    """

    MANDATORY_FIELDS = ["gpu_id", "temperature", "power_w", "utilization", "frequency"]

    TEMP_MIN = 15.0
    TEMP_MAX = 105.0
    POWER_MIN = 20.0
    POWER_MAX = 900.0
    UTIL_MIN = 0.0
    UTIL_MAX = 100.0
    FREQ_MIN = 200
    FREQ_MAX = 2800

    @classmethod
    def audit_record(cls, record: Dict[str, Any]) -> QualityResult:
        """
        Audita un registro individual de telemetría proveniente del sensor.
        """
        issues: List[str] = []

        # 1. Verificación de campos obligatorios presentes
        for req_field in cls.MANDATORY_FIELDS:
            if req_field not in record:
                issues.append(f"Campo obligatorio faltante: '{req_field}'")

        if issues:
            return QualityResult(is_valid=False, issues=issues, cleaned_record=None)

        gpu_id = record.get("gpu_id")
        temp = record.get("temperature")
        power = record.get("power_w")
        util = record.get("utilization")
        freq = record.get("frequency")

        # 2. Detección de valores nulos o None
        if temp is None:
            issues.append(f"{gpu_id}: Temperatura es nula (None/NaN)")
        if power is None:
            issues.append(f"{gpu_id}: Potencia eléctrica es nula (None/NaN)")
        if util is None:
            issues.append(f"{gpu_id}: Utilización es nula (None/NaN)")
        if freq is None:
            issues.append(f"{gpu_id}: Frecuencia de reloj es nula (None/NaN)")

        if issues:
            return QualityResult(is_valid=False, issues=issues, cleaned_record=None)

        # 3. Conversión de tipos y validación de rangos numéricos
        try:
            temp_val = float(temp)
            power_val = float(power)
            util_val = float(util)
            freq_val = float(freq)
        except (ValueError, TypeError) as e:
            issues.append(f"{gpu_id}: Error de tipo en datos numéricos ({e})")
            return QualityResult(is_valid=False, issues=issues, cleaned_record=None)

        # 4. Verificación de límites físicos
        if not (cls.TEMP_MIN <= temp_val <= cls.TEMP_MAX):
            issues.append(
                f"{gpu_id}: Temperatura {temp_val:.1f} °C fuera de rango admisible [{cls.TEMP_MIN}, {cls.TEMP_MAX}] °C"
            )

        if not (cls.POWER_MIN <= power_val <= cls.POWER_MAX):
            issues.append(
                f"{gpu_id}: Potencia {power_val:.1f} W fuera de rango admisible [{cls.POWER_MIN}, {cls.POWER_MAX}] W"
            )

        if not (cls.UTIL_MIN <= util_val <= cls.UTIL_MAX):
            issues.append(
                f"{gpu_id}: Utilización {util_val:.1f}% fuera de rango admisible [{cls.UTIL_MIN}, {cls.UTIL_MAX}]%"
            )

        if not (cls.FREQ_MIN <= freq_val <= cls.FREQ_MAX):
            issues.append(
                f"{gpu_id}: Frecuencia {freq_val:.0f} MHz fuera de rango admisible [{cls.FREQ_MIN}, {cls.FREQ_MAX}] MHz"
            )

        # 5. Detección de inconsistencias lógicas entre variables cruzadas
        # Ejemplo: Temperatura extrema (>95°C) con disipación de potencia casi nula (<40W) y utilización 0%
        if temp_val > 95.0 and power_val < 40.0 and util_val == 0.0:
            issues.append(
                f"{gpu_id}: Inconsistencia física: Temp extrema ({temp_val:.1f} °C) sin consumo eléctrico ({power_val:.1f} W). Posible falla de termistor o bus I2C."
            )

        is_valid = len(issues) == 0
        cleaned = dict(record) if is_valid else None

        return QualityResult(is_valid=is_valid, issues=issues, cleaned_record=cleaned)

    @classmethod
    def audit_batch(cls, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Audita un lote completo de registros de telemetría y entrega métricas
        consolidadas de veracidad.
        """
        total = len(records)
        valid = 0
        anomalies = 0
        missing = 0
        all_issues = []

        for r in records:
            res = cls.audit_record(r)
            if res.is_valid:
                valid += 1
            else:
                anomalies += 1
                for iss in res.issues:
                    all_issues.append(iss)
                    if "nula" in iss.lower() or "faltante" in iss.lower():
                        missing += 1

        veracity_rate = (valid / total * 100.0) if total > 0 else 0.0

        return {
            "total_records": total,
            "valid_records": valid,
            "anomalous_records": anomalies,
            "missing_records": missing,
            "veracity_rate_pct": round(veracity_rate, 2),
            "issues_list": all_issues,
        }
