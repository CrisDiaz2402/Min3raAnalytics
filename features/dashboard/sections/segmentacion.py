import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def render():
    # Configuración
    st.set_page_config(page_title="Segmentación de Clientes", layout="wide")

    st.title("🧩 Segmentación Inteligente de Clientes")
    st.write("Sube tu dataset para analizar y visualizar segmentos de clientes de forma interactiva.")

    uploaded_file = st.file_uploader("📁 Sube tu archivo CSV", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.subheader("👀 Vista previa de los datos")
        st.dataframe(df.head())

        # Variables numéricas seleccionadas
        features = [
            'frecuencia_compra',
            'promedio_gasto',
            'dias_desde_ultima_compra',
            'nivel_satisfaccion',
            'tiempo_promedio_sesion',
            'paginas_vistas_promedio'
        ]

        X = df[features]

        # Escalar
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Sidebar: configuración del modelo
        st.sidebar.header("⚙️ Configuración del Modelo")
        n_clusters = st.sidebar.slider("Número de Clusters", min_value=2, max_value=10, value=4)

        # KMeans
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        df['cluster'] = kmeans.fit_predict(X_scaled)

        # PCA
        pca = PCA(n_components=2)
        principal_components = pca.fit_transform(X_scaled)
        df['PC1'] = principal_components[:, 0]
        df['PC2'] = principal_components[:, 1]

        st.subheader("📊 Visualización de Clusters (PCA)")
        fig_pca = px.scatter(
            df,
            x='PC1',
            y='PC2',
            color='cluster',
            hover_data=features,
            title="Distribución de Clusters en Espacio Reducido (PCA)"
        )
        st.plotly_chart(fig_pca, use_container_width=True)

        # Perfil general de clusters
        st.subheader("🔍 Perfil General de Clusters")
        cluster_summary = df.groupby('cluster')[features].mean().reset_index()

        fig_profile = px.bar(
            cluster_summary.melt(id_vars='cluster', var_name='Variable', value_name='Valor Promedio'),
            x='Variable',
            y='Valor Promedio',
            color='cluster',
            barmode='group',
            title="Comparación de Características Promedio por Cluster"
        )
        st.plotly_chart(fig_profile, use_container_width=True)

        # === NUEVA VISUALIZACIÓN 1: BOXPLOT INTERACTIVO ===
        st.subheader("📦 Distribución Interna por Cluster")
        selected_variable = st.selectbox("Selecciona una variable para comparar su distribución entre clusters", features)

        fig_box = px.box(
            df,
            x='cluster',
            y=selected_variable,
            points='all',
            title=f"Distribución de '{selected_variable}' por Cluster",
            color='cluster'
        )
        st.plotly_chart(fig_box, use_container_width=True)

        # === NUEVA VISUALIZACIÓN 2: SELECTOR DE CLUSTER ===
        st.subheader("🔍 Detalle por Cluster")
        selected_cluster = st.selectbox("Selecciona un Cluster para ver su perfil", sorted(df['cluster'].unique()))

        cluster_data = df[df['cluster'] == selected_cluster]

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Clientes en este cluster", len(cluster_data))
        with col2:
            st.metric("Promedio de gasto", f"${cluster_data['promedio_gasto'].mean():.2f}")

        fig_cluster_profile = px.bar(
            cluster_data[features].mean().reset_index(),
            x='index',
            y=0,
            labels={"index": "Variable", "0": "Valor Promedio"},
            title=f"Perfil del Cluster {selected_cluster}"
        )
        st.plotly_chart(fig_cluster_profile, use_container_width=True)

        # Tabla con resultados
        st.subheader("📑 Clientes Segmentados")
        st.dataframe(df[['cliente_id', 'cluster'] + features].head(20))

        # # Sección de Insights
        # st.subheader("💡 Interpretación Visual")
        # st.markdown("""
        # - ¿Qué cluster tiene mayor gasto promedio?
        # - ¿Cuál parece tener clientes inactivos o con baja interacción?
        # - ¿Hay clusters muy similares entre sí?
        # - ¿Puedes identificar el segmento más rentable o más leal?

        # Utiliza las visualizaciones para encontrar patrones y definir estrategias.
        # """)

        st.success("¡Análisis completado! Explora los segmentos para diseñar acciones efectivas.")
