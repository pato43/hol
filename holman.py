import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from fpdf import FPDF

# Configuración inicial del Dashboard
st.set_page_config(
    page_title="Dashboard de Proyectos - Holman Service México",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal del Dashboard
st.title("Dashboard de Seguimiento de Proyectos 📊")
st.markdown(
    """
    Bienvenido al **Dashboard de Seguimiento de Proyectos** de **Holman Service México**.  
    Este sistema permite visualizar el avance de los proyectos, gestionar datos, analizar anomalías y generar reportes.
    """
)

# Barra lateral con pestañas
tabs = st.sidebar.radio(
    "Navegación por etapas:",
    ("Inicio", "Etapa 1: Levantamiento", "Etapa 2: Cotización", 
     "Etapa 3: Programación de Obra", "Etapa 4: Ejecución y Monitoreo", "Generar Reporte PDF")
)

# --------------------- Pestaña: Inicio ---------------------
if tabs == "Inicio":
    st.subheader("📌 Introducción")
    st.markdown(
        """
        Este dashboard permite supervisar las etapas principales de un proyecto:
        - **Levantamiento de Información**
        - **Cotización**
        - **Programación de Obra**
        - **Ejecución y Monitoreo**
        - **Generación de Reportes**

        Utiliza los gráficos interactivos y herramientas disponibles para analizar el progreso.
        """
    )

# --------------------- Pestaña: Etapa 1: Levantamiento ---------------------
elif tabs == "Etapa 1: Levantamiento":
    st.subheader("Etapa 1: Levantamiento de Información")
    st.markdown("En esta sección se detalla el estado y progreso de los levantamientos iniciales por proyecto.")

    levantamiento_data = {
        "ID Proyecto": [1, 2, 3],
        "Nombre Proyecto": ["Edificio Corporativo A", "Planta Industrial B", "Residencial C"],
        "Responsable": ["Arq. Pérez", "Ing. López", "Arq. Martínez"],
        "Fecha Inicio Levantamiento": ["2023-01-01", "2023-02-15", "2023-03-20"],
        "Fecha Fin Levantamiento": ["2023-01-10", "2023-02-20", "2023-03-25"],
        "Estado Levantamiento": ["Completado", "En Progreso", "Pendiente"],
    }
    df_levantamiento = pd.DataFrame(levantamiento_data)
    df_levantamiento["Fecha Inicio Levantamiento"] = pd.to_datetime(df_levantamiento["Fecha Inicio Levantamiento"])
    df_levantamiento["Fecha Fin Levantamiento"] = pd.to_datetime(df_levantamiento["Fecha Fin Levantamiento"])

    st.markdown("### Información de Levantamiento por Proyecto")
    st.dataframe(df_levantamiento, use_container_width=True)

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

    selected_levantamiento = st.selectbox(
        "Selecciona un Proyecto para Detallar Levantamiento", 
        df_levantamiento["Nombre Proyecto"]
    )
    detalle_levantamiento = df_levantamiento[df_levantamiento["Nombre Proyecto"] == selected_levantamiento].iloc[0]
    st.markdown(f"""
    **Proyecto:** {detalle_levantamiento['Nombre Proyecto']}  
    **Responsable:** {detalle_levantamiento['Responsable']}  
    **Inicio:** {detalle_levantamiento['Fecha Inicio Levantamiento'].strftime('%d-%m-%Y')}  
    **Fin Estimado:** {detalle_levantamiento['Fecha Fin Levantamiento'].strftime('%d-%m-%Y')}  
    **Estado:** {detalle_levantamiento['Estado Levantamiento']}
    """)

    total_pendientes = len(df_levantamiento[df_levantamiento["Estado Levantamiento"] == "Pendiente"])
    if total_pendientes > 0:
        st.warning(f"Hay {total_pendientes} proyecto(s) pendiente(s) de levantamiento.")
# --------------------- Etapa 2: Cotización ---------------------
elif tabs == "Etapa 2: Cotización":
    st.subheader("Etapa 2: Cotización")
    st.markdown(
        "En esta etapa se lleva a cabo un análisis detallado de los costos asociados al proyecto, "
        "considerando materiales, mano de obra, equipos y otros insumos necesarios."
    )

    cotizacion_data = {
        "Concepto": ["Materiales", "Mano de Obra", "Equipos", "Transporte", "Imprevistos"],
        "Costo Unitario (MXN)": [50000, 30000, 15000, 8000, 5000],
        "Cantidad": [20, 15, 10, 5, 1],
    }
    cotizacion_df = pd.DataFrame(cotizacion_data)
    cotizacion_df["Costo Total (MXN)"] = cotizacion_df["Costo Unitario (MXN)"] * cotizacion_df["Cantidad"]

    st.markdown("### Tabla de Costos por Concepto")
    st.dataframe(cotizacion_df, use_container_width=True)

    costo_total = cotizacion_df["Costo Total (MXN)"].sum()
    st.markdown(f"### Costo Total del Proyecto: **MXN {costo_total:,.2f}**")

    fig_cotizacion = px.pie(
        cotizacion_df,
        names="Concepto",
        values="Costo Total (MXN)",
        title="Distribución de Costos del Proyecto",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig_cotizacion, use_container_width=True)

# --------------------- Etapa 3: Programación de Obra ---------------------
elif tabs == "Etapa 3: Programación de Obra":
    st.subheader("Etapa 3: Programación de Obra")
    cronograma_data = {
        "Actividad": [
            "Preparación del Terreno",
            "Adquisición de Materiales",
            "Construcción de Cimientos",
            "Estructura Principal",
            "Acabados Finales",
        ],
        "Duración (días)": [10, 15, 20, 30, 25],
        "Inicio Estimado": [
            "2024-01-01",
            "2024-01-11",
            "2024-01-26",
            "2024-02-15",
            "2024-03-17",
        ],
        "Fin Estimado": [
            "2024-01-10",
            "2024-01-25",
            "2024-02-14",
            "2024-03-16",
            "2024-04-10",
        ],
    }
    cronograma_df = pd.DataFrame(cronograma_data)

    st.markdown("### Cronograma de Actividades")
    st.dataframe(cronograma_df, use_container_width=True)

    fig_gantt = px.timeline(
        cronograma_df,
        x_start="Inicio Estimado",
        x_end="Fin Estimado",
        y="Actividad",
        title="Cronograma de Obra",
        color="Actividad",
        labels={"Actividad": "Tareas"}
    )
    fig_gantt.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(fig_gantt, use_container_width=True)

# --------------------- Generar Reporte PDF ---------------------
elif tabs == "Generar Reporte PDF":
    st.subheader("Generar Reporte PDF")
    if st.button("Generar Reporte PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Reporte de Seguimiento de Proyectos", ln=True, align="C")
        pdf.cell(200, 10, txt="Generado por Holman Service México", ln=True, align="C")
        pdf.ln(10)
        for i, row in df_levantamiento.iterrows():
            pdf.cell(0, 10, txt=f"- Proyecto: {row['Nombre Proyecto']} | Estado: {row['Estado Levantamiento']}", ln=True)
        pdf.output("reporte_seguimiento.pdf")
        st.success("¡Reporte PDF generado correctamente!")
