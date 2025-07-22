import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Auditoría TI", layout="wide")
st.title("🧩 Evaluación de Auditoría de Servicios de TI")

# Subida de archivo
archivo = st.file_uploader("Sube el archivo Excel con los datos", type=["xlsx"])
if archivo is not None:
    df = pd.read_excel(archivo)

    # Mostrar los datos
    st.subheader("Vista previa de los datos")
    st.dataframe(df)

    # Filtro por categoría si existe esa columna
    if 'Categoría' in df.columns:
        categoria = st.selectbox("Selecciona una categoría", options=["Todas"] + list(df['Categoría'].dropna().unique()))
        if categoria != "Todas":
            df = df[df['Categoría'] == categoria]

    # Visualización con gráfico si hay columnas numéricas
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if len(numeric_cols) >= 2:
        x_col = st.selectbox("Selecciona variable X", numeric_cols)
        y_col = st.selectbox("Selecciona variable Y", numeric_cols, index=1)

        fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
        st.plotly_chart(fig, use_container_width=True)

