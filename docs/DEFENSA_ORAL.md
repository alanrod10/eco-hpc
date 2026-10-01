# GUÍA DE PREPARACIÓN PARA LA DEFENSA ORAL
## ECO-HPC: Agente Supervisor de Eficiencia Energética en Entornos HPC

---

Esta guía sintetiza la arquitectura, los conceptos teóricos, la demostración práctica y las respuestas técnicas para exponer y defender el proyecto completo con soltura, rigor y seguridad técnica en una sola jornada de estudio.

---

## 1. Discursos de Exposición

### 1.1. Explicación Ultracorta (60 Segundos)
> *"ECO-HPC es un agente supervisor que recibe telemetría simulada de GPU, controla la calidad de esos datos, determina el estado del sistema y genera una acción simulada orientada a reducir consumo y mantener condiciones térmicas seguras. El proyecto usa las 5 V del Big Data para explicar cómo los datos alimentan al agente, PEAS para describirlo, MapReduce para el procesamiento histórico y NoSQL como arquitectura de almacenamiento a escala."*

---

### 1.2. Guion de Exposición Técnica Completa (5 Minutos)

Este guion estructura la exposición de forma secuencial en 8 bloques conceptuales claros:

1. **El Problema:**  
   El entrenamiento y la inferencia de modelos masivos de IA demandan clústeres de supercómputo con cientos o miles de aceleradores GPU. Estos dispositivos consumen megavatios de electricidad y operan cerca de sus límites térmicos. Sin supervisión inteligente, ocurren dos problemas graves: derroche eléctrico en fases de subutilización (*idle*) y riesgo de degradación de hardware ante picos térmicos no controlados.

2. **La Solución ECO-HPC:**  
   Diseñamos ECO-HPC, un agente supervisor basado en reglas deterministas que monitorea en tiempo real la telemetría del clúster, evalúa el estado operativo de cada GPU y ejecuta acciones preventivas simuladas para equilibrar consumo y temperatura.

3. **Los Datos:**  
   La fuente primaria de alimentación es la telemetría M2M (Machine-to-Machine) e IoT industrial. Cada acelerador emite variables continuas: temperatura de unión, potencia eléctrica instantánea, porcentaje de uso computacional y frecuencia de reloj.

4. **Las 5 V del Big Data:**  
   A escala de 1.024 GPUs, la telemetría genera 88,4 millones de registros diarios y más de 22 GB/día (**Volumen**). Requiere una doble temporalidad (**Velocidad**): un objetivo arquitectónico de baja latencia en streaming (<1s como supuesto de diseño) para el agente y procesamiento batch diferido con MapReduce para el histórico. Coexisten formatos heterogéneos (**Variedad**): CSV estructurado, JSON semiestructurado y logs TXT. Se implementa un filtro de 5 capas (**Veracidad**) para rechazar fallos físicos de sensado antes de decidir. Y se traduce en ahorro de kWh y mitigación de huella de carbono (**Valor**).

5. **El Marco PEAS:**  
   Formalizamos al agente según Russell & Norvig:
   - **Performance:** Reducir consumo eléctrico y mantener temperaturas bajo el umbral configurado (<85 °C en simulación).
   - **Environment:** Clúster HPC con aceleradores para IA.
   - **Actuators:** Acciones simuladas de modulación de reloj (DVFS), incremento de ventiladores y cuotas de cómputo en SLURM.
   - **Sensors:** Percepciones sensoriales continuas de temperatura, potencia, uso y reloj.

6. **La Decisión del Agente:**  
   El agente mantiene memoria y acumuladores en su estado interno. Evalúa jerárquicamente:
   - Si el dato es contradictorio o nulo $\rightarrow$ `DATOS NO CONFIABLES` (Revisar sensor).
   - Si la temperatura supera 85 °C $\rightarrow$ `PROTECCION` (Reducir frecuencia y cooling al 100%).
   - Si la potencia es alta con baja utilización $\rightarrow$ `AHORRO` (Ajustar P-State por DVFS).
   - Si está balanceado $\rightarrow$ `NORMAL` (Mantener parámetros vigentes).

7. **Procesamiento Histórico y Almacenamiento (MapReduce / NoSQL):**  
   Implementamos en Python un pipeline didáctico de **MapReduce** (Map, Shuffle, Reduce) que agrega el lote histórico consolidado para calcular perfiles medios y kWh consumidos. Para la arquitectura a escala, se propone conceptualmente una base de datos **NoSQL wide-column** (tomando Apache Cassandra como referencia) por su capacidad teórica de absorber 88,4 millones de escrituras diarias sin bloqueo transaccional.

