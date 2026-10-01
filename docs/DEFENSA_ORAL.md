# GUÍA DE PREPARACIÓN PARA LA DEFENSA ORAL
## ECO-HPC: Agente Supervisor de Eficiencia Energética en Entornos HPC

---

Esta guía está diseñada para que puedas comprender, internalizar y defender el proyecto completo con soltura, rigor y seguridad técnica en **una sola jornada de estudio**.

---

## 1. Discursos de Apertura según el Tiempo Asignado

### 1.1. Discurso de 30 Segundos (Elevator Pitch)
> *"ECO-HPC es un prototipo que demuestra cómo los flujos continuos de telemetría de Big Data alimentan a un Agente Inteligente para optimizar el consumo energético y la seguridad térmica en un clúster de Inteligencia Artificial. A partir de lecturas de sensores de GPUs simuladas, el agente evalúa la calidad de los datos, actualiza su estado interno y decide en tiempo real si debe mantener la operación, reducir frecuencias para ahorrar energía o activar protecciones térmicas para preservar el hardware."*

---

### 1.2. Discurso de 2 Minutos (Flujo Causal: Problema → Solución)
> *"**El problema:** El entrenamiento de modelos masivos de IA demanda una enorme infraestructura de supercómputo que consume megavatios de electricidad y genera altas temperaturas. Si dejamos que las GPUs operen sin supervisión inteligente, se producen dos problemas graves: derroche eléctrico en momentos de subutilización y riesgo de degradación del silicio ante picos térmicos.
>
> **La solución con datos y agentes:** Diseñamos ECO-HPC, un agente supervisor basado en reglas. Las GPUs emiten telemetría continua de temperatura, potencia y utilización por canales M2M. Esos datos pasan primero por un filtro estricto de **Veracidad** para descartar anomalías de sensado.
>
> **La decisión:** Si los datos son válidos, el agente evalúa sus reglas deterministas. Si detecta una GPU con baja utilización pero alto consumo, pasa al estado **AHORRO** y modula la frecuencia de reloj. Si detecta temperaturas críticas mayores a 85 °C, pasa al estado **PROTECCIÓN** y activa refrigeración y limitación de carga. Si el dato es físicamente imposible, pasa a **DATOS NO CONFIABLES** y rechaza intervenir a ciegas.
>
> **El resultado:** Transformamos datos crudos de telemetría en decisiones operativas que ahorran kilovatios-hora, cuidan el hardware y mejoran la sostenibilidad ambiental de la Inteligencia Artificial."*

---

