import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y TEMÁTICA ESTÉTICA ROSA
# ---------------------------------------------------------
st.set_page_config(
    page_title="STEELIA | Corrosión del Acero",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilos CSS con alto contraste: texto café oscuro elegante sobre fondos rosa pastel
custom_css = """
<style>
    /* Fondo general de la aplicación */
    .stApp {
        background-color: #FFF0F4 !important;
        color: #3A1C24 !important;
        font-family: 'Segoe UI', -apple-system, sans-serif;
    }

    /* FORZAR VISIBILIDAD DEL MENÚ LATERAL (SIDEBAR) */
    section[data-testid="stSidebar"] {
        background-color: #FCE2EB !important;
        border-right: 2px solid #F8BBD0 !important;
    }

    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] div[role="radiogroup"] span {
        color: #4A1A2C !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }

    /* Encabezados */
    h1, h2, h3, h4, h5 {
        color: #A82250 !important;
        font-weight: 700 !important;
    }

    /* Tarjetas principales */
    .stCard {
        background-color: #FFFFFF !important;
        border-radius: 22px !important;
        padding: 26px !important;
        box-shadow: 0 8px 20px rgba(222, 115, 155, 0.12) !important;
        border: 2px solid #FAD2E1 !important;
        margin-bottom: 22px !important;
        color: #3A1C24 !important;
    }

    /* FORZAR CONTRASTE DE LAS TABLAS (ST.TABLE / ST.DATAFRAME) */
    div[data-testid="stTable"] table,
    div[data-testid="stDataFrame"] {
        color: #2D121A !important;
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
        border: 1px solid #F8BBD0 !important;
    }

    div[data-testid="stTable"] th {
        background-color: #FAD2E1 !important;
        color: #5C1D33 !important;
        font-weight: bold !important;
        font-size: 1.05rem !important;
    }

    div[data-testid="stTable"] td {
        color: #2D121A !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        background-color: #FFFFFF !important;
    }

    /* Banner superior rosado */
    .pink-header-card {
        background: linear-gradient(135deg, #FAD2E1 0%, #F5ABCE 100%) !important;
        border-radius: 24px !important;
        padding: 32px !important;
        color: #4A1A2C !important;
        box-shadow: 0 10px 25px rgba(222, 115, 155, 0.22) !important;
        margin-bottom: 28px !important;
        border: 1px solid #F8BBD0 !important;
    }

    /* Cajas de ecuaciones */
    .formula-box {
        background-color: #FFF0F5 !important;
        border-left: 6px solid #D81B60 !important;
        padding: 16px !important;
        border-radius: 14px !important;
        font-family: 'Courier New', monospace !important;
        color: #5C1D33 !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        margin: 14px 0 !important;
    }

    /* Estilo de botones en rosa fucsia/pastel */
    .stButton > button {
        background: linear-gradient(135deg, #E91E63 0%, #C2185B 100%) !important;
        color: white !important;
        border-radius: 16px !important;
        border: none !important;
        padding: 12px 28px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(233, 30, 99, 0.3) !important;
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
# 3. NAVEGACIÓN Y SIDEBAR CON ETIQUETAS VISIBLES
# ---------------------------------------------------------
st.sidebar.markdown("<h1 style='text-align: center; color: #A82250;'>💖 STEELIA</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #4A1A2C; font-size: 0.95em;'><b>Análisis & Corrosión del Acero</b><br>Ingeniería Civil México</p>", unsafe_allow_html=True)
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
        <h1 style="margin:0; font-size: 2.8rem; color: #4A1A2C;">🌸 STEELIA</h1>
        <h3 style="margin-top: 5px; color: #A82250; font-weight: 500;">
            Análisis y estimación de la corrosión del acero
        </h3>
        <p style="font-size: 1.15rem; margin-top: 15px;">
            Plataforma educativa e interactiva diseñada para evaluar la degradación electroquímica,
            la cinética de corrosión y la pérdida de espesor en elementos de acero estructural,
            contextualizada bajo la normativa de ingeniería civil de México.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.subheader("✨ Bienvenido a STEELIA")
        st.write(
            "STEELIA combina el rigor de la ciencia de los materiales con los criterios del "
            "**Capítulo 4 de las Normas Técnicas Complementarias (NTC-Concreto)** "
            "y los modelos cinéticos internacionales **ISO 9224**.\n\n"
            "Usa el menú interactivo a tu izquierda para navegar entre los módulos educativos "
            "y la calculadora de pérdida de espesor."
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="stCard" style="text-align: center;">', unsafe_allow_html=True)
        st.markdown("### 🧮 Acceso Rápido")
        st.info("Utiliza el panel lateral para ingresar a la **Calculadora de Corrosión**.")
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# SECCIÓN 2: ¿QUÉ ES LA CORROSIÓN DEL ACERO?
# ---------------------------------------------------------
elif menu == "¿Qué es la Corrosión?":
    st.title("🧪 Fundamentos Electroquímicos")
    st.write("La **corrosión del acero** es la degradación espontánea del hierro ($Fe$) inducida por reacciones de transferencia de electrones con el medio ambiente.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.markdown("### 1. Reacción Anódica (Oxidación)")
        st.write("El hierro metálico cede electrones y se disuelve:")
        st.markdown('<div class="formula-box">Fe → Fe²⁺ + 2e⁻</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.markdown("### 2. Reacción Catódica (Reducción)")
        st.write("El agua y el oxígeno consumen los electrones liberados:")
        st.markdown('<div class="formula-box">O₂ + 2H₂O + 4e⁻ → 4OH⁻</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="stCard">', unsafe_allow_html=True)
    st.markdown("### Formación de Herrumbre")
    st.write("Los iones $Fe^{2+}$ y $OH^-$ precipitan como hidróxido ferroso y reaccionan con más oxígeno para formar el óxido hidratado o herrumbre:")
    st.markdown('<div class="formula-box">4Fe(OH)₂ + O₂ + 2H₂O → 4Fe(OH)₃ → Fe₂O₃·H₂O</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# SECCIÓN 3: FACTORES INFLUYENTES
# ---------------------------------------------------------
elif menu == "Factores Influyentes":
    st.title("🌡️ Factores que Aceleran la Corrosión")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.markdown("### 💧 Humedad Relativa y Tiempo de Humedecimiento")
        st.write("A partir del 70-80% de humedad, se forma una película electrolítica sobre el acero que dispara la reacción electroquímica.")
        st.markdown("### 🌡️ Temperatura")
        st.write("Eleva la velocidad de las reacciones químicas cinéticas hasta que la evaporación reduce la humedad superficial.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.markdown("### 🌊 Salinidad y Cloruros (Cl⁻)")
        st.write("Destruyen las capas pasivantes protectoras del acero e incrementan fuertemente la conductividad del medio.")
        st.markdown("### 🏭 Contaminación ($SO_2$)")
        st.write("Típica de atmósferas urbanas e industriales, genera depósitos ácidos que aceleran la velocidad de deterioro.")
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# SECCIÓN 4: NORMATIVA MEXICANA (NTC)
# ---------------------------------------------------------
elif menu == "Normativa Mexicana (NTC)":
    st.title("🇲🇽 Clasificación Mexicana de Exposición (NTC-Concreto Cap. 4)")
    st.write("En México, la durabilidad de las estructuras se norma mediante las **Normas Técnicas Complementarias (NTC)**:")

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
# SECCIÓN 6: CALCULADORA INTERACTIVA DE CORROSIÓN
# ---------------------------------------------------------
elif menu == "Calculadora de Corrosión":
    st.title("🧮 Calculadora de Pérdida de Espesor")

    col_in, col_out = st.columns([1, 1])

    with col_in:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.markdown("### 1. Geometría del Elemento")
        e0 = st.number_input("Espesor inicial ($e_0$) en mm:", min_value=0.1, value=12.0, step=0.5)
        emin = st.number_input("Espesor mínimo permitido ($e_{min}$) en mm:", min_value=0.0, max_value=e0, value=8.0, step=0.5)
        t_exp = st.slider("Tiempo de exposición ($t$) en años:", min_value=1, max_value=100, value=25)

        st.markdown("### 2. Modelo Matemático")
        modelo = st.radio("Modelo de cálculo:", ["Modelo Lineal (Vc constante)", "Modelo Ley de Potencia (ISO 9224)"])

        st.markdown("### 3. Tasa de Corrosión")
        usar_manual = st.checkbox("Ingresar Vc manualmente", value=True)
        if usar_manual:
            vc_um = st.number_input("Velocidad ($V_c$) en µm/año:", min_value=0.1, value=65.0)
        else:
            cat_iso_sel = st.selectbox("Categoría de referencia ISO 9223:", list(ISO_DATA.keys()))
            vc_um = ISO_DATA[cat_iso_sel]["ref"]

        b_exp = 0.52
        if modelo == "Modelo Ley de Potencia (ISO 9224)":
            b_exp = st.slider("Exponente empírico ($b$):", min_value=0.10, max_value=1.00, value=0.52)
        st.markdown("</div>", unsafe_allow_html=True)

    vc_mm = vc_um / 1000.0
    if modelo == "Modelo Lineal (Vc constante)":
        delta_e = vc_mm * t_exp
    else:
        delta_e = vc_mm * (t_exp**b_exp)

    e_restante = e0 - delta_e
    pct_perdida = (delta_e / e0) * 100.0
    tasa_anual_mm = delta_e / t_exp

    with col_out:
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        st.markdown("### 📊 Resultados de la Estimación")
        st.metric("TASA DE PÉRDIDA DE ESPESOR ANUAL", f"{tasa_anual_mm:.4f} mm/año", delta=f"{vc_um:.1f} µm/año")

        m1, m2 = st.columns(2)
        m1.metric("Pérdida Acumulada (Δe)", f"{delta_e:.3f} mm")
        m2.metric("Espesor Restante", f"{e_restante:.3f} mm")

        if e_restante < emin:
            st.error("🚨 **ALERTA CRÍTICA:** El espesor restante es inferior al espesor mínimo estructural permitido.")
        else:
            st.success("✅ **ESTADO ACEPTABLE:** El elemento conserva el margen de seguridad.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Gráfica Plotly
    t_arr = np.linspace(0, t_exp, 100)
    e_arr = e0 - (vc_mm * t_arr) if modelo == "Modelo Lineal (Vc constante)" else e0 - (vc_mm * (t_arr**b_exp))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_arr, y=e_arr, mode="lines", name="Espesor Restante (mm)", line=dict(color="#D81B60", width=4)))
    fig.add_trace(go.Scatter(x=[0, t_exp], y=[emin, emin], mode="lines", name="Espesor Mínimo Límite", line=dict(color="#E91E63", dash="dash")))
    fig.update_layout(title="<b>Proyección Temporal del Espesor del Acero</b>", xaxis_title="Años", yaxis_title="Espesor (mm)", paper_bgcolor="#FFF0F4", plot_bgcolor="#FFFFFF")
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# SECCIÓN 7: MÉTODOS DE PROTECCIÓN
# ---------------------------------------------------------
elif menu == "Métodos de Protección":
    st.title("🛡️ Métodos de Protección Anticorrosiva")
    st.markdown("""
    <div class="stCard">
        <ul>
            <li><b>Pinturas y Recubrimientos:</b> Sistemas multicapa que forman barreras contra la humedad y el oxígeno.</li>
            <li><b>Galvanizado en Caliente:</b> Recubrimiento de zinc que actúa como ánodo de sacrificio.</li>
            <li><b>Protección Catódica:</b> Imposición de corrientes para mantener el acero en estado catódico.</li>
            <li><b>Acieros Patinables (Corten):</b> Aleaciones especiales que forman una pátina densa autoprotectora.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# SECCIÓN 8: APLICACIONES EN INGENIERÍA CIVIL (AMPLIADA)
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
    2. **Varillas de Refuerzo dentro del Concreto (NTC Capítulo 4):** El acero no interactúa libremente con el aire; está embebido en una matriz alcalina ($pH \approx 12.5 - 13.5$) que crea una **capa de pasivación**. La corrosión inicia únicamente cuando:
       * El frente de **carbonatación** alcanza el nivel de la varilla reduciendo el $pH$.
       * Los **iones cloruro** penetran el espesor de recubrimiento y rompen la pasivación.
       * *Consecuencia:* Al corroerse, la herrumbre ocupa hasta **6 veces el volumen del acero original**, generando presiones expansivas internas que agrietan y desprenden el recubrimiento de concreto (*spalling*).
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# SECCIÓN 9: ¿CÓMO UTILIZAR STEELIA?
# ---------------------------------------------------------
elif menu == "¿Cómo utilizar STEELIA?":
    st.title("📖 Guía de Uso")
    st.markdown("""
    1. Entra a la **Calculadora de Corrosión**.
    2. Ingresa el espesor inicial ($e_0$) y el mínimo permitido ($e_{min}$).
    3. Selecciona el modelo cinético deseado y ajusta los años de exposición.
    4. Observa los resultados automáticos y el gráfico dinámico.
    """)

# ---------------------------------------------------------
# SECCIÓN 10: REFERENCIAS APA 7
# ---------------------------------------------------------
elif menu == "Referencias APA 7":
    st.title("📚 Referencias Bibliográficas")
    st.markdown("""
    - **Gobierno de la Ciudad de México.** (2023). *Normas Técnicas Complementarias (NTC-Concreto, Capítulo 4: Durabilidad)*.
    - **International Organization for Standardization.** (2012). *Corrosion of metals and alloys* (ISO Standard No. 9223 / 9224:2012).
    """)
