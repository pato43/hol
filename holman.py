import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from fpdf import FPDF  # Librería para generar PDFs

# Configuración inicial del Dashboard
st.set_page_config(
    page_title="Dashboard de Proyectos - Holman Service México",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal del Dashboard
st.title("Dashboard de Seguimiento de Proyectos 📊")
st.markdown("""
Bienvenido al **Dashboard de Seguimiento de Proyectos** de **Holman Service México**.  
Este sistema permite visualizar el avance de los proyectos, gestionar datos, analizar anomalías y generar reportes.
""")

# Barra lateral con pestañas
tabs = st.sidebar.radio(
    "Navegación por etapas:",
    ("Inicio", "Etapa 1: Levantamiento", "Etapa 2: Cotización", 
     "Etapa 3: Programación de Obra", "Anomalías y Alertas", "Generar Reporte PDF")
)

# Función para generar PDF
def generar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Reporte de Seguimiento de Proyectos", ln=True, align="C")
    pdf.cell(200, 10, txt="Generado por Holman Service México", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=10)

    # Ejemplo: Datos de levantamiento en el PDF
    pdf.cell(0, 10, txt="Resumen de Levantamiento:", ln=True)
    for i, row in df_levantamiento.iterrows():
        pdf.cell(0, 10, txt=f"- Proyecto: {row['Nombre Proyecto']} | Estado: {row['Estado Levantamiento']}", ln=True)
    pdf.output("reporte_seguimiento.pdf")
    st.success("¡Reporte PDF generado correctamente! Descarga el archivo desde la carpeta de ejecución.")

# Pestaña: Inicio
if tabs == "Inicio":
    st.subheader("📌 Introducción")
    st.markdown("""
    Este dashboard permite supervisar las etapas principales de un proyecto:
    - **Levantamiento de Información**
    - **Cotización**
    - **Programación y Ejecución de Obra**
    - **Detección de Anomalías y Alertas**
    Utiliza los gráficos interactivos y herramientas disponibles para analizar el progreso.
    """)

# Pestaña: Levantamiento
elif tabs == "Etapa 1: Levantamiento":
    st.subheader("Etapa 1: Levantamiento de Información")
    st.markdown("En esta sección se detalla el estado y progreso de los levantamientos iniciales por proyecto.")

    # Simulación de datos para la etapa de levantamiento
    levantamiento_data = {
        "ID Proyecto": [1, 2, 3],
        "Nombre Proyecto": ["Edificio Corporativo A", "Planta Industrial B", "Residencial C"],
        "Responsable": ["Arq. Pérez", "Ing. López", "Arq. Martínez"],
        "Fecha Inicio Levantamiento": ["2023-01-01", "2023-02-15", "2023-03-20"],
        "Fecha Fin Levantamiento": ["2023-01-10", "2023-02-20", "2023-03-25"],
        "Estado Levantamiento": ["Completado", "En Progreso", "Pendiente"],
    }
    df_levantamiento = pd.DataFrame(levantamiento_data)

    # Conversión de fechas a formato datetime
    df_levantamiento["Fecha Inicio Levantamiento"] = pd.to_datetime(df_levantamiento["Fecha Inicio Levantamiento"])
    df_levantamiento["Fecha Fin Levantamiento"] = pd.to_datetime(df_levantamiento["Fecha Fin Levantamiento"])

    # Mostrar tabla de levantamiento
    st.markdown("### Información de Levantamiento por Proyecto")
    st.dataframe(df_levantamiento, use_container_width=True)

    # Gráfico de estado del levantamiento
    fig_levantamiento = px.bar(
        df_levantamiento,
        x="Nombre Proyecto",
        y=["Fecha Inicio Levantamiento", "Fecha Fin Levantamiento"],
        title="Duración del Levantamiento por Proyecto",
        labels={"value": "Fecha", "variable": "Etapa"},
        barmode="group",
        text_auto=True
    )
    st.plotly_chart(fig_levantamiento, use_container_width=True)

    # Filtro para seleccionar proyectos específicos en la etapa de levantamiento
    selected_levantamiento = st.selectbox(
        "Selecciona un Proyecto para Detallar Levantamiento", 
        df_levantamiento["Nombre Proyecto"]
    )

    # Mostrar información detallada del proyecto seleccionado
    detalle_levantamiento = df_levantamiento[df_levantamiento["Nombre Proyecto"] == selected_levantamiento].iloc[0]
    st.markdown(f"""
    **Proyecto:** {detalle_levantamiento['Nombre Proyecto']}  
    **Responsable:** {detalle_levantamiento['Responsable']}  
    **Inicio:** {detalle_levantamiento['Fecha Inicio Levantamiento'].strftime('%d-%m-%Y')}  
    **Fin Estimado:** {detalle_levantamiento['Fecha Fin Levantamiento'].strftime('%d-%m-%Y')}  
    **Estado:** {detalle_levantamiento['Estado Levantamiento']}
    """)

    # Mensaje de advertencia para proyectos pendientes
    total_pendientes = len(df_levantamiento[df_levantamiento["Estado Levantamiento"] == "Pendiente"])
    if total_pendientes > 0:
        st.warning(f"Hay {total_pendientes} proyecto(s) pendiente(s) de levantamiento.")

# Pestaña: Generar Reporte PDF
elif tabs == "Generar Reporte PDF":
    st.subheader("Generar Reporte PDF")
    st.markdown("""
    Haz clic en el botón para generar un reporte en formato PDF con los datos actuales de levantamiento.
    """)
    if st.button("Generar Reporte PDF"):
        generar_pdf()
# --------------------- Etapa 4: Ejecución y Monitoreo ---------------------
st.subheader("Etapa 4: Ejecución y Monitoreo")
st.markdown("En esta sección se realiza el seguimiento de la ejecución de los proyectos y se detectan posibles anomalías.")

# Simulación de datos para la etapa de ejecución
ejecucion_data = {
    "ID Proyecto": [1, 2, 3],
    "Nombre Proyecto": ["Edificio Corporativo A", "Planta Industrial B", "Residencial C"],
    "Progreso (%)": [100, 65, 30],
    "Desviación Presupuesto (%)": [5, -2, 10],
    "Retraso Días": [0, 5, 15],
    "Estado General": ["Finalizado", "En Progreso", "Retrasado"],
}
df_ejecucion = pd.DataFrame(ejecucion_data)

# Mostrar tabla de ejecución
st.markdown("### Información de Ejecución por Proyecto")
st.dataframe(df_ejecucion, use_container_width=True)

# Gráfico de progreso por proyecto
fig_ejecucion = px.bar(
    df_ejecucion,
    x="Nombre Proyecto",
    y="Progreso (%)",
    title="Progreso de Ejecución por Proyecto",
    color="Estado General",
    color_discrete_map={
        "Finalizado": "green",
        "En Progreso": "orange",
        "Retrasado": "red",
    },
    text_auto=True,
)
st.plotly_chart(fig_ejecucion, use_container_width=True)

# Filtro para seleccionar un proyecto específico
selected_ejecucion = st.selectbox("Selecciona un Proyecto para Detallar Ejecución", df_ejecucion["Nombre Proyecto"])

detalle_ejecucion = df_ejecucion[df_ejecucion["Nombre Proyecto"] == selected_ejecucion].iloc[0]
st.markdown(f"""
**Proyecto:** {detalle_ejecucion['Nombre Proyecto']}  
**Progreso:** {detalle_ejecucion['Progreso (%)']}%  
**Desviación Presupuesto:** {detalle_ejecucion['Desviación Presupuesto (%)']}%  
**Retraso:** {detalle_ejecucion['Retraso Días']} días  
**Estado General:** {detalle_ejecucion['Estado General']}
""")

# Advertencias sobre anomalías en ejecución
anomalías = df_ejecucion[(df_ejecucion["Desviación Presupuesto (%)"].abs() > 10) | (df_ejecucion["Retraso Días"] > 10)]
if not anomalías.empty:
    st.warning(f"⚠️ Se detectaron {len(anomalías)} anomalías en la ejecución de los proyectos.")
    st.dataframe(anomalías, use_container_width=True)

# --------------------- Detección de Anomalías ---------------------
st.subheader("Detección de Anomalías y Alertas")
st.markdown("En esta sección se generan alertas automáticas basadas en datos simulados para identificar posibles problemas en tiempo real.")

# Simulación de datos de anomalías
alertas_data = {
    "ID Proyecto": [2, 3],
    "Nombre Proyecto": ["Planta Industrial B", "Residencial C"],
    "Tipo Anomalía": ["Retraso Extremo", "Sobrecosto Significativo"],
    "Descripción": ["Retraso acumulado de 5 días", "Incremento del 10% sobre el presupuesto"],
    "Nivel de Alerta": ["Media", "Alta"],
}
df_alertas = pd.DataFrame(alertas_data)

# Mostrar tabla de alertas
st.markdown("### Alertas Detectadas")
st.dataframe(df_alertas, use_container_width=True)

# Gráfico ilustrativo de alertas
fig_alertas = px.pie(
    df_alertas,
    names="Nivel de Alerta",
    title="Distribución de Niveles de Alerta",
    color="Nivel de Alerta",
    color_discrete_map={
        "Alta": "red",
        "Media": "orange",
        "Baja": "green",
    },
)
st.plotly_chart(fig_alertas, use_container_width=True)

# --------------------- Generar Reporte en PDF ---------------------
st.subheader("Generación de Reporte en PDF")
st.markdown("Puedes generar un reporte del seguimiento de proyectos, incluyendo gráficos e información relevante.")

from fpdf import FPDF

def generar_reporte_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Título
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Reporte de Seguimiento de Proyectos", ln=True, align="C")
    pdf.ln(10)
    
    # Sección de Ejecución
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt="Etapa 4: Ejecución y Monitoreo", ln=True)
    pdf.set_font("Arial", size=10)
    for index, row in df_ejecucion.iterrows():
        pdf.cell(200, 10, txt=f"Proyecto: {row['Nombre Proyecto']}, Progreso: {row['Progreso (%)']}%, Retraso: {row['Retraso Días']} días, Estado: {row['Estado General']}", ln=True)
    pdf.ln(10)
    
    # Sección de Alertas
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt="Detección de Anomalías", ln=True)
    pdf.set_font("Arial", size=10)
    for index, row in df_alertas.iterrows():
        pdf.cell(200, 10, txt=f"Proyecto: {row['Nombre Proyecto']}, Tipo: {row['Tipo Anomalía']}, Nivel: {row['Nivel de Alerta']}", ln=True)

    # Guardar PDF
    pdf.output("reporte_proyectos.pdf")
    st.success("Reporte generado exitosamente: 'reporte_proyectos.pdf'")

# Botón para generar PDF
if st.button("Generar Reporte PDF"):
    generar_reporte_pdf()