### 1.3. Discurso de 5 Minutos (Estructura Académica Completa de la Cátedra)
> *"Buenos días. Nuestro proyecto integrador aborda la relación entre el **Big Data como infraestructura de sensado y la Inteligencia Artificial**, aplicado al observatorio de Hardware, Supercómputo y Sostenibilidad Ambiental.
>
> **1. Las 5 V del Big Data en el Escenario HPC:**
> Planteamos un escenario conceptual de **1.024 GPUs**. A una lectura por segundo, esto genera **88,4 millones de registros diarios**, equivalente a más de **22 GB por día** (**Volumen**). Necesitamos una doble **Velocidad**: baja latencia en streaming (menor a un segundo) para que el agente evite el sobrecalentamiento, y procesamiento en batch mediante **MapReduce** para el análisis histórico de consumo. La **Variedad** está reflejada en nuestros datasets: métricas estructuradas en CSV, objetos semiestructurados en JSON y logs no estructurados del sistema. La **Veracidad** la resolvemos con un módulo de auditoría que filtra datos fuera de rango o contradictorios antes de alimentar al agente. Y el **Valor** se concreta en la reducción de costos y emisiones de carbono.
>
> **2. El Agente Inteligente y el Marco PEAS:**
> Siguiendo a Russell y Norvig, formalizamos el agente con la estructura PEAS: su medida de rendimiento es maximizar el ahorro energético manteniendo las temperaturas en rango seguro; su entorno es el clúster HPC de IA; sus sensores son las lecturas de telemetría de hardware; y sus actuadores son comandos simulados de modulación de frecuencia (DVFS), escalado de ventiladores y cuotas de cómputo en SLURM.
>
> **3. Arquitectura y Transparencia Técnica:**
> Implementamos un prototipo funcional con **16 GPUs simuladas** usando Python, Pandas y Streamlit. Diseñamos un agente basado en reglas con estado interno: es deliberadamente determinista y transparente, sin cajas negras de machine learning innecesarias. Para el histórico, desarrollamos un pipeline didáctico de **MapReduce** (Map, Shuffle y Reduce) que calcula el consumo acumulado en kWh. Para la producción a escala, justificamos conceptualmente el uso de bases de datos **NoSQL** orientadas a series temporales por su alta tasa de escritura secuencial y compresión.
>
> **4. Marco Legal (Ley 25.326):**
> Analizamos que la telemetría pura es un dato técnico M2M, pero se transforma en dato personal según el Art. 2 de la Ley 25.326 cuando se asocia al usuario, trabajo y horario en el gestor SLURM. Por ello, aplicamos el principio de minimización disociando la identidad del flujo de control.
>
> En conclusión, ECO-HPC demuestra cómo la ingeniería de datos hace posible una Inteligencia Artificial operativamente viable y ambientalmente responsable."*

---

## 2. Glosario Técnico en Lenguaje Sencillo

* **Big Data:** Gestión y análisis de volúmenes de datos tan masivos, rápidos o variados que superan la capacidad de las herramientas tradicionales de procesamiento de datos.
* **Las 5 V:** Volumen (cantidad de datos), Velocidad (frecuencia de llegada y respuesta requerida), Variedad (diversidad de formatos), Veracidad (confiabilidad y calidad de la medición) y Valor (utilidad práctica de la información obtenida).
* **M2M (Machine-to-Machine):** Comunicación directa y automatizada entre dispositivos o sensores y un sistema de procesamiento, sin intervención humana directa.
* **HPC (High Performance Computing):** Computación de Alto Rendimiento; infraestructura de servidores agrupados en clústeres para procesar tareas computacionales extremadamente pesadas, como el entrenamiento de redes neuronales.
* **PEAS:** Marco metodológico de Inteligencia Artificial que define formalmente a un agente mediante sus cuatro componentes: **P**erformance (Medida de Rendimiento), **E**nvironment (Entorno), **A**ctuators (Actuadores) y **S**ensors (Sensores).
* **Agente Inteligente:** Entidad computacional capaz de percibir su entorno a través de sensores, procesar esa información y actuar sobre dicho entorno mediante actuadores para alcanzar un objetivo prefijado.
* **Percepción:** Conjunto específico de lecturas que los sensores entregan al agente en un instante determinado.
* **Estado Interno:** Memoria o condición actual del agente que retiene información del pasado reciente para no decidir de forma puramente reactiva e inconexa.
* **Sensor:** Dispositivo o componente que mide una magnitud física o lógica del entorno (ej. termistor para temperatura, shunt para corriente eléctrica).
* **Actuador:** Mecanismo mediante el cual el agente ejecuta una acción física o lógica para modificar el entorno (ej. reducir el multiplicador de reloj de la GPU).
* **MapReduce:** Paradigma de procesamiento distribuido para grandes volúmenes de datos. Se divide en: **Map** (transforma registros individuales en pares clave-valor), **Shuffle** (agrupa todos los valores con la misma clave) y **Reduce** (agrega o calcula métricas consolidadas sobre cada grupo).
* **NoSQL:** Sistemas de gestión de bases de datos no relacionales, diseñados para escalabilidad horizontal, esquemas flexibles y altísima velocidad de escritura.
* **Veracidad:** Dimensión del Big Data que evalúa la exactitud, consistencia, integridad y ausencia de ruido en los datos recolectados.
* **Sesgo de Sensado:** Desviación constante y sistemática en la medición provocada por diferencias de calibración en los circuitos de lectura física.
* **DVFS (Dynamic Voltage and Frequency Scaling):** Técnica de hardware que permite aumentar o disminuir dinámicamente el voltaje y la frecuencia de operación de un procesador para ahorrar energía o disipar menos calor.
* **PUE (Power Usage Effectiveness):** Métrica estándar de centros de datos que mide la eficiencia energética: relación entre la energía total consumida por el edificio y la energía que efectivamente consumen los equipos de cómputo (lo ideal es tender a 1.0).