8. **Sostenibilidad y Marco Legal:**  
   El valor directo se refleja en la reducción de costos energéticos y emisiones de CO₂. En el marco legal, conforme a la Ley 25.326, la telemetría técnica pura se convierte en dato personal cuando el gestor de trabajos la vincula con la identidad del usuario; por ello aplicamos el principio de minimización disociando los identificadores en el bucle de control.

---

## 2. Glosario Técnico Fundamental

* **Big Data:** Tratamiento y análisis de datos cuyo volumen, velocidad o variedad excede las capacidades de sistemas convencionales de almacenamiento y procesamiento.
* **Las 5 V:** Volumen (cantidad acumulada), Velocidad (frecuencia de emisión y procesamiento), Variedad (heterogeneidad de esquemas), Veracidad (confiabilidad y calidad de los datos) y Valor (utilidad práctica para la toma de decisiones).
* **M2M (Machine-to-Machine):** Flujos de comunicación directa entre dispositivos, instrumentos o sensores hacia sistemas de procesamiento sin intermediación humana.
* **HPC (High Performance Computing):** Computación de Alto Rendimiento; infraestructura de servidores agrupados en clústeres para procesar tareas computacionales pesadas, como el entrenamiento de redes neuronales.
* **PEAS:** Marco de Russell & Norvig que caracteriza a un agente mediante Rendimiento (*Performance*), Entorno (*Environment*), Actuadores (*Actuators*) y Sensores (*Sensors*).
* **Agente Inteligente:** Entidad computacional que percibe su entorno a través de sensores, procesa la información y actúa sobre él mediante actuadores para alcanzar objetivos prefijados.
* **Percepción:** Vector de lecturas sensoriales entregado al agente en un instante de muestreo determinado.
* **Estado Interno:** El agente mantiene memoria histórica de decisiones, estados por GPU y acumuladores del sistema. Las reglas actuales evalúan de forma determinista la percepción presente y no utilizan aprendizaje automático ni dependen de la decisión anterior.
* **DVFS (Dynamic Voltage and Frequency Scaling):** Técnica de hardware que modula dinámicamente el voltaje y la frecuencia de reloj del procesador para reducir consumo o temperatura.
* **MapReduce:** Paradigma formal de computación distribuida: **Map** (extrae tuplas clave-valor), **Shuffle** (agrupa valores por clave compartida) y **Reduce** (agrega métricas consolidadas sobre cada grupo).
* **NoSQL Wide-Column (Propuesta Conceptual):** Modelo de almacenamiento propuesto conceptualmente para producción (referenciado en Apache Cassandra), optimizado para inserción secuencial continua de métricas temporales particionadas sin bloqueos ACID.
* **Veracidad:** Dimensión que asegura exactitud, consistencia física y ausencia de datos espurios antes de la toma de decisiones.

---

## 3. Guion de Demostración en la Aplicación (5 Pasos)

La pantalla **DEMOSTRACIÓN** contiene una secuencia interactiva estructurada en 5 escenarios:

| Paso | Escenario | Datos Clave | Resultado del Agente | Explicación Breve |
| :---: | :--- | :--- | :--- | :--- |
| **01** | **01 — NORMAL** | GPU-01: 60,9 °C, 385 W, 65% util | Estado: **NORMAL**<br>Decisión: **MANTENER** | El hardware opera en balance dentro de la envolvente de diseño. No requiere intervención. |
| **02** | **02 — AHORRO** | GPU-04: 58,0 °C, 380 W, 14% util | Estado: **AHORRO**<br>Decisión: **REDUCIR FRECUENCIA** | La GPU disipa 380 W pero su uso es de solo 14%. El agente detecta ineficiencia y modula reloj por DVFS para ahorrar ~152 W. |
| **03** | **03 — PROTECCION** | GPU-07: 89,0 °C, 720 W, 97% util | Estado: **PROTECCION**<br>Decisión: **PROTEGER HARDWARE** | La temperatura supera el umbral configurado (85 °C en la simulación). El agente aplica DVFS restrictivo, refrigeración al 100% y power-capping. |
| **04** | **04 — ANOMALÍA** | GPU-12: 150,0 °C, 10 W, 0% util | Estado: **DATOS NO CONFIABLES**<br>Decisión: **REVISAR SENSOR** | Inconsistencia física imposible (150 °C sin consumo). Una percepción no es una orden: el agente no apaga el nodo a ciegas y aísla el dato. |
| **05** | **05 — MAPREDUCE** | Lote de 160 registros consolidados | Agregación Map-Shuffle-Reduce | Muestra la V de Velocidad: batch diferido con MapReduce calculando energía asumiendo ventanas de 60 s por registro (10 registros = 10 minutos acumulados). |

