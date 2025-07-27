import streamlit as st

def render():
    st.title("👤 Sobre Nosotros - Min3ra Analytics")

    # Introducción a la empresa y el problema
    st.markdown("""
    **Min3ra Analytics** nace como respuesta a los desafíos de las empresa de e-commerce que cuenta con una extensa base de datos de clientes, productos y transacciones.
    """)

    # Propuesta de valor
    st.subheader("💡 Nuestra Propuesta de Valor")
    st.markdown("""
    En Min3ra Analytics ofrecemos una solución integral, accesible y basada en herramientas libres para:
    
    - Predecir el abandono de clientes  
    - Predicir el volumen de compras por cliente
    - Segmentar clientes de forma efectiva
    - Visualizar resultados con dashboards interactivos

    Todo esto sin depender de herramientas costosas, manteniendo la escalabilidad y el enfoque profesional.
    """)

    # Equipo de trabajo
    st.subheader("👥 Nuestro Equipo")
    st.markdown("""
    Contamos con un equipo interdisciplinario con habilidades técnicas y estratégicas:

    - **Sebastian Fiallos** – CEO  
      *Líder estratégico y relaciones comerciales.*
    
    - **Cristian Díaz** – CTO  
      *Responsable de infraestructura tecnológica y seguridad de datos.*
    
    - **Stiven Guapucal** – Data Scientist  
      *Encargado del desarrollo de modelos predictivos, análisis de datos y soluciones inteligentes.*
    """)

    # Valores diferenciales (resumidos aquí también)
    st.subheader("🔎 ¿Por qué elegirnos?")
    st.markdown("""
    - ✅ Soluciones personalizadas y rápidas  
    - ✅ Modelos interpretables, no cajas negras  
    - ✅ Enfoque 100% técnico y profesional
    """)

    # Cierre
    st.info("En Min3ra Analytics creemos que los datos deben convertirse en decisiones inteligentes. Esa es nuestra misión.")
