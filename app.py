"""
app.py - ECO-HPC: Agente Supervisor de Eficiencia Energética para un entorno HPC
-------------------------------------------------------------------------------
Trabajo Práctico Integrador: "Las 5 V del Big Data como infraestructura de alimentación
para sistemas de Inteligencia Artificial".
Observatorio: IA + HARDWARE + COMPUTACIÓN DE ALTO RENDIMIENTO (HPC) + SOSTENIBILIDAD AMBIENTAL
"""

import json
import os
import pandas as pd
import streamlit as st

from agent import EcoHpcAgent, AgentDecision
from data_quality import DataQualityAuditor
from mapreduce_demo import execute_mapreduce
from rules import AgentAction, AgentState, RuleThresholds
from simulator import generate_baseline_telemetry, generate_historical_batch, export_datasets


# ==============================================================================
# CONFIGURACIÓN DE PÁGINA STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="ECO-HPC — Agente Supervisor de Eficiencia Energética",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilos CSS profesionales y académicos (sin sobrecarga visual)
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.2rem;
    }
    .badge-simulated {
        background-color: #f1f5f9;
        color: #475569;
        font-size: 0.75rem;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        border: 1px solid #cbd5e1;
        font-weight: 600;
    }
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    .decision-box-normal {
        border-left: 6px solid #10b981;
        background-color: #f0fdf4;
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 0.8rem;
    }
    .decision-box-ahorro {
        border-left: 6px solid #0284c7;
        background-color: #f0f9ff;
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 0.8rem;
    }
    .decision-box-proteccion {
        border-left: 6px solid #ef4444;
        background-color: #fef2f2;
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 0.8rem;
    }
    .decision-box-anomalia {
        border-left: 6px solid #8b5cf6;
        background-color: #faf5ff;
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 0.8rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# GESTIÓN CENTRALIZADA DE ESTADO Y DATOS (SINGLE SOURCE OF TRUTH)
# ==============================================================================
@st.cache_data(show_spinner=False)
def load_centralized_data():
    """Carga los datasets centralizados o los genera si no existen."""
    csv_path = os.path.join("data", "telemetry.csv")
    json_path = os.path.join("data", "telemetry.json")
    logs_path = os.path.join("data", "logs.txt")

    if not (os.path.exists(csv_path) and os.path.exists(json_path) and os.path.exists(logs_path)):
        export_datasets("data")

    df = pd.read_csv(csv_path)
    with open(json_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)
    with open(logs_path, "r", encoding="utf-8") as f:
        logs_lines = f.readlines()

    return df, json_data, logs_lines


if "agent_instance" not in st.session_state:
    st.session_state.agent_instance = EcoHpcAgent()

agent: EcoHpcAgent = st.session_state.agent_instance
df_historical, json_data, logs_lines = load_centralized_data()

# Tomar la última instantánea temporal para el estado actual de las 16 GPUs
latest_timestamp = df_historical["timestamp"].max()
df_current = df_historical[df_historical["timestamp"] == latest_timestamp].copy()
current_telemetry = df_current.to_dict(orient="records")

# Procesamiento centralizado del cluster mediante el agente
current_decisions = agent.process_cluster(current_telemetry)
cluster_summary = agent.get_cluster_summary(current_decisions)


# ==============================================================================
# BARRA LATERAL (NAVEGACIÓN Y CONTROLES)
# ==============================================================================
st.sidebar.markdown("### ⚡ **ECO-HPC**")
st.sidebar.markdown(
    "<span class='badge-simulated'>PROTOTIPO HPC · 16 GPUs SIMULADAS</span>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

menu_option = st.sidebar.radio(
    "Navegación del Proyecto:",
    [
        "1. Inicio & Presentación",
        "2. Modo Demo (Exposición Oral)",
        "3. Dashboard General",
        "4. Telemetría de GPUs",
        "5. Pantalla del Agente (Decisión)",
        "6. Las 5 V del Big Data",
        "7. Calidad de Datos & Veracidad",
        "8. Demostración MapReduce",
        "9. Marco PEAS & Ficha Técnica",
        "10. Arquitectura (Prototipo vs Escala)",
        "11. Sostenibilidad & NoSQL & Ley 25.326",
        "12. Fuentes & Evidencia Académica",
    ],
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Estado General del Agente:**")
st.sidebar.info(f"**{cluster_summary['general_status']}**")
st.sidebar.caption(
    f"Intervenciones: {cluster_summary['interventions_count']} | Ahorro: ~{cluster_summary['simulated_savings_kwh']} kWh"
)

if st.sidebar.button("🔄 Regenerar Telemetría / Reset"):
    export_datasets("data")
    st.cache_data.clear()
    agent.reset_state()
    st.rerun()


# ==============================================================================
# VISTA 1: INICIO & PRESENTACIÓN
# ==============================================================================
if menu_option == "1. Inicio & Presentación":
    st.markdown("<h1 class='main-title'>ECO-HPC — Agente Supervisor de Eficiencia Energética</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Trabajo Práctico Integrador: Las 5 V del Big Data como infraestructura de alimentación para sistemas de IA</p>", unsafe_allow_html=True)

    col_obs1, col_obs2 = st.columns([3, 2])
    with col_obs1:
        st.markdown(
            """
            ### Observatorio Académico
            **IA + HARDWARE + COMPUTACIÓN DE ALTO RENDIMIENTO (HPC) + SOSTENIBILIDAD AMBIENTAL**

            Este proyecto demuestra de manera integrada cómo los flujos continuos de telemetría de hardware
            (Big Data M2M/IoT) actúan como la infraestructura de sensado y percepción que alimenta a un
            **Agente Inteligente Basado en Reglas**, cuyo objetivo es maximizar la eficiencia energética y garantizar
            la seguridad térmica en un clúster de cómputo para Inteligencia Artificial.

            #### Problema Técnico Central
            El entrenamiento y la inferencia de modelos masivos de IA demandan clústeres masivos de aceleradores GPU.
            Estos dispositivos:
            - **Consumen volúmenes masivos de energía** eléctrica (cientos de kilovatios/megavatios).
            - **Generan calor extremo**, requiriendo disipación térmica activa y refrigeración forzada.
            - **Presentan variabilidad de utilización** (períodos de subutilización o *idle* manteniendo frecuencias altas).
            - **Sufren derivas o anomalías en sus sensores**, que no deben desencadenar acciones erróneas.
            """
        )

        st.info(
            """
            **Pregunta central que responde el agente ECO-HPC:**
            - ¿Qué está ocurriendo en el hardware?
            - ¿En qué estado se encuentra la GPU?
            - ¿Qué decisión corresponde?
            - ¿Por qué? (Justificación técnica)
            - ¿Qué acción se recomienda o simula?
            """
        )

    with col_obs2:
        st.markdown("### Escala y Transparencia Técnica")
        st.markdown(
            """
            | Dimensión | Definición del Proyecto |
            | :--- | :--- |
            | **Escala Conceptual** | Clúster HPC de hasta **1.024 GPUs** |
            | **Escala del Prototipo** | **16 GPUs simuladas** en 4 nodos |
            | **Tipo de Agente** | Reactivo con Estado Interno (Reglas) |
            | **Actuadores** | **SIMULADOS** (DVFS, cooling, SLURM) |
            | **Hardware Físico** | **SIMULADO** (sin control de fierros reales) |
            | **Paradigma Batch** | **MapReduce** didáctico en Python |
            | **Marco Legal** | **Ley 25.326** y Res. AAIP 47/2018 |
            """
        )

        st.warning(
            "⚠️ **Aclaración Metodológica:** Las acciones del prototipo son estrictamente simuladas. "
            "No se actúa sobre hardware físico real. La escala de 1.024 GPUs es un supuesto conceptual de dimensionamiento."
        )


# ==============================================================================
# VISTA 2: MODO DEMO (EXPOSICIÓN ORAL EN 3-5 MINUTOS)
# ==============================================================================
elif menu_option == "2. Modo Demo (Exposición Oral)":
    st.markdown("<h1 class='main-title'>🎙️ Modo Demostración de Exposición Oral</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Secuencia interactiva de 5 pasos diseñada para la defensa oral ante el tribunal evaluador</p>", unsafe_allow_html=True)

    demo_step = st.radio(
        "Seleccioná el Escenario de la Exposición:",
        [
            "Paso 1: Sistema Normal (Operación Nominal)",
            "Paso 2: Oportunidad de Ahorro (Subutilización con Alto Consumo)",
            "Paso 3: Protección Crítica (Temperatura Elevada y Sobrecarga)",
            "Paso 4: Veracidad y Detección de Anomalías (Fallo de Sensor)",
            "Paso 5: Procesamiento Batch con MapReduce (Cálculo Histórico)",
        ],
        horizontal=True,
    )

    st.markdown("---")

    if "Paso 1" in demo_step:
        st.subheader("Paso 1 — Estado Normal: Operación Balanceada")
        st.markdown(
            "> *\"Este es nuestro entorno HPC operando en condiciones nominales. Los sensores reportan parámetros térmicos y de potencia dentro de la envolvente de diseño.\"*"
        )
        sample = next((d for d in current_decisions if d.gpu_id == "GPU-01"), current_decisions[0])
        col1, col2, col3 = st.columns([1, 1, 2])
        col1.metric("GPU Evaluada", sample.gpu_id)
        col1.metric("Temperatura", f"{sample.perceptions['temperature']} °C")
        col2.metric("Potencia Eléctrica", f"{sample.perceptions['power_w']} W")
        col2.metric("Utilización de Cómputo", f"{sample.perceptions['utilization']} %")

        with col3:
            st.markdown(
                f"""
                <div class='decision-box-normal'>
                    <h4>ESTADO INTERNO: {sample.state.value}</h4>
                    <p><b>Decisión:</b> {sample.action.value}</p>
                    <p><b>¿Qué está ocurriendo?</b> {sample.what_is_happening()}</p>
                    <p><b>Motivo:</b> {sample.reason}</p>
                    <p><b>Acción Simulada:</b> {sample.action_details}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    elif "Paso 2" in demo_step:
        st.subheader("Paso 2 — Estado Ahorro: Oportunidad de Eficiencia Energética")
        st.markdown(
            "> *\"Aquí el agente detecta una ineficiencia energética: la GPU está subutilizada (ej. esperando I/O o trabajo concluido), pero continúa disipando 380 W con reloj elevado. El agente decide reducir frecuencia.\"*"
        )
        sample = next((d for d in current_decisions if d.gpu_id == "GPU-04"), current_decisions[0])
        col1, col2, col3 = st.columns([1, 1, 2])
        col1.metric("GPU Evaluada", sample.gpu_id)
        col1.metric("Temperatura", f"{sample.perceptions['temperature']} °C", delta="-12 °C (Segura)")
        col2.metric("Potencia Eléctrica", f"{sample.perceptions['power_w']} W", delta="Elevada para carga baja", delta_color="inverse")
        col2.metric("Utilización de Cómputo", f"{sample.perceptions['utilization']} %", delta="Subutilizada", delta_color="inverse")

        with col3:
            st.markdown(
                f"""
                <div class='decision-box-ahorro'>
                    <h4>ESTADO INTERNO: {sample.state.value}</h4>
                    <p><b>Decisión:</b> {sample.action.value}</p>
                    <p><b>¿Qué está ocurriendo?</b> {sample.what_is_happening()}</p>
                    <p><b>Motivo:</b> {sample.reason}</p>
                    <p><b>Acción Simulada:</b> {sample.action_details}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    elif "Paso 3" in demo_step:
        st.subheader("Paso 3 — Estado Protección: Alerta Térmica y Estrés de Hardware")
        st.markdown(
            "> *\"Durante un entrenamiento intensivo de LLM, la temperatura trepa a 89 °C superando el umbral crítico de 85 °C y el consumo alcanza 720 W. El agente activa protección inmediata para preservar el hardware.\"*"
        )
        sample = next((d for d in current_decisions if d.gpu_id == "GPU-07"), current_decisions[0])
        col1, col2, col3 = st.columns([1, 1, 2])
        col1.metric("GPU Evaluada", sample.gpu_id)
        col1.metric("Temperatura", f"{sample.perceptions['temperature']} °C", delta="CRÍTICA (>85°C)", delta_color="inverse")
        col2.metric("Potencia Eléctrica", f"{sample.perceptions['power_w']} W", delta="PICO EXTREMO", delta_color="inverse")
        col2.metric("Utilización de Cómputo", f"{sample.perceptions['utilization']} %", delta="97% (Saturación)")

        with col3:
            st.markdown(
                f"""
                <div class='decision-box-proteccion'>
                    <h4>ESTADO INTERNO: {sample.state.value}</h4>
                    <p><b>Decisión:</b> {sample.action.value}</p>
                    <p><b>¿Qué está ocurriendo?</b> {sample.what_is_happening()}</p>
                    <p><b>Motivo:</b> {sample.reason}</p>
                    <p><b>Acción Simulada:</b> {sample.action_details}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    elif "Paso 4" in demo_step:
        st.subheader("Paso 4 — Veracidad: Rechazo de Percepciones Anómalas o Inconsistentes")
        st.markdown(
            "> *\"Demostración de la V de Veracidad. El sensor reporta 150 °C pero con 10 W de consumo y 0% de uso. Es físicamente inconsistente. Una percepción no es una orden: el agente no apaga el servidor a ciegas, sino que aísla el dato y marca DATOS NO CONFIABLES.\"*"
        )
        sample = next((d for d in current_decisions if d.gpu_id == "GPU-12"), current_decisions[0])
        col1, col2, col3 = st.columns([1, 1, 2])
        col1.metric("GPU Evaluada", sample.gpu_id)
        col1.metric("Temperatura", f"{sample.perceptions['temperature']} °C", delta="ANOMALÍA FÍSICA", delta_color="inverse")
        col2.metric("Potencia Eléctrica", f"{sample.perceptions['power_w']} W", delta="Inconsistente con T", delta_color="inverse")
        col2.metric("Utilización", f"{sample.perceptions['utilization']} %")

        with col3:
            st.markdown(
                f"""
                <div class='decision-box-anomalia'>
                    <h4>ESTADO INTERNO: {sample.state.value}</h4>
                    <p><b>Decisión:</b> {sample.action.value}</p>
                    <p><b>¿Qué está ocurriendo?</b> {sample.what_is_happening()}</p>
                    <p><b>Motivo:</b> {sample.reason}</p>
                    <p><b>Acción Simulada:</b> {sample.action_details}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    elif "Paso 5" in demo_step:
        st.subheader("Paso 5 — MapReduce: Agregación Batch para Análisis Histórico")
        st.markdown(
            "> *\"Para la V de Velocidad, mientras el agente actúa en baja latencia, el histórico se procesa en Batch mediante MapReduce para calcular la energía total y perfiles de consumo medio por GPU.\"*"
        )
        mr_results = execute_mapreduce(df_historical.to_dict(orient="records"))
        st.write(f"**Registros históricos procesados:** {mr_results['input_records_count']} lecturas consolidadas.")

        mr_table = pd.DataFrame(list(mr_results["reduce_results"].values()))
        st.dataframe(
            mr_table[
                [
                    "gpu_id",
                    "valid_samples",
                    "avg_power_w",
                    "max_temperature_c",
                    "avg_utilization_pct",
                    "total_energy_kwh",
                    "operational_profile",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )


# ==============================================================================
# VISTA 3: DASHBOARD GENERAL
# ==============================================================================
elif menu_option == "3. Dashboard General":
    st.markdown("<h1 class='main-title'>📊 Dashboard del Clúster HPC</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Monitoreo agregado y telemetría en tiempo real del clúster de aceleradores</p>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("GPUs Simuladas", cluster_summary["total_gpus"], help="16 GPUs distribuidas en 4 nodos de cómputo")
    col2.metric("Temp. Promedio", f"{cluster_summary['avg_temperature']} °C", help="Promedio de lecturas térmicas válidas")
    col3.metric("Consumo Total", f"{cluster_summary['total_power_w']} W", help="Potencia total instantánea disipada por el clúster")
    col4.metric("Utilización Media", f"{cluster_summary['avg_utilization']} %", help="Carga de cálculo promedio de los núcleos de IA")
    col5.metric("Ahorro Acumulado", f"{cluster_summary['simulated_savings_kwh']} kWh", help="Energía eléctrica ahorrada por intervenciones del agente")

    st.markdown("---")

    col_chart1, col_chart2 = st.columns([3, 2])
    with col_chart1:
        st.markdown("#### Distribución de Estados del Agente en el Clúster")
        states_df = pd.DataFrame(
            [{"Estado": k, "Cantidad de GPUs": v} for k, v in cluster_summary["states_count"].items()]
        )
        st.bar_chart(states_df.set_index("Estado"), color="#0284c7")

    with col_chart2:
        st.markdown("#### Acciones Operativas Simuladas")
        actions_df = pd.DataFrame(
            [{"Acción": k, "Frecuencia": v} for k, v in cluster_summary["actions_count"].items()]
        )
        st.dataframe(actions_df, hide_index=True, use_container_width=True)

    st.markdown("---")
    st.markdown("#### Vista Rápida por Nodo de Cómputo")
    node_cols = st.columns(4)
    for idx, node_id in enumerate(["node-01", "node-02", "node-03", "node-04"]):
        node_gpus = [d for d in current_decisions if d.perceptions.get("node") == node_id]
        with node_cols[idx]:
            st.markdown(f"**{node_id.upper()}** (4 GPUs)")
            for g in node_gpus:
                temp_disp = f"{g.perceptions.get('temperature')}°C" if g.perceptions.get('temperature') else "ERR"
                st.caption(f"{g.gpu_id}: **{g.state.value}** ({temp_disp}, {g.perceptions.get('power_w')}W)")


# ==============================================================================
# VISTA 4: TELEMETRÍA DE GPUS
# ==============================================================================
elif menu_option == "4. Telemetría de GPUs":
    st.markdown("<h1 class='main-title'>📡 Percepciones de Telemetría de GPUs</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Datos sensoriales recopilados por M2M / IoT desde los nodos de cómputo</p>", unsafe_allow_html=True)

    # Conversión estructurada a DataFrame
    table_rows = []
    for d in current_decisions:
        p = d.perceptions
        table_rows.append(
            {
                "GPU": d.gpu_id,
                "Nodo": p.get("node"),
                "Temp (°C)": p.get("temperature"),
                "Potencia (W)": p.get("power_w"),
                "Utilización (%)": p.get("utilization"),
                "Reloj (MHz)": p.get("frequency"),
                "Cooling (%)": p.get("cooling"),
                "Carga de Trabajo": p.get("job_status"),
                "Estado Agente": d.state.value,
                "Decisión": d.action.value,
            }
        )
    df_table = pd.DataFrame(table_rows)

    st.dataframe(
        df_table.style.map(
            lambda val: "background-color: #fef2f2; color: #991b1b; font-weight: bold;"
            if val == "PROTECCION"
            else (
                "background-color: #f0f9ff; color: #075985; font-weight: bold;"
                if val == "AHORRO"
                else (
                    "background-color: #faf5ff; color: #581c87; font-weight: bold;"
                    if val == "DATOS NO CONFIABLES"
                    else ""
                )
            ),
            subset=["Estado Agente"],
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")
    st.markdown("#### Gráficos de Correlación Térmica y de Consumo")
    valid_plot_df = df_table.dropna(subset=["Temp (°C)", "Potencia (W)", "Utilización (%)"]).copy()
    valid_plot_df = valid_plot_df[valid_plot_df["Temp (°C)"] < 120]  # Excluir anomalía para gráfico limpio

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.scatter_chart(
            valid_plot_df,
            x="Utilización (%)",
            y="Potencia (W)",
            color="Estado Agente",
        )
        st.caption("Relación Utilización vs Potencia: Muestra GPUs en subutilización con alto consumo (cuadrante Ahorro).")
    with col_g2:
        st.scatter_chart(
            valid_plot_df,
            x="Potencia (W)",
            y="Temp (°C)",
            color="Estado Agente",
        )
        st.caption("Relación Potencia vs Temperatura: Muestra el punto crítico donde la GPU entra en Protección.")


# ==============================================================================
# VISTA 5: PANTALLA DEL AGENTE (DECISIÓN Y CICLO COGNITIVO)
# ==============================================================================
elif menu_option == "5. Pantalla del Agente (Decisión)":
    st.markdown("<h1 class='main-title'>🧠 Pantalla del Agente ECO-HPC</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Ciclo cognitivo completo: Percepciones → Control de Calidad → Estado Interno → Decisión → Acción Simulada</p>", unsafe_allow_html=True)

    gpu_options = [d.gpu_id for d in current_decisions]
    selected_gpu = st.selectbox("Seleccionar GPU para inspeccionar el ciclo del agente:", gpu_options, index=6)

    chosen_decision = next(d for d in current_decisions if d.gpu_id == selected_gpu)
    p = chosen_decision.perceptions

    st.markdown("---")

    col_flow1, col_flow2, col_flow3 = st.columns([1, 1, 2])

    with col_flow1:
        st.markdown("#### 1. Percepciones (Sensores)")
        st.write(f"**GPU:** `{chosen_decision.gpu_id}`")
        st.write(f"**Nodo:** `{p.get('node')}`")
        st.write(f"**Temperatura:** `{p.get('temperature')} °C`")
        st.write(f"**Potencia:** `{p.get('power_w')} W`")
        st.write(f"**Utilización:** `{p.get('utilization')} %`")
        st.write(f"**Frecuencia:** `{p.get('frequency')} MHz`")
        st.write(f"**Cooling Fan:** `{p.get('cooling')} %`")
        st.write(f"**Trabajo:** `{p.get('job_status')}`")

    with col_flow2:
        st.markdown("#### 2. Control de Calidad")
        if chosen_decision.is_data_valid:
            st.success("✅ **Lectura Válida**")
            st.caption("Superó los rangos físicos y filtros de consistencia cruzada.")
        else:
            st.error("❌ **Anomalía Detectada**")
            for iss in chosen_decision.quality_issues:
                st.caption(f"• {iss}")

        st.markdown("#### 3. Regla Aplicada")
        st.code(chosen_decision.rule_id, language="text")

    with col_flow3:
        st.markdown("#### 4. Estado, Decisión y Acción")
        st_val = chosen_decision.state.value

        box_class = (
            "decision-box-proteccion"
            if st_val == "PROTECCION"
            else (
                "decision-box-ahorro"
                if st_val == "AHORRO"
                else (
                    "decision-box-anomalia"
                    if st_val == "DATOS NO CONFIABLES"
                    else "decision-box-normal"
                )
            )
        )

        st.markdown(
            f"""
            <div class='{box_class}'>
                <h3 style='margin-top:0;'>ESTADO INTERNO: {chosen_decision.state.value}</h3>
                <p><b>DECISIÓN DEL AGENTE:</b> <span style='font-size:1.15rem; font-weight:bold;'>{chosen_decision.action.value}</span></p>
                <hr style='margin: 0.5rem 0;'>
                <p><b>¿Qué está ocurriendo?</b><br>{chosen_decision.what_is_happening()}</p>
                <p><b>¿Por qué? (Justificación Técnica):</b><br>{chosen_decision.reason}</p>
                <p><b>Acción Operativa Simulada:</b><br>{chosen_decision.action_details}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("#### Diagrama del Flujo Fundamental del Agente")
    st.code(
        """
        SENSORES (Telemetría cruda M2M)
           ↓
        PERCEPCIONES (Vector numérico tipado)
           ↓
        CONTROL DE CALIDAD (Filtro de veracidad de límites físicos e inconsistencias)
           ↓
        ESTADO INTERNO (Actualización de memoria y clasificación: NORMAL, AHORRO, PROTECCIÓN, ANOMALÍA)
           ↓
        DECISIÓN (Evaluación de reglas jerárquicas deterministas)
           ↓
        ACCIÓN SIMULADA (Recomendación operativa: MANTENER, AHORRAR, REFRIGERAR, PROTEGER)
        """,
        language="text",
    )


# ==============================================================================
# VISTA 6: LAS 5 V DEL BIG DATA
# ==============================================================================
elif menu_option == "6. Las 5 V del Big Data":
    st.markdown("<h1 class='main-title'>🌐 Las 5 V del Big Data en ECO-HPC</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Cómo las 5 dimensiones fundamentan la infraestructura de datos que alimenta a la Inteligencia Artificial</p>", unsafe_allow_html=True)

    tab_vol, tab_vel, tab_var, tab_ver, tab_val = st.tabs(
        ["1. Volumen", "2. Velocidad", "3. Variedad", "4. Veracidad", "5. Valor"]
    )

    with tab_vol:
        st.subheader("Volumen: Cálculo Pedagógico a Escala vs Prototipo")
        st.markdown(
            """
            Para comprender por qué la telemetría de un clúster HPC constituye un problema de Big Data,
            analizamos el **SUPUESTO CALCULADO DEL ESCENARIO** a escala conceptual:
            """
        )
        st.latex(
            r"\text{Volumen Diario} = N_{\text{GPU}} \times f_{\text{lecturas}} \times 86.400\,\frac{\text{seg}}{\text{día}} \times \text{Tamaño Registro}"
        )

        col_v1, col_v2 = st.columns(2)
        with col_v1:
            st.markdown(
                r"""
                **Escenario Conceptual de Referencia (1.024 GPUs):**
                - Cantidad de GPUs: **1.024**
                - Frecuencia de muestreo: **1 lectura / segundo** por GPU
                - Eventos por segundo: **1.024 registros/segundo**
                - Eventos diarios: $1.024 \times 86.400 = \mathbf{88.473.600}$ **registros/día**
                - Tamaño de registro crudo (JSON con metadata): **~250 bytes**
                - **Volumen diario estimado:** $\approx \mathbf{22,12\text{ GB/día}}$ sin comprimir.
                - **Volumen anual estimado:** $\approx \mathbf{8\text{ TB/año}}$ sólo en telemetría de aceleradores.
                """
            )
        with col_v2:
            st.markdown(
                """
                **Prototipo Pequeño ≠ Volumen Conceptual Pequeño:**
                - El prototipo opera intencionalmente con **16 GPUs simuladas** para garantizar
                  ejecución ligera, explicabilidad didáctica e interactividad fluida.
                - La arquitectura conceptual está diseñada para escalar horizontalmente hacia
                  millones de registros diarios.
                """
            )

    with tab_vel:
        st.subheader("Velocidad: Dualidad Baja Latencia vs Procesamiento Batch")
        st.markdown(
            """
            En un clúster HPC existen dos requerimientos temporales antagónicos y complementarios:

            1. **Baja Latencia (Streaming / Tiempo Real < 1-2 segundos):**
               - Necesaria para el **Agente Supervisor**: detección instantánea de picos térmicos,
                 riesgo de embalamiento térmico (*thermal runaway*) y derroche eléctrico.
               - El agente debe percibir y decidir en milisegundos.

            2. **Batch / Diferido (Horas / Días / Semanas):**
               - Procesamiento de series temporales históricas mediante **MapReduce**.
               - Cálculo de métricas consolidadas: consumo medio por trabajo, detección de derivas en sensores,
                 cálculo del PUE (Power Usage Effectiveness) y auditoría de sostenibilidad.
            """
        )

    with tab_var:
        st.subheader("Variedad: Datos Estructurados, Semiestructurados y No Estructurados")
        st.markdown("La telemetría HPC no proviene en un único formato homogéneo:")

        col_var1, col_var2, col_var3 = st.columns(3)
        with col_var1:
            st.markdown("##### Estructurados (CSV / Tablas)")
            st.caption("Series temporales con esquema estricto y tipos numéricos fijos:")
            st.dataframe(df_historical[["gpu_id", "temperature", "power_w", "utilization"]].head(5), hide_index=True)

        with col_var2:
            st.markdown("##### Semiestructurados (JSON)")
            st.caption("Objetos emitidos por APIs REST o exporters de DCGM con atributos flexibles:")
            st.json(json_data[0])

        with col_var3:
            st.markdown("##### No Estructurados (Logs)")
            st.caption("Líneas de syslog / dmesg / IPMI en texto plano:")
            st.text("\n".join([line.strip() for line in logs_lines[:5]]))

    with tab_ver:
        st.subheader("Veracidad: Limpieza, Filtros y Rechazo de Datos Sospechosos")
        st.markdown(
            """
            En entornos con miles de sensores de hardware ocurren fallos de medición, ruido electromagnético,
            derivas por temperatura del silicio y pérdida de paquetes.
            
            **Principio de Veracidad en ECO-HPC:**
            El agente jamás asume que todo dato recibido es verídico. Si una lectura viola leyes físicas
            (como 150 °C con 10 W de consumo) o contiene valores nulos, el sistema activa el estado
            **DATOS NO CONFIABLES** y rehúsa tomar decisiones erróneas sobre el hardware.
            """
        )

    with tab_val:
        st.subheader("Valor: De los Datos a la Sostenibilidad y Eficiencia")
        st.markdown(
            """
            El valor del Big Data no radica en acumular terabytes, sino en transformar percepciones en decisiones:

            ```text
            DATOS CRUDOS (Telemetría de potencia, temperatura y utilización)
                 ↓
            INFORMACIÓN (Identificación de GPUs subutilizadas o sobrecalentadas)
                 ↓
            DECISIÓN (Reglas deterministas del agente ECO-HPC)
                 ↓
            ACCIÓN (Reducción de reloj por DVFS o aumento de refrigeración)
                 ↓
            VALOR (Ahorro de energía en kWh, reducción de emisiones y prolongación de vida útil)
            ```
            """
        )


# ==============================================================================
# VISTA 7: CALIDAD DE DATOS & VERACIDAD
# ==============================================================================
elif menu_option == "7. Calidad de Datos & Veracidad":
    st.markdown("<h1 class='main-title'>🛡️ Auditoría de Calidad de Datos y Veracidad</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Detección sistemática de anomalías, datos faltantes y violaciones de leyes físicas</p>", unsafe_allow_html=True)

    batch_audit = DataQualityAuditor.audit_batch(df_historical.to_dict(orient="records"))

    col_q1, col_q2, col_q3, col_q4 = st.columns(4)
    col_q1.metric("Registros Totales", batch_audit["total_records"])
    col_q2.metric("Registros Válidos", batch_audit["valid_records"])
    col_q3.metric("Anomalías Detectadas", batch_audit["anomalous_records"], delta="Filtrados", delta_color="inverse")
    col_q4.metric("Tasa de Veracidad", f"{batch_audit['veracity_rate_pct']} %")

    st.markdown("---")
    st.subheader("Lista de Anomalías Registradas en el Dataset Centralizado")

    issues_unique = list(set(batch_audit["issues_list"]))
    for iss in issues_unique:
        st.warning(f"⚠️ {iss}")

    st.markdown("---")
    st.markdown(
        """
        #### Clasificación de Sesgos y Fallas en Telemetría de Hardware
        1. **Sesgo de Medición:** Diferencias en la calibración del conversor analógico-digital (ADC) del sensor térmico entre distintos fabricantes o lotes de GPUs.
        2. **Sesgo de Muestreo:** Nodos de cómputo que reportan con frecuencias dispares (ej. cada 1s vs cada 5s) debido a saturación de la red de gestión OOB (Out-of-band).
        3. **Deriva del Sensor (*Sensor Drift*):** Degradación física paulatina de los termistores por ciclos térmicos continuos, provocando lecturas que se desvían con el tiempo.
        """
    )


# ==============================================================================
# VISTA 8: DEMOSTRACIÓN MAPREDUCE
# ==============================================================================
elif menu_option == "8. Demostración MapReduce":
    st.markdown("<h1 class='main-title'>🔄 Demostración Didáctica de MapReduce</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Procesamiento Batch distribuido simulado en Python: Map → Shuffle → Reduce</p>", unsafe_allow_html=True)

    st.info(
        "💡 **Aclaración Académica:** Esta demostración implementa algorítmicamente el paradigma formal "
        "MapReduce (Dean & Ghemawat, 2004) en memoria local de Python. No requiere desplegar un clúster físico Hadoop."
    )

    mr_data = execute_mapreduce(df_historical.to_dict(orient="records"))

    col_mr1, col_mr2, col_mr3 = st.columns(3)
    col_mr1.metric("Registros de Entrada", mr_data["input_records_count"])
    col_mr2.metric("Pares Clave-Valor Mapped", mr_data["map_output_count"])
    col_mr3.metric("Claves Únicas Shuffled", mr_data["unique_keys_count"])

    st.markdown("---")

    step_mr = st.radio(
        "Explorar Etapa del Pipeline MapReduce:",
        ["1. Entrada de Datos", "2. Etapa MAP", "3. Etapa SHUFFLE & SORT", "4. Etapa REDUCE (Resultados)"],
        horizontal=True,
    )

    if "1. Entrada" in step_mr:
        st.markdown("##### Entrada de Datos (Lote Histórico de Telemetría)")
        st.dataframe(df_historical.head(10), use_container_width=True)

    elif "2. Etapa MAP" in step_mr:
        st.markdown("##### Etapa MAP: Emisión de Pares <Clave, Valor>")
        st.markdown(
            "Cada *Mapper* procesa un registro y emite la tupla: `<gpu_id, {power_w, temperature, count}>`"
        )
        sample_map = [
            {"Clave (GPU)": k, "Valor Emitido (Métricas)": str(v)} for k, v in mr_data["map_sample"]
        ]
        st.table(sample_map)

    elif "3. Etapa SHUFFLE" in step_mr:
        st.markdown("##### Etapa SHUFFLE & SORT: Agrupamiento por Clave")
        st.markdown(
            "La infraestructura agrupa todos los valores emitidos para cada GPU bajo una misma lista particionada:"
        )
        st.json(mr_data["shuffle_sample"])

    elif "4. Etapa REDUCE" in step_mr:
        st.markdown("##### Etapa REDUCE: Agregación Final")
        st.markdown(
            "Cada *Reducer* computa la potencia media, la temperatura pico y la energía acumulada por GPU:"
        )
        mr_df = pd.DataFrame(list(mr_data["reduce_results"].values()))
        st.dataframe(mr_df, use_container_width=True, hide_index=True)


# ==============================================================================
# VISTA 9: MARCO PEAS & FICHA TÉCNICA
# ==============================================================================
elif menu_option == "9. Marco PEAS & Ficha Técnica":
    st.markdown("<h1 class='main-title'>📋 Marco PEAS y Ficha Técnica del Agente</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Formalización según los estándares de Russell & Norvig para Agentes Inteligentes</p>", unsafe_allow_html=True)

    col_peas1, col_peas2 = st.columns(2)

    with col_peas1:
        st.markdown("### Tabla PEAS Formal")
        st.markdown(
            """
            | Componente PEAS | Descripción en ECO-HPC |
            | :--- | :--- |
            | **Performance**<br>*(Rendimiento)* | Maximizar la eficiencia energética (reducción de kWh y disipación) garantizando temperaturas seguras (<85°C) y cumplimiento de SLAs. |
            | **Environment**<br>*(Entorno)* | Clúster HPC con aceleradores GPU para cargas de Inteligencia Artificial (entrenamiento LLMs, inferencia). |
            | **Actuators**<br>*(Actuadores)* | Ajuste de frecuencia de reloj (DVFS), escalado de ventiladores/bombas de refrigeración y limitación de carga en SLURM (**SIMULADOS**). |
            | **Sensors**<br>*(Sensores)* | Telemetría M2M de temperatura (°C), potencia eléctrica (W), utilización (%), reloj (MHz) y estado de trabajo. |
            """
        )

    with col_peas2:
        st.markdown("### Ficha Técnica de ECO-HPC")
        st.markdown(
            """
            - **Nombre del Agente:** ECO-HPC Supervisor
            - **Tipo de Agente:** Reactivo basado en reglas con estado interno
            - **Entorno de Operación:** HPC / Data Center de Inteligencia Artificial
            - **Escala Conceptual:** Hasta 1.024 GPUs
            - **Escala de Prototipo:** 16 GPUs simuladas en 4 nodos
            - **Software Empleado:** Python 3.14, Streamlit, Pandas, Pytest
            - **Entrada de Datos:** CSV estructurado, JSON semiestructurado, logs de texto
            - **Salida:** Diagnóstico, estado del clúster, recomendación y acciones simuladas
            - **Limitaciones Declaradas:** No actúa sobre hardware real; umbrales configurados como parámetros de simulación.
            """
        )


# ==============================================================================
# VISTA 10: ARQUITECTURA (PROTOTIPO VS ESCALA)
# ==============================================================================
elif menu_option == "10. Arquitectura (Prototipo vs Escala)":
    st.markdown("<h1 class='main-title'>🏗️ Arquitectura del Sistema</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Comparativa explícita: Arquitectura implementada en el prototipo vs Arquitectura conceptual de producción a escala</p>", unsafe_allow_html=True)

    col_arch1, col_arch2 = st.columns(2)

    with col_arch1:
        st.markdown("### Arquitectura Implementada (Prototipo)")
        st.success("🟢 **IMPLEMENTADO EN ESTE REPOSITORIO**")
        st.code(
            """
            [SIMULADOR DE TELEMETRÍA] (simulator.py)
                    ↓
            [DATASETS LOCALES] (telemetry.csv / json / logs.txt)
                    ↓
            [CONTROL DE CALIDAD] (data_quality.py - Filtro Veracidad)
                    ↓
            [AGENTE ECO-HPC] (agent.py + rules.py)
                    ↓
            [DECISIÓN & ACCIÓN SIMULADA]
                    ↓
            [DASHBOARD WEB INTERACTIVO] (Streamlit app.py)
            """,
            language="text",
        )
        st.caption("Diseñada para simplicidad, transparencia, portabilidad y defensa oral en 1 jornada.")

    with col_arch2:
        st.markdown("### Arquitectura Conceptual (Producción a Escala)")
        st.info("🔵 **PROPUESTA CONCEPTUAL PARA 1.024 GPUs**")
        st.code(
            """
            [1.024 GPUs EN CLÚSTER HPC] (NVIDIA NVML / DCGM Exporter)
                    ↓
            [INGESTA DISTRIBUIDA] (Apache Kafka / Apache Pulsar - 1.024 rec/s)
                    ↓
            [STREAM PROCESSING] (Apache Flink / Spark Streaming < 1s)
                    ↓
            [ALMACENAMIENTO DISTRIBUIDO] (Base de Datos NoSQL Time-Series)
                    ↓
            [AGENTE DISTRIBUIDO] (Motor de Reglas + Interfaz SLURM / IPMI)
                    ↓
            [ACTUADORES REALES] (Driver GPU DVFS + Controladores Chillers)
            """,
            language="text",
        )
        st.caption("Propuesta conceptual que no requiere ser desplegada físicamente para cumplir el TP.")


# ==============================================================================
# VISTA 11: SOSTENIBILIDAD & NOSQL & LEY 25.326
# ==============================================================================
elif menu_option == "11. Sostenibilidad & NoSQL & Ley 25.326":
    st.markdown("<h1 class='main-title'>🌱 Sostenibilidad, NoSQL y Aspectos Legales</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Integración multidimensional de impacto ambiental, almacenamiento y privacidad de datos</p>", unsafe_allow_html=True)

    tab_sos, tab_nosql, tab_ley = st.tabs(["Sostenibilidad Ambiental", "Justificación NoSQL", "Ley Nacional N.º 25.326"])

    with tab_sos:
        st.subheader("Sostenibilidad Ambiental en HPC para IA")
        st.markdown(
            """
            El entrenamiento de modelos de lenguaje e inteligencia artificial consume megavatios-hora de energía.
            La relación entre IA, hardware y sostenibilidad en ECO-HPC se fundamenta en:

            1. **Evitar el Desperdicio en Reposo (*Idle Energy Waste*):**
               Cuando una GPU concluye un batch o espera transferencias de red, mantener el reloj a máxima
               frecuencia genera un consumo parásito innecesario. La acción **AHORRAR** reduce el consumo en ~40%.
            2. **Preservación Térmica y Ciclo de Vida del Silicio:**
               Operar continuamente a >85°C acelera la electromigración del silicio. La acción **PROTEGER**
               evita el recambio prematuro de hardware de alto costo ecológico y de manufactura.
            3. **Reducción de Huella de Carbono Simulada:**
               Cada kilovatio-hora ahorrado evita la emisión de gases de efecto invernadero según la matriz energética.
            """
        )

    with tab_nosql:
        st.subheader("Justificación Técnica de una Solución NoSQL para Producción a Escala")
        st.markdown(
            """
            ¿Por qué para 1.024 GPUs en producción se propone una base de datos **NoSQL** y no una relacional tradicional?

            - **Patrón de Escritura Intensivo (*Append-heavy write throughput*):** 1.024 inserciones por segundo,
              88.4 millones de registros diarios. Las bases relacionales tradicionales colapsan por bloqueo de transacciones ACID y mantenimiento de índices B-Tree.
            - **Modelo Time-Series / Wide-Column NoSQL (ej. InfluxDB, TimescaleDB o Apache Cassandra):**
              Estructura optimizada para series de tiempo, compresión por columnas y particionamiento por rangos temporales.
            - **Escalabilidad Horizontal:** Capacidad de agregar nodos de almacenamiento sin detener el clúster.
            - **Políticas de Retención (*TTL - Time To Live*):** Roll-up automático de datos de 1 segundo a promedios de 1 minuto tras 30 días.
            """
        )

    with tab_ley:
        st.subheader("Marco Legal: Ley N.º 25.326 de Protección de los Datos Personales (Argentina)")
        st.markdown(
            """
            **Pregunta Clave de Examen:** *¿Los datos de telemetría de una GPU son datos personales?*

            - **Respuesta Técnica Corta:** **No en su estado crudo, pero SÍ cuando se correlacionan.**
            - **Fundamento Legal:** La telemetría pura (temperatura 60°C, potencia 350W) es métrica de máquina (M2M).
              Sin embargo, según el **Art. 2 de la Ley 25.326**, es dato personal toda información referida a personas físicas determinadas o determinables.
              Si los logs del gestor de trabajos (SLURM) asocian:
              `USUARIO (Legajo/Nombre) + TRABAJO + HORARIO + GPU ASIGNADA`
              la telemetría permite inferir pautas de trabajo, productividad, horarios laborales o propiedad intelectual del investigador.

            #### Principios de Privacidad Aplicados a ECO-HPC:
            - **Minimización de Datos (Art. 4 Ley 25.326):** El agente supervisor sólo percibe identificadores de hardware (`GPU-01`, `nodo`), disociando por completo la identidad del usuario.
            - **Finalidad Específica:** Los datos energéticos se usan exclusivamente para optimización térmica y de consumo.
            - **Medidas de Seguridad (Res. AAIP 47/2018):** Control de acceso basado en roles (RBAC) y cifrado de canales de telemetría.
            """
        )


# ==============================================================================
# VISTA 12: FUENTES & EVIDENCIA ACADÉMICA
# ==============================================================================
elif menu_option == "12. Fuentes & Evidencia Académica":
    st.markdown("<h1 class='main-title'>📚 Fuentes y Evidencia Académica</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Registro riguroso de fuentes oficiales, bibliográficas y técnicas consultadas</p>", unsafe_allow_html=True)

    sources = [
        {
            "Fuente": "Ley N.º 25.326",
            "Título": "Protección de los Datos Personales (Texto Actualizado)",
            "Organización": "Honorable Congreso de la Nación Argentina / InfoLEG",
            "URL": "https://servicios.infoleg.gob.ar/infolegInternet/anexos/60000-64999/64790/norma.htm",
            "Dato que Respalda": "Definición de datos personales, principios de calidad, seguridad y confidencialidad en Argentina.",
        },
        {
            "Fuente": "Resolución 47/2018",
            "Título": "Medidas de Seguridad Recomendadas para el Tratamiento de Datos Personales",
            "Organización": "Agencia de Acceso a la Información Pública (AAIP)",
            "URL": "https://servicios.infoleg.gob.ar/infolegInternet/anexos/315000-319999/315998/norma.htm",
            "Dato que Respalda": "Estándares de seguridad técnica en medios informatizados para tratamiento de datos.",
        },
        {
            "Fuente": "Russell, S. & Norvig, P.",
            "Título": "Artificial Intelligence: A Modern Approach (4th Edition)",
            "Organización": "Pearson (2020)",
            "URL": "https://aima.cs.berkeley.edu/",
            "Dato que Respalda": "Definición formal del marco PEAS, agentes inteligentes reactivos y con estado interno.",
        },
        {
            "Fuente": "Dean, J. & Ghemawat, S.",
            "Título": "MapReduce: Simplified Data Processing on Large Clusters",
            "Organización": "Google / OSDI '04 (2004)",
            "URL": "https://research.google/pubs/pub62/",
            "Dato que Respalda": "Paradigma formal de procesamiento Map, Shuffle y Reduce para análisis masivo.",
        },
        {
            "Fuente": "NVIDIA Corporation",
            "Título": "NVIDIA Data Center GPU Manager (DCGM) & NVML API Documentation",
            "Organización": "NVIDIA Developer Documentation (2024)",
            "URL": "https://docs.nvidia.com/datacenter/dcgm/latest/",
            "Dato que Respalda": "Métricas industriales estándar de telemetría de GPU (temperatura, potencia, reloj, throttling).",
        },
        {
            "Fuente": "The Green500",
            "Título": "Green500 List - Top500 Supercomputers Energy Efficiency",
            "Organización": "TOP500.org (2024)",
            "URL": "https://www.top500.org/lists/green500/",
            "Dato que Respalda": "Métricas de eficiencia energética en supercómputo y cálculo de GFLOPS/Watt.",
        },
    ]

    st.table(pd.DataFrame(sources))


# ==============================================================================
# PIE DE PÁGINA COMÚN
# ==============================================================================
st.markdown("---")
st.caption(
    "ECO-HPC — Proyecto Integrador de Ciencia de Datos e Inteligencia Artificial | Observatorio HPC + IA + Sostenibilidad | Prototipo Académico Simulado"
)
