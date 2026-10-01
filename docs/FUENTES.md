# REGISTRO FORMAL DE FUENTES Y EVIDENCIA ACADÉMICA
## Proyecto ECO-HPC: Agente Supervisor de Eficiencia Energética

---

El presente documento registra de manera rigurosa, verificable y trazable las fuentes primarias de información técnica, normativa y académica utilizadas en la elaboración de **ECO-HPC**.

Cada entrada clasifica el tipo de conocimiento según el **Control de Evidencia**:
* **HECHO CONFIRMADO:** Respaldado directamente por normas oficiales, especificaciones de fabricantes o literatura académica canónica.
* **SUPUESTO CALCULADO:** Derivado matemáticamente a partir de parámetros razonables de ingeniería para nuestro escenario.
* **SIMULACIÓN:** Datos generados mediante modelos computacionales para demostrar el funcionamiento del agente.
* **PROPUESTA:** Diseño arquitectónico formulado para una futura implementación a gran escala.

---

## 1. Fuentes Jurídicas y Normativas Oficiales

### 1.1. Ley Nacional N.º 25.326 — Protección de los Datos Personales
* **Fuente:** InfoLEG (Centro de Documentación e Información, Ministerio de Justicia de la Nación Argentina).
* **Título Oficial:** *Ley N.º 25.326 de Protección de los Datos Personales (Habeas Data)*.
* **Autor / Organización:** Honorable Congreso de la Nación Argentina.
* **Fecha / Sanción:** Sancionada en octubre de 2000; promulgada parcialmente por Decreto 1616/2000. Texto actualizado con reformas.
* **URL Oficial:** `https://servicios.infoleg.gob.ar/infolegInternet/anexos/60000-64999/64790/norma.htm`
* **Qué dato o concepto respalda:**  
  - Definición de datos personales (Art. 2): Información referida a personas determinadas o determinables.
  - Principio de calidad y minimización de datos (Art. 4): Exige recabar únicamente los datos necesarios y pertinentes para la finalidad.
  - Deber de seguridad y confidencialidad (Arts. 9 y 10): Obligación de adoptar medidas técnicas que eviten la alteración, pérdida o acceso no autorizado.
* **Nivel de Evidencia:** **HECHO CONFIRMADO.**

---

### 1.2. Resolución 47/2018 — Agencia de Acceso a la Información Pública (AAIP)
* **Fuente:** InfoLEG / Sitio Oficial de la AAIP (`argentina.gob.ar/aaip`).
* **Título Oficial:** *Resolución 47/2018: Medidas de Seguridad Recomendadas para el Tratamiento y Conservación de los Datos Personales en Medios Informatizados y No Informatizados*.
* **Autor / Organización:** Agencia de Acceso a la Información Pública (Órgano de Control de la Ley 25.326).
* **Fecha:** 24 de julio de 2018.
* **URL Oficial:** `https://servicios.infoleg.gob.ar/infolegInternet/anexos/315000-319999/315998/norma.htm`
* **Qué dato o concepto respalda:**  
  - Estándares de seguridad técnica aplicables a bancos de datos y sistemas de cómputo (Anexo I: Medios Informatizados).
  - Pautas sobre control de acceso basado en roles (RBAC), registro de auditoría (*logging*), copias de respaldo y cifrado de canales de comunicación.
* **Nivel de Evidencia:** **HECHO CONFIRMADO.**

---

## 2. Fuentes Académicas y Paradigmas de Inteligencia Artificial y Big Data

### 2.1. Russell, S. & Norvig, P. — Agentes Inteligentes y Marco PEAS
* **Fuente:** Pearson Education.
* **Título:** *Artificial Intelligence: A Modern Approach* (4th Edition).
* **Autor:** Stuart Russell y Peter Norvig.
* **Año:** 2020.
* **URL de Referencia:** `https://aima.cs.berkeley.edu/`
* **Qué dato o concepto respalda:**  
  - Formalización del marco **PEAS** (Performance measure, Environment, Actuators, Sensors) en el Capítulo 2.
  - Definición y taxonomía de agentes: Agentes reactivos simples, agentes reactivos basados en modelos con estado interno y agentes basados en metas/utilidad.
  - Justificación de la racionalidad de un agente basada en reglas explícitas frente a modelos opacos.
* **Nivel de Evidencia:** **HECHO CONFIRMADO.**

---