---

## 4. Banco de Preguntas Clave y Respuestas Técnicas

### Pregunta 1: ¿Por qué este problema pertenece a Big Data y no a un monitoreo tradicional?
* **Explicación Simple:**  
  Porque a escala de 1.024 GPUs la telemetría genera más de 88 millones de eventos por día en múltiples formatos, exigiendo streaming en tiempo real y procesamiento masivo en batch.
* **Explicación Técnica:**  
  El monitoreo clásico (SNMP o Nagios) recopila métricas agregadas cada varios minutos. En HPC para IA, la alta densidad de potencia (utilizando como contexto técnico modelos clase NVIDIA H100 SXM con hasta 700 W configurables según especificaciones de NVIDIA, mientras que variantes PCIe operan en 300-350 W; el prototipo utiliza GPUs simuladas y no posee H100 físicas) exige muestreo a nivel de segundos. El volumen proyectado alcanza aproximadamente 22,12 GB/día sin comprimir (≈ 8,07 TB/año), involucra formatos variados (CSV, JSON, logs), exige filtros estrictos de veracidad física y genera valor directo en eficiencia energética.
* **Ejemplo en ECO-HPC:**  
  En la vista *Las 5 V del Big Data*, la pestaña *Volumen* desglosa la fórmula matemática que demuestra la escala de 88.473.600 lecturas diarias para 1.024 GPUs.

---

### Pregunta 2: ¿Cuáles son las 5 V y cómo están representadas concretamente en el proyecto?
* **Explicación Simple:**  
  Volumen (cálculo de 88,4M registros diarios), Velocidad (streaming <1s vs batch MapReduce), Variedad (CSV, JSON, logs), Veracidad (filtro de datos ilógicos) y Valor (ahorro en kWh y protección térmica).
* **Explicación Técnica:**  
  Cada V tiene un componente verificable:
  - **Volumen:** Ecuación formal $N_{\text{GPU}} \times f \times 86400 \times \text{bytes}$.
  - **Velocidad:** Doble ventana temporal demostrada: respuesta inmediata en memoria del agente y consolidación diferida con MapReduce.
  - **Variedad:** Tres datasets sincronizados en `data/`: estructurado (CSV), semiestructurado (JSON) y no estructurado (logs TXT).
  - **Veracidad:** Demostrada en `data_quality.py` aislando lecturas con fallas físicas (GPU-12 con 150 °C sin potencia y GPU-13 con NaN).
  - **Valor:** Cuantificado en la aplicación mediante kilovatios-hora ahorrados acumulados por las intervenciones del supervisor.
* **Ejemplo en ECO-HPC:**  
  En la vista *Las 5 V del Big Data*, cada dimensión cuenta con su panel interactivo con datos del repositorio.

---

### Pregunta 3: ¿Por qué la telemetría se clasifica como comunicación M2M / IoT?
* **Explicación Simple:**  
  Porque proviene de sensores electrónicos integrados en el hardware que transmiten paquetes directamente a los controladores de gestión del sistema sin intermediación humana.
* **Explicación Técnica:**  
  M2M (*Machine-to-Machine*) describe el intercambio autónomo de información entre equipos. Los aceleradores disponen de sensores embebidos (termistores, convertidores analógico-digitales y shunts de corriente) que envían lecturas mediante buses I2C, SMBus o PCIe hacia los controladores BMC (*Baseboard Management Controller*) y el demonio DCGM de NVIDIA, conformando un flujo de sensado continuo puramente instrumental.
* **Ejemplo en ECO-HPC:**  
  En la vista *Telemetría de GPUs*, la tabla visualiza las percepciones crudas emitidas directamente por los nodos (`node-01` a `node-04`).

---