---

## 3. Guion Paso a Paso para la Demostración en la Aplicación (3 a 5 Minutos)

| Paso | Pantalla en Streamlit | Qué Mostrar | Qué Decir Oralmente |
| :---: | :--- | :--- | :--- |
| **1** | **Dashboard General** | Tarjetas de métricas: 16 GPUs, potencia total, temp promedio. | *"Este es nuestro clúster HPC. Aquí vemos el estado global del hardware: 16 GPUs simuladas consumiendo energía de forma consolidada."* |
| **2** | **Telemetría de GPUs** | Tabla de datos sensoriales y gráfico de correlación. | *"Estas son las percepciones que llegan por M2M. Cada GPU reporta temperatura, potencia, uso de cómputo y reloj cada segundo."* |
| **3** | **Pantalla del Agente (Normal)** | Seleccionar `GPU-01` en el inspector. | *"El agente recibe estas lecturas. Como GPU-01 opera a 62 °C con 350 W y 70% de uso, determina estado NORMAL y decide MANTENER."* |
| **4** | **Pantalla del Agente (Ahorro)** | Seleccionar `GPU-04` o activar Modo Demo Paso 2. | *"En GPU-04 vemos el valor del agente: la utilización cayó al 14%, pero el consumo sigue en 380 W. El agente detecta la ineficiencia, entra en AHORRO y reduce el reloj mediante DVFS."* |
| **5** | **Pantalla del Agente (Protección)** | Seleccionar `GPU-07` o activar Modo Demo Paso 3. | *"En GPU-07 ocurre una situación crítica: entrenamiento pesado, temperatura en 89 °C y 720 W. El agente pasa a PROTECCIÓN y ordena aumentar refrigeración y aplicar power-capping."* |
| **6** | **Calidad de Datos (Anomalía)** | Seleccionar `GPU-12` o ver pestaña Veracidad. | *"Aquí demostramos la V de Veracidad: GPU-12 reporta 150 °C con 10 W. Es físicamente imposible. Una percepción no es una orden: el agente no apaga el servidor a ciegas, marca DATOS NO CONFIABLES y pide revisión del sensor."* |
| **7** | **MapReduce** | Pantalla MapReduce: ver Map, Shuffle y Reduce. | *"Para la analítica Batch histórica, ejecutamos MapReduce. Mapeamos cada lectura a su GPU, la agrupamos en Shuffle y el Reducer calcula el consumo promedio y los kWh totales acumulados."* |

---

## 4. Banco de Preguntas Difíciles del Tribunal Evaluador

### Pregunta 1: ¿Por qué este problema se clasifica como Big Data y no simplemente como monitoreo tradicional de sistemas?
* **Respuesta Corta Directa:**  
  Porque a escala de un clúster HPC de 1.024 GPUs, la telemetría de alta frecuencia genera más de 88 millones de lecturas diarias y 22 GB por jornada en múltiples formatos heterogéneos, requiriendo arquitecturas de streaming de baja latencia combinadas con procesamiento batch distribuido.
