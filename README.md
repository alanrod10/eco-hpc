# ECO-HPC: Agente Supervisor de Eficiencia Energética para Entornos HPC

[![Python Version](https://img.shields.io/badge/python-3.14%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Testing](https://img.shields.io/badge/tests-24%20passed-brightgreen.svg)]()
[![License](https://img.shields.io/badge/license-Academic-lightgrey.svg)]()

> **Trabajo Práctico Integrador:** "Las 5 V del Big Data como infraestructura de alimentación para sistemas de Inteligencia Artificial"  
> **Observatorio Académico:** IA + HARDWARE + COMPUTACIÓN DE ALTO RENDIMIENTO (HPC) + SOSTENIBILIDAD AMBIENTAL  

---

## 📌 1. Resumen del Proyecto

**ECO-HPC** es un sistema de supervisión inteligente que demuestra cómo los flujos continuos de telemetría de hardware (Big Data M2M/IoT) actúan como la infraestructura de sensado y percepción que alimenta a un **Agente Reactivo Basado en Reglas con Estado Interno**. 

El objetivo primordial del agente es optimizar el consumo eléctrico, prolongar la vida útil del hardware y garantizar la seguridad térmica en un clúster de supercómputo para Inteligencia Artificial.

### Definición del Estado Interno del Agente:
El agente mantiene memoria histórica de decisiones, estados por GPU y acumuladores del sistema. Las reglas actuales evalúan de forma determinista la percepción presente y no utilizan aprendizaje automático ni dependen de la decisión anterior.

### Preguntas Canónicas que Responde el Agente:
1. **¿Qué está ocurriendo en el hardware?** (Diagnóstico integral de la percepción).
2. **¿En qué estado se encuentra la GPU?** (`NORMAL`, `AHORRO`, `PROTECCION` o `DATOS NO CONFIABLES`).
3. **¿Qué decisión corresponde?** (`MANTENER`, `AHORRAR`, `REFRIGERAR`, `PROTEGER` o `REVISAR SENSOR`).
4. **¿Por qué?** (Justificación analítica y técnica basada en reglas explícitas).
5. **¿Qué acción se recomienda o simula?** (Comando operativo simulado de DVFS, refrigeración o SLURM).

---

## ⚙️ 2. Transparencia Técnica: Matriz de Realidad

Para garantizar máximo rigor metodológico y transparencia técnica:

| Componente | Estado en este Repositorio | Descripción |
| :--- | :--- | :--- |
| **Agente Supervisor** | **REALMENTE IMPLEMENTADO** | Implementado en Python (`agent.py`) con memoria histórica y acumuladores. |
| **Motor de Reglas** | **REALMENTE IMPLEMENTADO** | Implementado en `rules.py` con umbrales configurables de simulación (85 °C de protección). |
| **Control de Calidad** | **REALMENTE IMPLEMENTADO** | Implementado en `data_quality.py` (filtro de veracidad física). |
| **Demostración MapReduce**| **REALMENTE IMPLEMENTADO** | Implementado en Python puro (`mapreduce_demo.py`) asumiendo ventanas de muestreo de 60s por registro (10 registros = 10 minutos). |
| **Interfaz Web** | **REALMENTE IMPLEMENTADA** | Dashboard interactivo en Streamlit (`app.py`) con 12 vistas y Demostración en 5 pasos. |
| **Suite de Pruebas** | **REALMENTE IMPLEMENTADA** | 24 pruebas automatizadas con Pytest (unitarias, integración y negativas). |
| **Hardware de GPUs** | **SIMULADO** | 16 GPUs simuladas (`GPU-01` a `GPU-16`) en 4 nodos. No posee H100 físicas ni actúa sobre silicio real. |
| **Actuadores** | **SIMULADO** | Las acciones (modulación DVFS, cooling, power-capping) son recomendaciones simuladas. |
| **Clúster de 1.024 GPUs** | **CONCEPTUAL** | Supuesto dimensionado matemáticamente para ilustrar el volumen del Big Data. |
| **Base NoSQL Distribuida**| **CONCEPTUAL** | Propuesta de arquitectura para producción a escala (TimescaleDB / Cassandra). |

---

## 🚀 3. Instalación y Ejecución Rápida

El proyecto fue diseñado bajo el principio de **no sobreingeniería**, permitiendo su despliegue en cualquier entorno con Python 3 sin configuraciones complejas.

### Requisitos Previos:
* Python 3.10 o superior (verificado y optimizado en Python 3.14).

### Paso 1: Clonar y crear entorno virtual
```bash
# Clonar o situarse en el directorio del proyecto
cd "/mnt/c/Proyecto HPC-ECO"

# Crear y activar el entorno virtual
python3 -m venv .venv
source .venv/bin/activate
```

### Paso 2: Instalar dependencias mínimas
```bash
pip install -r requirements.txt
```

### Paso 3: Iniciar la aplicación web Streamlit
```bash
streamlit run app.py
```
La aplicación se abrirá automáticamente en tu navegador web en: `http://localhost:8501`.

---

## 🧪 4. Ejecución de la Suite de Pruebas Automatizadas

El proyecto incluye 24 pruebas exhaustivas que validan el comportamiento determinista del agente, la robustez ante fallos, la calidad de datos y el paradigma MapReduce:

```bash
# Ejecutar todas las pruebas con salida detallada
pytest -v
```

### Cobertura de las Pruebas:
* `tests/test_agent.py`: Verifica los 4 escenarios obligatorios (`NORMAL`, `AHORRO`, `PROTECCION`, `DATOS NO CONFIABLES`) y el resumen del clúster.
* `tests/test_data_quality.py`: Valida la detección de campos faltantes, valores nulos, lecturas fuera de rango físico y contradicciones cruzadas.
* `tests/test_integration.py`: Comprueba la **Única Fuente de Verdad** entre CSV, JSON, logs, el agente y el dashboard.
* `tests/test_mapreduce.py`: Verifica matemáticamente las etapas de Map, Shuffle y Reduce.
* `tests/test_negative.py`: Pruebas negativas con entradas corruptas, tipos de datos incompatibles y valores extremos.

---

## 📁 5. Estructura del Repositorio

```text
/mnt/c/Proyecto HPC-ECO/
├── app.py                  # Aplicación web interactiva en Streamlit (12 vistas)
├── agent.py                # Clase EcoHpcAgent y ciclo cognitivo formal
├── rules.py                # Estados, acciones, umbrales y motor de reglas determinista
├── data_quality.py         # Filtro de Veracidad y auditoría de límites físicos
├── mapreduce_demo.py       # Algoritmo didáctico MapReduce en Python puro
├── simulator.py            # Generador y exportador de telemetría multi-formato
├── requirements.txt        # Dependencias mínimas del proyecto (pandas, streamlit, pytest)
├── pytest.ini              # Configuración del entorno de pruebas unitarias
├── .gitignore              # Exclusiones de Git (.venv, __pycache__, etc.)
│
├── data/                   # Datasets centralizados (Única Fuente de Verdad)
│   ├── telemetry.csv       # Formato Estructurado
│   ├── telemetry.json      # Formato Semiestructurado
│   └── logs.txt            # Formato No Estructurado (syslog/IPMI)
│
├── tests/                  # Suite de 24 pruebas automatizadas
│   ├── test_agent.py
│   ├── test_data_quality.py
│   ├── test_integration.py
│   ├── test_mapreduce.py
│   └── test_negative.py
│
└── docs/                   # Documentación académica y preparación de defensa
    ├── TP_ECO_HPC.md       # Informe académico completo del Trabajo Práctico
    ├── DEFENSA_ORAL.md     # Guía obligatoria de estudio para la defensa en 1 jornada
    ├── ARQUITECTURA.md     # Especificación técnica del prototipo vs escala conceptual
    └── FUENTES.md          # Registro formal de fuentes oficiales (InfoLEG, AAIP, etc.)
```

---

## 🎙️ 6. Guía Rápida para la Exposición Oral (Modo Demo)

La aplicación web cuenta con una sección dedicada: **"2. Modo Demo (Exposición Oral)"**, estructurada en 5 pasos secuenciales para exponer el trabajo en **3 a 5 minutos** sin necesidad de navegar múltiples menús:

1. **Paso 1 (Operación Nominal):** Muestra `GPU-01` en régimen normal (62 °C, 350 W, 70% uso) → Decisión: `MANTENER`.
2. **Paso 2 (Oportunidad de Ahorro):** Muestra `GPU-04` subutilizada (14% uso) disipando 380 W innecesarios → Decisión: `AHORRAR` (modulación DVFS de reloj).
3. **Paso 3 (Protección Crítica):** Muestra `GPU-07` bajo carga extrema (89 °C, 720 W, 97% uso) → Decisión: `PROTEGER` (refrigeración forzada al 100% y power-capping).
4. **Paso 4 (Control de Veracidad):** Muestra `GPU-12` con sensor averiado (150 °C, 10 W, 0% uso) → Decisión: `REVISAR SENSOR` (rechaza actuar a ciegas, estado `DATOS NO CONFIABLES`).
5. **Paso 5 (Analítica Batch MapReduce):** Ejecuta la consolidación histórica calculando el promedio de potencia y los kWh totales acumulados por cada GPU.

Para repasar las posibles preguntas de la mesa evaluadora con respuestas de dos niveles (simple y técnico), consulta [docs/DEFENSA_ORAL.md](docs/DEFENSA_ORAL.md).

---

## ⚖️ 7. Consideraciones Legales y Éticas (Ley N.º 25.326)

Conforme a la **Ley Nacional N.º 25.326 de Protección de los Datos Personales** de la República Argentina y las pautas de la **Resolución AAIP 47/2018**:
* La telemetría pura de máquina (`M2M`) no constituye per se un dato personal.
* Sin embargo, cuando la telemetría se vincula a través del planificador de tareas (*SLURM*) con el legajo del usuario, el script y la franja horaria, adquiere carácter de **dato personal indirecto** al permitir perfilar la actividad o inferir líneas de investigación protegidas.
* ECO-HPC aplica el principio de **Minimización de Datos (Art. 4)**: el agente supervisor procesa únicamente identificadores técnicos de hardware, disociando de forma absoluta la identidad del usuario del bucle de control.
