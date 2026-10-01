# ARQUITECTURA TÉCNICA DEL SISTEMA: ECO-HPC

---

## 1. Visión General de la Arquitectura

El sistema **ECO-HPC** implementa una arquitectura desacoplada y modular orientada a eventos de telemetría de hardware. El diseño responde a una estricta separación metodológica entre dos niveles:

1. **Arquitectura Implementada en el Prototipo:** Diseñada en Python con Pandas y Streamlit para priorizar simplicidad, reproducibilidad local y transparencia académica.
2. **Arquitectura Propuesta para Producción a Escala (1.024 GPUs):** Diseño conceptual que ilustra cómo el sistema se proyectaría de forma distribuida en un centro de cómputo de alto rendimiento.

---

## 2. Arquitectura Implementada en el Prototipo

El prototipo funcional opera mediante una canalización lineal determinista de datos estructurada en torno a una **Única Fuente de Verdad** (*Single Source of Truth*):

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
│   AHORRO / PROTECCION  │      │  CONFIABLES            │
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
│   • Vista de clúster   │      │   • Map local          │
│   • Inspector de GPU   │      │   • Shuffle local      │
│   • Modo Demo 5 pasos  │      │   • Reduce local       │
└────────────────────────┘      └────────────────────────┘
```

### 2.1. Componentes y Tecnologías Reales del Repositorio
* **Lenguaje y Entorno:** Python 3.14 estructurado modularmente sin dependencias de infraestructura pesada.
* **Procesamiento de Datos:** Pandas 3.0.6 para manipulación y visualización de series temporales estructuradas.
* **Interfaz Gráfica:** Streamlit 1.64.0 con dashboard interactivo estructurado en 12 vistas y Guion de Demostración en 5 pasos.
* **Archivos de Datos:** Repositorio en `data/` con formatos sincronizados (`telemetry.csv`, `telemetry.json`, `logs.txt`) que cubren 160 registros (16 GPUs × 10 timestamps).
* **Motor MapReduce Local:** `mapreduce_demo.py` en Python puro que implementa Map, Shuffle y Reduce en memoria local pedagógica.
* **Suite de QA y Testing:** 24 pruebas automatizadas con Pytest 9.1.1 (unitarias, integración y casos negativos).

### 2.2. Módulos y Responsabilidades del Prototipo
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
   - Declara los umbrales de simulación de manera abierta y parametrizable (el umbral de 85 °C es un parámetro preventivo de simulación y no un límite universal de toda GPU).
4. **`agent.py` (Agente Inteligente con Estado Interno):**
   - Implementa el ciclo cognitivo formal: *Percepciones → Control de Calidad → Estado Interno → Decisión → Acción*.
   - El agente mantiene memoria histórica de decisiones, estados por GPU y acumuladores del sistema. Las reglas actuales evalúan de forma determinista la percepción presente y no utilizan aprendizaje automático ni alteran automáticamente sus reglas.
   - Mantiene el historial de intervenciones y acumula el ahorro energético proyectado en kWh simulados.
5. **`mapreduce_demo.py` (Motor de Análisis Batch):**
   - Implementa algorítmicamente en Python puro las etapas de `map_function`, `shuffle_function` y `reduce_function` en memoria local (sin Hadoop ni Spark).
   - Calcula métricas consolidadas asumiendo una ventana de muestreo fija de 60 segundos por registro, donde cada timestamp identifica el inicio de su intervalo (10 registros representan 10 ventanas = 10 minutos acumulados como supuesto del dataset).
6. **`app.py` (Interfaz de Usuario Streamlit):**
   - Presenta el sistema en 12 vistas estructuradas con navegación lateral y Guion de Demostración en 5 pasos.

---

## 3. Arquitectura Propuesta para Producción a Escala (Conceptual / Futuro)

> [!NOTE]
> **CLASIFICACIÓN: PROPUESTO / CONCEPTUAL / FUTURO**  
> Esta sección describe un diseño arquitectónico de referencia para supercómputo distribuido. Ninguno de estos servicios distribuidos (Apache Kafka, Apache Pulsar, Apache Flink, Apache Cassandra, clúster Hadoop/Spark físico, SLURM real ni GPUs H100 físicas) se encuentra desplegado en el prototipo local.

Para un entorno real de supercómputo que supervise 1.024 GPUs aceleradoras, la arquitectura física se proyecta mediante una infraestructura distribuida:

```text
[ RACK 01 ] ... [ RACK 32 ]  (1.024 GPUs en 128 Nodos - contexto técnico clase NVIDIA H100 SXM)
       │              │
       ▼              ▼
[ DAEMONS LOCALES DE TELEMETRÍA ] (NVIDIA DCGM Exporters / PromQL / Redfish BMC)
       │  (Frecuencia teórica: 1 lectura / seg por GPU -> 1.024 msgs/seg)
       ▼
════════════════════════════════════════════════════════════════════════════
[ BUS DE INGESTA DISTRIBUIDA EN STREAMING ] (Apache Kafka / Apache Pulsar - PROPUESTO)
  • Particionamiento por `node_id` y `gpu_id`
  • Estimación teórica de transferencia: ~22,12 GB / día
