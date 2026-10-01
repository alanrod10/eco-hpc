# TRABAJO PRÁCTICO INTEGRADOR: ECO-HPC
## Las 5 V del Big Data como infraestructura de alimentación para sistemas de Inteligencia Artificial

---

* **Observatorio Académico:** IA + HARDWARE + COMPUTACIÓN DE ALTO RENDIMIENTO (HPC) + SOSTENIBILIDAD AMBIENTAL  
* **Producto Central:** ECO-HPC — Agente Supervisor de Eficiencia Energética para un entorno HPC  
* **Tipo de Agente:** Reactivo basado en reglas con estado interno  
* **Versión de Prototipo:** 1.0 (Entorno Académico Demostrable)  
* **Fecha:** Octubre 2026  

---

## 1. Introducción

En la era contemporánea de la Inteligencia Artificial, el entrenamiento y despliegue de modelos masivos (tales como Modelos de Lenguaje de Gran Escala - LLMs y redes de visión profunda) dependen críticamente de centros de datos de **Computación de Alto Rendimiento (HPC)** equipados con clústeres de aceleradores de cómputo (GPUs). 

No obstante, esta capacidad computacional sin precedentes conlleva un costo operativo y ecológico significativo: consumos eléctricos de megavatios-hora, generación masiva de calor residual, estrés electromecánico del silicio y un impacto ambiental directo en emisiones de carbono.

El presente proyecto integrador desarrolla **ECO-HPC**, un sistema compuesto por una infraestructura de telemetría de Big Data que alimenta a un **Agente Inteligente Supervisor**. Su propósito es monitorizar el estado operativo del hardware en tiempo real, diagnosticar desbalances térmicos o energéticos, y formular decisiones operativas orientadas a conciliar el rendimiento computacional con la **sostenibilidad ambiental**.

---

## 2. Caso de Estudio: Entorno HPC para Cargas de IA

### 2.1. Escala Conceptual vs. Escala del Prototipo
Para dotar al trabajo de rigor de ingeniería y viabilidad pedagógica, se establece una clara distinción entre la escala teórica de diseño y la implementación funcional:

* **Escala Conceptual de Referencia (Producción a Escala):**  
  Clúster HPC compuesto por **1.024 GPUs de clase centro de datos** (utilizando como contexto técnico de referencia la arquitectura NVIDIA H100 SXM con hasta 700 W configurables según documentación oficial de NVIDIA, mientras que variantes como PCIe operan típicamente en 300-350 W), interconectadas en una topología distribuida de nodos de cómputo para cargas intensivas de entrenamiento e inferencia de IA.
* **Escala del Prototipo Funcional:**  
  Conjunto representativo de **16 GPUs simuladas** (identificadas como `GPU-01` a `GPU-16`), agrupadas en 4 nodos de cómputo (`node-01` a `node-04`). Esta escala permite una ejecución ágil, determinista y completamente auditable en un entorno local, manteniendo la misma estructura dimensional que un clúster a gran escala.

> **Declaración de Contexto de Hardware y Transparencia Técnica:** Esta referencia a especificaciones industriales (ej. H100 SXM con hasta 700 W configurables) corresponde a hardware real utilizado como contexto técnico de referencia. El prototipo utiliza GPUs **SIMULADAS** y no posee hardware H100 físico. Asimismo, el valor de 700 W es un parámetro de simulación y no constituye un límite universal de toda GPU. El prototipo no envía comandos de control de bajo nivel ni manipula voltaje físico en componentes electrónicos reales.

---

## 3. Objetivos

### 3.1. Objetivo Académico
Demostrar de forma unificada y coherente:
1. Cómo las **5 V del Big Data** actúan como la infraestructura de sensado que nutre a un sistema de Inteligencia Artificial.
2. La definición formal del agente inteligente bajo el marco **PEAS** (Russell & Norvig).
3. El funcionamiento interno del ciclo cognitivo del agente: *Sensores → Percepciones → Control de Calidad → Estado Interno → Decisión → Acción*.
4. La aplicación del paradigma **MapReduce** para el análisis batch de series temporales de telemetría.
5. La justificación técnica de arquitecturas de almacenamiento **NoSQL** a escala.
6. El análisis de **Veracidad**, calibración y sesgos de sensado de hardware.
7. Las implicancias de privacidad y protección de datos conforme a la **Ley Nacional N.º 25.326** de la República Argentina y la Resolución AAIP 47/2018.