### Pregunta 4: ¿Qué significa el marco PEAS y cómo se formalizó para ECO-HPC?
* **Explicación Simple:**  
  PEAS es el marco formal de Russell & Norvig: Rendimiento (ahorro y seguridad térmica), Entorno (clúster HPC de IA), Actuadores (DVFS, cooling y SLURM simulados) y Sensores (telemetría continua).
* **Explicación Técnica:**  
  - **P (Performance):** Criterio de rendimiento cuyo objetivo es reducir el consumo en Watts y kWh acumulados simulados, buscando operar bajo el umbral preventivo configurado para el prototipo (<85 °C en simulación, parámetro no universal) con la meta de mitigar el impacto sobre los acuerdos de nivel de servicio (SLAs) de los trabajos de IA. Describe un objetivo arquitectónico y no una garantía estricta de cumplimiento de SLA.
  - **E (Environment):** Entorno multi-acelerador, continuo en sus variables térmicas y eléctricas, y parcialmente observable ante fallos de sensado.
  - **A (Actuators):** Señales de control simuladas para transiciones de P-States (DVFS), modulación de ventilación forzada y cuotas de cola en SLURM.
  - **S (Sensors):** Percepciones numéricas estructuradas que capturan temperatura, potencia, utilización y frecuencia.
* **Ejemplo en ECO-HPC:**  
  En la vista *Marco PEAS & Ficha Técnica*, cuatro tarjetas presentan cada componente formal acompañado de sus parámetros.

---

### Pregunta 5: ¿Dónde está el agente inteligente y en qué consiste su inteligencia?
* **Explicación Simple:**  
  Está implementado en `agent.py` y `rules.py`. Su inteligencia radica en auditar la veracidad del dato, actualizar su estado interno y tomar deterministamente la mejor decisión para ahorrar energía o proteger el hardware.
* **Explicación Técnica:**  
  Según Russell & Norvig, la racionalidad de un agente radica en seleccionar acciones que maximicen el valor esperado de su métrica de desempeño a partir de su secuencia de percepciones y su conocimiento incorporado. ECO-HPC no dispara respuestas a ciegas: audita primero la consistencia física del dato, mantiene memoria en su estado interno y decide de forma justificada y auditable si corresponde mantener, ahorrar, proteger o solicitar mantenimiento.
* **Ejemplo en ECO-HPC:**  
  En la vista *Agente (Decisión & Ciclo)*, se visualiza el ciclo en 5 bloques: `PERCEPCIÓN → CONTROL DE CALIDAD → ESTADO → DECISIÓN → ACCIÓN SIMULADA`.

---

### Pregunta 6: ¿Por qué se utilizó un agente basado en reglas y no Machine Learning o Redes Neuronales?
* **Explicación Simple:**  
  Por explicabilidad total, determinismo, rapidez de ejecución y seguridad operativa en hardware crítico, evitando la opacidad de cajas negras y sobrecarga computacional innecesaria.
* **Explicación Técnica:**  
  En la supervisión de hardware de misión crítica, cada intervención operativa debe ser completamente predecible y explicable. Modelos complejos de aprendizaje automático o redes neuronales introducen riesgos de alucinación ante datos fuera de distribución, opacidad diagnóstica (*black box*) y sobrecarga computacional que consumiría los mismos recursos que se busca optimizar. El prototipo permite demostrar una lógica de decisión reproducible sobre datos de telemetría simulados mediante un sistema de reglas deterministas jerárquicas totalmente auditable.
* **Ejemplo en ECO-HPC:**  
  En `rules.py`, la función `evaluate_rules()` implementa la jerarquía determinista: Regla 0 (Veracidad) $\rightarrow$ Regla 1 (Protección) $\rightarrow$ Regla 2 (Ahorro) $\rightarrow$ Regla 3 (Operación Normal).

---

### Pregunta 7: ¿Qué es el estado interno del agente y por qué una percepción no es una orden?
* **Explicación Simple:**  
  El agente mantiene memoria histórica de decisiones, estados por GPU y acumuladores del sistema. Las reglas actuales evalúan de forma determinista la percepción presente y no utilizan aprendizaje automático ni dependen de la decisión anterior. Una percepción no es una orden porque debe pasar por validación de calidad antes de actuar.
* **Explicación Técnica:**  
  Si una percepción fuera una orden inmediata (agente reflejo simple sin estado), un transitorio térmico espurio o una falla electromagnética en un sensor (como una lectura errónea de 150 °C) ordenaría apagar un nodo de cómputo en medio de un entrenamiento de IA de semanas de duración. El agente somete la percepción al control de veracidad y actualiza su memoria interna antes de autorizar cualquier cambio de régimen.
