import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Auditoría TI", layout="wide")
st.title("🧩 Evaluación de Auditoría de Servicios de TI")

# 1. Subir archivo Excel
uploaded_file = st.file_uploader("📤 Sube tu archivo de preguntas (Excel)", type=["xlsx"])

if uploaded_file:
    # 2. Leer el archivo
    df = pd.read_excel(uploaded_file)
    
    # Validar columnas
    if "Dominio" not in df.columns or "Pregunta" not in df.columns:
        st.error("❌ El archivo debe tener columnas llamadas 'Dominio' y 'Pregunta'")
    else:
        st.success("✅ Archivo cargado correctamente")
        
        st.markdown("---")
        st.subheader("📋 Responde las preguntas:")

        # 3. Mostrar preguntas con sliders o radios
        respuestas = []
        for idx, row in df.iterrows():
            puntuacion = st.slider(
                f"**{row['Dominio']}** - {row['Pregunta']}",
                min_value=1, max_value=5, value=3, step=1
            )
            respuestas.append({
                "Dominio": row["Dominio"],
                "Pregunta": row["Pregunta"],
                "Respuesta": puntuacion
            })

        # 4. Al hacer clic en botón, procesar resultados
        if st.button("📊 Generar Informe"):
            df_resp = pd.DataFrame(respuestas)

            # 5. Calcular promedio por dominio
            resumen = df_resp.groupby("Dominio")["Respuesta"].mean().reset_index()
            resumen.columns = ["Dominio", "Promedio"]
            
            st.markdown("### 🔎 Promedios por dominio")
            st.dataframe(resumen, use_container_width=True)

            # 6. Radar chart o gráfico de barras
            chart_type = st.selectbox("Selecciona tipo de gráfico", ["Radar (Polar)", "Barras"])

            if chart_type == "Radar (Polar)":
                fig = px.line_polar(
                    resumen,
                    r='Promedio',
                    theta='Dominio',
                    line_close=True,
                    range_r=[0, 5],
                    title="Evaluación por Dominio",
                    markers=True
                )
            else:
                fig = px.bar(
                    resumen,
                    x='Dominio',
                    y='Promedio',
                    title="Evaluación por Dominio",
                    range_y=[0, 5],
                    text_auto=True,
                    color='Promedio',
                    color_continuous_scale='Viridis'
                )
            st.plotly_chart(fig, use_container_width=True)

            # 7. Indicadores tipo semáforo + interpretación
            st.markdown("### 🚦 Interpretación por dominio")
            for _, row in resumen.iterrows():
                promedio = row["Promedio"]
                dominio = row["Dominio"]

                if promedio < 2.1:
                    st.error(f"🔴 {dominio}: Riesgo Alto ({promedio:.2f}) - Urgente mejora")
                elif promedio < 3.6:
                    st.warning(f"🟡 {dominio}: Riesgo Medio ({promedio:.2f}) - Mejorar procesos")
                else:
                    st.success(f"🟢 {dominio}: Cumplimiento Bueno ({promedio:.2f}) - Buen nivel")