### 3.2. Objetivo Práctico
Construir y verificar una suite de software funcional en **Python, Pandas y Streamlit** que permita inspeccionar en tiempo real:
* ¿Qué está ocurriendo en el hardware?
* ¿En qué estado interno se encuentra la GPU?
* ¿Qué decisión operativa corresponde?
* ¿Por qué? (Justificación analítica basada en reglas explícitas).
* ¿Qué acción correctiva se simula?

---

## 4. Consigna 1 — Las 5 V del Big Data en ECO-HPC

### 4.1. Volumen: Supuesto Calculado del Escenario
El volumen de datos generado por la telemetría de hardware no es arbitrario; obedece a la densidad de sensado requerida para la supervisión térmica y eléctrica.

**Fórmula Pedagógica de Estimación:**
$$\text{Volumen Diario} = N_{\text{GPU}} \times f_{\text{lecturas}} \times 86.400\,\frac{\text{s}}{\text{día}} \times \text{Tamaño Registro}$$

* **Cálculo para el Escenario Conceptual (1.024 GPUs):**
  * $N_{\text{GPU}} = 1.024\text{ aceleradores}$
  * Frecuencia de muestreo ($f_{\text{lecturas}}$) = $1\text{ lectura/segundo}$ por GPU
  * Eventos por segundo en el clúster = $1.024\text{ eventos/segundo}$
  * Eventos diarios = $1.024 \times 86.400 = \mathbf{88.473.600\text{ registros/día}}$
  * Tamaño promedio por registro estructurado/JSON (metadata, timestamp, métricas térmicas, eléctricas y de carga) = $\approx 250\text{ bytes}$
  * **Volumen diario sin comprimir:** $88.473.600 \times 250\text{ bytes} \approx \mathbf{22,12\text{ GB/día}}$
  * **Volumen mensual (30 días):** $\approx \mathbf{663,5\text{ GB/mes}}$
  * **Volumen anual:** $\approx \mathbf{8\text{ TB/año}}$ únicamente en telemetría sensorial de hardware.

* **Relación con el Prototipo:**  
  El prototipo genera y procesa lotes de telemetría de 16 GPUs. Esto reafirma el axioma: **prototipo pequeño ≠ volumen conceptual pequeño**.

### 4.2. Velocidad: Dualidad Streaming vs. Procesamiento Batch
El sistema satisface dos demandas operativas con latencias dispares:
1. **Baja Latencia / Streaming (< 1-2 segundos):**  
   Requerida por el **Agente Supervisor ECO-HPC**. Los transistores de una GPU pueden alcanzar embalamiento térmico en cuestión de segundos ante un fallo en las bombas de refrigeración o un pico de corriente. La percepción, control de calidad y toma de decisión deben resolverse casi en tiempo real.
2. **Procesamiento Batch / Diferido (Horas / Días):**  
   Requerido para la agregación histórica mediante **MapReduce**. Permite calcular perfiles medios de disipación, auditoría energética acumulada en kilovatios-hora (kWh), factor de efectividad en el uso de energía (PUE) y detección de derivas a largo plazo en los sensores.

### 4.3. Variedad: Heterogeneidad Multi-Formato
En un centro de datos HPC coexisten múltiples formatos de datos representados en el proyecto:
* **Estructurados (`data/telemetry.csv`):** Tablas de series temporales con esquema estricto y tipos numéricos definidos (`timestamp`, `gpu_id`, `temperature`, `power_w`, `utilization`, `frequency`).
* **Semiestructurados (`data/telemetry.json`):** Objetos emitidos por servicios de monitoreo (como exportadores de *NVIDIA Data Center GPU Manager - DCGM* o endpoints REST de gestión *Redfish*), con pares clave-valor flexibles y anidamiento de atributos.
* **No Estructurados (`data/logs.txt`):** Registros textuales emitidos por el kernel del sistema operativo, el gestor de trabajos (SLURM) y controladores de gestión del chasis (*IPMI/syslog*), que contienen eventos de fallo, advertencias de paridad de bus o desconexión de dispositivos.

