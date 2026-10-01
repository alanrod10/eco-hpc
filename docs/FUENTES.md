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

## 1. Bibliografía Académica

### 1.1. Joyanes Aguilar, L. — Fundamentos de Big Data y las 5 V
* **Referencia:** Joyanes Aguilar, L. (2013). *Big Data: Análisis de grandes volúmenes de datos en organizaciones*. Alfaomega.
* **Qué dato o concepto respalda:**  
  - Caracterización conceptual y metodológica de las dimensiones del Big Data: Volumen, Velocidad, Variedad, Veracidad y Valor.
  - El rol del Big Data como infraestructura de captura y sensado para la alimentación de sistemas analíticos y de toma de decisiones.
* **Nivel de Evidencia:** **HECHO CONFIRMADO.**

---

### 1.2. Russell, S. J. & Norvig, P. — Agentes Inteligentes y Marco PEAS
* **Referencia:** Russell, S. J. & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach*. Pearson.
* **URL de Referencia:** `https://aima.cs.berkeley.edu/`
* **Qué dato o concepto respalda:**  
  - Formalización del marco **PEAS** (Performance measure, Environment, Actuators, Sensors) en el Capítulo 2 (*Intelligent Agents*).
  - Definición y taxonomía de agentes: agentes reactivos simples y agentes reactivos con modelo de estado interno.
  - Justificación de la racionalidad de un agente basada en reglas explícitas frente a modelos opacos.
* **Nivel de Evidencia:** **HECHO CONFIRMADO.**

---

### 1.3. Dean, J. & Ghemawat, S. — Paradigma MapReduce
* **Referencia:** Dean, J. & Ghemawat, S. (2004). *MapReduce: Simplified Data Processing on Large Clusters*. Communications of the ACM, 51(1), 107-113. Google Research.
* **URL Oficial:** `https://research.google/pubs/pub62/`
* **Qué dato o concepto respalda:**  
  - Semántica formal de las fases: función `Map(k1, v1) -> list(k2, v2)`, etapa intermedia de particionamiento y ordenamiento (*Shuffle & Sort*), y función de reducción agregada `Reduce(k2, list(v2)) -> list(k3, v3)`.
  - Aplicabilidad del procesamiento en paralelo para análisis masivo de series de tiempo históricas sin depender de bases relacionales.
* **Nivel de Evidencia:** **HECHO CONFIRMADO.**

---

## 2. Fuentes Normativas y Documentación Técnica Oficial

### 2.1. Ley Nacional N.º 25.326 — Protección de los Datos Personales
* **Fuente:** InfoLEG (Centro de Documentación e Información, Ministerio de Justicia de la Nación Argentina).
* **Título Oficial:** *Ley N.º 25.326 de Protección de los Datos Personales (Habeas Data)*.
* **Autor / Organización:** Honorable Congreso de la Nación Argentina.
* **Fecha / Sanción:** Sancionada en octubre de 2000; promulgada parcialmente por Decreto 1616/2000. Texto actualizado con reformas.
* **URL Oficial:** `https://servicios.infoleg.gob.ar/infolegInternet/anexos/60000-64999/64790/norma.htm`
* **Qué dato o concepto respalda:**  
  - Definición de datos personales y datos sensibles (Art. 2): Información referida a personas determinadas o determinables, y régimen especial restrictivo para datos sensibles.
  - Principios de calidad, pertinencia y finalidad (Art. 4): Exige recabar datos ciertos, adecuados y no utilizarlos para finalidades incompatibles.
  - Deber de seguridad y confidencialidad (Arts. 9 y 10): Obligación de adoptar medidas técnicas que eviten la alteración, pérdida o acceso no autorizado.
* **Nivel de Evidencia:** **HECHO CONFIRMADO.**

---

### 2.2. Resolución 47/2018 — Agencia de Acceso a la Información Pública (AAIP)
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

