import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y TEMÁTICA ROSA
# ---------------------------------------------------------
st.set_page_config(
    page_title="STEELIA | Corrosión del Acero en Ingeniería Civil",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilos CSS personalizados en tonalidades Rosa Pastel, Algodón de Azúcar, Blush y Cuarzo
custom_css = """
<style>
    /* Fondo principal y textos */
    .stApp {
        background-color: #FFF5F7;
        color: #5C3A45;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }

    /* Encabezados */
    h1, h2, h3, h4, h5 {
        color: #B84B70 !important;
        font-weight: 700;
    }

    /* Tarjetas y Contenedores */
    .stCard {
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 6px 20px rgba(222, 143, 171, 0.15);
        border: 2px solid #FAD6E1;
        margin-bottom: 20px;
    }

    .pink-header-card {
        background: linear-gradient(135deg, #FAD6E1 0%, #F5C2D3 100%);
        border-radius: 20px;
        padding: 30px;
        color: #7A2443;
        box-shadow: 0 8px 25px rgba(222, 143, 171, 0.25);
        margin-bottom: 25px;
    }

    /* Botones primarios */
    .stButton > button {
        background: linear-gradient(135deg, #E06D92 0%, #B84B70 100%);
        color: white !important;
        border-radius: 14px;
        border: none;
        padding: 12px 28px;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(184, 75, 112, 0.3);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #B84B70 0%, #8A2D4F 100%);
        box-shadow: 0 6px 20px rgba(138, 45, 79, 0.4);
        transform: translateY(-2px);
    }

    /* Cajas de fórmulas y ecuaciones */
    .formula-box {
        background-color: #FFF0F4;
        border-left: 5px solid #E06D92;
        padding: 16px;
        border-radius: 12px;
        font-family: 'Courier New', Courier, monospace;
        color: #7A2443;
        font-weight: bold;
        margin: 12px 0;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #FCE8EF;
        border-right: 2px solid #F7C8D8;
    }

    /* Pestañas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #F8DCE5;
        border-radius: 10px 10px 0 0;
        color: #7A2443;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #B84B70 !important;
        color: white !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. DATOS DE REFERENCIA NORMATIVA (MÉXICO E ISO)
# ---------------------------------------------------------
NTC_CATEGORIES = {
    "A1": "Elementos protegidos por membrana impermeable o superficies interiores enceradas.",
    "A2": "Suelos no agresivos y ambientes exteriores no agresivos.",
    "B1": "Interiores con humedecimiento/secado repetido, exteriores ligeramente agresivos y agua dulce dura.",
    "B2": "Ambientes exteriores agresivos y ciertas exposiciones a agua con cloruros.",
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
    "<h1 style='text-align: center; color: #B84B70;'>🌸 STEELIA</h1>",
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    "<p style='text-align: center; color: #7A2443; font-size: 0.9em;'>"
    "Análisis y Estimación de Corrosión en Acero<br>"
    "<b>Contexto Técnico de México</b></p>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Selecciona una sección:",
    [
        "Portada",
        "¿Qué es la Corrosión?",
        "Factores Influyentes",
        "Normativa Mexicana (NTC)",
        "Contexto de México",
        "Calculadora de Corrosión",
        "Métodos de Protección",
        "Aplicaciones en Ingeniería Civil",
        "¿Cómo utilizar STEELIA?",
        "Referencias APA 7",
    ],
)

# ---------------------------------------------------------
# SECCIÓN 1: PORTADA
# ---------------------------------------------------------
if menu == "Portada":
    st.markdown(
        """
    <div class="pink-header-card">
        <h1 style="margin:0; font-size: 2.8rem; color: #7A2443;">STEELIA</h1>
        <h3 style="margin-top: 5px; color: #A33A5E; font-weight: 400;">
            Análisis y estimación de la corrosión del acero
        </h3>
        <p style="font-size: 1.1rem; margin-top: 15px;">
            Plataforma interactiva especializada en la evaluación cinético-electroquímica,
            degradación atmosférica y cálculo de pérdida de espesor de acero estructural
            adaptada al marco de la ingeniería civil en México.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.subheader("Bienvenida / Propósito Institucional")
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
        st.markdown("### Acceso Rápido")
        st.write("Accede directamente a los módulos principales:")
        st.info("💡 Usa el menú lateral para ir a la **Calculadora de Corrosión**.")
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# SECCIÓN 2: ¿QUÉ ES LA CORROSIÓN DEL ACERO?
# ---------------------------------------------------------
elif menu == "¿Qué es la Corrosión?":
    st.title(" Fundamentos Electroquímicos de la Corrosión")

    st.write(
        "La **corrosión del acero** es la degradación físico-química espontánea "
        "del hierro metálico ($Fe$) inducida por su reacción electroquímica con el entorno "
        "atmosférico, regresando al material a su estado termodinámico más estable."
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
        st.write("En presencia de agua y oxígeno disuelto, los electrones son consumidos:")
        st.markdown(
            '<div class="formula-box">O₂ + 2H₂O + 4e⁻ → 4OH⁻</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="stCard">', unsafe_allow_html=True)
    st.markdown("### Formación de Herrumbre (Producto Final)")
    st.write(
        "Los iones $Fe^{2+}$ y $OH^-$ precipitan inicialmente como hidróxido ferroso $Fe(OH)_2$, "
        "el cual se oxida a hidróxido férrico $Fe(OH)_3$ y finalmente a óxido de hierro hidratado:"
    )
    st.markdown(
        '<div class="formula-box">4Fe(OH)₂ + O₂ + 2H₂O → 4Fe(OH)₃ → Fe₂O₃·H₂O</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# SECCIÓN 3: NORMATIVA MEXICANA (NTC)
# ---------------------------------------------------------
elif menu == "Normativa Mexicana (NTC)":
    st.title("🇲🇽 Clasificación Mexicana de Exposición (NTC-Concreto Capítulo 4)")

    st.write(
        "En México, el marco normativo de referencia para la durabilidad en edificación está regido "
        "por las **Normas Técnicas Complementarias para Diseño y Construcción de Estructuras "
        "de Concreto (Capítulo 4)** del Reglamento de Construcciones."
    )

    st.info(
        "📌 **Nota de Aplicación Normativa:** Las categorías A1 a D corresponden a la "
        "clasificación mexicana de exposición en estructuras de concreto reforzado. Para evaluar "
        "la corrosión del acero estructural desnudo expuesto a la atmósfera, STEELIA permite "
        "complementar estos escenarios con tasas de corrosión ($V_c$) medidas localmente o "
        "referencias de la norma internacional **ISO 9223**."
    )

    df_ntc = pd.DataFrame(
        [
            {"Categoría NTC": k, "Condición de Exposición Oficial": v}
            for k, v in NTC_CATEGORIES.items()
        ]
    )
    st.table(df_ntc)

# ---------------------------------------------------------
# SECCIÓN 4: CALCULADORA INTERACTIVA DE CORROSIÓN
# ---------------------------------------------------------
elif menu == "Calculadora de Corrosión":
    st.title("🧮 Calculadora de Corrosión y Pérdida de Espesor")
    st.write(
        "Introduce los datos geométricos del elemento estructural y las condiciones "
        "cinéticas para calcular la degradación temporal."
    )

    col_in, col_out = st.columns([1, 1])

    with col_in:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.markdown("### 1. Parámetros Geométricos")
        e0 = st.number_input(
            "Espesor inicial ($e_0$) en mm:",
            min_value=0.1,
            max_value=200.0,
            value=12.0,
            step=0.5,
        )
        emin = st.number_input(
            "Espesor mínimo permitido ($e_{min}$) en mm:",
            min_value=0.0,
            max_value=e0,
            value=8.0,
            step=0.5,
        )
        t_exp = st.slider(
            "Tiempo de exposición ($t$) en años:", min_value=1, max_value=100, value=25
        )

        st.markdown("### 2. Selección del Modelo")
        modelo = st.radio(
            "Modelo Matemático:",
            ["Modelo Lineal (Vc constante)", "Modelo Ley de Potencia (ISO 9224)"],
        )

        st.markdown("### 3. Velocidad de Corrosión")
        usar_manual = st.checkbox("Ingresar Vc medida manualmente", value=True)
        if usar_manual:
            vc_um = st.number_input(
                "Velocidad de corrosión ($V_c$) en µm/año:", min_value=0.1, value=65.0
            )
        else:
            cat_iso_sel = st.selectbox(
                "Referencia ISO 9223 complementaria:", list(ISO_DATA.keys())
            )
            vc_um = ISO_DATA[cat_iso_sel]["ref"]
            st.caption(f"Valor representativo seleccionado: {vc_um} µm/año")

        b_exp = 0.52
        if modelo == "Modelo Ley de Potencia (ISO 9224)":
            b_exp = st.slider(
                "Exponente empírico ($b$):",
                min_value=0.10,
                max_value=1.00,
                value=0.52,
                step=0.01,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    # Conversiones y cálculos
    vc_mm = vc_um / 1000.0  # 1 mm = 1000 µm

    if modelo == "Modelo Lineal (Vc constante)":
        delta_e = vc_mm * t_exp
    else:
        delta_e = vc_mm * (t_exp**b_exp)

    e_restante = e0 - delta_e
    pct_perdida = (delta_e / e0) * 100.0
    tasa_anual_mm = delta_e / t_exp

    with col_out:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.markdown("###  Resultados Principales")

        st.metric(
            " TASA DE PÉRDIDA DE ESPESOR ANUAL",
            f"{tasa_anual_mm:.4f} mm/año",
            delta=f"{vc_um:.1f} µm/año",
        )

        m1, m2 = st.columns(2)
        m1.metric("Pérdida Acumulada (Δe)", f"{delta_e:.3f} mm")
        m2.metric("Espesor Restante", f"{e_restante:.3f} mm")

        m3, m4 = st.columns(2)
        m3.metric("Porcentaje de Pérdida", f"{pct_perdida:.1f} %")
        m4.metric("Tiempo Evaluado", f"{t_exp} años")

        st.markdown("---")
        if e_restante < emin:
            st.error(
                f"🚨 **ESTADO CRÍTICO:** El espesor estimado ({e_restante:.2f} mm) ha descendido "
                f"por debajo del límite mínimo permitido ({emin:.2f} mm)."
            )
        elif pct_perdida > 25:
            st.warning("⚠️ **ALERTA ESTRUCTURAL:** Pérdida superior al 25% del espesor inicial.")
        else:
            st.success("✅ **ESTADO ACEPTABLE:** El elemento mantiene su margen de seguridad.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Graficación Plotly
    t_arr = np.linspace(0, t_exp, 100)
    if modelo == "Modelo Lineal (Vc constante)":
        e_arr = e0 - (vc_mm * t_arr)
    else:
        e_arr = e0 - (vc_mm * (t_arr**b_exp))

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=t_arr,
            y=e_arr,
            mode="lines",
            name="Espesor Restante (mm)",
            line=dict(color="#B84B70", width=4),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[0, t_exp],
            y=[emin, emin],
            mode="lines",
            name="Espesor Mínimo Límite (emin)",
            line=dict(color="#E06D92", width=2, dash="dash"),
        )
    )

    fig.update_layout(
        title="<b>Evolución del Espesor del Acero a través del Tiempo</b>",
        xaxis_title="Tiempo de Exposición (años)",
        yaxis_title="Espesor (mm)",
        paper_bgcolor="#FFF5F7",
        plot_bgcolor="#FFFFFF",
        font=dict(color="#5C3A45"),
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# SECCIÓN 5: REFERENCIAS APA 7
# ---------------------------------------------------------
elif menu == "Referencias APA 7":
    st.title("📚 Referencias Bibliográficas")
    st.markdown(
        """
    - **Gobierno de la Ciudad de México.** (2023). *Normas Técnicas Complementarias para Diseño
      y Construcción de Estructuras de Concreto (NTC-Concreto, Capítulo 4: Durabilidad)*.
      Gaceta Oficial de la Ciudad de México.
    - **International Organization for Standardization.** (2012). *Corrosion of metals and
      alloys — Corrosivity of atmospheres — Classification, determination and estimation*
      (ISO Standard No. 9223:2012).
    - **International Organization for Standardization.** (2012). *Corrosion of metals and
      alloys — Corrosivity of atmospheres — Guiding values for the corrosivity categories*
      (ISO Standard No. 9224:2012).
    - **Revie, R. W., & Uhlig, H. H.** (2008). *Corrosion and corrosion control: An introduction
      to corrosion science and engineering* (4th ed.). John Wiley & Sons.
    """
    )