import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y TEMÁTICA ROSA DE ALTO CONTRASTE
# ---------------------------------------------------------
st.set_page_config(
    page_title="STEELIA | Corrosión del Acero en Ingeniería Civil",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilos CSS avanzados: Máximo contraste visual + Estética Girly/Elegante
custom_css = """
<style>
    /* Fondo general de la aplicación */
    .stApp {
        background-color: #FFF2F6 !important;
        color: #2E0D17 !important;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }

    /* FORZAR VISIBILIDAD EN TODO TIPO DE TEXTOS NATIVOS DE STREAMLIT */
    p, span, label, div, li, input, select, textarea {
        color: #2E0D17 !important;
    }

    /* MENÚ LATERAL (SIDEBAR) CON ALTO CONTRASTE */
    section[data-testid="stSidebar"] {
        background-color: #FCD8E5 !important;
        border-right: 2px solid #F5A9C4 !important;
    }

    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] div[role="radiogroup"] span {
        color: #421222 !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }

    /* ENCABEZADOS DE SECCIÓN */
    h1, h2, h3, h4, h5 {
        color: #9C1B4E !important;
        font-weight: 800 !important;
    }

    /* TARJETAS CONTENEDORAS PRINCIPALES */
    .stCard {
        background-color: #FFFFFF !important;
        border-radius: 24px !important;
        padding: 28px !important;
        box-shadow: 0 10px 25px rgba(216, 27, 96, 0.12) !important;
        border: 2px solid #F7B5CD !important;
        margin-bottom: 24px !important;
    }

    /* TARJETAS DE RESULTADO DE CALCULADORA (WOW EFFECT) */
    .metric-card-pink {
        background: linear-gradient(135deg, #FFFFFF 0%, #FFF0F5 100%) !important;
        border: 2px solid #F06292 !important;
        border-radius: 20px !important;
        padding: 20px !important;
        text-align: center !important;
        box-shadow: 0 6px 18px rgba(240, 98, 146, 0.2) !important;
    }

    .metric-title {
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        color: #880E4F !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }

    .metric-value {
        font-size: 1.8rem !important;
        font-weight: 900 !important;
        color: #C2185B !important;
        margin-top: 5px !important;
    }

    /* BANNER ENCABEZADO ROSA PASTEUL */
    .pink-header-card {
        background: linear-gradient(135deg, #F8BBD0 0%, #F48FB1 100%) !important;
        border-radius: 28px !important;
        padding: 35px !important;
        color: #380B1D !important;
        box-shadow: 0 12px 30px rgba(233, 30, 99, 0.25) !important;
        margin-bottom: 30px !important;
        border: 2px solid #F06292 !important;
    }

    /* CAJAS DE FÓRMULAS QUÍMICAS / MATEMÁTICAS */
    .formula-box {
        background-color: #FFF0F5 !important;
        border-left: 6px solid #D81B60 !important;
        padding: 18px !important;
        border-radius: 16px !important;
        font-family: 'Courier New', monospace !important;
        color: #421222 !important;
        font-weight: bold !important;
        font-size: 1.15rem !important;
        margin: 16px 0 !important;
    }

    /* CONTROLES DE ENTRADA (INPUTS, NUMBERS, SELECTS) */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: #FFF9FB !important;
        border: 2px solid #F48FB1 !important;
        border-radius: 12px !important;
        color: #2E0D17 !important;
    }

    /* TABLAS Y DATAFRAMES CON MÁXIMA LEGIBILIDAD */
    div[data-testid="stTable"] table {
        color: #2E0D17 !important;
        background-color: #FFFFFF !important;
        border-radius: 16px !important;
        border: 2px solid #F8BBD0 !important;
        overflow: hidden !important;
    }

    div[data-testid="stTable"] th {
        background-color: #F8BBD0 !important;
        color: #421222 !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
    }

    div[data-testid="stTable"] td {
        color: #2E0D17 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        background-color: #FFFFFF !important;
    }

    /* BOTONES PRINCIPALES */
    .stButton > button {
        background: linear-gradient(135deg, #E91E63 0%, #AD1457 100%) !important;
        color: #FFFFFF !important;
        border-radius: 18px !important;
        border: none !important;
        padding: 14px 32px !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        box-shadow: 0 6px 20px rgba(233, 30, 99, 0.35) !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. DATOS NORMATIVOS (NTC MÉXICO E ISO 9223)
# ---------------------------------------------------------
NTC_CATEGORIES = {
    "A1": "Elementos protegidos por membrana impermeable o superficies interiores enceradas.",
    "A2": "Suelos no agresivos y ambientes exteriores no agresivos.",
    "B1": "Interiores con humedecimiento/secado repetido, exteriores ligeramente agresivos.",
    "B2": "Ambientes exteriores agresivos y exposiciones con cloruros.",
    "C": "Exposición a agua con > 20,000 ppm de cloruros en zonas de humedecimiento y secado.",
    "D": "Suelos agresivos y ambientes especialmente desfavorables no contemplados en A1-C.",
}

ISO_DATA = {
    "C1 (Muy baja)": {"min": 0.0, "max": 1.3, "ref": 0.7},
    "C2 (Baja)": {"min": 1.3, "max": 25.0, "ref": 13.0},
    "C3 (Media)": {"min": 25.0, "max": 50.0, "ref": 37.5},
    "C4 (Alta)": {"min": 50.0, "max": 80.0, "ref": 65.0},
    "C5 (Muy alta)": {"min": 80.0, "max": 200.0, "ref": 140.0},
    "CX (Extrema)": {"min": 200.0, "max": 700.0, "ref": 450.0},
}

# ---------------------------------------------------------
# 3. NAVEGACIÓN Y SIDEBAR
# ---------------------------------------------------------
st.sidebar.markdown(
    "<h1 style='text-align: center; color: #880E4F;'>🌸 STEELIA</h1>",
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    "<p style='text-align: center; color: #421222; font-size: 0.95em;'><b>Análisis & Corrosión del Acero</b><br>Ingeniería Civil México</p>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

opciones_menu = [
    "Portada",
    "¿Qué es la Corrosión?",
    "Factores Influyentes",
    "Normativa Mexicana (NTC)",
    "Contexto de México",
    "Calculadora de Corrosión",
    "Métodos de Protección",
    "Aplicaciones en Ingeniería",
    "¿Cómo utilizar STEELIA?",
    "Referencias APA 7",
]

menu = st.sidebar.radio("Navega por las secciones:", opciones_menu)

# ---------------------------------------------------------
# SECCIÓN 1: PORTADA
# ---------------------------------------------------------
if menu == "Portada":
    st.markdown(
        """
    <div class="pink-header-card">
        <h1 style="margin:0; font-size: 3rem; color: #380B1D;">💖 STEELIA</h1>
        <h3 style="margin-top: 8px; color: #880E4F; font-weight: 700;">
            Análisis y estimación de la corrosión del acero
        </h3>
        <p style="font-size: 1.2rem; margin-top: 15px; color: #2E0D17;">
            Plataforma interactiva especializada en la evaluación cinético-electroquímica,
            degradación atmosférica y cálculo de pérdida de espesor de acero estructural,
            adaptada a la ingeniería civil en México.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.subheader("✨ Propósito Institucional")
        st.write(
            "STEELIA es una herramienta técnico-educativa desarrollada con Python "
            "y Streamlit que integra los modelos cinéticos lineales y de potencia "
            "(ISO 9224) con las categorías de exposición de las **Normas Técnicas "
            "Complementarias de México (NTC-Concreto Capítulo 4)**.\n\n"
            "Permite evaluar la pérdida anual de espesor, estimar la vida útil residual "
            "de elementos de acero estructural expuestos a la atmósfera y prevenir fallas "
            "catastróficas en la infraestructura nacional."
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="stCard" style="text-align: center;">', unsafe_allow_html=True)
        st.markdown("### 🧮 Calculadora de Corrosión")
        st.write("Accede a la herramienta interactiva de estimación cuantitativa:")
        st.info("💡 Usa el menú lateral para ingresar a la **Calculadora de Corrosión**.")
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# SECCIÓN 2: ¿QUÉ ES LA CORROSIÓN DEL ACERO?
# ---------------------------------------------------------
elif menu == "¿Qué es la Corrosión?":
    st.title("🧪 Fundamentos Electroquímicos")
    st.write(
        "La **corrosión del acero** es la degradación físico-química espontánea del hierro ($Fe$) "
        "inducida por reacciones electroquímicas de transferencia de electrones con el medio ambiente."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.markdown("### 1. Reacción Anódica (Oxidación)")
        st.write("El hierro metálico cede electrones y se disuelve en forma de cationes ferrosos:")
        st.markdown('<div class="formula-box">Fe → Fe²⁺ + 2e⁻</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.markdown("### 2. Reacción Catódica (Reducción)")
        st.write("En presencia de agua y oxígeno disuelto, los electrones liberados se consumen:")
        st.markdown('<div class="formula-box">O₂ + 2H₂O + 4e⁻ → 4OH⁻</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="stCard">', unsafe_allow_html=True)
    st.markdown("### Formación de Herrumbre (Producto Final)")
    st.write(
        "Los iones $Fe^{2+}$ y $OH^-$ precipitan como hidróxido ferroso $Fe(OH)_2$, el cual se oxida a hidróxido férrico "
        "$Fe(OH)_3$ y finalmente a óxido de hierro hidratado (herrumbre):"
    )
    st.markdown('<div class="formula-box">4Fe(OH)₂ + O₂ + 2H₂O → 4Fe(OH)₃ → Fe₂O₃·H₂O</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# SECCIÓN 3: FACTORES INFLUYENTES
# ---------------------------------------------------------
elif menu == "Factores Influyentes":
    st.title("🌡️ Factores Ambiental-Cinéticos")
    st.write("Principales variables físico-químicas que aceleran o modifican la corrosión del acero:")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.markdown("### 💧 Humedad Relativa y Tiempo de Humedecimiento")
        st.write("Por encima del 70-80% de humedad, se forma una película microscópica de agua electrolítica sobre el acero que dispara la cinética electroquímica.")
        st.markdown("### 🌡️ Temperatura")
        st.write("Incrementa la velocidad de las reacciones cinéticas hasta que la evaporación reduce la humedad superficial.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.markdown("### 🌊 Salinidad y Cloruros (Cl⁻)")
        st.write("Los iones cloruro rompen las capas pasivantes protectoras del acero e incrementan drásticamente la conductividad del electrólito.")
        st.markdown("### 🏭 Contaminación ($SO_2$)")
        st.write("Típica de atmósferas urbanas e industriales, genera depósitos ácidos que aceleran la velocidad de deterioro.")
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# SECCIÓN 4: NORMATIVA MEXICANA (NTC)
# ---------------------------------------------------------
elif menu == "Normativa Mexicana (NTC)":
    st.title("🇲🇽 Clasificación Mexicana de Exposición (NTC-Concreto Cap. 4)")
    st.write("Criterios de durabilidad y clasificación ambiental establecidos por la normativa mexicana vigente:")

    df_ntc = pd.DataFrame([
        {"Categoría NTC": k, "Condición de Exposición Oficial": v}
        for k, v in NTC_CATEGORIES.items()
    ])
    st.table(df_ntc)

# ---------------------------------------------------------
# SECCIÓN 5: CONTEXTO DE MÉXICO
# ---------------------------------------------------------
elif menu == "Contexto de México":
    st.title("🌴 Corrosión Atmosférica en México")
    st.markdown("""
    <div class="stCard">
        <h3>Variaciones Regionales</h3>
        <ul>
            <li><b>Sureste y Península de Yucatán:</b> Altas temperaturas, humedad relativa constante y fuerte presencia de cloruros por brisa marina.</li>
            <li><b>Costas del Golfo y Pacífico:</b> Ambientes marinos agresivos que requieren recubrimientos especializados.</li>
            <li><b>Centro e Interior del País:</b> Áreas urbanas e industriales condicionadas por contaminantes como el dióxido de azufre ($SO_2$).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# SECCIÓN 6: CALCULADORA INTERACTIVA DE CORROSIÓN (DISEÑO WOW)
# ---------------------------------------------------------
elif menu == "Calculadora de Corrosión":
    st.markdown("""
    <div class="pink-header-card" style="padding: 24px; margin-bottom: 20px;">
        <h2 style="margin:0; color: #380B1D;">🧮 Calculadora de Corrosión y Pérdida de Espesor</h2>
        <p style="margin-top: 5px; color: #2E0D17; font-weight: 600;">
            Estimación cinético-cuantitativa basada en los modelos Lineal e ISO 9224
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_geo, tab_mod, tab_tasa = st.tabs(["📐 1. Geometría", "🔬 2. Modelo", "⚡ 3. Velocidad"])

    with tab_geo:
        col_g1, col_g2, col_g3 = st.columns(3)
        e0 = col_g1.number_input("Espesor inicial ($e_0$) [mm]:", min_value=0.1, max_value=200.0, value=12.0, step=0.5)
        emin = col_g2.number_input("Espesor mínimo ($e_{min}$) [mm]:", min_value=0.0, max_value=e0, value=8.0, step=0.5)
        t_exp = col_g3.slider("Tiempo de exposición ($t$) [años]:", min_value=1, max_value=100, value=25)

    with tab_mod:
        col_m1, col_m2 = st.columns(2)
        modelo = col_m1.radio("Modelo Matemático:", ["Modelo Lineal (Vc constante)", "Modelo Ley de Potencia (ISO 9224)"])
        b_exp = 0.52
        if modelo == "Modelo Ley de Potencia (ISO 9224)":
            b_exp = col_m2.slider("Exponente empírico ($b$):", min_value=0.10, max_value=1.00, value=0.52, step=0.01)
        else:
            col_m2.info("💡 El modelo lineal asume una velocidad de corrosión constante en el tiempo ($\Delta e = V_c \cdot t$).")

    with tab_tasa:
        col_v1, col_v2 = st.columns(2)
        usar_manual = col_v1.checkbox("Ingresar velocidad ($V_c$) manualmente", value=True)
        if usar_manual:
            vc_um = col_v1.number_input("Velocidad de corrosión ($V_c$) [µm/año]:", min_value=0.1, value=65.0, step=5.0)
        else:
            cat_iso_sel = col_v2.selectbox("Categoría de referencia ISO 9223:", list(ISO_DATA.keys()))
            vc_um = ISO_DATA[cat_iso_sel]["ref"]
            col_v2.caption(f"Valor promedio sugerido: **{vc_um} µm/año**")

    # OPERACIONES MATEMÁTICAS EN PYTHON
    vc_mm = vc_um / 1000.0  # Conversión µm/año a mm/año
    delta_e = vc_mm * t_exp if modelo == "Modelo Lineal (Vc constante)" else vc_mm * (t_exp ** b_exp)
    e_restante = e0 - delta_e
    pct_perdida = (delta_e / e0) * 100.0
    tasa_anual_mm = delta_e / t_exp

    st.markdown("---")
    st.markdown("### 📊 Panel de Resultados Estructurales")

    # MÉTRICAS ESTILIZADAS EN ROSA DE ALTO IMPACTO
    r1, r2, r3, r4 = st.columns(4)
    r1.markdown(f'<div class="metric-card-pink"><div class="metric-title">Tasa Anual</div><div class="metric-value">{tasa_anual_mm:.4f}<span style="font-size:0.9rem"> mm/año</span></div></div>', unsafe_allow_html=True)
    r2.markdown(f'<div class="metric-card-pink"><div class="metric-title">Pérdida Acumulada</div><div class="metric-value">{delta_e:.3f}<span style="font-size:0.9rem"> mm</span></div></div>', unsafe_allow_html=True)
    r3.markdown(f'<div class="metric-card-pink"><div class="metric-title">Espesor Restante</div><div class="metric-value">{e_restante:.3f}<span style="font-size:0.9rem"> mm</span></div></div>', unsafe_allow_html=True)
    r4.markdown(f'<div class="metric-card-pink"><div class="metric-title">Pérdida Material</div><div class="metric-value">{pct_perdida:.1f}<span style="font-size:0.9rem"> %</span></div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    # ALERTAS DE SEGURIDAD
    if e_restante < emin:
        st.error(f"🚨 **ESTADO CRÍTICO:** El espesor restante ({e_restante:.2f} mm) es inferior al límite de seguridad permitido ({emin:.2f} mm).")
    elif pct_perdida > 25:
        st.warning(f"⚠️ **ALERTA ESTRUCTURAL:** Se ha perdido más del 25% del espesor inicial del acero.")
    else:
        st.success(f"✅ **ESTADO ACEPTABLE:** El elemento mantiene su margen de seguridad estructural aceptable.")

    # GRÁFICA INTERACTIVA PLOTLY
    t_arr = np.linspace(0, t_exp, 100)
    e_arr = e0 - (vc_mm * t_arr) if modelo == "Modelo Lineal (Vc constante)" else e0 - (vc_mm * (t_arr**b_exp))

    fig = go.Figure()
    fig.add_