### 4.4. Veracidad: Validación Física y Detección de Anomalías
La veracidad es la dimensión crítica que determina si una percepción es confiable. En hardware real, los sensores pueden verse afectados por ruido eléctrico, caídas de tensión en buses I2C/SMBus o fallos del conversor ADC.

ECO-HPC incorpora un módulo formal de auditoría de veracidad (`data_quality.py`). Si un registro presenta temperaturas físicamente imposibles en silicio (ej. 150 °C) o contradicciones lógicas (102 °C con 0% de uso y 10 W de consumo), el dato no se procesa a ciegas: el agente entra en estado **DATOS NO CONFIABLES** y rechaza aplicar cambios sobre el clúster.

### 4.5. Valor: La Cadena de Transformación
El Big Data no aporta valor por su acumulación cuantitativa, sino por su capacidad de habilitar intervenciones acertadas:
$$\text{DATO CRUDO} \longrightarrow \text{INFORMACIÓN} \longrightarrow \text{DECISIÓN} \longrightarrow \text{ACCIÓN} \longrightarrow \text{VALOR (kWh ahorrados + seguridad)}$$

---

## 5. Consigna 2 — Fuentes de Datos y Marco PEAS

### 5.1. Fuentes de Datos
* **Fuente Primaria (Implementada en el Prototipo):**  
  **M2M / IoT (Machine-to-Machine):** Telemetría continua generada por los sensores integrados en las placas de cómputo (termistores de unión, shunts de corriente eléctrica, tacómetros de refrigeración y contadores de ciclos de reloj).
* **Fuentes Secundarias (Integradas didácticamente en el ecosistema):**
  * Logs del sistema operativo y gestores de recursos (*SLURM Workload Manager*).
  * Parámetros ambientales externos (sensores térmicos del pasillo frío/caliente del datacenter).
  * Registros manuales de mantenimiento de hardware.

### 5.2. Marco Formal PEAS (Russell & Norvig)

| Elemento PEAS | Especificación Técnica en ECO-HPC |
| :--- | :--- |
| **Performance Measure**<br>*(Medida de Rendimiento)* | Maximizar la eficiencia energética del clúster (reducción de consumo en Watts y kWh acumulados), operando bajo el umbral de protección térmica configurado para el prototipo/simulación (temperatura $<85\text{ }^\circ\text{C}$, el cual no es un límite universal de toda GPU) y garantizando los acuerdos de nivel de servicio (SLAs) de los trabajos de IA. |
| **Environment**<br>*(Entorno de Operación)* | Clúster HPC compuesto por aceleradores GPU interconectados ejecutando cargas de trabajo de IA (entrenamiento distribuido, inferencia de modelos masivos). Entorno parcialmente observable, determinista en reglas pero dinámico y continuo en lecturas. |
| **Actuators**<br>*(Actuadores)* | Comandos operacionales de ajuste dinámico de frecuencia y voltaje (DVFS / P-States), control de ciclos de trabajo de refrigeración (duty-cycle de ventiladores/bombas) y modulación de cuotas de cómputo en SLURM (**SIMULADOS**). |
| **Sensors**<br>*(Sensores)* | Telemetría M2M: Sensor de temperatura de unión (°C), sensor de potencia activa (W), monitor de tasa de utilización de núcleos de cómputo (%), frecuencia de reloj (MHz) y estado del trabajo. |

---

## 6. Consigna 3 — Ingesta, MapReduce y Justificación NoSQL

### 6.1. Flujo de Ingesta y Procesamiento
El prototipo implementa una canalización lineal, desacoplada y verificada:
1. **Generación/Ingesta:** El simulador (`simulator.py`) sintetiza series temporales realistas en archivos CSV, JSON y logs de texto.
2. **Control de Calidad:** `data_quality.py` intercepta el flujo y evalúa la veracidad mediante límites físicos y consistencia lógica.
3. **Inferencia del Agente:** `agent.py` y `rules.py` procesan los datos válidos, actualizan el estado interno y emiten la decisión.
4. **Visualización y Explotación:** `app.py` expone el estado y los resultados a través del dashboard interactivo.