═══════════════╤════════════════════════════════════════════════════════════
               │
       ┌───────┴────────────────────────────────────────┐
       │ (Baja Latencia de Streaming Proyectada)        │ (Escritura Persistente)
       ▼                                                ▼
┌─────────────────────────────────┐   ┌─────────────────────────────────────┐
│  STREAM PROCESSING & REGLAS     │   │   ALMACENAMIENTO NOSQL WIDE-COLUMN  │
│  (Apache Flink / Spark Stream)  │   │   (Apache Cassandra - REFERENCIA)   │
│   • Filtrado de Veracidad       │   │   • Estructura basada en LSM-Trees  │
│   • Inferencia de Reglas Agente │   │   • Partición por GPU y Timestamp   │
│   • Detección de picos térmicos │   │   • Políticas de Retención (TTL)    │
└──────────────┬──────────────────┘   └──────────────────┬──────────────────┘
               │                                         │
               ▼                                         ▼
┌─────────────────────────────────┐   ┌─────────────────────────────────────┐
│    CONTROLADORES DE ACTUACIÓN   │   │   ANALÍTICA BATCH HISTÓRICA         │
│   • Driver NVIDIA (NVML DVFS)   │   │   (Clúster Hadoop / Spark Batch)    │
│   • SLURM Power Capping API     │   │   • Agregaciones batch periódicas   │
│   • Control de Chillers y BMC   │   │   • Detección de Deriva de Sensores │
└─────────────────────────────────┘   └─────────────────────────────────────┘
```

### 3.1. Justificación de Tecnologías para Producción a Escala
* **Ingesta (Apache Kafka / Apache Pulsar - Propuesta):** Permite el desacoplamiento asíncrono entre los nodos emisores y los procesadores, proveyendo amortiguación (*buffer*) persistente en disco ante ráfagas de telemetría.
* **Procesamiento en Tiempo Real (Apache Flink - Propuesta):** Planteado conceptualmente para evaluar ventanas temporales deslizantes (*sliding windows*) y detectar tendencias de incremento abrupto de temperatura antes de alcanzar el umbral preventivo.
* **Almacenamiento NoSQL Wide-Column (Apache Cassandra - Referencia Conceptual):** Para una implementación productiva se propone una base NoSQL de tipo wide-column, tomando Apache Cassandra como tecnología de referencia. Esta arquitectura es conceptual y no se implementa en el prototipo. Se fundamenta en su arquitectura distribuida peer-to-peer y motor LSM-Tree optimizado para absorción secuencial continua de escrituras sin contención por bloqueos transaccionales ACID.
* **Actuadores de Producción (Propuesta Conceptual):** Plantea la integración con la API de *SLURM Workload Manager* y controladores de bajo nivel (como `libnvidia-ml.so` para perfiles DVFS o power-capping) en entornos donde se disponga de hardware real.

---

## 4. Matriz de Auditoría de Realidad

Esta matriz formaliza el estado de cada componente del proyecto, asegurando total coherencia entre lo expresado en la documentación y lo efectivamente desarrollado:

| Componente | Clasificación | Entorno / Ubicación | Descripción Técnica |
| :--- | :--- | :--- | :--- |
| **Agente Supervisor** | **Implementado** | `agent.py` | Clase `EcoHpcAgent` operativa con ciclo cognitivo formal y estado interno (memoria histórica y acumuladores). |
| **Motor de Reglas** | **Implementado** | `rules.py` | Lógica determinista jerárquica con reglas de veracidad, protección, ahorro y régimen nominal. |
| **Control de Calidad** | **Implementado** | `data_quality.py` | Auditoría de tipos, valores nulos, límites físicos y consistencia lógica cruzada. |
| **Demostración MapReduce**| **Implementado** | `mapreduce_demo.py` | Implementación algorítmica local pura de Map, Shuffle y Reduce para análisis batch didáctico sobre ventanas de 60s (sin Hadoop ni Spark). |
| **Interfaz de Usuario** | **Implementado** | `app.py` | Dashboard interactivo profesional con 12 vistas y Modo Demo para exposición oral. |
| **Suite de Pruebas** | **Implementado** | `tests/` | 24 pruebas automatizadas con Pytest (unitarias, integración de flujo y negativas). |
| **Dataset de Telemetría**| **Simulado / Creado**| `data/` | CSV, JSON y logs generados con distribuciones realistas basadas en contexto técnico de hardware HPC. |
| **Aceleradores GPU** | **Simulado** | Software | Representación computacional de 16 GPUs en 4 nodos de cómputo; el prototipo no posee GPUs H100 físicas. |
| **Actuadores Físicos** | **Simulado** | Software | Órdenes simuladas (modulación DVFS, cooling, SLURM); sin manipulación de silicio real. |
| **Clúster de 1.024 GPUs** | **Conceptual** | Diseño teórico | Supuesto de dimensionamiento calculado para ilustrar el volumen de datos en Big Data. |
| **Base NoSQL Distribuida**| **Conceptual** | Diseño teórico | Propuesta conceptual tomando Apache Cassandra (wide-column) como referencia de producción sin despliegue físico en el prototipo. |
