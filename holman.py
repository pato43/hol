import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from fpdf import FPDF

# Configuración inicial del Dashboard
st.set_page_config(
    page_title="Dashboard de Proyectos - Holtmont México",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal del Dashboard
st.title("Dashboard de Seguimiento de Proyectos 📊")
st.markdown(
    """
    Bienvenido al **Dashboard de Seguimiento de Proyectos** de **Holtmont México**.  
    Este sistema permite visualizar el avance de los proyectos, gestionar datos, analizar anomalías y generar reportes.
    """
)

# Barra lateral con pestañas
tabs = st.sidebar.radio(
    "Navegación por etapas:",
    ("Inicio", "Factura Simulada", "Etapa 1: Levantamiento", "Etapa 2: Cotización", 
     "Etapa 3: Programación de Obra", "Etapa 4: Ejecución y Monitoreo", 
     "Pago de la Obra", "Generar Factura", "Generar Reporte PDF")
)

# Inicializar estado global de la factura seleccionada
if "factura_detalle" not in st.session_state:
    st.session_state["factura_detalle"] = None

# --------------------- Pestaña: Inicio ---------------------
if tabs == "Inicio":
    st.subheader("📌 Introducción")
    st.markdown(
        """
        Este dashboard permite supervisar las etapas principales de un proyecto de construcción:
        - **Levantamiento de Información**
        - **Cotización**
        - **Orden de Compra**
        - **Compra de Materiales**
        - **Programación de Obra**
        - **Ejecución de la Obra**
        - **Pago de la Obra**

        Todos los procesos se automatizan a partir de los datos de una **factura simulada**.
        """
    )

# --------------------- Pestaña: Factura Simulada ---------------------
elif tabs == "Factura Simulada":
    st.subheader("Factura Simulada")
    st.markdown(
        """
        En esta sección se generarán los datos clave para automatizar los procesos en base a la factura.
        No es necesario subir un archivo, ya que los datos se simulan para esta demo.
        """
    )

    # Simulación de factura
    factura_data = {
        "Factura": ["F001", "F002", "F003"],
        "Fecha": ["2024-01-15", "2024-02-05", "2024-03-10"],
        "Proveedor": ["Proveedor A", "Proveedor B", "Proveedor C"],
        "Monto Total (MXN)": [500000, 300000, 250000],
        "Estado de Pago": ["Pendiente", "Pagado", "Pendiente"],
        "Productos": [
            "Materiales de construcción, Mano de obra, Equipos",
            "Materiales, Mano de obra",
            "Equipos, Materiales de construcción"
        ]
    }

    df_factura = pd.DataFrame(factura_data)

    st.markdown("### Detalles de Facturas Simuladas")
    st.dataframe(df_factura, use_container_width=True)

    # Filtrar factura por número
    factura_seleccionada = st.selectbox(
        "Selecciona una factura para ver detalles", options=[""] + list(df_factura["Factura"])
    )

    # Verificar y almacenar los detalles de la factura seleccionada
    if factura_seleccionada:
        factura_detalle = df_factura[df_factura["Factura"] == factura_seleccionada].iloc[0]
        st.session_state["factura_detalle"] = factura_detalle
        st.markdown(f"""
        **Factura:** {factura_detalle['Factura']}  
        **Proveedor:** {factura_detalle['Proveedor']}  
        **Fecha de Emisión:** {factura_detalle['Fecha']}  
        **Monto Total:** MXN {factura_detalle['Monto Total (MXN)']:,.2f}  
        **Estado de Pago:** {factura_detalle['Estado de Pago']}  
        **Productos/Servicios:** {factura_detalle['Productos']}
        """)
    elif st.session_state["factura_detalle"] is not None:
        st.markdown("Se está utilizando la última factura seleccionada previamente.")
    else:
        st.warning("Por favor, selecciona una factura válida para proceder.")

    # Automatización de los puntos basados en la factura
    st.markdown("### Procesos Automatizados a partir de la Factura")
    st.markdown("1. **Levantamiento de Obra:** Se actualizan automáticamente los datos de levantamiento.")
    st.markdown("2. **Cotización:** Se genera la cotización basada en los productos mencionados.")
    st.markdown("3. **Orden de Compra:** La factura seleccionada representa la aceptación de la empresa.")
    st.markdown("4. **Compra de Materiales:** Los materiales mencionados en la factura son procesados para la compra.")
    st.markdown("5. **Programación de Obra y Timeline:** Se genera automáticamente según las fechas de la factura.")
    st.markdown("6. **Tiempo de Vida de la Obra:** Se calcula en base a la duración de la obra especificada en la factura.")
    st.markdown("7. **Ejecución de la Obra:** Se vinculan documentos como planos, contratos y planes de ejecución.")
    st.markdown("8. **Pago de la Obra:** El estado de pago se usa para activar el siguiente paso del proyecto.")

    st.success("Los procesos están automatizados basándose en los datos de la factura seleccionada.")