### 6.2. Demostración Didáctica de MapReduce
Para satisfacer el análisis batch histórico, el sistema incorpora una implementación en Python puro (`mapreduce_demo.py`) que ilustra las fases formales del paradigma de Dean & Ghemawat (Google, 2004):

1. **Entrada:** Serie temporal de lecturas históricas multi-nodo.
2. **Fase MAP:** Transforma cada registro en pares clave-valor:
   $$\text{Map}(\text{registro}) \longrightarrow \langle \text{gpu\_id}, \{\text{power\_w}, \text{temperature}, \text{count}=1\} \rangle$$
3. **Fase SHUFFLE & SORT:** Agrupa todos los valores emitidos bajo la misma clave identificadora de hardware:
   $$\text{Shuffle} \longrightarrow \text{dict}\left[ \text{gpu\_id}, [\text{valor}_1, \text{valor}_2, \dots] \right]$$
4. **Fase REDUCE:** Función de agregación matemática que reduce la lista de valores a métricas consolidadas:
   $$\text{AvgPower} = \frac{\sum \text{power\_w}}{N}, \quad \text{MaxTemp} = \max(\text{temperature}), \quad \text{Energía (kWh)} = \frac{\text{AvgPower} \times \text{Horas}}{1000}$$
   Donde $\text{Horas} = \frac{N \times \Delta t}{3600}$, siendo $\Delta t = 60\text{ s}$ el intervalo temporal real representado por las marcas de tiempo consecutivas del dataset histórico.

> **Aclaración Académica:** Mientras que el escenario conceptual de streaming para el agente considera 1 lectura/segundo para baja latencia, el dataset histórico del prototipo representa muestras periódicas consolidadas cada 60 segundos (1 minuto), tal como se verifica en sus marcas de tiempo ISO. El cálculo de energía en MapReduce utiliza estrictamente este intervalo real de 60 segundos por muestra del dataset. La demostración representa fielmente la semántica algorítmica del paradigma MapReduce en memoria local; no constituye un clúster físico Hadoop/Spark en producción.

### 6.3. Justificación de Arquitectura NoSQL para Producción a Escala
¿Por qué una implementación real con 1.024 GPUs requiere almacenamiento **NoSQL** en lugar de una base de datos relacional (RDBMS)?

1. **Rendimiento de Escritura Intensiva (*Append-Heavy Throughput*):**  
   Con 1.024 inserciones por segundo (más de 88 millones diarias), un motor relacional tradicional se degrada debido a los bloqueos de transacciones ACID y a la sobrecarga de rebalanceo de índices de árbol B (*B-Trees*).
2. **Modelo de Series Temporales / Wide-Column NoSQL:**  
   Bases de datos como **InfluxDB**, **TimescaleDB** o **Apache Cassandra** utilizan estructuras basadas en *Log-Structured Merge-trees (LSM-Trees)*, optimizadas para escrituras secuenciales ultrarrápidas y almacenamiento columnar que favorece una alta tasa de compresión (reduciendo el almacenamiento en un 70-80%).
3. **Escalabilidad Horizontal y Tolerancia a Fallos:**  
   Permite añadir nodos de base de datos de manera transparente mediante particionamiento (*sharding*) por rango temporal y clave de nodo.
4. **Políticas Nativas de Retención y Downsampling (*TTL*):**  
   Facilita la consolidación automática: retener datos con resolución de 1 segundo durante 14 días y compactar a promedios de 1 minuto para análisis históricos de largo plazo.

---

## 7. Consigna 4 — Veracidad, Sesgos de Hardware y Ley 25.326

