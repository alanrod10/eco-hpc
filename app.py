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

# Estilos CSS profesionales - TEMA CLARO Y ALTO CONTRASTE PARA PROYECTOR
st.markdown(
    """
    <style>
    /* Tipografía y jerarquía de alto contraste */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #0f172a;
    }
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.2rem;
        letter-spacing: -0.02em;
    }
    .sub-title {
        font-size: 1.15rem;
        color: #334155;
        margin-bottom: 1.4rem;
        font-weight: 500;
    }
    .section-header {
        font-size: 1.45rem;
        font-weight: 700;
        color: #0f4c81;
        margin-top: 1.2rem;
        margin-bottom: 0.6rem;
    }
    .badge-simulated {
        background-color: #f1f5f9;
        color: #1e293b;
        font-size: 0.85rem;
        padding: 0.3rem 0.6rem;
        border-radius: 6px;
        border: 2px solid #94a3b8;
        font-weight: 700;
        display: inline-block;
    }
    .badge-step {
        background-color: #0f4c81;
        color: #ffffff;
        font-size: 0.9rem;
        font-weight: 700;
        padding: 0.25rem 0.6rem;
        border-radius: 4px;
        display: inline-block;
        margin-bottom: 0.4rem;
    }

    /* Tarjetas de Métricas optimizadas para Proyector */
    .stMetric {
        background-color: #ffffff !important;
        border: 2px solid #cbd5e1 !important;
        border-radius: 10px !important;
        padding: 14px 18px !important;
        box-shadow: 0 2px 4px rgba(15, 23, 42, 0.05) !important;
    }
    .stMetric label {
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        color: #334155 !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        color: #0f172a !important;
    }

    /* Cajas de Decisión Semánticas con Alto Contraste */
    .decision-card {
        border-radius: 8px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.04);
        font-size: 1.05rem;
        line-height: 1.5;
    }
    .decision-card h3 {
        margin-top: 0;
        font-size: 1.4rem;
        font-weight: 800;
        margin-bottom: 0.6rem;
    }
    .decision-box-normal {
        border: 2px solid #86efac;
        border-left: 10px solid #16a34a;
        background-color: #f0fdf4;
        color: #14532d;
    }
    .decision-box-ahorro {
        border: 2px solid #fde68a;
        border-left: 10px solid #d97706;
        background-color: #fffbeb;
        color: #78350f;
    }
    .decision-box-proteccion {
        border: 2px solid #fca5a5;
        border-left: 10px solid #dc2626;
        background-color: #fef2f2;
        color: #7f1d1d;
    }
    .decision-box-anomalia {
        border: 2px solid #d8b4fe;
        border-left: 10px solid #9333ea;
        background-color: #faf5ff;
        color: #581c87;
    }

    /* Flujo visual del agente */
    .flow-box {
        background-color: #ffffff;
        border: 2px solid #cbd5e1;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .flow-box h4 {
        margin-top: 0;
        color: #0f4c81;
        font-weight: 700;
        font-size: 1.15rem;
    }

    /* Cajas pedagógicas PEAS */
    .peas-card {
        background-color: #ffffff;
        border: 2px solid #e2e8f0;
        border-top: 6px solid #0f4c81;
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }
    .peas-card h3 {
        color: #0f4c81;
        font-weight: 800;
        margin-top: 0;
        margin-bottom: 0.5rem;
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
        "2. Demostración",
        "3. Dashboard General",
        "4. Telemetría de GPUs",
        "5. Agente (Decisión & Ciclo)",
        "6. Las 5 V del Big Data",
        "7. Calidad de Datos & Veracidad",
        "8. MapReduce Histórico",
        "9. Marco PEAS & Ficha Técnica",
        "10. Arquitectura (Prototipo vs Escala)",
        "11. Sostenibilidad & NoSQL & Ley 25.326",
        "12. Fuentes & Evidencia Académica",
    ],
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Estado Global del Agente:**")
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
    st.markdown("<p class='sub-title'>Trabajo Práctico Integrador: Las 5 V del Big Data como infraestructura de alimentación para sistemas de Inteligencia Artificial</p>", unsafe_allow_html=True)

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
            **Preguntas centrales que responde el agente ECO-HPC:**
            1. **¿Qué está ocurriendo?** Diagnóstico del estado térmico, eléctrico y de carga.
            2. **¿En qué estado se encuentra la GPU?** Normal, Ahorro, Protección o Datos No Confiables.
            3. **¿Qué decisión corresponde?** Mantener, Ahorrar (DVFS), Proteger o Revisar sensor.
            4. **¿Por qué?** Justificación técnica determinista basada en reglas.
            5. **¿Qué acción se recomienda o simula?** Ajuste de reloj, control térmico o cuotas de cómputo.
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
            | **Hardware Físico** | **SIMULADO** (sin control de hardware físico) |
            | **Paradigma Batch** | **MapReduce** didáctico en Python |
            | **Marco Legal** | **Ley 25.326** y Res. AAIP 47/2018 |
            """
        )

        st.warning(
            "⚠️ **Aclaración Metodológica:** Las acciones del prototipo son estrictamente simuladas. "
            "No se actúa sobre hardware físico real. La escala de 1.024 GPUs es un supuesto conceptual de dimensionamiento."
        )


