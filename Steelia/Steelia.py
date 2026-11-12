import numpy as np
import pandas as pd
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

# Estilos CSS avanzados: Fondo rosa pastel + Tarjetas limpias + Texto vino oscuro
custom_css = """
<style>
    /* Fondo general rosado suave */
    .stApp {
        background-color: #FFF0F4 !important;
        color: #260511 !important;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }

    /* FORZAR TEXTO VINO MUY OSCURO EN TODOS LOS TEXTOS GLOBALES */
    p, span, label, div, li, .stMarkdown {
        color: #260511 !important;
    }

    /* FORZAR CAJAS DE ENTRADA NUMÉRICA Y SELECTORES SIEMPRE BLANCOS CON LETRA OSCURA */
    div[data-baseweb="input"],
    div[data-baseweb="base-input"],
    div[data-baseweb="select"] > div,
    input[type="number"],
    input[type="text"] {
        background-color: #FFFFFF !important;
        color: #260511 !important;
        -webkit-text-fill-color: #260511 !important;
        border-color: #E91E63 !important;
        font-weight: 700 !important;
    }

    /* Botones + y - de los number_input */
    button[data-testid="stNumberInputStepDown"],
    button[data-testid="stNumberInputStepUp"] {
        background-color: #FCE2EB !important;
        color: #800A38 !important;
    }

    /* Listas desplegables abiertas */
    ul[role="listbox"], ul[role="listbox"] li {
        background-color: #FFFFFF !important;
        color: #260511 !important;
    }

    /* MENÚ LATERAL (SIDEBAR) */
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

    /* ENCABEZADOS */
    h1, h2, h3, h4, h5 {
        color: #800A38 !important;
        font-weight: 800 !important;
    }

    /* TARJETAS BLANCAS INTEGRALES (SIN CONTENEDORES VACÍOS) */
    .stCard {
        background-color: #FFFFFF !important;
        border-radius: 22px !important;
        padding: 26px !important;
        box-shadow: 0 8px 22px rgba(216, 27, 96, 0.12) !important;
        border: 2px solid #F4A5C2 !important;
        margin-bottom: 22px !important;
    }

    .stCard h3 {
        margin-top: 0 !important;
        color: #800A38 !important;
        border-bottom: 2px solid #FCE2EB;
        padding-bottom: 8px;
        margin-bottom: 14px;
    }

    /* ALERTAS NATIVAS */
    div[data-testid="stAlert"],
    div[data-testid="stAlert"] > div {
        background-color: #FFE4EE !important;
        border: 2px solid #E91E63 !important;
        border-radius: 16px !important;
    }
    div[data-testid="stAlert"] * {
        color: #260511 !important;
        font-weight: 700 !important;
    }

    /* TARJETAS DE MÉTRICAS EN CALCULADORA */
    .metric-card-pink {
        background: linear-gradient(135deg, #FFFFFF 0%, #FFE8F0 100%) !important;
        border: 2px solid #E91E63 !important;
        border-radius: 20px !important;
        padding: 18px !important;
        text-align: center !important;
        box-shadow: 0 6px 18px rgba(233, 30, 99, 0.18) !important;
    }

    .metric-title {
        font-size: 0.85rem !important;
        font-weight: 800 !important;
        color: #800A38 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }

    .metric-value {
        font-size: 1.7rem !important;
        font-weight: 900 !important;
        color: #AD1457 !important;
        margin-top: 4px !important;
    }

    /* BANNER ENCABEZADO */
    .pink-header-card {
        background: linear-gradient(135deg, #F8A5C2 0%, #F472B6 100%) !important;
        border-radius: 26px !important;
        padding: 30px !important;
        box-shadow: 0 12px 30px rgba(233, 30, 99, 0.22) !important;
        margin-bottom: 26px !important;
        border: 2px solid #EC4899 !important;
    }
    .pink-header-card * {
        color: #260511 !important;
    }

    /* CAJAS DE FÓRMULAS */
    .formula-box {
        background-color: #FFF0F5 !important;
        border-left: 6px solid #C2185B !important;
        padding: 14px 18px !important;
        border-radius: 12px !important;
        font-family: 'Courier New', monospace !important;
        color: #260511 !important;
        font-weight: bold !important;
        font-size: 1.15rem !important;
        margin: 12px 0 !important;
    }

    /* TABLAS */
    div[data-testid="stTable"] table {
        background-color: #FFFFFF !important;
        border-radius: 16px !important;
        border: 2px solid #F48FB1 !important;
    }
    div[data-testid="stTable"] th {
        background-color: #F8A5C2 !important;
        color: #260511 !important;
        font-weight: 900 !important;
    }
    div[data-testid="stTable"] td {
        color: #260511 !important;
        background-color: #FFFFFF !important;
    }

    /* BOTONES */
    .stButton > button {
        background: linear-gradient(135deg, #E91E63 0%, #AD1457 100%) !important;
        color: #FFFFFF !important;
        border-radius: 14px !important;
        border: none !important;
        font-weight: 700 !important;
    }
    .stButton > button p {
        color: #FFFFFF !important;
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
        <h1 style="margin:0; font-size: 3rem;">💖 STEELIA</h1>
        <h3 style="margin-top: 8px; font-weight: 800;">
            Análisis y estimación de la corrosión del acero
        </h3>
        <p style="font-size: 1.2rem; margin-top: 15px; font-weight: 600;">
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
        st.markdown(
            """
        <div class="stCard">
            <h3>✨ Propósito Institucional</h3>
            <p>
                <b>STEELIA</b> es una herramienta técnico-educativa desarrollada en Python
                que integra los modelos cinéticos lineales y de potencia (ISO 9224) con las categorías
                de exposición de las <b>Normas Técnicas Complementarias de México (NTC-Concreto Capítulo 4)</b>.
            </p>
            <p>
                Permite evaluar la pérdida anual de espesor, estimar la vida útil residual
                de elementos de acero estructural expuestos a la atmósfera y prevenir fallas
                catastróficas en la infraestructura nacional.
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="stCard" style="text-align: center;">
            <h3>🧮 Calculadora Interactiva</h3>
            <p>
                Simula en tiempo real el desgaste estructural del acero, compara modelos matemáticos
                y evalúa la vida útil remanente según distintos microclimas de México.
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.info("💡 Selecciona **Calculadora de Corrosión** en el menú lateral izquierdo para iniciar.")

