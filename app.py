"""EcoTrack Streamlit UI — natural-language daily carbon estimate."""

import streamlit as st

from estimator import estimate, total_kg

st.set_page_config(page_title="EcoTrack", page_icon="🌱", layout="centered")

st.markdown(
    """
    <style>
    .stApp { background-color: #f7f4ef; }
    h1, h2, h3 { color: #2f5d3a !important; font-weight: 650; }
    .stButton > button, button[kind="formSubmit"], div[data-testid="stForm"] button {
        background-color: #3f7d4e !important;
        color: #fff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.5rem 1.4rem;
        font-weight: 600;
    }
    .stButton > button:hover, button[kind="formSubmit"]:hover {
        background-color: #2f5d3a !important;
        color: #fff !important;
    }
    div[data-testid="stMetricValue"] { color: #2f5d3a; }
    .block-container { padding-top: 2.4rem; padding-bottom: 3rem; max-width: 720px; }
    </style>
    """,
    unsafe_allow_html=True,
)

if "history" not in st.session_state:
    st.session_state.history = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None

st.title("🌱 EcoTrack")
st.write(
    "Cuéntame tu día en una frase y te devuelvo una **estimación amable** "
    "de tu huella. La idea es entender, no juzgar."
)

st.info(
    "Los valores son **estimaciones aproximadas** (orden de magnitud) "
    "con fines educativos, no una medición exacta."
)

with st.form("daily_entry"):
    text = st.text_area(
        "¿Qué hiciste hoy?",
        placeholder="Hoy comí carne y viajé 20km en bus",
        height=110,
    )
    submitted = st.form_submit_button("Calcular huella")

if submitted:
    items = estimate(text)
    if not items:
        st.session_state.last_result = {"ok": False, "text": text}
    else:
        kg = total_kg(items)
        st.session_state.last_result = {
            "ok": True,
            "text": text,
            "kg": kg,
            "rows": [
                {
                    "Actividad": item.label,
                    "kg CO2e": item.kg_co2e,
                    "Tipo": item.category,
                }
                for item in items
            ],
        }
        st.session_state.history.append(
            {"Entrada": text.strip(), "kg CO2e": kg}
        )

result = st.session_state.last_result
if result is not None:
    st.divider()
    if not result["ok"]:
        st.success(
            "No encontré actividades todavía. Prueba con algo como: "
            "**«Hoy comí pollo y viajé 10 km en moto»**."
        )
    else:
        st.metric("Huella estimada de hoy", f"{result['kg']:.2f} kg CO2e")
        st.caption("Desglose por actividad")
        st.table(result["rows"])
        st.caption("Recuerda: son valores aproximados para explorar hábitos, no para sentirte mal.")

if st.session_state.history:
    st.subheader("Historial de esta sesión")
    st.table(list(reversed(st.session_state.history)))
    st.caption("El historial vive solo en esta sesión; si recargas la página, se reinicia.")