* **Ejemplo en ECO-HPC:**  
  La clase `EcoHpcAgent` en `agent.py` mantiene `state_history`, `simulated_savings_kwh` y `interventions_counter`, registrando cada transición.

---

### Pregunta 8: ¿Qué es la V de Veracidad y qué errores detecta el control de calidad?
* **Explicación Simple:**  
  Es la dimensión que audita la confiabilidad y coherencia física de los datos antes de permitir la toma de decisiones. El módulo detecta campos faltantes, nulos, tipos incorrectos, valores fuera de rango físico y contradicciones lógicas entre variables.
* **Explicación Técnica:**  
  El módulo `data_quality.py` ejecuta cinco comprobaciones formales:
  1. Presencia de campos obligatorios (`gpu_id`, `temperature`, `power_w`, `utilization`, `frequency`).
  2. Detección de valores `None` o `NaN`.
  3. Conversión y coherencia de tipos numéricos.
  4. Rangos físicos admisibles (T: 15–105 °C, P: 20–900 W, Util: 0–100%, Freq: 200–2800 MHz).
  5. Inconsistencias lógicas cruzadas (temperatura >95 °C con potencia <40 W y 0% de uso).
  *Nota metodológica:* La desduplicación de paquetes no está implementada en el prototipo local y corresponde a un control conceptual para ingesta distribuida.
* **Ejemplo en ECO-HPC:**  
  En la vista *Calidad de Datos & Veracidad*, se muestra cómo GPU-12 es rechazada por marcar 150 °C con 10 W, y GPU-13 por contener `NaN` y potencia negativa.

---

### Pregunta 9: ¿Qué es MapReduce y qué papel juega en este proyecto?
* **Explicación Simple:**  
  Es un paradigma de procesamiento en paralelo para grandes volúmenes de datos. En ECO-HPC se utiliza en la V de Velocidad para el análisis Batch histórico: mapea lecturas por GPU, las agrupa en Shuffle y en Reduce calcula el consumo medio y la energía acumulada en kWh.
* **Explicación Técnica:**  
  MapReduce formaliza la agregación histórica en tres fases:
  1. **Map:** Transforma cada registro de telemetría en un par clave-valor: $\langle \text{gpu\_id}, \{\text{potencia}, \text{temp}, \text{count}\} \rangle$.
  2. **Shuffle:** Agrupa todas las emisiones bajo listas particionadas por cada acelerador.
  3. **Reduce:** Agrega métricas consolidadas: potencia media, temperatura máxima y energía acumulada. Cada registro representa una ventana de muestreo fija de 60 segundos cuyo timestamp identifica el inicio de esa ventana (ej. 10 registros de 12:00 a 12:09 cubren 10 ventanas = 10 minutos acumulados, $\text{Horas} = \frac{N \times 60\,\text{s}}{3600\,\text{s/h}} = 0{,}1667\text{ h}$ como supuesto del dataset).
  *Nota:* Está implementado como demostración didáctica local en Python puro; no utiliza un clúster físico Hadoop ni Spark.
* **Ejemplo en ECO-HPC:**  
  En la vista *MapReduce Histórico*, se puede explorar interactivamente cada etapa (`Entrada` $\rightarrow$ `Map` $\rightarrow$ `Shuffle` $\rightarrow$ `Reduce`) con los 160 registros consolidados.

---

### Pregunta 10: ¿Por qué se propone una base de datos NoSQL para producción a escala y no SQL tradicional?
* **Explicación Simple:**  
  Porque un escenario de 1.024 GPUs genera más de 88,4 millones de escrituras diarias continuas. Para producción se propone una base wide-column, tomando Apache Cassandra como referencia conceptual, la cual absorbe escrituras secuenciales sin bloqueos transaccionales ACID.
* **Explicación Técnica:**  
  Para una implementación productiva se propone una base NoSQL de tipo wide-column, tomando Apache Cassandra como tecnología de referencia. Esta arquitectura es conceptual y no se implementa en el prototipo. Una base relacional (RDBMS) penaliza la inserción masiva continua debido a la contención en el registro de transacciones (*write-ahead log*) y el rebalanceo de índices de árbol B (*B-Trees*). Las bases wide-column estructuradas sobre LSM-Trees (*Log-Structured Merge-trees*) escriben secuencialmente en memoria (*Memtable*) y vuelcan a disco en archivos inmutables (*SSTables*) particionados por GPU y tiempo, facilitando escalabilidad horizontal y políticas nativas de retención (*TTL*).