# ---------------------------------------------------------
# SECCIÓN 2: ¿QUÉ ES LA CORROSIÓN DEL ACERO?
# ---------------------------------------------------------
elif menu == "¿Qué es la Corrosión?":
    st.title("🧪 Fundamentos Electroquímicos de la Corrosión")
    st.write(
        "La **corrosión** se define como el deterioro físico-químico destructivo de un metal debido a su reacción "
        "electroquímica espontánea con el medio ambiente. Mientras que la **oxidación** describe específicamente "
        "la pérdida de electrones de un átomo, la corrosión engloba todo el sistema de celda galvánica que devuelve "
        "al acero manufacturado a su estado mineral termodinámicamente estable (óxidos e hidróxidos de hierro)."
    )

    st.markdown(
        """
    <div class="stCard">
        <h3>⚙️ Los 4 Componentes Indispensables de la Celda de Corrosión</h3>
        <p>Para que el acero al carbono se corroa en la atmósfera, deben coexistir simultáneamente cuatro elementos:</p>
        <ol>
            <li><b>Ánodo:</b> Zona del acero donde ocurre la disolución metálica (oxidación del hierro).</li>
            <li><b>Cátodo:</b> Zona de la superficie metálica donde se consumen los electrones liberados.</li>
            <li><b>Electrólito:</b> Película microscópica de humedad condensada sobre el acero que contiene iones disueltos (sales, contaminantes) y permite el flujo iónico.</li>
            <li><b>Camino Metálico:</b> El propio cuerpo del acero estructural, que conduce los electrones desde el ánodo hacia el cátodo.</li>
        </ol>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
        <div class="stCard">
            <h3>1. Reacción Anódica (Oxidación)</h3>
            <p>El átomo de hierro neutro cede dos electrones y pasa a solución acuosa como catión ferroso:</p>
            <div class="formula-box">Fe → Fe²⁺ + 2e⁻</div>
            <p style="font-size: 0.9rem;"><i>Es aquí donde ocurre la pérdida real de masa y espesor de la pieza estructural.</i></p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="stCard">
            <h3>2. Reacción Catódica (Reducción)</h3>
            <p>En ambientes atmosféricos neutros o alcalinos, el oxígeno disuelto y el agua capturan los electrones:</p>
            <div class="formula-box">O₂ + 2H₂O + 4e⁻ → 4OH⁻</div>
            <p style="font-size: 0.9rem;"><i>Se generan iones hidroxilo (OH⁻) que alcalinizan localmente la zona catódica.</i></p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
    <div class="stCard">
        <h3>3. Formación de Herrumbre y Expansión Volumétrica</h3>
        <p>
            Los cationes ferrosos (Fe²⁺) y los aniones hidroxilo (OH⁻) migran en el electrólito y reaccionan
            para precipitar hidróxido ferroso, el cual al oxidarse nuevamente con el aire forma la herrumbre:
        </p>
        <div class="formula-box">Fe²⁺ + 2OH⁻ → Fe(OH)₂  |  4Fe(OH)₂ + O₂ + 2H₂O → 4Fe(OH)₃ → Fe₂O₃·H₂O</div>
        <p>
            <b>Impacto estructural:</b> A diferencia del aluminio o el acero inoxidable, cuya capa de óxido es densa y protectora,
            la herrumbre del acero al carbono (Fe₂O₃·H₂O) es <b>porosa, frágil y no adherente</b>, permitiendo que el oxígeno
            y la humedad sigan penetrando continuamente hacia el metal sano.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# SECCIÓN 3: FACTORES INFLUYENTES
# ---------------------------------------------------------
elif menu == "Factores Influyentes":
    st.title("🌡️ Factores Ambientales y Materiales que Modifican la Corrosión")
    st.write(
        "La velocidad de corrosión ($V_c$) no es una propiedad intrínseca fija del acero, sino una respuesta "
        "dinámica del sistema metal-ambiente. A continuación se detallan los 6 factores críticos:"
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
        <div class="stCard">
            <h3>💧 1. Humedad Relativa y Tiempo de Humedecimiento (TOW)</h3>
            <ul>
                <li><b>Humedad Crítica:</b> Existe un umbral alrededor del <b>70% - 80% de Humedad Relativa (HR)</b> por debajo del cual la corrosión atmosférica es prácticamente nula por falta de electrólito líquido.</li>
                <li><b>Tiempo de Humedecimiento (<i>Time of Wetness</i>):</b> Representa el número de horas al año en que la superficie del acero permanece cubierta por una película de agua (condensación, rocío, lluvia o niebla). A mayor TOW, mayor deterioro acumulado.</li>
            </ul>
        </div>
        <div class="stCard">
            <h3>🌊 3. Salinidad y Deposición de Cloruros (Cl⁻)</h3>
            <ul>
                <li><b>Acción Despasivante:</b> Los iones cloruro provenientes del aerosol marino son pequeños y altamente móviles; penetran y destruyen cualquier película protectora en el acero.</li>
                <li><b>Efecto Higroscópico:</b> Las sales depositadas absorben humedad del ambiente incluso cuando la humedad relativa baja al 75%, prolongando artificialmente el tiempo de humedecimiento.</li>
            </ul>
        </div>
        <div class="stCard">
            <h3>🔩 5. Composición Química y Diseño del Acero</h3>
            <ul>
                <li><b>Elementos Aleantes:</b> La adición controlada de <b>Cobre (Cu), Cromo (Cr), Níquel (Ni) y Fósforo (P)</b> (aceros patinables ASTM A588) promueve la formación de una pátina compacta que frena la difusión de oxígeno.</li>
                <li><b>Detalles Geométricos:</b> Las zonas con agua estancada, hendiduras estrechas (<i>crevice corrosion</i>) o contacto entre metales distintos (corrosión galvánica) sufren ataques acelerados.</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="stCard">
            <h3>🌡️ 2. Temperatura Ambiental</h3>
            <ul>
                <li><b>Efecto Cinético (Ley de Arrhenius):</b> Un aumento en la temperatura acelera la velocidad de las reacciones electroquímicas y la difusión de iones en el electrólito.</li>
                <li><b>Efecto Dual:</b> En climas cálido-húmedos (como el sureste mexicano), la alta temperatura combinada con alta humedad maximiza la corrosión. En climas cálido-secos, el calor evapora rápidamente el rocío y detiene el proceso.</li>
            </ul>
        </div>
        <div class="stCard">
            <h3>🏭 4. Contaminación Atmosférica (SO₂ y NOₓ)</h3>
            <ul>
                <li><b>Acidificación del Electrólito:</b> En zonas urbanas e industriales, el dióxido de azufre (SO₂) emitido por combustibles fósiles se disuelve en la película de humedad formando <b>ácido sulfúrico (H₂SO₄)</b>.</li>
                <li><b>Ciclo Regenerativo:</b> Los sulfatos atacan el hierro y regeneran ácido continuamente, elevando la velocidad de corrosión hasta 5 o 10 veces respecto a una atmósfera rural limpia.</li>
            </ul>
        </div>
        <div class="stCard">
            <h3>🛡️ 6. Recubrimientos y Barreras Protectoras</h3>
            <ul>
                <li><b>Aislamiento Físico:</b> Los sistemas de pintura epóxica y poliuretano bloquean el paso de agua y oxígeno hacia el sustrato metálico.</li>
                <li><b>Protección Galvánica:</b> El galvanizado (recubrimiento de zinc) protege al acero incluso si sufre rayaduras, ya que el zinc se oxida preferentemente (ánodo de sacrificio).</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

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
    st.title("🌴 Panorama de la Corrosión Atmosférica en México")
    st.write(
        "México cuenta con más de **11,000 kilómetros de litorales marítimos** y una gran variedad de microclimas. "
        "La interacción entre la alta humedad relativa, las elevadas temperaturas y los vientos cargados de aerosol marino (cloruros) "
        "convierte al país en un escenario donde la velocidad de deterioro del acero estructural varía drásticamente según la región."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
        <div class="stCard">
            <h3>☀️ 1. Sureste y Península de Yucatán (Campeche, Tabasco, Quintana Roo, Yucatán)</h3>
            <ul>
                <li><b>Severidad Ambiental:</b> Extremadamente alta (Categorías C4 a C5 / Exposiciones NTC C y D).</li>
                <li><b>Mecanismo Dominante:</b> Alta humedad relativa (&gt;80% constante), altas temperaturas medias y vientos alisios que arrastran sales de cloruro (Cl⁻) desde el Golfo de México y Mar Caribe.</li>
                <li><b>Tiempo de Humedecimiento (<i>TOW</i>):</b> Muy prolongado debido al clima cálido-húmedo tropical.</li>
            </ul>
        </div>
        <div class="stCard">
            <h3>🏭 3. Zonas Urbanas e Industriales del Interior (CDMX, Monterrey, Guadalajara)</h3>
            <ul>
                <li><b>Severidad Ambiental:</b> Moderada a Alta (Categorías C2 a C4 / Exposiciones NTC B1 a B2).</li>
                <li><b>Mecanismo Dominante:</b> Corrosión impulsada por acidificación del aire por emisión de dióxido de azufre (SO₂) y óxidos de nitrógeno (NOₓ).</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="stCard">
            <h3>🌊 2. Litorales del Golfo de México y Pacífico (Veracruz, Tamaulipas, Sinaloa, Guerrero)</h3>
            <ul>
                <li><b>Severidad Ambiental:</b> Alta a Extrema (Categorías C4 a CX / Exposición NTC C).</li>
                <li><b>Mecanismo Dominante:</b> Fuerte brisa marina y eventos meteorológicos como los "Nortes" que transportan partículas de sal tierra adentro.</li>
            </ul>
        </div>
        <div class="stCard">
            <h3>🇲🇽 4. Fuentes Oficiales de Información Climático-Técnica en México</h3>
            <ul>
                <li><b>CONAGUA y Servicio Meteorológico Nacional (SMN):</b> Promedios anuales de Humedad Relativa, Temperatura y Precipitación.</li>
                <li><b>Instituto Mexicano del Transporte (IMT):</b> Mapas de corrosividad en la red carretera nacional y puentes.</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------
# SECCIÓN 6: CALCULADORA INTERACTIVA DE CORROSIÓN
# ---------------------------------------------------------
elif menu == "Calculadora de Corrosión":
    st.markdown(
        """
    <div class="pink-header-card" style="padding: 22px; margin-bottom: 18px;">
        <h2 style="margin:0;">🧮 Simulador Interactivo de Corrosión y Vida Útil</h2>
        <p style="margin-top: 4px; font-weight: 700;">
            Ajusta los parámetros en tiempo real, prueba escenarios ambientales y compara los modelos cinéticos
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("**⚡ Escenarios Rápidos de Prueba (Haz clic para cargar valores típicos):**")
    p1, p2, p3, p4 = st.columns(4)
    if "vc_val" not in st.session_state:
        st.session_state.vc_val = 65.0
    if "e0_val" not in st.session_state:
        st.session_state.e0_val = 12.0
    if "emin_val" not in st.session_state:
        st.session_state.emin_val = 8.0

    if p1.button("🏙️ Ambiente Urbano (CDMX)"):
        st.session_state.vc_val = 35.0
    if p2.button("🌴 Costa / Campeche (Marino)"):
        st.session_state.vc_val = 140.0
    if p3.button("🏭 Zona Industrial Pesada"):
        st.session_state.vc_val = 85.0
    if p4.button("🏡 Interior Seco / Rural"):
        st.session_state.vc_val = 12.0

    st.markdown("<br>", unsafe_allow_html=True)

    col_controls, col_dash = st.columns([1.1, 1.9])

    with col_controls:
        st.markdown(
            """
        <div class="stCard" style="padding: 18px; margin-bottom: 12px;">
            <h3 style="margin:0; border:none; padding:0;">⚙️ Parámetros de Entrada</h3>
        </div>
        """,
            unsafe_allow_html=True,
        )

        e0 = st.number_input(
            "Espesor inicial del perfil ($e_0$) [mm]:",
            min_value=1.0,
            max_value=200.0,
            value=st.session_state.e0_val,
            step=0.5,
        )
        emin = st.number_input(
            "Espesor mínimo estructural ($e_{min}$) [mm]:",
            min_value=0.5,
            max_value=float(e0 - 0.1),
            value=min(st.session_state.emin_val, float(e0 - 0.5)),
            step=0.5,
        )
        t_exp = st.slider(
            "Tiempo de exposición proyectado ($t$) [años]:",
            min_value=1,
            max_value=100,
            value=30,
        )

        st.markdown("---")
        modelo = st.radio(
            "Modelo Matemático Principal:",
            ["Modelo Lineal (Vc constante)", "Modelo Ley de Potencia (ISO 9224)"],
        )

        usar_manual = st.checkbox("Ingresar tasa Vc manualmente", value=True)
        if usar_manual:
            vc_um = st.number_input(
                "Velocidad de corrosión ($V_c$) [µm/año]:",
                min_value=0.5,
                max_value=1000.0,
                value=st.session_state.vc_val,
                step=5.0,
            )
        else:
            cat_iso_sel = st.selectbox("Categoría de referencia ISO 9223:", list(ISO_DATA.keys()))
            vc_um = ISO_DATA[cat_iso_sel]["ref"]
            st.info(f"Tasa de referencia: **{vc_um} µm/año**")

        b_exp = 0.52
        if modelo == "Modelo Ley de Potencia (ISO 9224)":
            b_exp = st.slider(
                "Exponente empírico de pasivación ($b$):",
                min_value=0.10,
                max_value=1.00,
                value=0.52,
                step=0.01,
            )

        comparar_modelos = st.checkbox("📊 Superponer ambos modelos en la gráfica", value=True)

    # Cálculos Matemáticos
    vc_mm = vc_um / 1000.0
    delta_e_lin = vc_mm * t_exp
    delta_e_pot = vc_mm * (t_exp**b_exp)

    delta_e = delta_e_lin if modelo == "Modelo Lineal (Vc constante)" else delta_e_pot
    e_restante = e0 - delta_e
    pct_perdida = (delta_e / e0) * 100.0
    tasa_anual_mm = delta_e / t_exp

    margen_espesor = e0 - emin
    if vc_mm > 0:
        if modelo == "Modelo Lineal (Vc constante)":
            vida_util_años = margen_espesor / vc_mm
        else:
            vida_util_años = (margen_espesor / vc_mm) ** (1.0 / b_exp)
    else:
        vida_util_años = 999.0

    with col_dash:
        m1, m2, m3, m4 = st.columns(4)
        m1.markdown(
            f'<div class="metric-card-pink"><div class="metric-title">Tasa Anual</div><div class="metric-value">{tasa_anual_mm:.4f}<span style="font-size:0.8rem"> mm/año</span></div></div>',
            unsafe_allow_html=True,
        )
        m2.markdown(
            f'<div class="metric-card-pink"><div class="metric-title">Pérdida Total</div><div class="metric-value">{delta_e:.3f}<span style="font-size:0.8rem"> mm</span></div></div>',
            unsafe_allow_html=True,
        )
        m3.markdown(
            f'<div class="metric-card-pink"><div class="metric-title">Espesor Final</div><div class="metric-value">{max(0.0, e_restante):.3f}<span style="font-size:0.8rem"> mm</span></div></div>',
            unsafe_allow_html=True,
        )
        m4.markdown(
            f'<div class="metric-card-pink"><div class="metric-title">Vida Útil Est.</div><div class="metric-value">{min(999, int(vida_util_años))}<span style="font-size:0.8rem"> años</span></div></div>',
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if e_restante < emin:
            st.error(
                f"🚨 ESTADO CRÍTICO: A los {t_exp} años, el espesor restante ({e_restante:.2f} mm) cae por debajo del límite estructural ({emin:.2f} mm). Falla estimada al año {int(vida_util_años)}."
            )
        elif pct_perdida > 20:
            st.warning(
                f"⚠️ ALERTA PREVENTIVA: Se ha perdido el {pct_perdida:.1f}% del espesor inicial. Se recomienda programar mantenimiento de recubrimiento."
            )
        else:
            st.success(
                f"✅ ESTADO SEGURO: El elemento conserva el {100 - pct_perdida:.1f}% de su sección transversal dentro del margen de seguridad."
            )

        t_arr = np.linspace(0, t_exp, 150)
        e_arr_lin = np.maximum(0, e0 - (vc_mm * t_arr))
        e_arr_pot = np.maximum(0, e0 - (vc_mm * (t_arr**b_exp)))

        fig = go.Figure()

        if modelo == "Modelo Lineal (Vc constante)":
            fig.add_trace(
                go.Scatter(
                    x=t_arr,
                    y=e_arr_lin,
                    mode="lines",
                    name="Modelo Lineal (Principal)",
                    line=dict(color="#C2185B", width=4),
                    fill="tozeroy",
                    fillcolor="rgba(244, 143, 177, 0.2)",
                )
            )
            if comparar_modelos:
                fig.add_trace(
                    go.Scatter(
                        x=t_arr,
                        y=e_arr_pot,
                        mode="lines",
                        name="Ley de Potencia ISO 9224 (Comparativa)",
                        line=dict(color="#880E4F", width=2, dash="dot"),
                    )
                )
        else:
            fig.add_trace(
                go.Scatter(
                    x=t_arr,
                    y=e_arr_pot,
                    mode="lines",
                    name="Ley de Potencia ISO 9224 (Principal)",
                    line=dict(color="#C2185B", width=4),
                    fill="tozeroy",
                    fillcolor="rgba(244, 143, 177, 0.2)",
                )
            )
            if comparar_modelos:
                fig.add_trace(
                    go.Scatter(
                        x=t_arr,
                        y=e_arr_lin,
                        mode="lines",
                        name="Modelo Lineal (Comparativa)",
                        line=dict(color="#880E4F", width=2, dash="dot"),
                    )
                )

        fig.add_trace(
            go.Scatter(
                x=[0, t_exp],
                y=[emin, emin],
                mode="lines",
                name=f"Límite Mínimo ({emin} mm)",
                line=dict(color="#D50000", width=3, dash="dash"),
            )
        )

        fig.update_layout(
            title="<b>Simulación Temporal de Reducción de Espesor</b>",
            xaxis_title="Tiempo de Exposición (años)",
            yaxis_title="Espesor del Acero (mm)",
            yaxis=dict(range=[0, e0 * 1.1]),
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFF5F8",
            font=dict(color="#260511", size=13),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=40, r=20, t=60, b=40),
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# SECCIÓN 7: MÉTODOS DE PROTECCIÓN (AMPLIADA Y DETALLADA)
# ---------------------------------------------------------
elif menu == "Métodos de Protección":
    st.title("🛡️ Estrategias y Métodos de Protección Anticorrosiva")
    st.write(
        "En la ingeniería civil, la selección del sistema de protección contra la corrosión depende de la categoría de agresividad "
        "ambiental (ISO 12944 / NTC), la vida útil de diseño de la estructura y la accesibilidad para labores de mantenimiento."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
        <div class="stCard">
            <h3>🎨 1. Sistemas de Recubrimientos y Pinturas Anticorrosivas</h3>
            <p>Constituyen el método más utilizado en estructuras metálicas expuestas. Operan bajo un esquema multicapa (ISO 12944):</p>
            <ul>
                <li><b>Capa Primaria (Primer):</b> Formulada con pigmentos inhibidores (fosfato de zinc) o <b>rica en zinc</b> para proveer adherencia y protección galvánica inicial.</li>
                <li><b>Capa Intermedia (Barrera):</b> Generalmente de resina <b>epóxica de altos sólidos</b>; aporta el espesor de película seca (EPS) necesario para bloquear la difusión de humedad y cloruros.</li>
                <li><b>Capa de Acabado (Topcoat):</b> Esmalte de <b>poliuretano alifático</b> o polisiloxano resistente a la radiación ultravioleta (UV), evitando el caleo y degradación solar.</li>
                <li><b>Preparación de Superficie:</b> Exige limpieza con chorro abrasivo (sandblasting grado Sa 2½ según ISO 8501) para garantizar el perfil de anclaje.</li>
            </ul>
        </div>

        <div class="stCard">
            <h3>⚡ 3. Protección Catódica (Ánodos de Sacrificio y Corriente Impresa)</h3>
            <p>Se emplea principalmente en estructuras enterradas (tuberías, cimentaciones) o sumergidas en agua de mar (muelles y pilotes):</p>
            <ul>
                <li><b>Principio Electroquímico:</b> Consiste en suministrar electrones externos al acero para polarizarlo negativamente y convertir toda la estructura en el <b>cátodo</b> de la celda, deteniendo por completo la disolución anódica del hierro.</li>
                <li><b>Ánodos Galvánicos (de Sacrificio):</b> Se conectan bloques de metales más electronegativos como <b>Zinc (Zn), Aluminio (Al) o Magnesio (Mg)</b>, los cuales se corroen preferentemente protegiendo al acero.</li>
                <li><b>Corriente Impresa (ICCP):</b> Utiliza rectificadores de corriente continua y ánodos inertes (titanio recubierto) para proteger infraestructuras de gran escala como puentes marinos y plataformas offshore.</li>
            </ul>
        </div>

        <div class="stCard">
            <h3>📐 5. Diseño Estructural Preventivo (Detalles Constructivos)</h3>
            <p>La geometría de los elementos influye directamente en la acumulación de humedad:</p>
            <ul>
                <li><b>Evitar Trampas de Agua:</b> Incorporar barrenos de drenaje en perfiles canal, vigas cajón y placas base.</li>
                <li><b>Continuidad de Soldaduras:</b> Preferir cordones de soldadura continuos sobre soldaduras intermitentes para evitar corrosión en rendijas (<i>crevice corrosion</i>).</li>
                <li><b>Aislamiento Galvánico:</b> Colocar empaques o arandelas dieléctricas de neopreno o teflón al unir acero al carbono con acero inoxidable o cobre.</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="stCard">
            <h3>🔩 2. Galvanizado por Inmersión en Caliente (HDG)</h3>
            <p>Regido por normas como <b>ASTM A123 / NMX-H-004</b>, consiste en sumergir las piezas de acero limpias en un baño de zinc fundido a ~450 °C:</p>
            <ul>
                <li><b>Unión Metalúrgica:</b> Se forman capas de aleación zinc-hierro extremadamente duras y resistentes a la abrasión mecánica durante el transporte y montaje.</li>
                <li><b>Triple Protección:</b> Actúa como barrera física impermeable, provee <b>protección catódica de sacrificio</b> si el recubrimiento se raya, y desarrolla una pátina estable de carbonato básico de zinc.</li>
                <li><b>Durabilidad:</b> En ambientes urbanos o rurales puede superar los <b>40 a 60 años</b> sin requerir mantenimiento.</li>
            </ul>
        </div>

        <div class="stCard">
            <h3>🏗️ 4. Aceros Patinables Resistentes a la Corrosión (Acero Corten)</h3>
            <p>Aleaciones estructurales de alta resistencia y baja aleación (especificación <b>ASTM A588 / A242</b>):</p>
            <ul>
                <li><b>Composición Especial:</b> Contienen pequeñas proporciones de <b>Cobre (0.25-0.55%), Cromo, Níquel y Fósforo</b>.</li>
                <li><b>Mecanismo de Autoprotección:</b> Al exponerse a ciclos alternados de humedecimiento y secado al aire libre, desarrollan una capa de óxido adherente, densa e impermeable (pátina) que sella los poros y reduce drásticamente la velocidad de corrosión posterior.</li>
                <li><b>Limitación Crítica:</b> No deben emplearse en ambientes marinos con alta concentración de cloruros ni en zonas permanentemente sumergidas, ya que la pátina protectora no logra estabilizarse.</li>
            </ul>
        </div>

        <div class="stCard">
            <h3>🔍 6. Inspección Periódica y Mantenimiento Programado</h3>
            <p>La gestión de integridad estructural requiere monitoreo continuo:</p>
            <ul>
                <li><b>Medición de Espesores por Ultrasonido (UT):</b> Permite verificar el espesor remanente real sin dañar la estructura y calibrar modelos predictivos como <b>STEELIA</b>.</li>
                <li><b>Pruebas de Adherencia y Espesor de Película Seca (EPS):</b> Control de calidad en obra mediante medidores magnéticos o de corrientes de Eddy (SSPC-PA 2).</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

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
        st.markdown(
            """
        <div class="stCard">
            <h3>🌉 1. Puentes Metálicos y Mixtos</h3>
            <p>Los puentes vehiculares y peatonales están expuestos de forma continua a vibraciones, ciclos de carga (fatiga) y agentes atmosféricos.</p>
            <ul>
                <li><b>Fatiga por Corrosión (<i>Corrosion Fatigue</i>):</b> La presencia de picaduras (<i>pitting</i>) genera <b>concentradores de esfuerzos</b> que aceleran la propagación de grietas.</li>
                <li><b>Zonas Críticas:</b> Uniones soldadas, nodos atornillados, placas de apoyo y cara inferior del tablero.</li>
            </ul>
        </div>
        <div class="stCard">
            <h3>🌊 3. Infraestructura Marítima y Costera</h3>
            <p>Las obras ubicadas en frentes costeros enfrentan las condiciones más severas (Categorías C5/CX):</p>
            <ul>
                <li><b>Zona de Salpicaduras y Mareas (<i>Splash Zone</i>):</b> Combina suministro continuo de oxígeno con humedecimiento por oleaje y altas concentraciones de cloruros (Cl⁻).</li>
                <li><b>Pilotaje Metálico:</b> Exige recubrimientos epóxicos espesos y <b>protección catódica</b>.</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="stCard">
            <h3>🏢 2. Edificios y Naves Industriales</h3>
            <ul>
                <li><b>Columnas y Trabes Expuestas:</b> La reducción del espesor reduce directamente el momento de inercia (I) y el área de la sección (A).</li>
                <li><b>Riesgo de Pandeo:</b> Al disminuir el espesor (t), aumenta la esbeltez (b/t), haciendo a la columna susceptible de fallar por pandeo elástico.</li>
            </ul>
        </div>
        <div class="stCard">
            <h3>📐 4. Criterios de Sobreespesor (<i>Corrosion Allowance</i>)</h3>
            <ul>
                <li>El estructuralista define un <b>espesor sacrificable de corrosión (e<sub>sacrif</sub>)</b> adicional al espesor requerido por cálculo mecánico.</li>
                <li>Herramientas como <b>STEELIA</b> permiten predecir cuándo se consumirá ese sobreespesor.</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------
# SECCIÓN 9: ¿CÓMO UTILIZAR STEELIA?
# ---------------------------------------------------------
elif menu == "¿Cómo utilizar STEELIA?":
    st.title("📖 Guía de Uso")
    st.markdown(
        """
    <div class="stCard">
        <h3>Paso a Paso para Simular en STEELIA</h3>
        <ol>
            <li>Dirígete a la <b>Calculadora de Corrosión</b> en el menú lateral.</li>
            <li>Opcionalmente, haz clic en uno de los botones de <b>Escenarios Rápidos</b> (ej. Costa / Campeche) para cargar tasas ambientales reales.</li>
            <li>Introduce el <b>Espesor inicial (e₀)</b> y el <b>Espesor mínimo permitido (eₘᵢₙ)</b> en milímetros.</li>
            <li>Mueve el deslizador de <b>Tiempo de exposición</b> y elige el modelo matemático (Lineal o Ley de Potencia ISO 9224).</li>
            <li>Analiza las 4 tarjetas de resultados, el semáforo de seguridad y la curva comparativa en tiempo real.</li>
        </ol>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# SECCIÓN 10: REFERENCIAS APA 7
# ---------------------------------------------------------
elif menu == "Referencias APA 7":
    st.title("📚 Referencias Bibliográficas")
    st.markdown(
        """
    <div class="stCard">
        <h3>Fuentes Normativas y Científicas</h3>
        <ul>
            <li><b>Gobierno de la Ciudad de México.</b> (2023). <i>Normas Técnicas Complementarias para Diseño y Construcción de Estructuras de Concreto (NTC-Concreto, Capítulo 4: Durabilidad)</i>. Gaceta Oficial de la Ciudad de México.</li>
            <li><b>International Organization for Standardization.</b> (2012). <i>Corrosion of metals and alloys — Corrosivity of atmospheres — Classification, determination and estimation</i> (ISO Standard No. 9223:2012 / 9224:2012).</li>
            <li><b>International Organization for Standardization.</b> (2017). <i>Paints and varnishes — Corrosion protection of steel structures by protective paint systems</i> (ISO Standard No. 12944).</li>
            <li><b>Revie, R. W., & Uhlig, H. H.</b> (2008). <i>Corrosion and corrosion control: An introduction to corrosion science and engineering</i> (4th ed.). John Wiley & Sons.</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )
