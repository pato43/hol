import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
from datetime import datetime
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
import folium
from streamlit_folium import st_folium

# --------------------- Configuración del Dashboard ---------------------
st.set_page_config(page_title="Holman Service Dashboard", layout="wide")

st.title("Holman Service México: Plataforma de Gestión de Obras [Demo]")

st.markdown(
    """
    ### Bienvenido:
    Esta plataforma es una herramienta de gestión integral para supervisar el progreso de proyectos, automatizar procesos y generar reportes clave. 
    ⚠️ **Nota:** Este es un entorno de demostración. Los datos y predicciones son simulados.
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
    "Fecha Inicio": ["2023-01-15", "2023-02-10", "2023-03-01"],
    "Fecha Fin Estimada": ["2023-12-31", "2024-06-30", "2024-03-31"],
}
df_proyectos = pd.DataFrame(proyectos)

# Cotizaciones simuladas
cotizacion_data = pd.DataFrame({
    "Recurso": ["Materiales", "Mano de Obra", "Tiempo Estimado"],
    "Costo": [50000, 30000, 20000],
})

# Materiales simulados (incluyendo la definición que faltaba en el error original)
materiales = {
    "Material": ["Cemento", "Varilla", "Grava", "Arena"],
    "Cantidad Comprada": [100, 50, 30, 40],
    "Cantidad Presupuestada": [120, 50, 30, 50],
    "Ubicación": ["CDMX", "Puebla", "Guadalajara", "Querétaro"],
}
df_materiales = pd.DataFrame(materiales)

# Pagos simulados
pagos = {
    "Etapa": ["Arranque", "Intermedio", "Final"],
    "Pagos Realizados": [50, 30, 0],
    "Pagos Pendientes": [50, 70, 100],
}
df_pagos = pd.DataFrame(pagos)

# Simulación para predicciones de costos finales
np.random.seed(42)
costos_iniciales = np.random.randint(100000, 300000, size=10)
inflacion_estim = costos_iniciales * (1 + np.random.normal(0.05, 0.02, size=10))
df_costos_pred = pd.DataFrame({
    "Costo Inicial": costos_iniciales,
    "Costo Final Estimado": inflacion_estim,
})

# --------------------- Navegación Principal ---------------------
tabs = st.tabs([
    "Resumen", "Cotizaciones", "Materiales", "Predicciones", "Pagos", "Facturas", "Timeline", "Riesgos"
])
# --------------------- Pestaña: Resumen ---------------------
with tabs[0]:
    st.subheader("Resumen de Proyectos")
    
    # Selección del proyecto para ver detalles
    selected_project = st.selectbox("Selecciona un Proyecto", df_proyectos["Nombre Proyecto"])
    project_info = df_proyectos[df_proyectos["Nombre Proyecto"] == selected_project].iloc[0]

    # Métricas clave del proyecto seleccionado
    col1, col2 = st.columns(2)
    col1.metric("Estado Actual", project_info["Estado Actual"])
    col1.metric("Avance (%)", f"{project_info['Avance (%)']}%")
    col2.metric("Irregularidades Detectadas", project_info["Irregularidades Detectadas"])
    col2.metric("Fecha Fin Estimada", project_info["Fecha Fin Estimada"])

    # Tabla completa de proyectos
    st.markdown("### Detalle de todos los proyectos:")
    st.dataframe(df_proyectos, use_container_width=True)

# --------------------- Pestaña: Cotizaciones ---------------------
with tabs[1]:
    st.subheader("Simulador de Costos")

    st.markdown("**Costos actuales por categoría:**")
    # Gráfico de barras para los costos por recurso
    fig_cotizaciones = px.bar(
        cotizacion_data, x="Recurso", y="Costo", text="Costo", title="Costos Estimados por Recurso"
    )
    st.plotly_chart(fig_cotizaciones, use_container_width=True)

    # Predicción de costos finales con inflación
    st.markdown("**Predicción de Costo Final Estimado:**")
    user_costo_inicial = st.slider("Ingresa un costo inicial:", min_value=100000, max_value=500000, step=5000)
    inflacion = 1.08  # 8% de inflación simulada
    costo_estimado = user_costo_inicial * inflacion
    st.metric("Costo Final Estimado", f"${costo_estimado:,.2f}")

    # Tabla de costos iniciales y finales estimados
    st.markdown("### Tabla de Predicciones de Costos:")
    st.dataframe(df_costos_pred, use_container_width=True)

# --------------------- Pestaña: Materiales ---------------------
with tabs[2]:
    st.subheader("Control de Materiales")

    st.markdown("**Comparativa de Materiales Comprados vs. Presupuestados:**")
    # Gráfico de barras para comparar cantidades compradas y presupuestadas
    fig_materiales = px.bar(
        df_materiales,
        x="Material",
        y=["Cantidad Comprada", "Cantidad Presupuestada"],
        barmode="group",
        title="Materiales Comprados vs Presupuestados"
    )
    st.plotly_chart(fig_materiales, use_container_width=True)

    st.markdown("**Ubicaciones de los Materiales:**")
    # Mapa interactivo para mostrar las ubicaciones de los materiales
    m = folium.Map(location=[19.432608, -99.133209], zoom_start=5)
    locations = {
        "CDMX": [19.432608, -99.133209],
        "Puebla": [19.041439, -98.206273],
        "Guadalajara": [20.659698, -103.349609],
        "Querétaro": [20.588793, -100.389888],
    }
    for i, row in df_materiales.iterrows():
        folium.Marker(
            location=locations[row["Ubicación"]],
            popup=f"Material: {row['Material']}<br>Cantidad Comprada: {row['Cantidad Comprada']}",
        ).add_to(m)
    st_folium(m, width=700, height=500)
# --------------------- Pestaña: Tareas Pendientes ---------------------
with tabs[3]:
    st.subheader("Gestión de Tareas Pendientes")

    st.markdown("### Lista de Tareas")
    # Tabla de tareas con estatus
    st.dataframe(df_tareas, use_container_width=True)

    st.markdown("### Actualización de Tareas")
    # Seleccionar tarea para modificar su estado
    selected_task = st.selectbox("Selecciona una Tarea", df_tareas["Tarea"])
    task_details = df_tareas[df_tareas["Tarea"] == selected_task].iloc[0]

    st.markdown(f"**Detalle de la Tarea Seleccionada:** {task_details['Descripción']}")
    new_status = st.radio(
        "Actualizar Estado", options=["Pendiente", "En Progreso", "Completada"], index=["Pendiente", "En Progreso", "Completada"].index(task_details["Estatus"])
    )

    if st.button("Actualizar Estado"):
        # Actualización simulada de la tarea
        df_tareas.loc[df_tareas["Tarea"] == selected_task, "Estatus"] = new_status
        st.success(f"Se actualizó el estado de '{selected_task}' a '{new_status}'")

# --------------------- Pestaña: Indicadores ---------------------
with tabs[4]:
    st.subheader("Indicadores Clave del Proyecto")

    # Métricas principales del proyecto
    st.markdown("### Indicadores Globales")
    col1, col2, col3 = st.columns(3)
    col1.metric("Progreso General (%)", f"{df_proyectos['Avance (%)'].mean():.2f}%")
    col2.metric("Proyectos Completados", len(df_proyectos[df_proyectos["Estado Actual"] == "Completado"]))
    col3.metric("Irregularidades Totales", df_proyectos["Irregularidades Detectadas"].sum())

    # Gráficos de indicadores
    st.markdown("### Comparativa de Avances por Proyecto")
    fig_indicadores = px.bar(
        df_proyectos,
        x="Nombre Proyecto",
        y="Avance (%)",
        text="Avance (%)",
        color="Estado Actual",
        title="Progreso por Proyecto",
    )
    st.plotly_chart(fig_indicadores, use_container_width=True)

# --------------------- Pestaña: Configuración ---------------------
with tabs[5]:
    st.subheader("Configuración")

    st.markdown("### Ajustes de Parámetros del Dashboard")
    # Entrada para modificar el factor de inflación
    st.markdown("**Factor de Inflación Simulado:**")
    new_inflation = st.slider("Selecciona el porcentaje de inflación", min_value=1.00, max_value=1.20, step=0.01, value=1.08)
    st.write(f"Inflación actual configurada: {new_inflation * 100:.2f}%")

    if st.button("Guardar Cambios"):
        inflacion = new_inflation
        st.success(f"El nuevo factor de inflación ({inflacion * 100:.2f}%) se ha aplicado correctamente.")

    st.markdown("### Reset de Datos")
    if st.button("Restaurar Valores Predeterminados"):
        st.warning("Los datos fueron restaurados a su estado inicial (Simulado).")