* **Ejemplo en ECO-HPC:**  
  En la vista *Sostenibilidad & NoSQL*, la pestaña *Justificación NoSQL* detalla la comparativa técnica entre el modelo relacional y el modelo wide-column.

---

### Pregunta 11: ¿Dónde aparece concretamente la sostenibilidad ambiental en el sistema?
* **Explicación Simple:**  
  En la reducción activa del consumo eléctrico parásito en fases de baja utilización (ahorro de kWh) y en la prevención de estrés térmico continuo para prolongar la vida útil de los equipos y reducir la huella de carbono.
* **Explicación Técnica:**  
  En HPC la sostenibilidad se evalúa mediante la energía total disipada y la métrica PUE (*Power Usage Effectiveness*). Cuando una GPU concluye un batch o espera I/O, mantener frecuencias elevadas causa un derroche eléctrico pasivo; la acción `AHORRAR` reduce el consumo en ~40% mediante modulación de reloj. Asimismo, la acción `PROTEGER` interviene preventivamente al superar el umbral configurado (85 °C en simulación), mitigando el estrés térmico severo y evitando el recambio prematuro de hardware de silicio.
* **Ejemplo en ECO-HPC:**  
  En el Dashboard General y en la vista *Sostenibilidad*, se visualiza el diagrama causal `DATOS → DECISIONES → EFICIENCIA → SOSTENIBILIDAD` y el ahorro acumulado en kWh.

---

### Pregunta 12: ¿Los datos de telemetría de GPU constituyen datos personales o sensibles según la Ley 25.326?
* **Explicación Simple:**  
  El prototipo utiliza telemetría técnica simulada y no trata directamente datos sensibles. En un centro de datos real, la telemetría no es un dato personal aisladamente, pero sí puede relacionarse con personas físicas cuando se cruza con las bases del planificador de tareas (SLURM).
* **Explicación Técnica:**  
  El prototipo opera exclusivamente sobre métricas de silicio (`temperature`, `power_w`, `frequency`). No trata directamente datos sensibles según el Art. 2 de la Ley 25.326 (origen racial, convicciones religiosas, opiniones políticas, afiliación sindical, salud o vida sexual). Sin embargo, en un clúster real, si la telemetría se vincula a la cuenta de usuario de un investigador y las tareas computacionales procesan datos clínicos o demográficos, se genera un vínculo con información personal sujeta a la ley. Se aplican allí los principios de calidad, pertinencia, finalidad (no utilizar telemetría técnica para vigilancia laboral encubierta), minimización (el agente opera únicamente con `gpu_id`) y seguridad/confidencialidad (Arts. 9 y 10 Ley 25.326 y Res. AAIP 47/2018).
* **Ejemplo en ECO-HPC:**  
  En la vista *Sostenibilidad & NoSQL*, la pestaña *Ley Nacional N.º 25.326* formaliza el encuadre normativo y los principios de minimización aplicados.

---

### Pregunta 13: ¿Qué componentes del sistema están realmente implementados, cuáles son simulados y cuáles son conceptuales?
* **Explicación Simple:**  
  Están **implementados** el agente de reglas deterministas, el módulo de calidad, el motor MapReduce pedagógico, la app Streamlit y los 24 tests. Son **simulados** las 16 GPUs, sus sensores y los actuadores. Son **conceptuales** la escala de 1.024 GPUs, Kafka y la base Cassandra de producción.
* **Explicación Técnica:**  
  - **Implementado en código ejecutable:** La lógica del agente (`agent.py`), el evaluador determinista (`rules.py`), la auditoría de calidad (`data_quality.py`), el algoritmo MapReduce local (`mapreduce_demo.py`), la interfaz gráfica (`app.py`) y las 24 pruebas automatizadas en `tests/`.
  - **Simulado en software:** Los 16 aceleradores GPU, sus valores continuos de telemetría generados con distribuciones coherentes y las acciones operativas recomendadas (sin alteración de registros de voltaje en hardware físico). La referencia a H100 SXM (hasta 700 W configurables) es un marco de contexto técnico; el prototipo no posee GPUs H100 físicas.
  - **Propuesta conceptual:** El clúster masivo de 1.024 GPUs para dimensionamiento de Big Data, la capa de streaming distribuida (Kafka/Flink) y la base NoSQL wide-column (Cassandra) para producción.
