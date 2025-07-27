import streamlit as st
from features.dashboard.sections import soon

def render():
    st.title("💡 Nuestra Solución - Min3ra Analytics")

    st.markdown("""
    Min3ra Analytics ofrece un servicio integral de **Minería de Datos** enfocado en resolver los principales desafíos de tu negocio, como el abandono de clientes, la optimización del marketing y la mejora logística.

    ### 🚀 ¿Qué ofrecemos?

    - 📊 **Segmentación de Clientes**  
      Agrupación inteligente basada en comportamiento y perfil de compra.
    
    - 📈 **Predicción de Ventas**  
      Modelos que estiman la demanda futura por categoría, región u otros filtros.
    
    - ❌ **Detección de Abandono de Clientes**  
      Clasificación de clientes en riesgo de abandonar la tienda.
    
    - 🧠 **Análisis de Comportamiento de Usuarios**  
      Estudio de rutas de navegación, productos más vistos y patrones de compra.
    
    - 📦 **Optimización de Logística y Stock**  
      Identificación de quiebres de stock, exceso de inventario y recomendaciones.
    
    - 📺 **Dashboards Interactivos**  
      Visualización clara, dinámica y usable para la toma de decisiones.

    ---

    ### 💎 Valor Diferencial frente a la Competencia

    | Característica                         | Min3ra Analytics     | Competencia tradicional |
    |----------------------------------------|-----------------------|--------------------------|
    | Soluciones Personalizadas              | ✅ Sí                 | ❌ Parciales             |
    | Tiempos de Entrega Rápidos             | ✅ 2-3 semanas        | ❌ 1-2 meses             |
    | Herramientas Gratuitas y Accesibles    | ✅ Sí                 | ❌ Costosas licencias    |
    | Modelos Explicables y Visuales         | ✅ Interpretable      | ❌ Caja negra            |
    | Equipo Especializado y Dinámico        | ✅ 100% técnico       | ❌ Generalistas          |

    ---
    
    Con Min3ra Analytics, obtendras una solución **ágil, poderosa y rentable**, construida con herramientas accesibles y metodologías profesionales.
    """)
    st.title("💯 Prueba Nuestras Demos")
    # Cards de servicios
    card_style = """
        <div style='border:2px solid #4F8BF9; border-radius:10px; margin:10px; padding:16px; background-color:#f9f9f9;'>
            <h3 style='color:#4F8BF9;'>{title}</h3>
            <p style='color:#333;'>{desc}</p>
        </div>
    """
    # Card 1
    col_card, col_btn = st.columns([5,1])
    with col_card:
        st.markdown(card_style.format(title="Segmentación de clientes", desc="Agrupa a tus clientes según su perfil y personaliza tus estrategias de negocio."), unsafe_allow_html=True)
    with col_btn:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        if st.button("Ver Más", key="ver_mas_segmentacion"):
            st.session_state["seccion_seleccionada"] = "segmentacion"
            st.rerun()

    # Card 2
    col_card, col_btn = st.columns([5,1])
    with col_card:
        st.markdown(card_style.format(title="Predicción de ventas", desc="Anticipa la demanda y maximiza tus ventas con inteligencia predictiva."), unsafe_allow_html=True)
    with col_btn:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        if st.button("Ver Más", key="ver_mas_ventas"):
            st.session_state["seccion_seleccionada"] = "ventas"
            st.rerun()

    # Card 3
    col_card, col_btn = st.columns([5,1])
    with col_card:
        st.markdown(card_style.format(title="Detección de abandono de clientes", desc="Identifica a tiempo a tus clientes en riesgo y reduce la tasa de abandono."), unsafe_allow_html=True)
    with col_btn:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        if st.button("Ver Más", key="ver_mas_abandono"):
            st.session_state["seccion_seleccionada"] = "demo"
            st.rerun()

    # Card 4
    col_card, col_btn = st.columns([5,1])
    with col_card:
        st.markdown(card_style.format(title="Análisis de comportamiento de usuarios", desc="Conoce cómo interactúan tus usuarios y toma decisiones basadas en su comportamiento."), unsafe_allow_html=True)
    with col_btn:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        if st.button("Ver Más", key="ver_mas_comportamiento"):
            st.session_state["seccion_seleccionada"] = "segmentacion_clientes"
            st.rerun()

    # Card 5
    col_card, col_btn = st.columns([5,1])
    with col_card:
        st.markdown(card_style.format(title="Optimización de logística y stock", desc="Optimiza rutas y controla tu inventario con decisiones basadas en datos."), unsafe_allow_html=True)
    with col_btn:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        if st.button("Ver Más", key="ver_mas_logistica"):
            st.session_state["seccion_seleccionada"] = "segmentacion_clientes"
            st.rerun()
    # Llamada a demo.py
    #from features.dashboard.sections.demo import render
    #render()