* **Explicación Técnica Ampliada:**  
  El monitoreo clásico recopila métricas agregadas cada varios minutos (ej. SNMP o Nagios). En HPC para IA, la densidad de potencia de los aceleradores modernos (700 W por chip) exige muestreo a nivel de segundos para evitar el embalamiento térmico. Cumple con las 5 dimensiones: Volumen masivo acumulativo, doble Velocidad (streaming <1s para control reflejo y batch para agregación histórica), Variedad en tres formatos de datos coexistentes, necesidad crítica de filtros de Veracidad física y generación directa de Valor en ahorro de megavatios y preservación de equipamiento.

---

### Pregunta 2: ¿Cuáles son las 5 V y cómo están representadas concretamente en el proyecto?
* **Respuesta Corta Directa:**  
  Volumen (cálculo formal de 88,4M registros diarios a escala), Velocidad (streaming en tiempo real del agente vs batch con MapReduce), Variedad (CSV estructurado, JSON semiestructurado y logs de texto), Veracidad (auditoría de límites físicos y datos ilógicos) y Valor (ahorro energético cuantificado en kWh y protección de hardware).
* **Explicación Técnica Ampliada:**  
  En el prototipo cada V tiene un respaldo verificable: el Volumen se formula con la ecuación matemática $N \times f \times 86400 \times \text{bytes}$; la Velocidad se comprueba con la respuesta instantánea del agente en la UI y el procesamiento histórico diferido; la Variedad se constata con los tres archivos en la carpeta `data/`; la Veracidad se demuestra aislando lecturas como los 150 °C de `GPU-12` en `data_quality.py`; y el Valor se visualiza en los kilovatios-hora ahorrados acumulados por las intervenciones del agente.

---

### Pregunta 3: ¿Por qué M2M / IoT es la fuente de datos principal?
* **Respuesta Corta Directa:**  
  Porque la telemetría proviene de sensores electrónicos integrados en las placas de hardware comunicándose directamente con los controladores de gestión del sistema sin intervención humana.
* **Explicación Técnica Ampliada:**  
  El acrónimo M2M (Machine-to-Machine) define flujos autónomos de máquina a máquina. Las GPUs disponen de circuitos de instrumentación embebidos (termistores, convertidores analógico-digitales y sensores de corriente por efecto shunt) que envían paquetes de datos a través de buses internos (I2C, SMBus o PCIe) hacia los controladores BMC (*Baseboard Management Controller*) y el demonio DCGM de NVIDIA. No interviene ningún operador humano en la generación de estos datos.

---

### Pregunta 4: ¿Qué significa PEAS y cómo se definió para ECO-HPC?
* **Respuesta Corta Directa:**  
  PEAS es el marco de Russell y Norvig para caracterizar agentes: Performance (eficiencia energética y seguridad térmica), Environment (clúster HPC para IA), Actuators (modulación DVFS, refrigeración y SLURM simulados) y Sensors (telemetría M2M de temperatura, potencia, uso y reloj).
* **Explicación Técnica Ampliada:**  
  - **P (Performance):** Minimizar el consumo en Watts y kWh sin degradar el SLA de las tareas de IA y manteniendo las temperaturas bajo 85 °C.  
  - **E (Environment):** Entorno multi-GPU, continuo en variables físicas, parcialmente observable debido a posibles fallos de sensores y determinista en la aplicación de políticas.  
  - **A (Actuators):** Actuadores simulados en el prototipo que representan órdenes de ajuste de frecuencia y voltaje (P-states), aceleración de ventiladores y cuotas de cómputo.  
  - **S (Sensors):** Percepciones recibidas que incluyen temperatura de unión, potencia instantánea, porcentaje de carga computacional y frecuencia de reloj.

---

### Pregunta 5: ¿Dónde radica la inteligencia del agente?
* **Respuesta Corta Directa:**  
  En su capacidad de evaluar su estado interno y relacionar variables físicas cruzadas para inferir el estado del sistema y actuar proactivamente antes de que ocurra una falla o un derroche.