* **Ejemplo en ECO-HPC:**  
  En la vista *Arquitectura (Prototipo vs Escala)*, la tabla *Matriz de Realidad y Transparencia Técnica* clasifica explícitamente cada componente.

---

### Pregunta 14: ¿Qué pasaría en producción a escala (1.024 GPUs) y por qué no se instaló Docker o Kafka en el prototipo?
* **Explicación Simple:**  
  En producción se desplegaría un bus Kafka y Flink para streaming masivo. No se instalaron en el prototipo por el principio de no sobreingeniería: agregarían sobrecarga y fragilidad de despliegue sin aportar mayor entendimiento de los conceptos teóricos.
* **Explicación Técnica:**  
  A escala de 1.024 aceleradores, la ingesta requiere un clúster distribuido (Apache Kafka o Apache Pulsar) con particionamiento por nodo y motores de stream processing (Apache Flink) con ventanas deslizantes de baja latencia. Desplegar esa infraestructura con contenedores pesados en una máquina local no demuestra mayor comprensión conceptual, sino una sobrecarga que compromete la reproducibilidad y estabilidad de la demostración. Implementar los algoritmos en Python nativo y limpio permite ofrecer una solución transparente, verificable y técnicamente defendible.
* **Ejemplo en ECO-HPC:**  
  En la vista *Arquitectura*, la columna *Arquitectura Conceptual* grafica la topología completa de producción con Kafka, Flink y NoSQL.

---

### Pregunta 15: ¿Qué limitaciones técnicas presenta el prototipo funcional actual?
* **Explicación Simple:**  
  El prototipo no controla hardware físico real, opera a escala de 16 GPUs simuladas, utiliza reglas deterministas fijas sin aprendizaje automático y ejecuta MapReduce de forma local en memoria.
* **Explicación Técnica:**  
  Con honestidad y rigor académico, se reconocen cinco limitaciones deliberadas de alcance:
  1. **Hardware Simulado:** El prototipo no manipula circuitos integrados ni termistores físicos reales; las percepciones y las acciones son simuladas mediante modelos computacionales reproducibles.
  2. **Escala del Prototipo:** Supervisa 16 GPUs (4 nodos de cómputo), dimensionando teóricamente la escala de 1.024 aceleradores para el análisis conceptual de Big Data.
  3. **Lógica de Reglas Deterministas:** El agente no utiliza Machine Learning ni adapta sus umbrales automáticamente; las reglas son estáticas y jerárquicas, priorizando auditabilidad y explicabilidad sobre adaptabilidad estocástica.
  4. **Entorno de Procesamiento Local:** MapReduce está implementado algorítmicamente en Python puro sobre memoria local; no constituye un clúster distribuido físico Hadoop/Spark ni cuenta con una base Cassandra desplegada.
  5. **Alcance del Control de Calidad:** Audita campos obligatorios, valores nulos, coherencia de tipos, rangos físicos y contradicciones lógicas cruzadas; no implementa mecanismos de desduplicación de paquetes de red.

---

## 5. Criterio de Comunicación Técnica: Respuesta en Dos Niveles

Al responder preguntas técnicas durante la defensa, estructurá la intervención en dos niveles sucesivos:

1. **Primer Nivel (Respuesta Corta y Directa):**  
   Comenzá siempre con una afirmación clara, concisa y comprensible de 1 a 2 frases que conteste el núcleo de la pregunta sin evasivas.  
   *Ejemplo:* *"El agente supervisa la telemetría sensorial para detectar si la GPU derrocha energía o se sobrecalienta, y ejecuta una acción determinista para protegerla o reducir su consumo."*

2. **Segundo Nivel (Fundamento Técnico Formal):**  
   Si se solicita profundizar o repregunta sobre el mecanismo interno, desplegá el vocabulario técnico preciso y la fundamentación formal.  
   *Ejemplo:* *"Formalmente, el vector de percepciones es auditado por el módulo de calidad para verificar su veracidad, y evaluado por un motor jerárquico determinista con estado interno que formaliza el marco PEAS, modulando el reloj por DVFS o aplicando señales de power-capping."*