### 2.2. Dean, J. & Ghemawat, S. — Paradigma MapReduce
* **Fuente:** Google Research / 6th Symposium on Operating System Design and Implementation (OSDI '04).
* **Título:** *MapReduce: Simplified Data Processing on Large Clusters*.
* **Autor:** Jeffrey Dean y Sanjay Ghemawat.
* **Año:** 2004.
* **URL Oficial:** `https://research.google/pubs/pub62/`
* **Qué dato o concepto respalda:**  
  - Semántica formal de las fases: función `Map(k1, v1) -> list(k2, v2)`, etapa intermedia de particionamiento y ordenamiento (*Shuffle & Sort*), y función de reducción agregada `Reduce(k2, list(v2)) -> list(k3, v3)`.
  - Aplicabilidad del procesamiento en paralelo para análisis masivo de series de tiempo históricas sin depender de bases relacionales.
* **Nivel de Evidencia:** **HECHO CONFIRMADO.**

---

## 3. Fuentes Técnicas de Hardware, HPC y Supercómputo

### 3.1. NVIDIA Data Center GPU Manager (DCGM) & NVML API
* **Fuente:** NVIDIA Developer Documentation.
* **Título:** *NVIDIA DCGM Architecture and Metric Reference Guide*.
* **Autor / Organización:** NVIDIA Corporation.
* **Versión / Fecha:** Documentación técnica oficial (versión 2024 / arquitectura Hopper/Blackwell).
* **URL Oficial:** `https://docs.nvidia.com/datacenter/dcgm/latest/`
* **Qué dato o concepto respalda:**  
  - Rangos térmicos y eléctricos reales de aceleradores de centro de datos: TDP (Thermal Design Power) de hasta 700 W en NVIDIA H100 PCIe/SXM.
  - Identificación de métricas de telemetría estándar: `gpu_utilization`, `temperature_gpu`, `power_draw`, `sm_clock_freq`, `fan_speed` y eventos de `thermal_violation_time`.
  - Mecanismos de protección por hardware: *Thermal Throttling*, modulación de estados de energía (*P-States*) y limitación de potencia por software (*power capping*).
* **Nivel de Evidencia:** **HECHO CONFIRMADO.**

---

### 3.2. The Green500 — Eficiencia Energética en Supercómputo
* **Fuente:** TOP500.org.
* **Título:** *The Green500 List: Ranking of the Most Energy-Efficient Supercomputers in the World*.
* **Autor / Organización:** TOP500 Project.
* **Fecha:** Ediciones bianuales (vigente 2024).
* **URL Oficial:** `https://www.top500.org/lists/green500/`
* **Qué dato o concepto respalda:**  
  - Métricas estándar de sostenibilidad en HPC: GFLOPS/Watt (miles de millones de operaciones en punto flotante por vatio consumido).
  - PUE (*Power Usage Effectiveness*) en centros de datos modernos de IA (rango típico de 1.15 a 1.35).
* **Nivel de Evidencia:** **HECHO CONFIRMADO.**

---

## 4. Cuadro de Clasificación de Evidencia del Proyecto ECO-HPC

| Afirmación o Elemento del Proyecto | Clasificación de Evidencia | Justificación Metodológica |
| :--- | :--- | :--- |
| **Consumo eléctrico de GPUs H100 (~700W) y límites térmicos (85°C)** | **Hecho Confirmado** | Extraído directamente de la documentación oficial de arquitectura de hardware NVIDIA. |
| **Definición de PEAS y taxonomía de agentes inteligentes** | **Hecho Confirmado** | Basado en el libro de texto canónico de Russell & Norvig (2020). |
| **Criterio de dato personal por vinculación cruzada** | **Hecho Confirmado** | Conforme a la definición del Art. 2 de la Ley 25.326 y dictámenes de la AAIP. |
| **Algoritmo de Map, Shuffle y Reduce** | **Hecho Confirmado** | Implementación fiel del paradigma matemático de Dean & Ghemawat (2004). |
| **Cálculo de 88.473.600 lecturas diarias en 1.024 GPUs (~22,1 GB/día)** | **Supuesto Calculado** | Derivado matemáticamente asumiendo muestreo de 1 segundo y payload promedio de 250 bytes. |
| **Lote de telemetría de 16 GPUs (`data/telemetry.csv`)** | **Simulación** | Generado sintéticamente con modelos realistas para demostrar los estados del agente. |
| **Ajuste de frecuencia DVFS y apagado de trabajos en SLURM** | **Simulación** | Comandos formulados conceptualmente y mostrados en la UI; no intervienen fierros reales. |
| **Arquitectura distribuida con Kafka, Flink y Cassandra/TimescaleDB** | **Propuesta** | Diseño conceptual para producción a escala; no se despliega en el prototipo local. |
