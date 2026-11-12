import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y TEMÁTICA ROSA DE MÁXIMO CONTRASTE
# ---------------------------------------------------------
st.set_page_config(
    page_title="STEELIA | Corrosión del Acero en Ingeniería Civil",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilos CSS de contraste absoluto para legibilidad 100% garantizada
custom_css = """
<style>
    /* Fondo general rosado suave */
    .stApp {
        background-color: #FFF0F4 !important;
        color: #2D0814 !important;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }

    /* FORZAR TEXTO VINO MUY OSCURO EN TODOS LOS TEXTOS GLOBALES, LABELS E INPUTS */
    p, span, label, div, li, input, select, textarea, .stMarkdown {
        color: #2D0814 !important;
        font-weight: 500;
    }

    /* MENÚ LATERAL (SIDEBAR): FONDO ROSA FRESCO CON TEXTO BORGOÑA PROFUNDO */
    section[data-testid="stSidebar"] {
        background-color: #F8C8DC !important;
        border-right: 3px solid #F080A8 !important;
    }

    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] div[role="radiogroup"] span,
    section[data-testid="stSidebar"] p {
        color: #380B1D !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
    }

    /* ENCABEZADOS DE SECCIÓN Y TÍTULOS */
    h1, h2, h3, h4, h5 {
        color: #800A38 !important;
        font-weight: 800 !important;
    }

    /* TARJETAS BLANCAS CON TEXTO MUY OSCURO Y BORDES ROSA PASTEL */
    .stCard {
        background-color: #FFFFFF !important;
        border-radius: 24px !important;
        padding: 28px !important;
        box-shadow: 0 10px 25px rgba(216, 27, 96, 0.12) !important;
        border: 2px solid #F4A5C2 !important;
        margin-bottom: 24px !important;
        color: #2D0814 !important;
    }

    .stCard p, .stCard li, .stCard div {
        color: #2D0814 !important;
    }

    /* CAJAS DE INFORMACIÓN Y ALERTAS NATIVAS DE STREAMLIT */
    div[data-testid="stAlert"] {
        background-color: #FFF5F8 !important;
        border: 2px solid #F06292 !important;
        border-radius: 16px !important;
    }
    div[data-testid="stAlert"] p {
        color: #380B1D !important;
        font-weight: 700 !important;
    }

    /* TARJETAS DE RESULTADO DE CALCULADORA (TEXTO VINO OSCURO / VALORES INTENSOS) */
    .metric-card-pink {
        background: linear-gradient(135deg, #FFFFFF 0%, #FFF0F5 100%) !important;
        border: 2px solid #E91E63 !important;
        border-radius: 20px !important;
        padding: 20px !important;
        text-align: center !important;
        box-shadow: 0 6px 18px rgba(233, 30, 99, 0.2) !important;
    }

    .metric-title {
        font-size: 0.95rem !important;
        font-weight: 800 !important;
        color: #800A38 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }

    .metric-value {
        font-size: 1.8rem !important;
        font-weight: 900 !important;
        color: #AD1457 !important;
        margin-top: 5px !important;
    }

    /* BANNER ENCABEZADO ROSA INTENSO CON TEXTO BORGOÑA ULTRA CONTRASTADO */
    .pink-header-card {
        background: linear-gradient(135deg, #F8A5C2 0%, #F472B6 100%) !important;
        border-radius: 28px !important;
        padding: 35px !important;
        color: #260511 !important;
        box-shadow: 0 12px 30px rgba(233, 30, 99, 0.25) !important;
        margin-bottom: 30px !important;
        border: 2px solid #EC4899 !important;
    }

    .pink-header-card h1, .pink-header-card h2, .pink-header-card h3, .pink-header-card p {
        color: #260511 !important;
    }

    /* CAJAS DE FÓRMULAS QUÍMICAS / MATEMÁTICAS */
    .formula-box {
        background-color: #FFF0F5 !important;
        border-left: 6px solid #C2185B !important;
        padding: 18px !important;
        border-radius: 16px !important;
        font-family: 'Courier New', monospace !important;
        color: #260511 !important;
        font-weight: bold !important;
        font-size: 1.15rem !important;
        margin: 16px 0 !important;
    }

    /* CONTROLES DE ENTRADA (INPUTS, NUMBERS, SELECTS) */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 2px solid #E91E63 !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="input"] input {
        color: #260511 !important;
        font-weight: 700 !important;
    }

    /* TABLAS Y DATAFRAMES CON MÁXIMA LEGIBILIDAD (ENCABEZADO OSCURO, FONT OSCURA) */
    div[data-testid="stTable"] table {
        color: #260511 !important;
        background-color: #FFFFFF !important;
        border-radius: 16px !important;
        border: 2px solid #F48FB1 !important;
        overflow: hidden !important;
    }

    div[data-testid="stTable"] th {
        background-color: #F8A5C2 !important;
        color: #260511 !important;
        font-weight: 900 !important;
        font-size: 1.05rem !important;
    }

    div[data-testid="stTable"] td {
        color: #260511 !important;
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
    "<h1 style='text-align: center; color: #800A38;'>🌸 STEELIA</h1>",
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    "<p style='text-align: center; color: #260511; font-size: 0.95em;'><b>Análisis & Corrosión del Acero</b><br>Ingeniería Civil México</p>",
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
        <h1 style="margin:0; font-size: 3rem; color: #260511;">💖 STEELIA</h1>
        <h3 style="margin-top: 8px; color: #500523; font-weight: 800;">
            Análisis y estimación de la corrosión del acero
        </h3>
        <p style="font-size: 1.2rem; margin-top: 15px; color: #260511; font-weight: 600;">
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
        st.info("💡 Usa el menú desplegable ubicado en la barra lateral izquierda para ingresar a la **Calculadora de Corrosión**.")
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
# SECCIÓN 5: CONTEXTO DE MÉXICO (EXTENDIDO Y ESPECTACULAR)
# ---------------------------------------------------------
elif menu == "Contexto de México":
    st.title("🌴 Panorama de la Corrosión Atmosférica en México")
    st.write(
        "México cuenta con más de **11,000 kilómetros de litorales marítimos** y una gran variedad de microclimas. "
        "La interacción entre la alta humedad relativa, las elevadas temperaturas y los vientos cargados de aerosol marino (cloruros) "
        "convierte al país en un laboratorio natural complejo donde la velocidad de deterioro del acero estructural puede variar drásticamente según la región."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.markdown("### ☀️ 1. Sureste y Península de Yucatán (Campeche, Tabasco, Quintana Roo, Yucatán)")
        st.write("""
        * **Severidad Ambiental:** Extremadamente alta (Categorías C4 a C5 / Exposiciones NTC C y D).
        * **Mecanismo Dominante:** Alta humedad relativa ($>80\%$ constante), altas temperaturas medias y vientos alisios que arrastran sales de cloruro ($Cl^-$) desde el Golfo de México y Mar Caribe.
        * **Tiempo de Humedecimiento (*TOW*):** Muy prolongado debido al clima cálido-húmedo tropical. La película de rocío depositada sobre los perfiles de acero durante la noche permanece líquida durante muchas horas, acelerando la corrosión anódica.
        * **Infraestructura Afectada:** Puentes marinos, muelles, terminales petroleras marítimas y edificaciones urbanas costeras.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.markdown("### 🏭 3. Zonas Urbanas e Industriales del Interior (CDMX, Monterrey, Guadalajara)")
        st.write("""
        * **Severidad Ambiental:** Moderada a Alta (Categorías C2 a C4 / Exposiciones NTC B1 a B2).
        * **Mecanismo Dominante:** Corrosión impulsada por acidificación del aire por emisión de dióxido de azufre ($SO_2$) y óxidos de nitrógeno ($NO_x$) provenientes del parque vehicular y plantas industriales.
        * **Impacto en Obras:** Naves industriales, puentes peatonales en avenidas principales y estructuras de soporte en subestaciones eléctricas.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.markdown("### 🌊 2. Litorales del Golfo de México y Pacífico (Veracruz, Tamaulipas, Sinaloa, Guerrero)")
        st.write("""
        * **Severidad Ambiental:** Alta a Extrema (Categorías C4 a CX / Exposición NTC C).
        * **Mecanismo Dominante:** Fuerte brisa marina y bruma salina. Eventos meteorológicos como los "Nortes" en el Golfo transportan partículas de sal varios kilómetros tierra adentro.
        * **Depósito de Cloruros:** Los cristales de sal depositados sobre el acero son altamente higroscópicos (absorben agua del aire a humedades relativas tan bajas como el 75%), manteniendo el acero mojado y conduciendo corriente eléctrica a velocidades elevadas.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.markdown("### 🇲🇽 4. Fuentes Oficiales de Información Climático-Técnica en México")
        st.write("""
        Para el cálculo de durabilidad y selección de recubrimientos en proyectos de ingeniería civil en México, se consultan datos oficiales de:
        * **CONAGUA y Servicio Meteorológico Nacional (SMN):** Promedios anuales de Humedad Relativa (HR), Temperatura ($T$) y Precipitación Pluvial.
        * **Instituto Mexicano del Transporte (IMT):** Mapas de corrosividad en la red carretera nacional y puentes de la SCT.
        * **IMTA y Redes de Monitoreo Atmosférico:** Medición de contaminantes acidificantes ($SO_2$).
        """)
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# SECCIÓN 6: CALCULADORA INTERACTIVA DE CORROSIÓN
# ---------------------------------------------------------
elif menu == "Calculadora de Corrosión":
    st.markdown("""
    <div class="pink-header-card" style="padding: 24px; margin-bottom: 20px;">
        <h2 style="margin:0; color: #260511;">🧮 Calculadora de Corrosión y Pérdida de Espesor</h2>
        <p style="margin-top: 5px; color: #260511; font-weight: 700;">
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

    # MÉTRICAS ESTILIZADAS EN ROSA DE ALTO IMPACTO Y TEXTO OSCURO NÍTIDO
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
    fig.add_trace(go.Scatter(x=t_arr, y=e_arr, mode="lines", name="Espesor Restante (mm)", line=dict(color="#C2185B", width=4)))
    fig.add_trace(go.Scatter(x=[0, t_exp], y=[emin, emin], mode="lines", name="Espesor Mínimo (emin)", line=dict(color="#D81B60", width=2, dash="dash")))

    fig.update_layout(
        title="<b>Curva Temporal de Pérdida de Espesor del Acero</b>",
        xaxis_title="Tiempo de Exposición (años)",
        yaxis_title="Espesor (mm)",
        paper_bgcolor="#FFF0F5",
        plot_bgcolor="#FFFFFF",
        font=dict(color="#260511", size=13),
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# SECCIÓN 7: MÉTODOS DE PROTECCIÓN
# ---------------------------------------------------------
elif menu == "Métodos de Protección":
    st.title("🛡️ Métodos de Protección Anticorrosiva")
    st.markdown("""
    <div class="stCard">
        <ul>
            <li><b>Pinturas y Recubrimientos:</b> Sistemas multicapa que forman barreras físicas contra la humedad y el oxígeno.</li>
            <li><b>Galvanizado en Caliente:</b> Inmersión en zinc fundido que actúa como ánodo galvánico de sacrificio.</li>
            <li><b>Protección Catódica:</b> Imposición de corriente continua para mantener el acero estructural como cátodo.</li>
            <li><b>Acieros Patinables (Corten):</b> Aleaciones especiales con Cu, Cr y Ni que forman una pátina densa autoprotectora.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# SECCIÓN 8: APLICACIONES EN INGENIERÍA CIVIL
# ---------------------------------------------------------
elif menu == "Aplicaciones en Ingeniería":
    st.title("🏗️ Relevancia de la Corrosión en la Ingeniería Civil")
    st.write(
        "El fenómeno de la corrosión representa uno de los mayores desafíos de **durabilidad, seguridad estructural y costos de mantenimiento** "
        "en la infraestructura moderna. En el diseño de ingeniería civil, la pérdida no controlada de sección transversal de acero "
        "modifica directamente la capacidad de carga, la rigidez y el comportamiento dinámico de las obras."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.markdown("### 🌉 1. Puentes Metálicos y Mixtos")
        st.write("""
        Los puentes vehiculares y peatonales están expuestos de forma continua a vibraciones, ciclos de carga (fatiga) y agentes atmosféricos.
        * **Fatiga por Corrosión (*Corrosion Fatigue*):** La presencia de picaduras (*pitting*) por micro-corrosión genera **concentradores de esfuerzos**. Bajo cargas cíclicas de tráfico, estas picaduras aceleran la iniciación y propagación de grietas por fatiga, provocando fallas frágiles repentinas.
        * **Zonas Críticas:** Uniones soldadas, nodos atornillados, placas de apoyo y la cara inferior del tablero donde la humedad condensada tarda en evaporarse.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.markdown("### 🌊 3. Infraestructura Marítima y Costera")
        st.write("""
        Las obras ubicadas en frentes costeros (muelles, espigones, plataformas y puentes marinos) enfrentan las condiciones más severas (Categorías C5/CX):
        * **Zona de Salpicaduras y Mareas (*Splash Zone*):** Es el área de mayor agresividad, ya que combina un suministro continuo de oxígeno con el humedecimiento por oleaje y altas concentraciones de cloruros ($Cl^-$).
        * **Pilotaje Metálico:** Pérdida de espesor acelerada en pilotes de acero estructural que soportan muelles, exigiendo sistemas combinados de recubrimiento epóxico espeso y **protección catódica con ánodos galvánicos de aluminio o zinc**.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.markdown("### 🏢 2. Edificios y Naves Industriales")
        st.write("""
        En la edificación urbana e industrial, la corrosión afecta principalmente a elementos estructurales sustentantes:
        * **Columnas y Trabes Expuestas:** La reducción del espesor de patines y almas en perfiles estructurales (secciones I, H, PTR) reduce directamente el momento de inercia ($I$) y el área de la sección ($A$).
        * **Riesgo de Pandeo Local y Global:** Al disminuir el espesor ($t$) de una placa sometida a compresión, aumenta drásticamente su esbeltez ($b/t$), haciendo a la columna susceptible de fallar por pandeo elástico a cargas menores de las calculadas originalmente.
        * **Ambientes Industriales Químicos:** Procesos de manufactura que emiten gases ácidos o vapores corrosivos requieren esquemas de inspección ultrasonográfica periódica.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.markdown("### 📐 4. Criterios de Sobreespesor (*Corrosion Allowance*)")
        st.write("""
        En la práctica del diseño estructural preventivo en zonas de alta corrosividad:
        * El estructuralista define un **espesor sacrificable de corrosión ($e_{sacrif}$)** adicional al espesor libre de esfuerzos requerido por cálculo.
        * Herramientas como **STEELIA** permiten predecir el tiempo exacto en que la velocidad de corrosión ($V_c$) consumirá ese sobreespesor, programando mantenimientos preventivos antes de comprometer la integridad del edificio.
        """)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="stCard">', unsafe_allow_html=True)
    st.markdown("### ⚡ 5. Diferenciación Crítica: Acero Desnudo vs. Varillas en Concreto Reforzado")
    st.write("""
    Es fundamental que el ingeniero civil distinga claramente los dos escenarios de estudio de la corrosión:
    
    1. **Acero Estructural Expuesto (Objeto de cálculo directo en STEELIA):** El metal interactúa directamente con la atmósfera libre. Su tasa de degradación se mide lineal o exponencialmente en micras por año ($\mu m/\text{año}$) según la humedad y contaminación ambiental.
    2. **Varillas de Refuerzo dentro del Concreto (NTC Capítulo 4):** El acero no interactúa libremente con el aire; está embebido en una matriz alcalina ($pH \approx 12.5 - 13.5$) que crea una **capa de pasivación**. La corrosión inicia únicamente cuando el frente de carbonatación o los cloruros rompen dicha pasivación, generando presiones expansivas internas que agrietan el concreto (*spalling*).
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# SECCIÓN 9: ¿CÓMO UTILIZAR STEELIA?
# ---------------------------------------------------------
elif menu == "¿Cómo utilizar STEELIA?":
    st.title("📖 Guía de Uso")
    st.markdown("""
    1. Dirígete a la **Calculadora de Corrosión** en el menú lateral.
    2. En la pestaña **1. Geometría**, introduce el espesor inicial ($e_0$), el mínimo permitido ($e_{min}$) y el tiempo.
    3. En la pestaña **2. Modelo**, selecciona entre el modelo Lineal o el de Ley de Potencia (ISO 9224).
    4. En la pestaña **3. Velocidad**, ajusta la tasa $V_c$ manualmente o selecciona una categoría ISO de referencia.
    5. Revisa el panel de tarjetas de resultados numéricos y la gráfica temporal interactiva.
    """)

# ---------------------------------------------------------
# SECCIÓN 10: REFERENCIAS APA 7
# ---------------------------------------------------------
elif menu == "Referencias APA 7":
    st.title("📚 Referencias Bibliográficas")
    st.markdown("""
    - **Gobierno de la Ciudad de México.** (2023). *Normas Técnicas Complementarias para Diseño y Construcción de Estructuras de Concreto (NTC-Concreto, Capítulo 4: Durabilidad)*. Gaceta Oficial de la Ciudad de México.
    - **International Organization for Standardization.** (2012). *Corrosion of metals and alloys — Corrosivity of atmospheres — Classification, determination and estimation* (ISO Standard No. 9223:2012 / 9224:2012).
    - **Revie, R. W., & Uhlig, H. H.** (2008). *Corrosion and corrosion control: An introduction to corrosion science and engineering* (4th ed.). John Wiley & Sons.
    """)

    fig = go.Figure()
    fig.add_
