# Importación de librerías
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from fpdf import FPDF
from sklearn.linear_model import LinearRegression
import numpy as np
from streamlit_option_menu import option_menu

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

# Menú superior con pestañas
with st.container():
    selected_tab = option_menu(
        menu_title=None,  # Dejar vacío para ocultar el título del menú
        options=["Inicio", "Etapa 1: Levantamiento", "Etapa 2: Cotización",
                 "Etapa 3: Programación de Obra", "Anomalías y Alertas", "Generar Reporte PDF"],
        icons=["house", "pencil", "file-invoice-dollar", "calendar", "exclamation-triangle", "file-pdf"],
        menu_icon="cast",  # Icono general del menú
        default_index=0,  # Pestaña seleccionada por defecto
        orientation="horizontal",
    )

# Pestaña: Inicio
if selected_tab == "Inicio":
    st.subheader("📌 Introducción")
    st.markdown("""
    Este dashboard permite supervisar las etapas principales de un proyecto:
    - **Levantamiento de Información**
    - **Cotización**
    - **Programación y Ejecución de Obra**
    - **Detección de Anomalías y Alertas**
    Utiliza los gráficos interactivos y herramientas disponibles para analizar el progreso.
    """)
# Pestaña: Etapa 1 - Levantamiento
if selected_tab == "Etapa 1: Levantamiento":
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
# Pestaña: Etapa 2 - Cotización
if selected_tab == "Etapa 2: Cotización":
    st.subheader("Etapa 2: Cotización")
    st.markdown("""
    En esta etapa se lleva a cabo un análisis detallado de los costos asociados al proyecto, considerando los materiales, 
    mano de obra, equipos y otros insumos necesarios.
    """)

    # Datos simulados para la cotización
    cotizacion_data = {
        "Concepto": ["Materiales", "Mano de Obra", "Equipos", "Transporte", "Imprevistos"],
        "Costo Unitario (MXN)": [50000, 30000, 15000, 8000, 5000],
        "Cantidad": [20, 15, 10, 5, 1],
        "Costo Total (MXN)": [1000000, 450000, 150000, 40000, 5000],
    }
    cotizacion_df = pd.DataFrame(cotizacion_data)

    # Mostrar tabla de costos
    st.markdown("### Tabla de Costos por Concepto")
    st.dataframe(cotizacion_df, use_container_width=True)

    # Calcular costo total
    costo_total = cotizacion_df["Costo Total (MXN)"].sum()
    st.markdown(f"### Costo Total del Proyecto: **MXN {costo_total:,.2f}**")

    # Gráfico de distribución de costos
    fig_cotizacion = plt.figure(figsize=(10, 6))
    plt.pie(
        cotizacion_df["Costo Total (MXN)"],
        labels=cotizacion_df["Concepto"],
        autopct="%1.1f%%",
        colors=sns.color_palette("pastel"),
    )
    plt.title("Distribución de Costos")
    st.pyplot(fig_cotizacion)

# Pestaña: Etapa 3 - Programación de Obra
if selected_tab == "Etapa 3: Programación de Obra":
    st.subheader("Etapa 3: Programación de Obra")
    st.markdown("""
    Esta etapa organiza las actividades y tiempos del proyecto en un cronograma estructurado, asegurando 
    una ejecución eficiente y controlada.
    """)

    # Datos simulados para el cronograma de obra
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
            "2025-01-01", "2025-01-11", "2025-01-26", "2025-02-15", "2025-03-17"
        ],
        "Fin Estimado": [
            "2025-01-10", "2025-01-25", "2025-02-14", "2025-03-16", "2025-04-10"
        ],
    }
    cronograma_df = pd.DataFrame(cronograma_data)

    # Mostrar cronograma
    st.markdown("### Cronograma de Actividades")
    st.dataframe(cronograma_df, use_container_width=True)

    # Gráfico de Gantt
    st.markdown("### Gráfico de Gantt")
    fig_gantt = plt.figure(figsize=(10, 6))
    for i, row in cronograma_df.iterrows():
        plt.barh(
            row["Actividad"],
            row["Duración (días)"],
            left=pd.to_datetime(row["Inicio Estimado"]).toordinal(),
            color=sns.color_palette("pastel")[i],
        )
    plt.gca().xaxis_date()
    plt.title("Cronograma de Obra", fontsize=14)
    plt.xlabel("Fechas")
    plt.ylabel("Actividades")
    st.pyplot(fig_gantt)
# Pestaña: Anomalías y Alertas
if selected_tab == "Anomalías y Alertas":
    st.subheader("Detección de Anomalías y Alertas")
    st.markdown("""
    En esta sección se generan alertas automáticas basadas en datos simulados para identificar posibles problemas en tiempo real.
    """)

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

# Pestaña: Generar Reporte PDF
if selected_tab == "Generar Reporte PDF":
    st.subheader("Generación de Reporte en PDF")
    st.markdown("""
    Puedes generar un reporte del seguimiento de proyectos, incluyendo gráficos e información relevante.
    """)

    # Función para generar PDF
    def generar_reporte_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Título
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, txt="Reporte de Seguimiento de Proyectos", ln=True, align="C")
        pdf.ln(10)
        
        # Sección de Cotización
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, txt="Etapa 2: Cotización", ln=True)
        pdf.set_font("Arial", size=10)
        for index, row in cotizacion_df.iterrows():
            pdf.cell(200, 10, txt=f"{row['Concepto']}: MXN {row['Costo Total (MXN)']:,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Costo Total Estimado: MXN {costo_total:,.2f}", ln=True)
        pdf.ln(10)
        
        # Sección de Anomalías
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, txt="Detección de Anomalías", ln=True)
        pdf.set_font("Arial", size=10)
        for index, row in df_alertas.iterrows():
            pdf.cell(200, 10, txt=f"Proyecto: {row['Nombre Proyecto']}, Tipo: {row['Tipo Anomalía']}, Nivel: {row['Nivel de Alerta']}", ln=True)

        # Guardar PDF
        pdf.output("reporte_proyectos.pdf")
        st.success("📄 Reporte generado exitosamente: 'reporte_proyectos.pdf'")

    # Botón para generar PDF
    if st.button("Generar Reporte PDF"):
        generar_reporte_pdf()
        st.info("Puedes descargar el archivo PDF desde el directorio de ejecución.")

# Mostrar el costo estimado destacado
with st.container():
    st.markdown(f"### 💰 Costo Total Estimado: **MXN {costo_total:,.2f}**")
    st.markdown("""
    Este costo incluye los conceptos detallados en la pestaña de cotización. 
    Revisa las etapas para un análisis más detallado.
    """)
