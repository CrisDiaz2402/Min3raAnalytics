import streamlit as st
from features.inicio import home
from features.dashboard import Dashboard
from features.dashboard.sections import soon, demo, segmentacion, ventas
from features.nosotros import nosotros

st.set_page_config(
    page_title="Min3ra Analytics",
    page_icon="🔎",
    layout="wide"
)

# Estilo de página personalizado con markdown
st.markdown(
    """
    <style>
        .main-title {
            font-size: 40px;
            font-weight: 800;
            color: #4A90E2;
            margin-bottom: 10px;
        }
        .sub-title {
            font-size: 20px;
            color: #5A5A5A;
            margin-top: -10px;
            margin-bottom: 30px;
        }
        .sidebar .sidebar-content {
            background-color: #f5f5f5;
        }
        .css-1v3fvcr {
            background-color: #f5f5f5 !important;
        }
        /* Estilos para los botones del menú lateral */
        section[data-testid="stSidebar"] button.stButton {
            width: 100% !important;
            min-width: 100% !important;
            max-width: 100% !important;
            height: 50px !important;
            margin-bottom: 12px;
            border-radius: 12px;
            font-size: 17px;
            font-weight: 500;
            display: flex;
            align-items: center;
            justify-content: center;
            box-sizing: border-box;
        }
        section[data-testid="stSidebar"] button.stButton > div {
            width: 100%;
            min-width: 100%;
            max-width: 100%;
            text-align: center;
            box-sizing: border-box;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# Encabezado con logo alineado a la derecha

# Encabezado con logo alineado a la derecha usando st.columns
col1, col2 = st.columns([6,1])
with col1:
    st.markdown('<div class="main-title">🔎 Min3ra Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Soluciones Inteligentes</div>', unsafe_allow_html=True)
with col2:
    st.image("assets/logo.png", width=300)


# Menú de navegación lateral

st.sidebar.title("📁 Navegación Principal")
st.sidebar.markdown("---")

# Botones de navegación

secciones = [
    ("🔮 Inicio", home.render),
    ("💹 Soluciones", Dashboard.render),
    ("👥 Sobre Nosotros", nosotros.render),
    ("segmentacion_clientes", soon.render), # No se muestra en el menú lateral
    ("demo", demo.render), # No se muestra en el menú lateral
    ("segmentacion", segmentacion.render),
    ("ventas", ventas.render)
    
]

# Inicializar la sección seleccionada en session_state
if "seccion_seleccionada" not in st.session_state:
    st.session_state["seccion_seleccionada"] = secciones[0][0]

for nombre, _ in secciones:
    # Solo mostrar botones para Inicio y Soluciones
    if nombre in ["🔮 Inicio", "💹 Soluciones", "👥 Sobre Nosotros"]:
        if st.sidebar.button(nombre, key=nombre):
            st.session_state["seccion_seleccionada"] = nombre

# Mostrar sección correspondiente y resaltar el botón activo
for nombre, funcion in secciones:
    if st.session_state["seccion_seleccionada"] == nombre:
        funcion()
        break
# Mostrar sección correspondiente

# Footer
st.markdown("---")
st.markdown(
    "<center><small>© 2025 Min3ra Analytics · Todos los derechos reservados</small></center>",
    unsafe_allow_html=True
)