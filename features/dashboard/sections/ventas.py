import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import numpy as np

def render():
    st.set_page_config(page_title="Predicción de Ventas", layout="wide")

    st.title("💰 Predicción Inteligente de Ventas por Cliente")
    st.write("Carga tu dataset para analizar y predecir el volumen de compras por cliente. Interactúa con las gráficas para descubrir qué impulsa las ventas.")

    uploaded_file = st.file_uploader("📁 Sube tu archivo CSV", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.subheader("👀 Vista previa de los datos")
        st.dataframe(df.head())

        # Codificación de variables categóricas
        label_cols = ['genero', 'ubicacion', 'metodo_pago']
        encoders = {col: LabelEncoder().fit(df[col]) for col in label_cols}
        for col, le in encoders.items():
            df[col + '_label'] = le.transform(df[col])

        # KPIs
        st.subheader("📌 Indicadores Clave")
        col1, col2 = st.columns(2)
        col1.metric("🧑‍🤝‍🧑 Total de Clientes", f"{df.shape[0]}")
        col2.metric("💳 Compra Promedio", f"${df['total_compras'].mean():.2f}")

        # Filtros interactivos
        st.sidebar.header("🔍 Filtros")
        genero_filtrado = st.sidebar.multiselect("Filtrar por género", df['genero'].unique(), default=df['genero'].unique())
        ubicacion_filtrada = st.sidebar.multiselect("Filtrar por ubicación", df['ubicacion'].unique(), default=df['ubicacion'].unique())
        metodo_pago_filtrado = st.sidebar.multiselect("Filtrar por método de pago", df['metodo_pago'].unique(), default=df['metodo_pago'].unique())

        df = df[
            (df['genero'].isin(genero_filtrado)) &
            (df['ubicacion'].isin(ubicacion_filtrada)) &
            (df['metodo_pago'].isin(metodo_pago_filtrado))
        ]

        # === GRAFICAS INTERACTIVAS MEJORADAS CON COLORES ===
        st.subheader("📊 Exploración Interactiva de Patrones de Compra")

        col1, col2 = st.columns(2)
        with col1:
            fig_edad = px.histogram(df, x='edad', y='total_compras', histfunc='avg', nbins=20,
                                    title="Promedio de Compras por Edad", color='edad')
            st.plotly_chart(fig_edad, use_container_width=True)

        with col2:
            fig_metodo = px.box(df, x='metodo_pago', y='total_compras', color='metodo_pago',
                                title="Distribución de Compras por Método de Pago",
                                color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(fig_metodo, use_container_width=True)

        fig_satisfaccion = px.scatter(df, x='nivel_satisfaccion', y='total_compras', color='genero',
                                      size='frecuencia_compra',
                                      title="Relación Satisfacción vs Compras (tamaño según frecuencia)",
                                      color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_satisfaccion, use_container_width=True)

        # NUEVA: Frecuencia vs Gasto
        fig_frec = px.scatter(df, x='frecuencia_compra', y='promedio_gasto',
                              color='genero', size='total_compras',
                              title="Frecuencia de Compra vs Gasto Promedio",
                              color_discrete_sequence=px.colors.qualitative.Bold)
        st.plotly_chart(fig_frec, use_container_width=True)

        # NUEVA: Deciles de compra
        st.subheader("📊 Clientes por Nivel de Compra")
        df['decil'] = pd.qcut(df['total_compras'], q=10, labels=[f'Decil {i+1}' for i in range(10)])
        fig_decil = px.histogram(df, x='decil', color='genero',
                                 title="Distribución de Clientes por Decil de Compra",
                                 color_discrete_sequence=px.colors.qualitative.Prism)
        st.plotly_chart(fig_decil, use_container_width=True)

        # NUEVA: Heatmap de correlaciones (simplificada para clientes)
        st.subheader("🔗 Correlaciones Visuales")
        cols_corr = [
            'total_compras',
            'frecuencia_compra',
            'promedio_gasto',
            'nivel_satisfaccion',
            'uso_cupon',
            'tiempo_promedio_sesion',
            'paginas_vistas_promedio'
        ]
        corr_matrix = df[cols_corr].corr()

        fig_corr, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
        st.pyplot(fig_corr)

        # MODELO
        st.subheader("🧠 Modelo Predictivo de Compras")
        feature_cols = [
            'genero_label', 'edad', 'ubicacion_label', 'frecuencia_compra', 'promedio_gasto',
            'dias_desde_ultima_compra', 'tiempo_promedio_sesion', 'paginas_vistas_promedio',
            'nivel_satisfaccion', 'carritos_abandonados', 'email_abierto_30d',
            'dias_registro', 'usa_movil', 'uso_cupon', 'visitas_semana', 'metodo_pago_label'
        ]

        X = df[feature_cols]
        y = df['total_compras']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        modelo = RandomForestRegressor(n_estimators=100, random_state=42)
        modelo.fit(X_train, y_train)
        y_pred = modelo.predict(X_test)

        score = modelo.score(X_test, y_test)
        st.success(f"🎯 Precisión del modelo (R²): {score:.2f}")

        # NUEVA: Predicción vs Real
        st.subheader("🔍 Visualización de Predicciones")
        df_eval = pd.DataFrame({'Real': y_test, 'Predicción': y_pred})
        fig_pred = px.scatter(df_eval, x='Real', y='Predicción', trendline='ols',
                              title="Comparación: Predicción vs Valor Real")
        st.plotly_chart(fig_pred, use_container_width=True)

        # Importancia de características
        importances = modelo.feature_importances_
        importance_df = pd.DataFrame({'Característica': feature_cols, 'Importancia': importances})
        importance_df = importance_df.sort_values(by='Importancia', ascending=True)

        st.subheader("🔍 Variables Más Influyentes")
        fig_imp = px.bar(importance_df, x='Importancia', y='Característica', orientation='h',
                         title="Importancia de cada característica en la predicción",
                         color='Importancia')
        st.plotly_chart(fig_imp, use_container_width=True)

        st.success("¡Análisis completo! Usa las visualizaciones para interpretar los impulsores clave de ventas.")

if __name__ == "__main__":
    render()