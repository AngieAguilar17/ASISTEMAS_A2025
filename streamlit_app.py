import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Auditoría TI", layout="wide")
st.title("🧩 Evaluación de Auditoría de Servicios de TI")

# Lista con todas las preguntas y dominios según tu tabla
preguntas = [
    {"Dominio": "Mejora Continua", "Pregunta": "¿Existe un proceso formal y documentado para identificar, registrar y priorizar oportunidades de mejora en los servicios de TI?"},
    {"Dominio": "Mejora Continua", "Pregunta": "¿Se utilizan métricas y reportes de manera consistente para medir el progreso y demostrar el éxito de las iniciativas de mejora?"},
    {"Dominio": "Mejora Continua", "Pregunta": "¿La cultura organizacional fomenta activamente la participación de todo el personal en las actividades de mejora continua?"},
    {"Dominio": "Control de Cambios", "Pregunta": "¿La organización sigue un procedimiento formal para la gestión de todos los cambios de TI, incluyendo la evaluación de riesgos, el impacto y la autorización?"},
    {"Dominio": "Control de Cambios", "Pregunta": "¿Se comunican eficazmente los cambios planificados y ejecutados a todas las partes interesadas relevantes para minimizar interrupciones?"},
    {"Dominio": "Control de Cambios", "Pregunta": "¿Existe una clara distinción y un manejo adecuado para los diferentes tipos de cambio (estándar, normal y de emergencia)?"},
    {"Dominio": "Gestión de Incidentes", "Pregunta": "¿Todos los incidentes son registrados, clasificados y priorizados de forma consistente según su impacto y urgencia?"},
    {"Dominio": "Gestión de Incidentes", "Pregunta": "¿Se cuenta con un proceso documentado para la resolución de incidentes, incluyendo escalamiento, con el objetivo de restaurar el servicio dentro de los SLAs acordados?"},
    {"Dominio": "Gestión de Incidentes", "Pregunta": "¿Se mantiene a los usuarios informados de manera proactiva sobre el estado y la resolución de sus incidentes?"},
    {"Dominio": "Gestión de Problemas", "Pregunta": "¿Se lleva a cabo un análisis estructurado para identificar las causas raíz de los incidentes recurrentes o de alto impacto?"},
    {"Dominio": "Gestión de Problemas", "Pregunta": "¿Se documentan y gestionan eficazmente las soluciones temporales (workarounds) y los errores conocidos (known errors)?"},
    {"Dominio": "Gestión de Problemas", "Pregunta": "¿Se implementan soluciones permanentes para los problemas con el fin de prevenir la recurrencia de incidentes?"},
    {"Dominio": "Gestión de Solicitudes de Servicio", "Pregunta": "¿Se dispone de un catálogo de servicios claro y accesible para que los usuarios puedan realizar solicitudes de servicio predefinidas?"},
    {"Dominio": "Gestión de Solicitudes de Servicio", "Pregunta": "¿El proceso para cumplir con las solicitudes de servicio está estandarizado y, en la medida de lo posible, automatizado para garantizar eficiencia?"},
    {"Dominio": "Gestión de Solicitudes de Servicio", "Pregunta": "¿Se establecen y comunican a los usuarios los tiempos esperados para el cumplimiento de cada tipo de solicitud de servicio?"},
    {"Dominio": "Mesa de Servicio", "Pregunta": "¿La Mesa de Servicio actúa como un punto único de contacto (SPOC) eficaz y bien conocido para todas las consultas y reportes de los usuarios?"},
    {"Dominio": "Mesa de Servicio", "Pregunta": "¿El personal de la Mesa de Servicio posee las habilidades (técnicas y de comunicación) y las herramientas necesarias para resolver un alto porcentaje de las solicitudes en el primer contacto?"},
    {"Dominio": "Mesa de Servicio", "Pregunta": "¿Se mide y analiza de forma regular la satisfacción del usuario con el soporte proporcionado por la Mesa de Servicio para identificar áreas de mejora?"},
    {"Dominio": "Gestión de Nivel de Servicio", "Pregunta": "¿Se han negociado, documentado y acordado formalmente los Acuerdos de Nivel de Servicio (SLA) con los clientes, basándose en los resultados de negocio?"},
    {"Dominio": "Gestión de Nivel de Servicio", "Pregunta": "¿Se monitorea de manera continua el desempeño de los servicios y se compara con las metas establecidas en los SLAs?"},
    {"Dominio": "Gestión de Nivel de Servicio", "Pregunta": "¿Se realizan revisiones periódicas de los SLAs con los clientes para asegurar que sigan siendo relevantes y que se esté entregando el valor esperado?"},
]

st.markdown("---")
st.subheader("📋 Responde las preguntas:")

respuestas = []
for idx, item in enumerate(preguntas):
    puntuacion = st.slider(
        f"**{item['Dominio']}** - {item['Pregunta']}",
        min_value=1, max_value=5, value=3, step=1,
        key=f"slider_{idx}"
    )
    respuestas.append({
        "Dominio": item["Dominio"],
        "Pregunta": item["Pregunta"],
        "Respuesta": puntuacion
    })

if st.button("📊 Generar Informe"):
    df_resp = pd.DataFrame(respuestas)

    # Calcular promedio por dominio
    resumen = df_resp.groupby("Dominio")["Respuesta"].mean().reset_index()
    resumen.columns = ["Dominio", "Promedio"]

    st.markdown("### 🔎 Promedios por dominio")
    st.dataframe(resumen, use_container_width=True)

    # Selección tipo de gráfico
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

    # Indicadores tipo semáforo + interpretación
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
