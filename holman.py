import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
from datetime import datetime
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression

# --------------------- Inicio del Dashboard ---------------------
# Título y descripción principal
st.title("Holman Service México: Plataforma de Gestión de Obras [Demo]")

st.markdown(
    """
    ### Contexto:
    *Automatiza procesos, centraliza información y detecta irregularidades para optimizar la gestión de proyectos.*
    
    Esta plataforma web permite a Holman Service tener una visión completa del progreso de las obras, asegurando un control preciso y facilitando la toma de decisiones en tiempo real.
    """
)

# --------------------- Datos Simulados ---------------------
# Proyectos simulados
proyectos = {
    "ID Proyecto": [1, 2, 3],
    "Nombre Proyecto": ["Edificio Corporativo A", "Planta Industrial B", "Residencial C"],
    "Estado Actual": ["Compra de Materiales", "Levantamiento", "Ejecución de la Obra"],
    "Avance (%)": [45, 10, 70],
    "Irregularidades Detectadas": [2, 0, 1],
}
df_proyectos = pd.DataFrame(proyectos)

# Irregularidades simuladas
irregularidades = {
    "Tipo": ["Documentos Faltantes", "Retrasos en Entrega", "Pagos Pendientes"],
    "Etapa Afectada": ["Compra de Materiales", "Cotización", "Ejecución de la Obra"],
    "Acción Requerida": [
        "Subir documentos faltantes",
        "Revisar cronograma",
        "Solicitar pago parcial",
    ],
}
df_irregularidades = pd.DataFrame(irregularidades)

# Materiales simulados
materiales = {
    "Material": ["Cemento", "Varilla", "Grava", "Arena"],
    "Cantidad Comprada": [100, 50, 30, 40],
    "Cantidad Presupuestada": [120, 50, 30, 50],
}
df_materiales = pd.DataFrame(materiales)

# Pagos simulados
pagos = {
    "Etapa": ["Arranque", "Intermedio", "Final"],
    "Pagos Realizados": [50, 30, 0],
    "Pagos Pendientes": [50, 70, 100],
}
df_pagos = pd.DataFrame(pagos)

# Datos de predicción simulados
np.random.seed(42)
avances = np.random.randint(5, 95, size=10)
duraciones = avances / 10 + np.random.normal(0, 2, size=10)
df_prediccion = pd.DataFrame({"Avance (%)": avances, "Duración Estimada (días)": duraciones})

# --------------------- Selección de Proyecto ---------------------
st.sidebar.header("Navegación del Dashboard")
st.sidebar.markdown("**Selecciona un proyecto para gestionar y analizar:**")
selected_project = st.sidebar.selectbox("Proyectos disponibles", df_proyectos["Nombre Proyecto"])

# Datos del proyecto seleccionado
project_info = df_proyectos[df_proyectos["Nombre Proyecto"] == selected_project].iloc[0]
st.sidebar.markdown("---")
st.sidebar.markdown("**Opciones adicionales:**")
st.sidebar.button("Actualizar Datos")
st.sidebar.checkbox("Mostrar predicciones de IA")
st.sidebar.button("Configurar Alertas")

# --------------------- Sección: Levantamiento ---------------------
st.subheader(f"Levantamiento del Proyecto: {selected_project}")
st.markdown("**Observaciones recopiladas durante la etapa inicial del proyecto.**")
levantamiento_df = pd.DataFrame({
    "Observación": ["Mediciones incompletas", "Falta de fotos", "Descripción detallada"],
    "Cumplido": ["No", "Sí", "No"],
})
st.dataframe(levantamiento_df, use_container_width=True)
st.warning("Algunas observaciones no han sido cumplidas. Por favor revisa los datos cargados.")

# --------------------- Sección: Cotización ---------------------
st.subheader("Cotización de Costos")
# Calculadora de costos simulada
cotizacion_data = pd.DataFrame({
    "Recurso": ["Materiales", "Mano de Obra", "Tiempo Estimado"],
    "Costo": [50000, 30000, 20000],
})
st.dataframe(cotizacion_data, use_container_width=True)

