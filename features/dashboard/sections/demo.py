import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

def render():
    st.set_page_config(page_title="Predicción Abandono", layout="wide")

    st.title("📉 Panel Inteligente - Predicción de Abandono de Clientes")
    st.write("Explora visualmente qué tipos de clientes están abandonando tu servicio. Usa los filtros e interpretaciones gráficas para descubrir patrones clave.")

    uploaded_file = st.file_uploader("📁 Sube tu archivo CSV", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.subheader("👀 Vista previa de los datos")
        st.dataframe(df.head())

        # Codificación de variables categóricas
        le_genero = LabelEncoder()
        le_ubicacion = LabelEncoder()
        le_churn = LabelEncoder()

        df['genero'] = le_genero.fit_transform(df['genero'])
        df['ubicacion'] = le_ubicacion.fit_transform(df['ubicacion'])
        df['cliente_abandona'] = le_churn.fit_transform(df['cliente_abandona'])

        df['genero_label'] = le_genero.inverse_transform(df['genero'])
        df['ubicacion_label'] = le_ubicacion.inverse_transform(df['ubicacion'])

        # Panel de indicadores
        st.subheader("📌 Indicadores Clave")
        col1, col2, col3 = st.columns(3)
        churn_rate = df['cliente_abandona'].mean() * 100
        clientes_total = df.shape[0]
        abandonaron = df['cliente_abandona'].sum()

        col1.metric("📊 Tasa de abandono", f"{churn_rate:.2f} %")
        col2.metric("👥 Total clientes", f"{clientes_total}")
        col3.metric("🚪 Clientes que abandonaron", f"{abandonaron}")

        # Filtros
        st.sidebar.header("🔍 Filtros")
        genero_filtrado = st.sidebar.multiselect("Filtrar por género", df['genero_label'].unique(), default=df['genero_label'].unique())
        ubicacion_filtrada = st.sidebar.multiselect("Filtrar por ubicación", df['ubicacion_label'].unique(), default=df['ubicacion_label'].unique())

        df_filtrado = df[(df['genero_label'].isin(genero_filtrado)) & (df['ubicacion_label'].isin(ubicacion_filtrada))]

        # NUEVOS GRÁFICOS Y MEJORAS

        # Rango de edad
        df_filtrado['edad_rango'] = pd.cut(df_filtrado['edad'], bins=[0, 25, 35, 50, 100],
                                           labels=['18-25', '26-35', '36-50', '51+'])

        # Gráfico: Abandono por Rango de Edad
        st.subheader("📊 Abandono por Rango de Edad")
        edad_churn = df_filtrado.groupby(['edad_rango', 'cliente_abandona']).size().reset_index(name='conteo')
        fig_edad = px.bar(edad_churn, x='edad_rango', y='conteo', color='cliente_abandona', barmode='group',
                          labels={'edad_rango': 'Rango de Edad', 'cliente_abandona': 'Abandono'},
                          color_discrete_map={0: 'green', 1: 'red'})
        st.plotly_chart(fig_edad, use_container_width=True)

        # Gráfico: Boxplot - Días desde última compra
        st.subheader("📦 Días desde Última Compra vs Abandono")
        fig_box = px.box(df_filtrado, x='cliente_abandona', y='dias_desde_ultima_compra',
                         labels={'cliente_abandona': 'Abandono', 'dias_desde_ultima_compra': 'Días desde Última Compra'},
                         color='cliente_abandona', color_discrete_map={0: 'green', 1: 'red'})
        st.plotly_chart(fig_box, use_container_width=True)

        # Gráfico: Satisfacción Promedio
        st.subheader("❤️ Nivel de Satisfacción Promedio según Abandono")
        sat_group = df_filtrado.groupby('cliente_abandona')['nivel_satisfaccion'].mean().reset_index()
        fig_sat = px.bar(sat_group, x='cliente_abandona', y='nivel_satisfaccion',
                         labels={'cliente_abandona': 'Abandono', 'nivel_satisfaccion': 'Satisfacción Promedio'},
                         color='cliente_abandona', color_discrete_map={0: 'green', 1: 'red'})
        st.plotly_chart(fig_sat, use_container_width=True)

        # Gráfico: Abandono por género
        st.subheader("🧍‍♂️ Abandono por Género")
        fig_gen = px.histogram(df_filtrado, x='genero_label', color='cliente_abandona', barmode='group',
                               labels={'genero_label': 'Género', 'cliente_abandona': 'Abandono'},
                               color_discrete_map={0: 'green', 1: 'red'})
        st.plotly_chart(fig_gen, use_container_width=True)

        # Gráfico: Abandono por ubicación
        st.subheader("🌍 Abandono por Ubicación")
        ubicacion_churn = df_filtrado.groupby(['ubicacion_label', 'cliente_abandona']).size().reset_index(name='conteo')
        fig_ubi = px.bar(ubicacion_churn, x='ubicacion_label', y='conteo', color='cliente_abandona', barmode='group',
                         labels={'ubicacion_label': 'Ubicación', 'cliente_abandona': 'Abandono'},
                         color_discrete_map={0: 'green', 1: 'red'})
        st.plotly_chart(fig_ubi, use_container_width=True)

        # Pie chart
        st.subheader("🧩 Distribución Global del Abandono")
        abandono_counts = df_filtrado['cliente_abandona'].value_counts().rename({0: 'No Abandonó', 1: 'Abandonó'})
        fig_pie = px.pie(names=abandono_counts.index, values=abandono_counts.values,
                         color=abandono_counts.index,
                         color_discrete_map={'Abandonó': 'red', 'No Abandonó': 'green'})
        st.plotly_chart(fig_pie, use_container_width=True)

        # Matriz de correlación
        st.subheader("📌 Correlación entre Variables")
        corr_df = df_filtrado.select_dtypes(include='number').corr()
        fig_corr = px.imshow(corr_df, text_auto=True, aspect="auto", color_continuous_scale='RdBu',
                             title='Matriz de Correlación')
        st.plotly_chart(fig_corr, use_container_width=True)

        # Entrenamiento de modelo para importancia
        st.subheader("🧠 Modelo Predictivo: Árbol de Decisión")
        X = df.drop(columns=['cliente_id', 'cliente_abandona', 'genero_label', 'ubicacion_label'])
        y = df['cliente_abandona']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        modelo = DecisionTreeClassifier(max_depth=4, random_state=42)
        modelo.fit(X_train, y_train)

        # Importancia de variables
        importances = modelo.feature_importances_
        features = X.columns
        imp_df = pd.DataFrame({'Característica': features, 'Importancia': importances})
        imp_df = imp_df.sort_values(by='Importancia', ascending=True)

        st.subheader("⭐ Factores que más influyen en el abandono")
        fig_imp = px.bar(imp_df, x='Importancia', y='Característica', orientation='h',
                         color='Importancia', color_continuous_scale='Viridis')
        st.plotly_chart(fig_imp, use_container_width=True)

        # Precisión del modelo
        y_pred = modelo.predict(X_test)
        precision = (y_pred == y_test).mean() * 100
        st.success(f"Precisión del modelo: {precision:.2f}% (modelo de Árbol de Decisión)")

# Llamada a la función principal
if __name__ == "__main__":
    render()