### 7.1. Sesgos y Errores en Telemetría de Hardware
Es fundamental diferenciar conceptualmente tres tipos de desvíos:
* **Sesgo de Medición (Sistemático):** Variación de fábrica en el circuito conversor analógico-digital (ADC) o calibración del termistor entre diferentes modelos o lotes de GPUs, reportando sistemáticamente $\pm 3\text{ }^\circ\text{C}$ de desviación.
* **Sesgo de Muestreo:** Desbalance en la tasa de llegada de percepciones. Ocurre cuando nodos bajo congestión de red de gestión OOB (*Out-of-band*) emiten telemetría cada 5 segundos, mientras que nodos menos cargados emiten cada 1 segundo, sobrerrepresentando a estos últimos en los promedios globales.
* **Deriva del Sensor (*Sensor Drift*):** Fenómeno físico provocado por el envejecimiento térmico del silicio y los ciclos de calentamiento/enfriamiento continuos, que alteran la resistencia óhmica de los componentes de sensado con el paso de los meses.
* **Diferenciación con Error Aleatorio y Dato Faltante:**  
  * *Error aleatorio:* Fluctuación estocástica de ruido blanco alrededor de la media (filtrable por promedio móvil).  
  * *Dato faltante:* Pérdida de paquetes en el canal de comunicación o caída temporal del demonio de monitoreo.  
  * *Sesgo:* Desviación constante y unidireccional que induce a conclusiones erróneas si no se compensa.

### 7.2. Marco Jurídico: Ley Nacional N.º 25.326 y Res. AAIP 47/2018

#### ¿La telemetría de una GPU es un dato personal?
* **Regla General:** En su estado estrictamente aislado, una lectura como `GPU-07: Temp=89°C, Power=720W` es un dato técnico de máquina (M2M) y **NO constituye dato personal**.
* **El Punto de Inflexión Legal (Art. 2 Ley 25.326):** La Ley 25.326 define como dato personal toda *"información de cualquier tipo referida a personas físicas o de existencia ideal determinadas o determinables"*.  
  En un centro de cómputo, cuando la telemetría del hardware se cruza con las bases de datos del planificador de tareas (SLURM/PBS):
  $$\text{ID DE USUARIO (Investigador)} + \text{SCRIPT/JOB} + \text{HORARIO} + \text{GPU ASIGNADA} + \text{TELEMETRÍA}$$
  los patrones de consumo, la duración de cálculo y las horas de ejecución revelan de manera indirecta pautas de conducta, productividad laboral, horarios de actividad del investigador e inferencias sobre líneas de investigación bajo secreto o propiedad intelectual.

#### Principios de Protección de Datos en ECO-HPC:
1. **Minimización de Datos (Art. 4):** El agente supervisor sólo percibe y almacena métricas físicas e identificadores de hardware (`gpu_id`, `node`). Toda referencia a identidad de usuario o títulos de scripts es eliminada del flujo de telemetría operativa.
2. **Principio de Finalidad (Art. 4, inc. 3):** Los datos recopilados se utilizan estrictamente para el control térmico, la seguridad de la infraestructura y la optimización energética, prohibiéndose su uso para vigilancia laboral o perfilamiento sin consentimiento.
3. **Medidas de Seguridad (Art. 9 Ley 25.326 y Res. AAIP 47/2018):** Implementación de controles de acceso basados en roles (RBAC) para consultar el histórico y cifrado de los canales de telemetría en tránsito.

---

## 8. Consigna 5 — Ficha Técnica del Agente ECO-HPC

