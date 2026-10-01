# ARQUITECTURA TÉCNICA DEL SISTEMA: ECO-HPC

---

## 1. Visión General de la Arquitectura

El sistema **ECO-HPC** implementa una arquitectura desacoplada y modular orientada a eventos de telemetría de hardware. El diseño responde a una estricta separación entre:
1. **La Arquitectura Implementada en el Prototipo:** Diseñada con Python 3.14, Pandas y Streamlit para garantizar simplicidad, reproducibilidad local y alta transparencia académica.
2. **La Arquitectura Conceptual a Escala (1.024 GPUs):** Diseñada para ilustrar cómo el sistema escalaría horizontalmente en un centro de datos de supercómputo en producción.

---

## 2. Arquitectura Implementada en el Prototipo

El prototipo funcional opera mediante una canalización lineal determinista de datos que garantiza una **Única Fuente de Verdad** (*Single Source of Truth*):

```text
┌────────────────────────────────────────────────────────┐
│             SIMULADOR DE TELEMETRÍA                    │
│                  (simulator.py)                        │
└──────────────────────────┬─────────────────────────────┘
                           │ Genera lote consistente
                           ▼
┌────────────────────────────────────────────────────────┐
│            DATASETS LOCALES (data/)                    │
│   ├── telemetry.csv  (Estructurado)                    │
│   ├── telemetry.json (Semiestructurado)                │
│   └── logs.txt       (No estructurado)                 │
└──────────────────────────┬─────────────────────────────┘
                           │ Lecturas de percepción
                           ▼
┌────────────────────────────────────────────────────────┐
│         CONTROL DE CALIDAD Y VERACIDAD                 │
│                (data_quality.py)                       │
│   • Detección de nulos y tipos                         │
│   • Filtro de rangos físicos [15°C - 105°C]            │
│   • Consistencia física cruzada                        │
└────────────┬───────────────────────────────┬───────────┘
             │ Si es válido                  │ Si es anómalo
             ▼                               ▼
┌────────────────────────┐      ┌────────────────────────┐
│   ESTADO: NORMAL /     │      │  ESTADO: DATOS NO      │
│   AHORRO / PROTECCIÓN  │      │  CONFIABLES            │
└────────────┬───────────┘      └────────────┬───────────┘
             │                               │
             ▼                               ▼
┌────────────────────────────────────────────────────────┐
│            MOTOR DE REGLAS JERÁRQUICO                  │
│                   (rules.py)                           │
│   • Umbrales de simulación configurables               │
│   • Asignación de acción determinista                  │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│               AGENTE SUPERVISOR                        │
│                   (agent.py)                           │
│   • Actualización de memoria interna (histórico)       │
│   • Acumulación de ahorro en kWh simulados             │
│   • Respuestas a preguntas canónicas                   │
└────────────┬───────────────────────────────┬───────────┘
             │                               │
             ▼                               ▼
┌────────────────────────┐      ┌────────────────────────┐
│  DASHBOARD INTERACTIVO │      │ DEMOSTRACIÓN MAPREDUCE │
│        (app.py)        │      │  (mapreduce_demo.py)   │
│   • Vista de clúster   │      │   • Map                │
│   • Inspector de GPU   │      │   • Shuffle            │
│   • Modo Demo 5 pasos  │      │   • Reduce             │
└────────────────────────┘      └────────────────────────┘
```

### 2.1. Módulos y Responsabilidades del Prototipo
1. **`simulator.py` (Generador de Escenarios):**
   - Sintetiza lecturas para 16 GPUs (`GPU-01` a `GPU-16`) en 4 nodos de cómputo.
   - Modela escenarios canónicos reproducibles: Normal, Ahorro (subutilización con alto reloj), Protección (alta temperatura y pico de potencia) y Anomalía de Veracidad (fallos de sensor, inconsistencias y valores nulos).
   - Exporta simultáneamente los 3 formatos representativos de la Variedad en Big Data.
2. **`data_quality.py` (Módulo de Veracidad):**
   - Implementa la clase `DataQualityAuditor`.
   - Verifica campos obligatorios, ausencia de nulos y adhesión a límites físicos de ingeniería para silicio de GPU.
   - Detecta inconsistencias cruzadas (ej. temperaturas extremas $>95\text{ }^\circ\text{C}$ sin consumo eléctrico $<40\text{ W}$).
3. **`rules.py` (Motor de Reglas y Umbrales):**
   - Define los 4 estados canónicos (`NORMAL`, `AHORRO`, `PROTECCION`, `DATOS NO CONFIABLES`) y las 5 acciones simuladas (`MANTENER`, `AHORRAR`, `REFRIGERAR`, `PROTEGER`, `REVISAR SENSOR`).
   - Declara los umbrales de simulación de manera abierta y parametrizable (no como leyes físicas inmutables).
4. **`agent.py` (Agente Inteligente con Estado Interno):**
   - Implementa el ciclo cognitivo formal: *Percepciones → Control de Calidad → Estado Interno → Decisión → Acción*.
   - Mantiene el historial de intervenciones y acumula el ahorro energético proyectado en kWh simulados.
5. **`mapreduce_demo.py` (Motor de Análisis Batch):**
   - Implementa algorítmicamente en Python puro las etapas de `map_function`, `shuffle_function` y `reduce_function`.
   - Calcula métricas consolidadas (promedio de potencia, temperatura máxima y energía total) sobre el histórico temporal.
6. **`app.py` (Interfaz de Usuario Streamlit):**
   - Presenta el sistema en 12 vistas estructuradas con navegación lateral.
   - Incluye el **Modo Demo de Exposición** para guiar la presentación oral ante el tribunal.