* **Explicación Técnica Ampliada:**  
  Siguiendo la teoría de agentes inteligentes de Russell & Norvig, la inteligencia no reside exclusivamente en algoritmos de aprendizaje estadístico o redes neuronales, sino en la capacidad de mapear secuencias de percepciones en acciones racionales orientadas a maximizar una medida de rendimiento prefijada. El agente no es un simple disparador reactivo directo: evalúa primero la calidad del dato, mantiene memoria en su estado interno, diagnostica discrepancias lógicas y selecciona la intervención óptima.

---

### Pregunta 6: ¿Por qué decidieron utilizar un agente basado en reglas y no un modelo de Machine Learning o Red Neuronal?
* **Respuesta Corta Directa:**  
  Por explicabilidad, determinismo, seguridad operativa en hardware de misión crítica y para demostrar con total transparencia el ciclo cognitivo formal del agente sin introducir cajas negras innecesarias.
* **Explicación Técnica Ampliada:**  
  En la supervisión de hardware e infraestructura de misión crítica, las decisiones deben ser 100% auditables, predecibles y de ejecución ultrarrápida (baja latencia en microsegundos). Un modelo de deep learning o aprendizaje por refuerzo introduce opacidad (*caja negra*), riesgo de alucinación o deriva ante datos fuera de distribución, y una sobrecarga computacional innecesaria que compite por los mismos recursos que pretende supervisar. La cátedra solicitó explícitamente demostrar el funcionamiento conceptual del agente; un sistema basado en reglas explícitas jerárquicas es la solución técnica más robusta y defendible.

---

### Pregunta 7: ¿Qué es el estado interno del agente y por qué una percepción no es automáticamente una orden?
* **Respuesta Corta Directa:**  
  El estado interno es la representación que el agente tiene sobre la condición actual del clúster (NORMAL, AHORRO, PROTECCIÓN o DATOS NO CONFIABLES). Una percepción no es una orden porque debe pasar por validación de calidad e interpretación lógica antes de decidir una acción.
* **Explicación Técnica Ampliada:**  
  Si una percepción fuera directamente una orden (*agente reflejo simple sin estado*), un pico transitorio de ruido en un termistor o una lectura anómala de 150 °C apagaría inmediatamente un clúster de supercómputo que está ejecutando un entrenamiento de IA de semanas de duración, causando pérdidas económicas irreparables. El agente de ECO-HPC posee estado interno: toma la percepción, la somete al filtro de veracidad, actualiza su modelo interno del entorno y solo si la condición es coherente emite una acción correctiva.

---

### Pregunta 8: ¿Qué es MapReduce y qué papel juega en este proyecto?
* **Respuesta Corta Directa:**  
  Es un paradigma de programación para procesar grandes volúmenes de datos en paralelo. En ECO-HPC se utiliza en la V de Velocidad para el análisis Batch histórico: mapea lecturas por GPU, las agrupa en Shuffle y calcula en Reduce el consumo medio y la energía acumulada.
* **Explicación Técnica Ampliada:**  
  MapReduce (Dean & Ghemawat, Google 2004) divide el procesamiento en tres etapas formales:  
  1. **Map:** Toma registros de telemetría y extrae pares clave-valor $\langle \text{gpu\_id}, \{\text{potencia}, \text{temp}, \text{count}\} \rangle$.  
  2. **Shuffle & Sort:** La infraestructura redistribuye los datos agrupando todas las emisiones que comparten la misma clave identificadora.  
  3. **Reduce:** Ejecuta una agregación matemática sobre cada lista de claves para obtener la potencia media, la temperatura máxima histórica y los kilovatios-hora totales. En el proyecto está implementado didácticamente en Python puro.

---