### 2.3. Apache Cassandra — Almacenamiento Wide-Column NoSQL
* **Fuente:** Apache Software Foundation Documentation.
* **Título:** *Apache Cassandra Documentation (Architecture Guide)*.
* **Autor / Organización:** The Apache Software Foundation.
* **Versión / Fecha:** Documentación oficial 2024.
* **URL Oficial:** `https://cassandra.apache.org/doc/latest/`
* **Qué dato o concepto respalda:**  
  - Tecnología NoSQL de tipo wide-column tomada como referencia conceptual para el almacenamiento distribuido en producción.
  - Arquitectura basada en *Log-Structured Merge-trees (LSM-Trees)*: escrituras secuenciales en memoria (*Memtable*), volcados a disco en *SSTables*, particionamiento horizontal peer-to-peer y políticas nativas de retención (*TTL*).
* **Nivel de Evidencia:** **HECHO CONFIRMADO (Referencia Técnica Conceptual).**

---

### 2.4. NVIDIA Data Center GPU Manager (DCGM) & NVML API
* **Fuente:** NVIDIA Developer Documentation.
* **Título:** *NVIDIA DCGM Architecture and Metric Reference Guide*.
* **Autor / Organización:** NVIDIA Corporation.
* **Versión / Fecha:** Documentación técnica oficial (versión 2024 / arquitectura Hopper/Blackwell).
* **URL Oficial:** `https://docs.nvidia.com/datacenter/dcgm/latest/`
* **Qué dato o concepto respalda:**  
  - Rangos térmicos y eléctricos de aceleradores reales: H100 SXM cuenta con hasta 700 W configurables según especificaciones oficiales de NVIDIA, mientras que el formato PCIe opera típicamente en 300-350 W. Se utiliza como marco contextual; el prototipo utiliza GPUs simuladas y 700 W no es un límite universal de toda GPU.
  - Identificación de métricas de telemetría estándar: `gpu_utilization`, `temperature_gpu`, `power_draw`, `sm_clock_freq`, `fan_speed` y eventos de `thermal_violation_time`.
  - Mecanismos de protección por hardware: *Thermal Throttling*, modulación de estados de energía (*P-States*) y limitación de potencia por software (*power capping*).
* **Nivel de Evidencia:** **HECHO CONFIRMADO.**

---

### 2.5. The Green500 — Eficiencia Energética en Supercómputo
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

## 3. Cuadro de Clasificación de Evidencia del Proyecto ECO-HPC

| Afirmación o Elemento del Proyecto | Clasificación de Evidencia | Justificación Metodológica |
| :--- | :--- | :--- |
| **Especificación de H100 SXM (hasta 700 W configurables) y métricas DCGM** | **Hecho Confirmado** | Extraído directamente de la documentación oficial de arquitectura de hardware NVIDIA. |
| **Definición de PEAS y taxonomía de agentes inteligentes** | **Hecho Confirmado** | Basado en el libro de texto canónico de Russell, S. J. & Norvig, P. (2021). |
| **Definición y principios de datos personales y sensibles** | **Hecho Confirmado** | Conforme a la definición del Art. 2 de la Ley 25.326 y dictámenes de la AAIP. |
| **Algoritmo de Map, Shuffle y Reduce** | **Hecho Confirmado** | Implementación fiel del paradigma matemático de Dean & Ghemawat (2004). |
| **Cálculo de 88.473.600 lecturas diarias en 1.024 GPUs (~22,12 GB/día)** | **Supuesto Calculado** | Derivado matemáticamente asumiendo muestreo de 1 segundo y payload promedio de 250 bytes. |
| **Lote de telemetría de 16 GPUs (`data/telemetry.csv`)** | **Simulación** | Generado sintéticamente con modelos realistas para demostrar los estados del agente. |
| **Ajuste de frecuencia DVFS y modulación de trabajos en SLURM** | **Simulación** | Comandos formulados conceptualmente y mostrados en la UI; no intervienen fierros reales. |
| **Semántica de ventana fija de 60 s por registro en MapReduce** | **Supuesto del Dataset / Supuesto Calculado** | Cada registro representa una ventana de muestreo fija de 60 s donde el timestamp identifica su inicio (10 registros = 10 min = 0,1667 h). No es una medición física continua. |
| **Arquitectura distribuida con Kafka, Flink y Apache Cassandra (wide-column)** | **Propuesta** | Diseño conceptual para producción a escala; no se despliega en el prototipo local. |
