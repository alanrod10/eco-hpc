"""
ui_components.py - Componentes de Presentación Reutilizables para ECO-HPC
-------------------------------------------------------------------------
Centraliza los fragmentos de HTML/CSS y las cajas de decisión semánticas que
antes estaban duplicados a lo largo de ``app.py`` (Single Source of Truth
también en la capa de presentación).

El mapeo Estado del Agente -> clase CSS se define una única vez
(``STATE_CSS_CLASS``) y se reutiliza en todas las vistas.
"""

from typing import Any, Dict, Iterable, Tuple

import streamlit as st

from rules import AgentState

# ==============================================================================
# ESTILOS CSS PROFESIONALES - TEMA CLARO Y ALTO CONTRASTE PARA PROYECTOR
# ==============================================================================
APP_CSS = """
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
"""

# Mapeo canónico único: Estado del Agente -> clase CSS de la caja de decisión.
STATE_CSS_CLASS: Dict[AgentState, str] = {
    AgentState.NORMAL: "decision-box-normal",
    AgentState.AHORRO: "decision-box-ahorro",
    AgentState.PROTECCION: "decision-box-proteccion",
    AgentState.DATOS_NO_CONFIABLES: "decision-box-anomalia",
}

# Mapeo canónico único: Estado del Agente -> estilo de celda para tablas (Plotly/styler).
STATE_CELL_STYLE: Dict[str, str] = {
    AgentState.PROTECCION.value: "background-color: #fef2f2; color: #991b1b; font-weight: bold;",
    AgentState.AHORRO.value: "background-color: #fffbeb; color: #92400e; font-weight: bold;",
    AgentState.DATOS_NO_CONFIABLES.value: "background-color: #faf5ff; color: #581c87; font-weight: bold;",
    AgentState.NORMAL.value: "background-color: #f0fdf4; color: #166534; font-weight: bold;",
}


def apply_styles() -> None:
    """Inyecta los estilos globales de la aplicación."""
    st.markdown(APP_CSS, unsafe_allow_html=True)


def render_title(title: str, subtitle: str = "") -> None:
    """Encabezado estándar de cada vista (título principal + subtítulo)."""
    st.markdown(f"<h1 class='main-title'>{title}</h1>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<p class='sub-title'>{subtitle}</p>", unsafe_allow_html=True)


def decision_box_class(state: AgentState) -> str:
    """Devuelve la clase CSS correspondiente al estado del agente."""
    return STATE_CSS_CLASS.get(state, "decision-box-normal")


def render_decision_card(
    decision: Any,
    title_prefix: str = "",
    extra_lines: Iterable[str] = (),
) -> None:
    """
    Caja de decisión semántica reutilizable: ESTADO / DECISIÓN / ACCIÓN / MOTIVO.
    ``extra_lines`` permite agregar filas informativas (por ejemplo, la respuesta
    canónica '¿Qué está ocurriendo?') sin duplicar el HTML.
    """
    heading = f"{title_prefix}{decision.gpu_id} — ESTADO: {decision.state.value}" if title_prefix else f"ESTADO: {decision.state.value}"
    extras_html = "".join(extra_lines)
    st.markdown(
        f"""
        <div class='decision-card {decision_box_class(decision.state)}'>
            <h3>{heading}</h3>
            <p><b>DECISIÓN:</b> {decision.action.value}</p>
            <p><b>ACCIÓN SIMULADA:</b> {decision.action_details}</p>
            <p><b>MOTIVO:</b> {decision.reason}</p>
            {extras_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def select_sample_decision(decisions: Iterable[Any], gpu_id: str) -> Any:
    """Obtiene la decisión de una GPU específica con un fallback seguro."""
    decisions = list(decisions)
    return next((d for d in decisions if d.gpu_id == gpu_id), decisions[0])


def render_step_header(step_badge: str, section_title: str) -> None:
    """Encabezado de paso de demostración: badge + título de sección."""
    st.markdown(
        f"<span class='badge-step'>{step_badge}</span> "
        f"<span class='section-header'>{section_title}</span>",
        unsafe_allow_html=True,
    )


def style_state_column(styler, column: str):
    """Aplica el color semántico del estado del agente a una columna de la tabla."""
    return styler.map(lambda val: STATE_CELL_STYLE.get(val, ""), subset=[column])