### Pregunta 9: ¿Por qué se propone una base de datos NoSQL para producción a escala y no una base de datos relacional tradicional (SQL)?
* **Respuesta Corta Directa:**  
  Porque a escala de 1.024 GPUs existen 88,4 millones de escrituras diarias continuas. Las bases relacionales colapsan por bloqueo transaccional ACID y sobrecarga de índices B-Tree, mientras que las NoSQL Time-Series están optimizadas para inserción secuencial masiva (*append-heavy*) y escalabilidad horizontal.
* **Explicación Técnica Ampliada:**  
  Una base relacional clásica como PostgreSQL o MySQL utiliza estructuras de almacenamiento orientadas a filas con transacciones ACID completas y rebalanceo de índices B-Tree por cada inserción. Con 1.024 escrituras concurrentes por segundo, los bloqueos de tablas y páginas provocan contención de I/O. Las bases NoSQL orientadas a series de tiempo (como InfluxDB, TimescaleDB o Apache Cassandra) utilizan motores basados en LSM-Trees (*Log-Structured Merge-trees*), que realizan escrituras secuenciales en memoria (*Memtable*) antes de bajarlas a disco en bloques comprimidos por columnas, soportando millones de métricas por segundo con compresión de hasta el 80% y particionamiento natural por ventanas de tiempo.

---

### Pregunta 10: ¿Qué ocurre si un sensor de hardware se descalibra, falla o reporta un valor erróneo?
* **Respuesta Corta Directa:**  
  El módulo de control de calidad (`data_quality.py`) detecta la violación de límites físicos o la contradicción lógica, el agente adopta el estado DATOS NO CONFIABLES y rechaza ejecutar órdenes automáticas, emitiendo una alerta de mantenimiento.
* **Explicación Técnica Ampliada:**  
  Esta es la manifestación directa de la V de Veracidad. El sistema valida cuatro niveles: completitud de campos, valores nulos o tipos incorrectos, límites físicos absolutos (temperaturas entre 15 °C y 105 °C, potencias entre 20 W y 900 W) y consistencia física cruzada. Si por ejemplo un sensor se cuelga y marca 150 °C pero la potencia es de 10 W, el sistema identifica que es físicamente imposible que un chip disipe 150 °C sin flujo de corriente eléctrica. El agente aísla ese canal de telemetría y no altera el funcionamiento del nodo.

---

### Pregunta 11: ¿Dónde aparece concretamente la sostenibilidad ambiental en el sistema?
* **Respuesta Corta Directa:**  
  En la reducción activa del consumo eléctrico parásito en fases de baja utilización (ahorro de kWh) y en la protección térmica que evita el envejecimiento prematuro del hardware, reduciendo la huella de carbono y el impacto de la fabricación de silicio.
* **Explicación Técnica Ampliada:**  
  La sostenibilidad en HPC se cuantifica mediante la métrica del PUE (*Power Usage Effectiveness*) y los kilovatios-hora consumidos. Cuando un modelo de IA termina un paso de cómputo y espera datos de red o I/O, mantener la GPU al máximo de frecuencia disipa cientos de vatios sin utilidad computacional. La acción **AHORRAR** del agente mitiga este derroche parásito reduciendo el reloj en un 40%. Asimismo, la acción **PROTEGER** evita operar el silicio en regímenes térmicos que aceleran la electromigración y la falla física, evitando el recambio prematuro de equipamiento de altísima intensidad material y ecológica.

---

### Pregunta 12: ¿Los datos de telemetría de una GPU son considerados datos personales según la legislación argentina?
* **Respuesta Corta Directa:**  
  De forma aislada no, pero sí pasan a ser datos personales cuando se correlacionan con los registros del planificador SLURM (usuario, script, horario y nodo asignado), ya que permiten identificar o hacer determinable a la persona física que ejecuta la tarea (Art. 2 Ley 25.326).
