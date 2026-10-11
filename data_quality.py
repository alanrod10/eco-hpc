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
from typing import Any, Dict, List, Optional


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

    # Etiquetas legibles para los campos numéricos auditados (DRY: una sola definición).
    _FIELD_LABELS = {
        "temperature": "Temperatura",
        "power_w": "Potencia eléctrica",
        "utilization": "Utilización",
        "frequency": "Frecuencia de reloj",
    }

    @classmethod
    def _null_issue(cls, gpu_id: Any, field_name: str) -> str:
        """Mensaje canónico para un campo numérico nulo."""
        label = cls._FIELD_LABELS[field_name]
        return f"{gpu_id}: {label} es nula (None/NaN)"

    @classmethod
    def _range_issue(
        cls, gpu_id: Any, field_name: str, value: float, vmin: float, vmax: float, unit: str
    ) -> Optional[str]:
        """Devuelve el problema de rango físico si el valor está fuera de [vmin, vmax]."""
        if vmin <= value <= vmax:
            return None
        label = cls._FIELD_LABELS[field_name]
        decimals = 0 if field_name == "frequency" else 1
        return (
            f"{gpu_id}: {label} {value:.{decimals}f} {unit} fuera de rango admisible "
            f"[{vmin}, {vmax}] {unit}"
        )

    @classmethod
    def audit_record(cls, record: Dict[str, Any]) -> QualityResult:
        """
        Audita un registro individual de telemetría proveniente del sensor.

        Capas de verificación:
        1. Campos obligatorios presentes.
        2. Valores no nulos.
        3. Conversión tipada de los valores numéricos.
        4. Límites físicos admisibles por variable.
        5. Inconsistencias lógicas entre variables cruzadas.
        """
        issues: List[str] = []

        # 1. Verificación de campos obligatorios presentes
        missing_fields = [f for f in cls.MANDATORY_FIELDS if f not in record]
        if missing_fields:
            issues = [f"Campo obligatorio faltante: '{f}'" for f in missing_fields]
            return QualityResult(is_valid=False, issues=issues, cleaned_record=None)

        gpu_id = record.get("gpu_id")

        # 2. Detección de valores nulos o None
        numeric_fields = ("temperature", "power_w", "utilization", "frequency")
        null_issues = [
            cls._null_issue(gpu_id, field_name)
            for field_name in numeric_fields
            if record.get(field_name) is None
        ]
        if null_issues:
            return QualityResult(is_valid=False, issues=null_issues, cleaned_record=None)

        # 3. Conversión de tipos y validación de rangos numéricos
        try:
            values = {field_name: float(record[field_name]) for field_name in numeric_fields}
        except (ValueError, TypeError) as e:
            issues.append(f"{gpu_id}: Error de tipo en datos numéricos ({e})")
            return QualityResult(is_valid=False, issues=issues, cleaned_record=None)

        # 4. Verificación de límites físicos
        physical_limits = [
            ("temperature", cls.TEMP_MIN, cls.TEMP_MAX, "°C"),
            ("power_w", cls.POWER_MIN, cls.POWER_MAX, "W"),
            ("utilization", cls.UTIL_MIN, cls.UTIL_MAX, "%"),
            ("frequency", cls.FREQ_MIN, cls.FREQ_MAX, "MHz"),
        ]
        for field_name, vmin, vmax, unit in physical_limits:
            issue = cls._range_issue(gpu_id, field_name, values[field_name], vmin, vmax, unit)
            if issue:
                issues.append(issue)

        # 5. Detección de inconsistencias lógicas entre variables cruzadas
        # Ejemplo: Temperatura extrema (>95°C) con disipación de potencia casi nula (<40W) y utilización 0%
        temp_val, power_val, util_val = values["temperature"], values["power_w"], values["utilization"]
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