st.markdown("**Estado de Cotizaciones:**")
fig_cotizaciones = px.bar(
    cotizacion_data, x="Recurso", y="Costo", text="Costo", title="Costos Estimados por Recurso"
)
st.plotly_chart(fig_cotizaciones, use_container_width=True)

# --------------------- Sección: Compra de Materiales ---------------------
st.subheader("Compra de Materiales")
st.markdown("**Control de Inventarios:** Materiales comprados vs. presupuestados.")
fig_materiales = px.bar(
    df_materiales,
    x="Material",
    y=["Cantidad Comprada", "Cantidad Presupuestada"],
    barmode="group",
    title="Comparativa de Materiales"
)
st.plotly_chart(fig_materiales, use_container_width=True)

# --------------------- Sección: Predicciones con IA ---------------------
st.subheader("Predicciones de Progreso y Duración (IA)")
st.markdown(
    "**Modelo utilizado:** Regresión Lineal para predecir la duración estimada con base en el avance."  
)
reg_model = LinearRegression()
x_train = df_prediccion[["Avance (%)"]]
y_train = df_prediccion[["Duración Estimada (días)"]]
reg_model.fit(x_train, y_train)

# Entrada de usuario para predicción
user_avance = st.slider("Selecciona el porcentaje de avance:", min_value=0, max_value=100, value=50)
pred_duracion = reg_model.predict([[user_avance]])[0][0]
st.metric(label="Duración Estimada", value=f"{pred_duracion:.2f} días")

# --------------------- Sección: Pagos ---------------------
st.subheader("Seguimiento de Pagos")
st.markdown("**Pagos realizados vs. pendientes:**")
fig_pagos = px.bar(
    df_pagos, 
    x="Etapa", 
    y=["Pagos Realizados", "Pagos Pendientes"], 
    barmode="group", 
    title="Seguimiento de Pagos"
)
st.plotly_chart(fig_pagos, use_container_width=True)

# --------------------- Generación de Reporte ---------------------
st.subheader("Generación de Reportes en PDF")

def generar_reporte_pdf(proyecto, avance, irregularidades_df, materiales_df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Título
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 10, txt="Reporte del Proyecto", ln=True, align="C")
    pdf.ln(10)

    # Información del Proyecto
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Nombre del Proyecto: {proyecto}", ln=True)
    pdf.cell(200, 10, txt=f"Avance General: {avance}%", ln=True)
    pdf.ln(10)

    # Tabla de Irregularidades
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Irregularidades Detectadas:", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", size=10)
    for index, row in irregularidades_df.iterrows():
        pdf.cell(200, 10, txt=f"- {row['Tipo']} en {row['Etapa Afectada']}: {row['Acción Requerida']}", ln=True)
    pdf.ln(10)

    # Tabla de Materiales
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, txt="Control de Materiales:", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", size=10)
    for index, row in materiales_df.iterrows():
        pdf.cell(200, 10, txt=f"- {row['Material']}: {row['Cantidad Comprada']} comprados de {row['Cantidad Presupuestada']}", ln=True)

    return pdf
  # Botón para generar el reporte en PDF
if st.button("Generar Reporte PDF"):
    pdf = generar_reporte_pdf(
        proyecto=selected_project,
        avance=project_info["Avance (%)"],
        irregularidades_df=df_irregularidades,
        materiales_df=df_materiales,
    )
    
    # Guardar el archivo temporalmente y mostrar el enlace de descarga
    file_name = f"reporte_{selected_project.replace(' ', '_')}.pdf"
    pdf.output(file_name)
    with open(file_name, "rb") as pdf_file:
        st.download_button(
            label="Descargar Reporte PDF",
            data=pdf_file,
            file_name=file_name,
            mime="application/pdf"
        )