```text
================================================================================
FICHA TÉCNICA FORMAL: AGENTE SUPERVISOR ECO-HPC
================================================================================
Nombre del Sistema:     ECO-HPC (Energy & Cooling Optimizer for HPC)
Versión:                1.0 (Prototipo Académico Demostrable)
Tipo de Agente:         Agente Reactivo Basado en Reglas con Estado Interno
Arquitectura Cognitiva: Sensores -> Calidad de Datos -> Estado -> Decisión -> Acción
--------------------------------------------------------------------------------
ENTORNO Y ALCANCE
Entorno:                Clúster HPC para Cargas de IA (Entrenamiento e Inferencia)
Escala Conceptual:      Hasta 1.024 GPUs de cómputo acelerado
Escala Prototipo:       16 GPUs simuladas distribuidas en 4 nodos de cómputo
Hardware Físico:        SIMULADO (sin conexión a actuadores industriales reales)
--------------------------------------------------------------------------------
VARIABLES SENSORIALES (PERCEPCIONES)
1. gpu_id:              Identificador único de acelerador (str, ej: "GPU-01")
2. temperature:         Temperatura de unión del núcleo (°C, float)
3. power_w:             Consumo eléctrico instantáneo (Watts, float)
4. utilization:         Tasa de uso de núcleos de cómputo (%, float [0-100])
5. frequency:           Frecuencia de reloj de operación (MHz, int)
6. cooling:             Velocidad de ventiladores/bombas (%, float [0-100])
7. job_status:          Estado de la tarea asignada (str)
--------------------------------------------------------------------------------
ESTADOS INTERNOS Y DEFINICIÓN DE MEMORIA
El agente mantiene memoria histórica de decisiones, estados por GPU y acumuladores
del sistema. Las reglas actuales evalúan de forma determinista la
percepción presente y no utilizan aprendizaje automático ni dependen de la decisión anterior.
Estados posibles:
1. NORMAL:              Parámetros dentro de la envolvente de diseño segura.
2. AHORRO:              GPU subutilizada manteniendo alto consumo innecesario.
3. PROTECCION:          Umbral de protección alcanzado (85 °C configurado para la simulación).
4. DATOS NO CONFIABLES: Detección de fallos de veracidad, lecturas nulas o ilógicas.
--------------------------------------------------------------------------------
ACCIONES OPERATIVAS (SIMULADAS)
1. MANTENER:            Conservar configuración nominal vigente.
2. AHORRAR:             Modulación DVFS (reducir reloj y fijar P-State bajo).
3. REFRIGERAR:          Incrementar ciclo de trabajo de refrigeración al 100%.
4. PROTEGER:            Throttling forzado, limitación de potencia y alerta a SLURM.
5. REVISAR SENSOR:      Aislar stream corrupto y generar ticket de mantenimiento.
--------------------------------------------------------------------------------
SOFTWARE Y TECNOLOGÍAS UTILIZADAS
Lenguaje:               Python 3.14
Procesamiento de Datos: Pandas 3.0.6
Interfaz Web:           Streamlit 1.64.0
Testing y QA:           Pytest 9.1.1 (24 pruebas unitarias, integración y negativas)
================================================================================
```

---

## 9. Arquitectura del Sistema

### 9.1. Arquitectura Implementada en el Prototipo
```text
      [ SIMULADOR DE TELEMETRÍA ] (simulator.py)
                    │
                    ▼
      [ FORMATOS MULTI-VARIEDAD ]
        ├── telemetry.csv  (Estructurado)
        ├── telemetry.json (Semiestructurado)
        └── logs.txt       (No estructurado)
                    │
                    ▼
      [ CONTROL DE CALIDAD Y VERACIDAD ] (data_quality.py)
        • Filtro de valores nulos
        • Verificación de rangos físicos [15°C - 105°C, 20W - 900W]
        • Consistencia lógica cruzada
                    │
                    ▼
      [ AGENTE SUPERVISOR ECO-HPC ] (agent.py + rules.py)
        • Actualización de Estado Interno
        • Inferencia mediante Reglas Deterministas
        • Formulación de Decisión y Justificación
                    │
                    ▼
      [ DASHBOARD INTERACTIVO Y MODO DEMO ] (Streamlit app.py)
        • Vista de Estado Global del Clúster
        • Inspector Detallado de GPUs
        • Visualizador MapReduce y Análisis Batch
```

### 9.2. Arquitectura Conceptual de Producción (Escala 1.024 GPUs)
```text
  [ 1.024 GPUs EN RACKS HPC ] ──▶ Sensores NVML / DCGM Exporter
               │
               ▼
  [ INGESTA DISTRIBUIDA EN STREAMING ] (Apache Kafka / Pulsar @ 1.024 msgs/s)
               │
         ┌─────┴────────────────────────┐
         ▼                              ▼
  [ STREAM PROCESSING ]         [ ALMACENAMIENTO NOSQL ]
   Apache Flink / Spark          Time-Series (TimescaleDB / InfluxDB)
   (Inferencia Agente < 1s)      (Particionado temporal y retención TTL)
         │                              │
         ▼                              ▼
  [ CONTROLADORES DEL HARDWARE ] [ ANALÍTICA BATCH HISTÓRICA ]
   SLURM Power-Capping            MapReduce / Spark Batch Jobs
   Driver NVIDIA DVFS             Cálculo de PUE y huella de carbono
   Controladores BMC / IPMI
```

---

## 10. Matriz de Auditoría de Realidad