---

## 3. Arquitectura Conceptual de Producción (Escala 1.024 GPUs)

Para un entorno real de supercómputo que supervise 1.024 GPUs aceleradoras, la arquitectura física evolucionaría hacia un modelo distribuido de alta disponibilidad:

```text
[ RACK 01 ] ... [ RACK 32 ]  (1.024 GPUs NVIDIA H100 en 128 Nodos)
       │              │
       ▼              ▼
[ DAEMONS LOCALES DE TELEMETRÍA ] (NVIDIA DCGM Exporters / PromQL / Redfish BMC)
       │  (Frecuencia: 1 lectura / seg por GPU -> 1.024 msgs/seg)
       ▼
════════════════════════════════════════════════════════════════════════════
[ BUS DE INGESTA DISTRIBUIDA EN STREAMING ] (Apache Kafka / Apache Pulsar)
  • Particionamiento por `node_id` y `gpu_id`
  • Tasa de transferencia sostenida: ~22.1 GB / día
═══════════════╤════════════════════════════════════════════════════════════
               │
       ┌───────┴────────────────────────────────────────┐
       │ (Baja Latencia: < 1 seg)                      │ (Escritura Persistente)
       ▼                                                ▼
┌─────────────────────────────────┐   ┌─────────────────────────────────────┐
│  STREAM PROCESSING & REGLAS     │   │   ALMACENAMIENTO DISTRIBUIDO NOSQL  │
│  (Apache Flink / Spark Stream)  │   │   (TimescaleDB / InfluxDB / Cass.)  │
│   • Filtrado de Veracidad       │   │   • Estructura LSM-Tree             │
│   • Inferencia de Reglas Agente │   │   • Compresión Columnar (80%)       │
│   • Detección de picos térmicos │   │   • Políticas de Retención (TTL)    │
└──────────────┬──────────────────┘   └──────────────────┬──────────────────┘
               │                                         │
               ▼                                         ▼
┌─────────────────────────────────┐   ┌─────────────────────────────────────┐
│    CONTROLADORES DE ACTUACIÓN   │   │   ANALÍTICA BATCH HISTÓRICA         │
│   • Driver NVIDIA (NVML DVFS)   │   │   (Clúster Hadoop / Spark Batch)    │
│   • SLURM Power Capping API     │   │   • MapReduce para PUE y TCO        │
│   • Control de Chillers y BMC   │   │   • Detección de Deriva de Sensores │
└─────────────────────────────────┘   └─────────────────────────────────────┘
```

### 3.1. Justificación de Tecnologías para Producción a Escala
* **Ingesta (Apache Kafka):** Garantiza desacoplamiento entre los 128 nodos emisores y los consumidores, ofreciendo *backpressure* y buffer persistente en disco ante ráfagas.
* **Procesamiento en Tiempo Real (Apache Flink):** Permite evaluar ventanas temporales deslizantes (*sliding windows*) en milisegundos para detectar tendencias de incremento abrupto de temperatura antes de alcanzar el umbral crítico.
* **Almacenamiento NoSQL Time-Series:** Permite almacenar 88,4 millones de lecturas diarias sin degradar los tiempos de inserción ni sufrir contención por bloqueos de transacciones ACID.
* **Actuadores de Producción:** Integración con la API de *SLURM Workload Manager* para modular el despacho de nuevos trabajos y llamadas a la biblioteca `libnvidia-ml.so` para aplicar límites de potencia (*power cap* de 700 W a 500 W) de forma segura.

---

## 4. Matriz de Auditoría de Realidad

Esta matriz formaliza el estado de cada componente del proyecto, asegurando total coherencia entre lo expresado en la documentación y lo efectivamente desarrollado:

| Componente | Clasificación | Entorno / Ubicación | Descripción Técnica |
| :--- | :--- | :--- | :--- |
| **Agente Supervisor** | **Implementado** | `agent.py` | Clase `EcoHpcAgent` operativa con ciclo cognitivo formal y estado interno. |
| **Motor de Reglas** | **Implementado** | `rules.py` | Lógica determinista jerárquica con reglas de veracidad, protección, ahorro y régimen nominal. |
| **Control de Calidad** | **Implementado** | `data_quality.py` | Auditoría de tipos, valores nulos, límites físicos y consistencia lógica cruzada. |
| **Demostración MapReduce**| **Implementado** | `mapreduce_demo.py` | Implementación algorítmica pura de Map, Shuffle y Reduce para análisis batch. |
| **Interfaz de Usuario** | **Implementado** | `app.py` | Dashboard interactivo profesional con 12 vistas y Modo Demo para exposición oral. |
| **Suite de Pruebas** | **Implementado** | `tests/` | 24 pruebas automatizadas con Pytest (unitarias, integración de flujo y negativas). |
| **Dataset de Telemetría**| **Simulado / Creado**| `data/` | CSV, JSON y logs generados con distribuciones realistas basadas en GPUs clase H100. |
| **Aceleradores GPU** | **Simulado** | Software | Representación computacional de 16 GPUs en 4 nodos de cómputo. |
| **Actuadores Físicos** | **Simulado** | Software | Órdenes simuladas (modulación DVFS, cooling, SLURM); sin manipulación de silicio real. |
| **Clúster de 1.024 GPUs** | **Conceptual** | Diseño teórico | Supuesto de dimensionamiento calculado para ilustrar el volumen de datos en Big Data. |
| **Base NoSQL Distribuida**| **Conceptual** | Diseño teórico | Justificación arquitectónica formal para producción a escala sin despliegue físico local. |