# ==============================================================================
# VISTA 2: DEMOSTRACIÓN (5 PASOS)
# ==============================================================================
elif menu_option == "2. Demostración":
    st.markdown("<h1 class='main-title'>⚡ DEMOSTRACIÓN DEL SISTEMA</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Secuencia interactiva en 5 pasos para demostrar el funcionamiento del sistema en vivo</p>", unsafe_allow_html=True)

    demo_step = st.radio(
        "Seleccioná el Escenario a Demostrar:",
        [
            "01 — NORMAL",
            "02 — AHORRO",
            "03 — PROTECCIÓN",
            "04 — ANOMALÍA",
            "05 — MAPREDUCE",
        ],
        horizontal=True,
    )

    st.markdown("---")

    if "01" in demo_step:
        st.markdown("<span class='badge-step'>01 — NORMAL</span> <span class='section-header'>Operación Normal: El sistema está estable</span>", unsafe_allow_html=True)
        st.markdown(
            "**Explicación breve:** Las condiciones térmicas y eléctricas operan dentro de la envolvente de diseño. El agente valida los datos y decide mantener la operación."
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
                <div class='decision-card decision-box-normal'>
                    <h3>ESTADO: {sample.state.value}</h3>
                    <p><b>DECISIÓN:</b> {sample.action.value}</p>
                    <p><b>ACCIÓN SIMULADA:</b> {sample.action_details}</p>
                    <p><b>MOTIVO:</b> {sample.reason}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    elif "02" in demo_step:
        st.markdown("<span class='badge-step'>02 — AHORRO</span> <span class='section-header'>Ahorro: Detección de ineficiencia energética</span>", unsafe_allow_html=True)
        st.markdown(
            "**Explicación breve:** La GPU disipa 380 W pero su uso es de solo 14% (espera de I/O). El agente detecta la ineficiencia y modula el reloj por DVFS para ahorrar ~152 W."
        )
        sample = next((d for d in current_decisions if d.gpu_id == "GPU-04"), current_decisions[0])
        col1, col2, col3 = st.columns([1, 1, 2])
        col1.metric("GPU Evaluada", sample.gpu_id)
        col1.metric("Temperatura", f"{sample.perceptions['temperature']} °C", delta="-12 °C (Segura)")
        col2.metric("Potencia Eléctrica", f"{sample.perceptions['power_w']} W", delta="Elevada para carga baja", delta_color="inverse")
        col2.metric("Utilización de Cómputo", f"{sample.perceptions['utilization']} %", delta="14% (Subutilizada)", delta_color="inverse")

        with col3:
            st.markdown(
                f"""
                <div class='decision-card decision-box-ahorro'>
                    <h3>ESTADO: {sample.state.value}</h3>
                    <p><b>DECISIÓN:</b> {sample.action.value}</p>
                    <p><b>ACCIÓN SIMULADA:</b> {sample.action_details}</p>
                    <p><b>MOTIVO:</b> {sample.reason}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    elif "03" in demo_step:
        st.markdown("<span class='badge-step'>03 — PROTECCIÓN</span> <span class='section-header'>Protección: La temperatura supera el umbral configurado</span>", unsafe_allow_html=True)
        st.markdown(
            "**Explicación breve:** Durante entrenamiento intensivo, la temperatura alcanza 89 °C superando el umbral preventivo configurado para la simulación (85 °C). El agente activa protección inmediata."
        )
        sample = next((d for d in current_decisions if d.gpu_id == "GPU-07"), current_decisions[0])
        col1, col2, col3 = st.columns([1, 1, 2])
        col1.metric("GPU Evaluada", sample.gpu_id)
        col1.metric("Temperatura", f"{sample.perceptions['temperature']} °C", delta=">= 85 °C (Alerta)", delta_color="inverse")
        col2.metric("Potencia Eléctrica", f"{sample.perceptions['power_w']} W", delta="Pico Extremo (720 W)", delta_color="inverse")
        col2.metric("Utilización de Cómputo", f"{sample.perceptions['utilization']} %", delta="97% (Saturación)")

        with col3:
            st.markdown(
                f"""
                <div class='decision-card decision-box-proteccion'>
                    <h3>ESTADO: {sample.state.value}</h3>
                    <p><b>DECISIÓN:</b> {sample.action.value}</p>
                    <p><b>ACCIÓN SIMULADA:</b> {sample.action_details}</p>
                    <p><b>MOTIVO:</b> {sample.reason}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    elif "04" in demo_step:
        st.markdown("<span class='badge-step'>04 — ANOMALÍA</span> <span class='section-header'>Anomalía: Detección de fallo sensorial de veracidad</span>", unsafe_allow_html=True)
        st.markdown(
            "**Explicación breve:** El sensor reporta 150 °C con solo 10 W de potencia. Una percepción no es una orden: el filtro de veracidad aísla la contradicción y marca DATOS NO CONFIABLES."
        )
        sample = next((d for d in current_decisions if d.gpu_id == "GPU-12"), current_decisions[0])
        col1, col2, col3 = st.columns([1, 1, 2])
        col1.metric("GPU Evaluada", sample.gpu_id)
        col1.metric("Temperatura", f"{sample.perceptions['temperature']} °C", delta="Anomalía (150 °C)", delta_color="inverse")
        col2.metric("Potencia Eléctrica", f"{sample.perceptions['power_w']} W", delta="10 W (Inconsistente)", delta_color="inverse")
        col2.metric("Utilización", f"{sample.perceptions['utilization']} %")

        with col3:
            st.markdown(
                f"""
                <div class='decision-card decision-box-anomalia'>
                    <h3>ESTADO: {sample.state.value}</h3>
                    <p><b>DECISIÓN:</b> {sample.action.value}</p>
                    <p><b>ACCIÓN SIMULADA:</b> {sample.action_details}</p>
                    <p><b>MOTIVO:</b> {sample.reason}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    elif "05" in demo_step:
        st.markdown("<span class='badge-step'>05 — MAPREDUCE</span> <span class='section-header'>Análisis Histórico: Agregación Batch con MapReduce</span>", unsafe_allow_html=True)
        st.markdown(
            "**Explicación breve:** Procesamiento batch con MapReduce (Map, Shuffle, Reduce) sobre 160 lecturas históricas. "
            "Cada registro representa una ventana de muestreo de 60 s donde su timestamp identifica el inicio de esa ventana "
            "(10 registros = 10 minutos acumulados como supuesto del dataset)."
        )
        mr_results = execute_mapreduce(df_historical.to_dict(orient="records"))
        st.info(f"**Lote procesado:** {mr_results['input_records_count']} registros históricos consolidados (10 ventanas de muestreo de 60 s = 10 minutos acumulados).")

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
# VISTA 3: DASHBOARD GENERAL (ENTENDIBLE EN 10 SEGUNDOS)
# ==============================================================================
elif menu_option == "3. Dashboard General":
    st.markdown("<h1 class='main-title'>ECO-HPC</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Agente Supervisor de Eficiencia Energética para un entorno HPC</p>", unsafe_allow_html=True)

    # 5 Métricas Principales en Primer Plano
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("GPU Simuladas", cluster_summary["total_gpus"], help="16 aceleradores simulados en 4 nodos de cómputo")
    col2.metric("Temp. Promedio", f"{cluster_summary['avg_temperature']} °C", help="Promedio de lecturas térmicas válidas")
    col3.metric("Consumo Total", f"{cluster_summary['total_power_w']} W", help="Potencia total instantánea disipada por el clúster")
    col4.metric("Utilización Media", f"{cluster_summary['avg_utilization']} %", help="Carga de cómputo promedio")
    col5.metric("Estado General", cluster_summary["general_status"], help="Diagnóstico consolidado del supervisor")

    st.markdown("---")

    col_chart1, col_chart2 = st.columns([3, 2])
    with col_chart1:
        st.markdown("#### Distribución de Estados del Agente en el Clúster")
        states_df = pd.DataFrame(
            [{"Estado": k, "Cantidad de GPUs": v} for k, v in cluster_summary["states_count"].items()]
        )
        st.bar_chart(states_df.set_index("Estado"), color="#0f4c81")

    with col_chart2:
        st.markdown("#### Acciones Operativas Recomendadas")
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
    st.markdown("<h1 class='main-title'>📡 Telemetría de Sensores (Percepciones M2M)</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Datos sensoriales recopilados por canales M2M/IoT desde los nodos de cómputo</p>", unsafe_allow_html=True)

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
                "background-color: #fffbeb; color: #92400e; font-weight: bold;"
                if val == "AHORRO"
                else (
                    "background-color: #faf5ff; color: #581c87; font-weight: bold;"
                    if val == "DATOS NO CONFIABLES"
                    else "background-color: #f0fdf4; color: #166534; font-weight: bold;"
                )
            ),
            subset=["Estado Agente"],
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")
    st.markdown("#### Correlación Térmica y de Consumo")
    valid_plot_df = df_table.dropna(subset=["Temp (°C)", "Potencia (W)", "Utilización (%)"]).copy()
    valid_plot_df = valid_plot_df[valid_plot_df["Temp (°C)"] < 120]

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.scatter_chart(
            valid_plot_df,
            x="Utilización (%)",
            y="Potencia (W)",
            color="Estado Agente",
        )
        st.caption("Relación Utilización vs Potencia: Identifica GPUs subutilizadas con consumo alto (cuadrante Ahorro).")
    with col_g2:
        st.scatter_chart(
            valid_plot_df,
            x="Potencia (W)",
            y="Temp (°C)",
            color="Estado Agente",
        )
        st.caption("Relación Potencia vs Temperatura: Muestra el punto crítico donde la GPU entra en Protección.")


# ==============================================================================
# VISTA 5: AGENTE (DECISIÓN & CICLO)
# ==============================================================================
elif menu_option == "5. Agente (Decisión & Ciclo)":
    st.markdown("<h1 class='main-title'>🧠 AGENTE ECO-HPC</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Ciclo cognitivo completo: Percepciones → Control de Calidad → Estado → Decisión → Acción</p>", unsafe_allow_html=True)

    gpu_options = [d.gpu_id for d in current_decisions]
    selected_gpu = st.selectbox("Seleccionar GPU para inspeccionar el ciclo cognitivo del agente:", gpu_options, index=6)

    chosen = next(d for d in current_decisions if d.gpu_id == selected_gpu)
    p = chosen.perceptions

    st.markdown("---")

    # Representación visual del flujo cognitivo del agente
    c_p1, c_p2, c_p3, c_p4, c_p5 = st.columns(5)
    with c_p1:
        st.markdown(
            f"""
            <div class='flow-box'>
                <h4>1. PERCEPCIONES</h4>
                <p><b>GPU:</b> {chosen.gpu_id}</p>
                <p><b>Temp:</b> {p.get('temperature')} °C</p>
                <p><b>Potencia:</b> {p.get('power_w')} W</p>
                <p><b>Uso:</b> {p.get('utilization')} %</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c_p2:
        st.markdown(
            f"""
            <div class='flow-box'>
                <h4>2. CALIDAD</h4>
                <p><b>Veracidad:</b> {'✅ VÁLIDA' if chosen.is_data_valid else '❌ ANOMALÍA'}</p>
                <p><b>Filtro:</b> Rango & Lógica</p>
                <p><b>Leyes Físicas:</b> Verificadas</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c_p3:
        st.markdown(
            f"""
            <div class='flow-box'>
                <h4>3. ESTADO</h4>
                <p><b>Memoria:</b> Actualizada</p>
                <p><b>Estado:</b><br><b style='color:#0f4c81; font-size:1.1rem;'>{chosen.state.value}</b></p>
                <p><b>Determinismo:</b> Sí</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c_p4:
        st.markdown(
            f"""
            <div class='flow-box'>
                <h4>4. DECISIÓN</h4>
                <p><b>Regla:</b> {chosen.rule_id}</p>
                <p><b>Decisión:</b><br><b style='color:#0f4c81; font-size:1.1rem;'>{chosen.action.value}</b></p>
                <p><b>Sin ML:</b> Regla fija</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c_p5:
        st.markdown(
            f"""
            <div class='flow-box'>
                <h4>5. ACCIÓN</h4>
                <p><b>Tipo:</b> SIMULADA</p>
                <p><b>DVFS / Cooling</b></p>
                <p><b>SLURM Quota</b></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Ficha de Decisión Detallada
    st_val = chosen.state.value
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
        <div class='decision-card {box_class}'>
            <h3>{chosen.gpu_id} — ESTADO: {chosen.state.value}</h3>
            <p style='font-size:1.2rem;'><b>DECISIÓN DEL AGENTE:</b> {chosen.action.value}</p>
            <p><b>ACCIÓN SIMULADA:</b> {chosen.action_details}</p>
            <p><b>MOTIVO:</b> {chosen.reason}</p>
            <hr style='border:0; border-top: 1px solid rgba(0,0,0,0.15); margin: 0.8rem 0;'>
            <p><b>¿Qué está ocurriendo?</b> {chosen.what_is_happening()}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "💡 **Definición Canónica de Estado Interno:** El agente mantiene memoria histórica de decisiones, estados por GPU "
        "y acumuladores del sistema. Las reglas actuales evalúan de forma determinista la percepción presente "
        "y no utilizan aprendizaje automático ni dependen de la decisión anterior."
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
        st.subheader("Volumen: Cuántos datos puede generar el sistema")
        st.markdown(
            """
            En un clúster HPC de producción para Inteligencia Artificial, la telemetría acumulativa de alta frecuencia
            genera volúmenes masivos de datos:
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
                **Prototipo Didáctico vs Escala Conceptual:**
                - El prototipo opera intencionalmente con **16 GPUs simuladas** para garantizar
                  ejecución liviana, total explicabilidad e interactividad fluida en cualquier máquina.
                - La arquitectura conceptual está diseñada para escalar horizontalmente hacia
                  millones de registros diarios.
                """
            )

    with tab_vel:
        st.subheader("Velocidad: Qué tan rápido se generan y procesan")
        st.markdown(
            """
            En ECO-HPC coexisten dos requerimientos de velocidad complementarios:

            1. **Baja Latencia (Streaming / Tiempo Real < 1-2 segundos):**
               - Necesaria para el **Agente Supervisor**: detección inmediata de picos térmicos
                 y derroche energético en GPUs desocupadas.
               - El agente percibe y decide en milisegundos.

            2. **Batch / Diferido (Horas / Días / Semanas):**
               - Procesamiento de series temporales históricas mediante **MapReduce**.
               - Cálculo de consumo energético acumulado en kWh, perfiles medios por GPU
                 y auditorías de sostenibilidad ambiental.
            """
        )

    with tab_var:
        st.subheader("Variedad: Qué formatos de datos existen")
        st.markdown("La telemetría de supercómputo no proviene en un único formato homogéneo:")

        col_var1, col_var2, col_var3 = st.columns(3)
        with col_var1:
            st.markdown("##### Estructurados (CSV)")
            st.caption("Series temporales con esquema estricto y tipos fijos:")
            st.dataframe(df_historical[["gpu_id", "temperature", "power_w", "utilization"]].head(5), hide_index=True)

        with col_var2:
            st.markdown("##### Semiestructurados (JSON)")
            st.caption("Objetos emitidos por APIs REST o exporters de DCGM:")
            st.json(json_data[0])

        with col_var3:
            st.markdown("##### No Estructurados (Logs TXT)")
            st.caption("Líneas de syslog / dmesg / IPMI en texto plano:")
            st.text("\n".join([line.strip() for line in logs_lines[:5]]))

    with tab_ver:
        st.subheader("Veracidad: Qué tan confiables son los datos")
        st.markdown(
            """
            En entornos con miles de sensores electrónicos ocurren fallos de medición, ruido electromagnético
            y derivas térmicas del silicio.
            
            **Principio de Veracidad en ECO-HPC:**
            El agente jamás asume que todo dato recibido es verídico. Si una lectura viola leyes físicas
            (como 150 °C con 10 W de potencia) o contiene valores nulos, el sistema activa el estado
            **DATOS NO CONFIABLES** y rechaza tomar decisiones automáticas sobre el hardware.
            """
        )

    with tab_val:
        st.subheader("Valor: Para qué sirven los datos")
        st.markdown(
            """
            El valor del Big Data no radica en almacenar terabytes, sino en transformar percepciones en decisiones:

            ```text
            DATOS CRUDOS (Telemetría de potencia, temperatura y utilización)
                 ↓
            INFORMACIÓN (Identificación de GPUs subutilizadas o sobrecalentadas)
                 ↓
            DECISIÓN (Reglas deterministas del agente ECO-HPC)
                 ↓
            ACCIÓN (Reducción de reloj por DVFS o aumento de refrigeración)
                 ↓
            VALOR (Ahorro de energía en kWh, reducción de emisiones y preservación de equipamiento)
            ```
            """
        )


# ==============================================================================
# VISTA 7: CALIDAD DE DATOS & VERACIDAD
# ==============================================================================
elif menu_option == "7. Calidad de Datos & Veracidad":
    st.markdown("<h1 class='main-title'>🛡️ Calidad de Datos y Veracidad</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Detección sistemática de anomalías, datos faltantes y violaciones de leyes físicas</p>", unsafe_allow_html=True)

    batch_audit = DataQualityAuditor.audit_batch(df_historical.to_dict(orient="records"))

    col_q1, col_q2, col_q3, col_q4 = st.columns(4)
    col_q1.metric("REGISTROS", batch_audit["total_records"], help="Total de lecturas de telemetría analizadas")
    col_q2.metric("VÁLIDOS", batch_audit["valid_records"], help="Lecturas que superaron todas las capas de calidad")
    col_q3.metric("ANOMALÍAS", batch_audit["anomalous_records"], delta="Filtrados", delta_color="inverse", help="Lecturas con violaciones de rangos o leyes físicas")
    col_q4.metric("FALTANTES", batch_audit["missing_records"], delta="Nulos/Incompletos", delta_color="inverse", help="Campos ausentes o valores nulos (NaN/None)")

    st.caption(f"**Tasa Global de Veracidad:** {batch_audit['veracity_rate_pct']} % de percepciones conformes a especificación.")

    st.markdown("---")
    st.markdown("#### Ejemplos de Anomalías Detectadas en el Dataset")

    col_ex1, col_ex2 = st.columns(2)
    with col_ex1:
        st.error("❌ **Ejemplo 1: Contradicción Física (GPU-12)**")
        st.write("- **Lectura:** Temperatura = 150 °C, Potencia = 10 W, Utilización = 0%")
        st.write("- **Diagnóstico:** Físicamente imposible disipar 150 °C con flujo de corriente despreciable.")
        st.write("- **Acción:** Clasificación como `DATOS NO CONFIABLES` y emisión de ticket de mantenimiento.")
    with col_ex2:
        st.error("❌ **Ejemplo 2: Valores Nulos y Fuera de Rango (GPU-13)**")
        st.write("- **Lectura:** Temperatura = `NaN`, Potencia = -45 W, Utilización = 108%")
        st.write("- **Diagnóstico:** Campo ausente, potencia negativa imposible y porcentaje mayor a 100%.")
        st.write("- **Acción:** Rechazo preventivo inmediato en la capa de auditoría.")

    st.markdown("---")
    st.markdown(
        """
        #### Clasificación de Sesgos y Fallas en Telemetría de Hardware
        1. **Sesgo de Medición:** Desviaciones por calibración del conversor analógico-digital (ADC) entre distintos lotes.
        2. **Sesgo de Muestreo:** Nodos que reportan a frecuencias dispares por congestión de la red de gestión OOB.
        3. **Deriva del Sensor (*Sensor Drift*):** Degradación paulatina de termistores tras miles de ciclos térmicos.
        """
    )


# ==============================================================================
# VISTA 8: MAPREDUCE HISTÓRICO
# ==============================================================================
elif menu_option == "8. MapReduce Histórico":
    st.markdown("<h1 class='main-title'>🔄 Procesamiento Batch con MapReduce</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Demostración didáctica del paradigma distribuido en Python: Map → Shuffle → Reduce</p>", unsafe_allow_html=True)

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
            "Cada *Reducer* computa la potencia media, la temperatura pico y la energía acumulada en kWh "
            "(asumiendo la semántica de ventana de muestreo de 60 s por registro: Horas = (Muestras * 60) / 3600, "
            "donde cada timestamp identifica el inicio de su ventana; 10 registros = 10 minutos acumulados como supuesto del dataset):"
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
        st.markdown("### Marco PEAS Formal")
        st.markdown(
            """
            <div class='peas-card'>
                <h3>P — Performance (Medida de Rendimiento)</h3>
                <p>Reducir consumo eléctrico y mantener condiciones térmicas seguras bajo el umbral configurado (&lt;85 °C en simulación).</p>
            </div>
            <div class='peas-card'>
                <h3>E — Environment (Entorno)</h3>
                <p>Entorno HPC con aceleradores GPU para cargas de Inteligencia Artificial.</p>
            </div>
            <div class='peas-card'>
                <h3>A — Actuators (Actuadores)</h3>
                <p>Acciones simuladas sobre frecuencia (DVFS), ventiladores de refrigeración y límites de carga en SLURM.</p>
            </div>
            <div class='peas-card'>
                <h3>S — Sensors (Sensores)</h3>
                <p>Telemetría continua de temperatura (°C), potencia (W), utilización (%), reloj (MHz) y estado de trabajo.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_peas2:
        st.markdown("### Ficha Técnica de ECO-HPC")
        st.markdown(
            """
            - **Nombre del Agente:** ECO-HPC Supervisor
            - **Tipo de Agente:** Reactivo basado en reglas con estado interno
            - **Definición del Estado Interno:** El agente mantiene memoria histórica de decisiones, estados por GPU y acumuladores del sistema. Las reglas actuales evalúan de forma determinista la percepción presente y no utilizan aprendizaje automático ni dependen de la decisión anterior.
            - **Entorno de Operación:** HPC / Data Center de Inteligencia Artificial
            - **Escala Conceptual:** Hasta 1.024 GPUs
            - **Escala de Prototipo:** 16 GPUs simuladas en 4 nodos
            - **Contexto Técnico:** Inspirado en aceleradores clase NVIDIA H100 SXM (con hasta 700 W configurables según especificaciones oficiales de NVIDIA; variantes PCIe operan en 300-350 W). El prototipo utiliza GPUs simuladas y no posee H100 físicas.
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
    st.markdown("<p class='sub-title'>Diferenciación explícita: Prototipo Implementado vs Arquitectura Conceptual a Escala</p>", unsafe_allow_html=True)

    col_arch1, col_arch2 = st.columns(2)

    with col_arch1:
        st.markdown("### Prototipo Implementado")
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
        st.caption("Diseñado para simplicidad, transparencia, portabilidad y explicación directa.")

    with col_arch2:
        st.markdown("### Arquitectura Conceptual")
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

    st.markdown("---")
    st.markdown("#### Matriz de Realidad y Transparencia Técnica")
    st.markdown(
        """
        | Componente | Clasificación | Justificación y Alcance |
        | :--- | :--- | :--- |
        | **Código del Agente y Reglas** | **IMPLEMENTADO** | Ejecución real en Python determinista con evaluación de estados. |
        | **Módulo de Calidad de Datos** | **IMPLEMENTADO** | Auditoría y filtros físicos ejecutados sobre datasets reales. |
        | **Algoritmo MapReduce** | **IMPLEMENTADO** | Demostración funcional en Python de Map, Shuffle y Reduce. |
        | **Dashboard Streamlit** | **IMPLEMENTADO** | Interfaz web interactiva con monitoreo e inspección en vivo. |
        | **Suite de Pruebas Automatizadas** | **IMPLEMENTADO** | 24 pruebas unitarias, de integración y negativas en Pytest. |
        | **Aceleradores GPU y Sensores** | **SIMULADO** | Modelado numérico sintético de hardware; no hay GPUs físicas. |
        | **Acciones de Actuadores** | **SIMULADO** | Recomendaciones operativas; no envían comandos eléctricos reales. |
        | **Clúster Masivo de 1.024 GPUs** | **CONCEPTUAL** | Escenario de referencia para dimensionamiento matemático de Big Data. |
        | **Base de Datos NoSQL de Producción** | **CONCEPTUAL** | Solución recomendada para 88.4M escrituras/día sin despliegue físico. |
        | **Planificador SLURM e Ingesta Kafka**| **CONCEPTUAL** | Componentes industriales justificados teóricamente en la arquitectura. |
        """
    )


# ==============================================================================
# VISTA 11: SOSTENIBILIDAD & NOSQL & LEY 25.326
# ==============================================================================
elif menu_option == "11. Sostenibilidad & NoSQL & Ley 25.326":
    st.markdown("<h1 class='main-title'>🌱 Sostenibilidad, NoSQL y Aspectos Legales</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Integración multidimensional de impacto ambiental, almacenamiento y privacidad de datos</p>", unsafe_allow_html=True)

    tab_sos, tab_nosql, tab_ley = st.tabs(["Sostenibilidad Ambiental", "Justificación NoSQL", "Ley Nacional N.º 25.326"])

    with tab_sos:
        st.subheader("¿Por qué hacemos esto?")
        st.markdown(
            """
            <div class='flow-box' style='background-color:#f0fdf4; border: 2px solid #86efac; border-radius:8px; padding:1.2rem; margin-bottom:1.2rem;'>
                <p style='margin:0; font-size:1.1rem; font-weight:700; color:#14532d; line-height:1.7;'>
                    DATOS (Telemetría sensorial continua M2M de potencia y temperatura)<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
                    DECISIONES (Agente supervisor determinista basado en reglas)<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
                    EFICIENCIA (Modulación de reloj por DVFS y control térmico simulado)<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;↓<br>
                    SOSTENIBILIDAD (Ahorro de kWh, reducción de emisiones de CO₂ y preservación del hardware)
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            El entrenamiento y despliegue de modelos de inteligencia artificial consume grandes cantidades de energía.
            La relación entre IA, hardware y sostenibilidad en ECO-HPC se fundamenta en:

            1. **Evitar el Desperdicio en Reposo (*Idle Energy Waste*):**
               Cuando una GPU concluye un batch o espera transferencias de red, mantener el reloj a máxima
               frecuencia genera un consumo parásito evitable. La acción **AHORRAR** reduce el consumo en ~40%.
            2. **Preservación Térmica en la Simulación:**
               Operar continuamente por encima del umbral de protección configurado (85 °C en la simulación)
               incrementa el estrés térmico del equipo. La acción **PROTEGER** evita operar el hardware en regímenes
               térmicos severos de forma prolongada (85 °C no es un límite universal de toda GPU).
            3. **Reducción de Huella de Carbono Simulada:**
               Cada kilovatio-hora ahorrado evita emisiones de gases de efecto invernadero según la matriz energética.
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
               Estructura optimizada para series de tiempo, compresión por columnas y particionamiento por ventanas temporales.
            - **Escalabilidad Horizontal:** Capacidad de agregar nodos de almacenamiento sin detener el clúster.
            - **Políticas de Retención (*TTL - Time To Live*):** Roll-up automático de datos de 1 segundo a promedios de 1 minuto tras 30 días.
            """
        )

    with tab_ley:
        st.subheader("Marco Legal: Ley N.º 25.326 de Protección de los Datos Personales (Argentina)")
        st.markdown(
            """
            **Pregunta Técnica Fundamental:** *¿Los datos de telemetría de una GPU son datos personales?*

            - **Respuesta Técnica Corta:** **No en su estado crudo, pero SÍ cuando se correlacionan.**
            - **Fundamento Legal:** La telemetría pura (temperatura 60°C, potencia 350W) es métrica de máquina (M2M).
              Sin embargo, según el **Art. 2 de la Ley 25.326**, es dato personal toda información referida a personas físicas determinadas o determinables.
              Si los logs del gestor de trabajos (SLURM) asocian:
              `USUARIO (Legajo/Nombre) + TRABAJO + HORARIO + GPU ASIGNADA`
              la telemetría permite inferir pautas de trabajo, horarios laborales o propiedad intelectual.

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
    st.markdown("<p class='sub-title'>Registro riguroso de fuentes oficiales, normativas legales y publicaciones científicas</p>", unsafe_allow_html=True)

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