* **Explicación Técnica Ampliada:**  
  Conforme a la Ley Nacional N.º 25.326 de Protección de los Datos Personales (Argentina) y el criterio de la Agencia de Acceso a la Información Pública (AAIP), un dato de máquina puramente técnico (`GPU-07 = 89 °C`) no identifica a un individuo. Sin embargo, en un entorno de HPC institucional, la telemetría está unida al gestor de colas: si sabemos qué investigador reservó ese nodo, el perfil de consumo y horarios de cómputo revela hábitos laborales, rendimiento o secretos de investigación. Por ello, el diseño técnico aplica el principio de **Minimización de Datos (Art. 4)** y **Seguridad (Res. AAIP 47/2018)**: el agente supervisor procesa únicamente datos disociados y anonimizados a nivel de hardware.

---

### Pregunta 13: Si tuvieras que ser completamente honesto ante el tribunal, ¿qué partes del sistema están realmente implementadas y qué partes son simuladas o conceptuales?
* **Respuesta Corta Directa:**  
  Están **realmente implementados** en Python el agente de reglas, el módulo de veracidad, el motor MapReduce, la aplicación Streamlit y la suite de 24 tests. Son **simulados** las GPUs, sus sensores y las órdenes de los actuadores. Son **conceptuales** la escala de 1.024 GPUs y la base de datos NoSQL de producción.
* **Explicación Técnica Ampliada:**  
  Presentamos una matriz de auditoría de realidad explícita:
  - **Implementado en código ejecutable:** La lógica del agente (`agent.py`), las reglas deterministas (`rules.py`), los filtros de veracidad (`data_quality.py`), el algoritmo MapReduce (`mapreduce_demo.py`), la UI interactiva (`app.py`) y las pruebas automatizadas (`tests/`).
  - **Simulado en software:** Los aceleradores GPU (16 instancias), los valores de telemetría (sintetizados con modelos coherentes de hardware) y los efectos físicos de los actuadores (no enviamos señales eléctricas a placas físicas).
  - **Propuesta conceptual:** La infraestructura de streaming distribuida (Kafka/Flink), el clúster masivo de 1.024 nodos y la base de datos NoSQL para retención masiva.

---

### Pregunta 14: ¿Por qué no instalaron Docker, Kafka, Kubernetes o Cassandra en este prototipo?
* **Respuesta Corta Directa:**  
  Por el principio de no sobreingeniería: esas herramientas añaden enorme complejidad de despliegue y consumo de memoria sin aportar ningún beneficio pedagógico adicional al Trabajo Práctico, cuya consigna se cumple íntegramente con Python y Pandas.
* **Explicación Técnica Ampliada:**  
  Desplegar una pila de infraestructura con contenedores, clústeres de mensajería y bases distribuidas no demuestra un mayor entendimiento de los conceptos fundamentales, sino una sobrecarga operativa innecesaria que dificulta la portabilidad y la reproducibilidad de la evaluación en un examen oral. El objetivo académico es demostrar que comprendemos el problema, el marco PEAS, las 5 V y la lógica algorítmica de MapReduce y NoSQL. Implementar esas herramientas conceptualmente y justificar su necesidad a escala en la arquitectura demuestra madurez de diseño sin poner en riesgo la estabilidad del proyecto.

---

## 5. Regla de Oro para Responder en el Examen Oral

Cuando el docente realice una pregunta, estructurá tu respuesta en dos niveles:

1. **Primer Nivel (Lenguaje Simple y Directo):**  
   Comenzá siempre con una frase clara, segura y conceptual que cualquiera pueda entender sin rodeos.  
   *Ejemplo:* *"El agente evalúa los sensores para saber si la GPU está gastando de más o recalentándose, y toma una decisión para protegerla o ahorrar energía."*
2. **Segundo Nivel (Fundamento Técnico Formal):**  
   Inmediatamente después, si el docente asiente o repregunta, introducí el vocabulario técnico de la materia.  
   *Ejemplo:* *"Específicamente, el vector de percepciones es filtrado por veracidad y procesado por un motor determinista con estado interno que implementa el marco PEAS, modulando la frecuencia por DVFS o activando refrigeración forzada."*