| Componente | Clasificación Técnica | Justificación Metodológica |
| :--- | :--- | :--- |
| **Dataset de Telemetría** | **Simulado / Implementado** | Generado mediante scripts reproducibles (`simulator.py`) basados en perfiles reales de hardware H100. |
| **Aceleradores GPU** | **Simulado** | Se simula el comportamiento de 16 GPUs sin requerir hardware físico de supercómputo. |
| **Sensores de Hardware** | **Simulado** | Vectores de percepción sintetizados con modelos térmicos y de carga de cómputo. |
| **Agente ECO-HPC** | **Realmente Implementado** | Código Python operativo (`agent.py`) con control de estado y evaluación jerárquica de reglas. |
| **Motor de Reglas** | **Realmente Implementado** | Lógica determinista implementada en `rules.py` con umbrales declarados de simulación. |
| **Actuadores** | **Simulado** | Las órdenes operativas se formulan y explican, pero no actúan sobre registros de voltaje físico. |
| **Demostración MapReduce** | **Realmente Implementada** | Pipeline algorítmico completo (Map, Shuffle, Reduce) ejecutado en memoria con Python puro. |
| **Base de Datos NoSQL** | **Propuesta Conceptual** | Justificación formal de arquitectura para producción; no se despliega un clúster distribuido en la demo. |
| **Clúster de 1.024 GPUs** | **Escenario Conceptual** | Supuesto dimensionado matemáticamente para ilustrar el volumen del Big Data. |
| **Cálculo de Sostenibilidad** | **Modelo Implementado** | Estimación algorítmica de kilovatios-hora ahorrados y reducción simulada de emisiones. |

---

## 11. Conclusión y Vínculo con la Sostenibilidad

El proyecto **ECO-HPC** demuestra de manera rigurosa y verificable que el Big Data constituye la infraestructura imprescindible sobre la cual se cimienta la Inteligencia Artificial sostenible:
1. Sin un flujo continuo de telemetría (**Volumen, Velocidad y Variedad**), el sistema carece de capacidad de observación.
2. Sin un filtro estricto de **Veracidad**, el agente inteligente corre el riesgo de tomar decisiones catastróficas inducidas por fallos de sensado.
3. El **Valor** se materializa cuando un agente basado en reglas, transparente y explicable, interviene proactivamente para mitigar el derroche energético y extender el ciclo de vida del hardware.

En un contexto global donde los centros de datos de IA consumen un porcentaje creciente de la matriz eléctrica mundial, arquitecturas de supervisión como ECO-HPC son indispensables para transformar el paradigma computacional hacia un horizonte de **eficiencia energética y sostenibilidad ambiental**.

---

## 12. Bibliografía y Fuentes Consultadas

1. **Honorable Congreso de la Nación Argentina (2000).** *Ley N.º 25.326 de Protección de los Datos Personales*. Promulgada por Decreto 1616/2000. Texto actualizado oficial en InfoLEG: `https://servicios.infoleg.gob.ar/infolegInternet/anexos/60000-64999/64790/norma.htm`.
2. **Agencia de Acceso a la Información Pública - AAIP (2018).** *Resolución 47/2018: Medidas de Seguridad Recomendadas para el Tratamiento y Conservación de los Datos Personales*. InfoLEG: `https://servicios.infoleg.gob.ar/infolegInternet/anexos/315000-319999/315998/norma.htm`.
3. **Russell, S., & Norvig, P. (2020).** *Artificial Intelligence: A Modern Approach* (4th Edition). Pearson. Capítulos 2 (*Intelligent Agents*) y 3.
4. **Dean, J., & Ghemawat, S. (2004).** *MapReduce: Simplified Data Processing on Large Clusters*. Communications of the ACM, 51(1), 107-113. Google Research.
5. **NVIDIA Corporation (2024).** *Data Center GPU Manager (DCGM) & NVML API Architecture Guide*. NVIDIA Developer Zone: `https://docs.nvidia.com/datacenter/dcgm/latest/`. Especificaciones de hardware: H100 SXM con hasta 700 W configurables; variante PCIe opera típicamente en 300-350 W.
6. **TOP500.org (2024).** *The Green500: Energy-Efficient Supercomputers List*. `https://www.top500.org/lists/green500/`.
