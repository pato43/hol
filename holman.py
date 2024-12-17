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
        "Selecciona una factura para ver detalles", df_factura["Factura"]
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

# --------------------- Etapa 2: Cotización ---------------------
elif tabs == "Etapa 2: Cotización":
    st.subheader("Etapa 2: Cotización")
    st.markdown("En esta etapa se genera la cotización automática basada en los productos de la factura seleccionada.")

    # Validar si hay una factura seleccionada y extraer productos relacionados
    if "factura_detalle" in locals() and not factura_detalle.empty:
        productos_relacionados = factura_detalle.get("Productos", "")
        if not isinstance(productos_relacionados, str) or not productos_relacionados.strip():
            productos_relacionados = "Sin productos relacionados"
    else:
        st.error("Por favor, selecciona una factura válida en la sección anterior para generar la cotización.")
        productos_relacionados = "Sin productos relacionados"

    # Simulación de costos para los productos en la factura seleccionada
    productos = productos_relacionados.split(", ") if isinstance(productos_relacionados, str) else []
    if productos:
        st.markdown("### Productos Relacionados")
        for idx, producto in enumerate(productos, 1):
            st.markdown(f"{idx}. {producto}")

        # Simulación de costos y cantidades
        costos_unitarios = [50000, 30000, 15000, 20000, 10000][:len(productos)]  # Costos simulados
        cantidades = [5, 10, 7, 3, 8][:len(productos)]  # Cantidades simuladas

        cotizacion_data = {
            "Producto": productos,
            "Costo Unitario (MXN)": costos_unitarios,
            "Cantidad": cantidades,
        }
        df_cotizacion = pd.DataFrame(cotizacion_data)
        df_cotizacion["Costo Total (MXN)"] = df_cotizacion["Costo Unitario (MXN)"] * df_cotizacion["Cantidad"]

        st.markdown("### Cotización Detallada")
        st.dataframe(df_cotizacion, use_container_width=True)

        # Mostrar costos totales
        costo_total_cotizacion = df_cotizacion["Costo Total (MXN)"].sum()
        st.markdown(f"### Costo Total de la Cotización: **MXN {costo_total_cotizacion:,.2f}**")

        # Detalle por producto
        st.markdown("### Detalles de Costos por Producto")
        for _, row in df_cotizacion.iterrows():
            st.markdown(
                f"""
                - **Producto:** {row['Producto']}  
                  **Costo Unitario:** MXN {row['Costo Unitario (MXN)']:,.2f}  
                  **Cantidad:** {row['Cantidad']}  
                  **Costo Total:** MXN {row['Costo Total (MXN)']:,.2f}
                """
            )
    else:
        st.warning("No se encontraron productos relacionados en la factura seleccionada.")

    # Sección interactiva para simular ajustes de costos
    st.markdown("### Ajustes de Cotización")
    st.markdown("Puedes modificar los costos unitarios y cantidades estimadas para analizar diferentes escenarios.")
    for idx, producto in enumerate(productos):
        nuevo_costo = st.number_input(
            f"Costo Unitario para {producto} (MXN):",
            min_value=0,
            value=costos_unitarios[idx],
            step=1000
        )
        nueva_cantidad = st.number_input(
            f"Cantidad para {producto}:",
            min_value=0,
            value=cantidades[idx],
            step=1
        )
        df_cotizacion.loc[idx, "Costo Unitario (MXN)"] = nuevo_costo
        df_cotizacion.loc[idx, "Cantidad"] = nueva_cantidad
        df_cotizacion.loc[idx, "Costo Total (MXN)"] = nuevo_costo * nueva_cantidad

    # Mostrar tabla de cotización actualizada
    st.markdown("### Cotización Ajustada")
    st.dataframe(df_cotizacion, use_container_width=True)

    # Calcular nuevo costo total
    costo_total_actualizado = df_cotizacion["Costo Total (MXN)"].sum()
    st.markdown(f"### Nuevo Costo Total de la Cotización: **MXN {costo_total_actualizado:,.2f}**")
# --------------------- Etapa 3: Programación de Obra ---------------------
elif tabs == "Etapa 3: Programación de Obra":
    st.subheader("Etapa 3: Programación de Obra")
    st.markdown("La programación de la obra se genera automáticamente con base en la cotización y la factura seleccionada.")

    # Simulación de cronograma
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

    # Gráfico de Gantt
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

    # Cálculo estimado de costos por actividad
    costo_diario = st.number_input("Introduce el costo diario promedio por actividad (MXN):", min_value=0, value=5000, step=1000)
    cronograma_df["Costo Estimado (MXN)"] = cronograma_df["Duración (días)"] * costo_diario

    st.dataframe(cronograma_df[["Actividad", "Duración (días)", "Costo Estimado (MXN)"]], use_container_width=True)

    # Gráfico de costos estimados
    fig_costos = px.bar(
        cronograma_df,
        x="Actividad",
        y="Costo Estimado (MXN)",
        title="Costo Estimado por Actividad",
        text_auto=True,
        color="Actividad",
    )
    st.plotly_chart(fig_costos, use_container_width=True)

# --------------------- Etapa 4: Ejecución y Monitoreo ---------------------
elif tabs == "Etapa 4: Ejecución y Monitoreo":
    st.subheader("Etapa 4: Ejecución y Monitoreo")
    st.markdown(
        "En esta etapa se realiza el seguimiento del progreso del proyecto, "
        "así como la entrega de documentación asociada."
    )

    # Simulación de datos de ejecución
    ejecucion_data = {
        "ID Proyecto": [1, 2, 3],
        "Nombre Proyecto": ["Edificio Corporativo A", "Planta Industrial B", "Residencial C"],
        "Progreso (%)": [100, 65, 30],
        "Documentos Entregados": [
            "Planos, Contratos, Reporte de Sueldos",
            "Planos, Contratos",
            "Pendiente"
        ],
        "Estado General": ["Finalizado", "En Progreso", "Retrasado"],
    }
    df_ejecucion = pd.DataFrame(ejecucion_data)

    st.markdown("### Estado de Ejecución por Proyecto")
    st.dataframe(df_ejecucion, use_container_width=True)

    # Gráfico de progreso por proyecto
    fig_ejecucion = px.bar(
        df_ejecucion,
        x="Nombre Proyecto",
        y="Progreso (%)",
        title="Progreso de Ejecución por Proyecto",
        color="Estado General",
        color_discrete_map={"Finalizado": "green", "En Progreso": "orange", "Retrasado": "red"},
        text_auto=True,
    )
    st.plotly_chart(fig_ejecucion, use_container_width=True)

    # Selección de proyecto para detalles
    proyecto_seleccionado = st.selectbox("Selecciona un Proyecto para Ver Detalles", df_ejecucion["Nombre Proyecto"])
    detalle_ejecucion = df_ejecucion[df_ejecucion["Nombre Proyecto"] == proyecto_seleccionado].iloc[0]
    st.markdown(f"""
    **Proyecto:** {detalle_ejecucion['Nombre Proyecto']}  
    **Progreso:** {detalle_ejecucion['Progreso (%)']}%  
    **Documentos Entregados:** {detalle_ejecucion['Documentos Entregados']}  
    **Estado General:** {detalle_ejecucion['Estado General']}
    """)

# --------------------- Etapa de Pago ---------------------
elif tabs == "Pago de la Obra":
    st.subheader("Etapa 5: Pago de la Obra")
    st.markdown("Control del estado de pago según la factura seleccionada.")

    # Estado del pago basado en la factura seleccionada
    if "factura_detalle" in locals() and not factura_detalle.empty:
        st.markdown("### Información de la Factura Seleccionada")
        st.markdown(f"""
        **Factura:** {factura_detalle['Factura']}  
        **Monto Total:** MXN {factura_detalle['Monto Total (MXN)']:,.2f}  
        **Estado de Pago:** {factura_detalle['Estado de Pago']}
        """)

        if factura_detalle["Estado de Pago"] == "Pendiente":
            st.warning("El pago aún está pendiente.")
        else:
            st.success("El pago ha sido completado.")
    else:
        st.error("No se ha seleccionado una factura válida para verificar el estado de pago.")

# --------------------- Generación del Reporte PDF ---------------------
elif tabs == "Generar Reporte PDF":
    st.subheader("Generar Reporte PDF")
    st.markdown("Genera un reporte completo con todos los datos procesados del proyecto.")

    def generar_reporte_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Título principal
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, txt="Reporte de Seguimiento de Proyectos - Holtmont México", ln=True, align="C")
        pdf.ln(10)

        # Sección: Factura
        if "factura_detalle" in locals() and not factura_detalle.empty:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(200, 10, txt="Factura Simulada", ln=True)
            pdf.set_font("Arial", size=10)
            pdf.cell(
                0, 10,
                txt=f"Factura: {factura_detalle['Factura']} | Proveedor: {factura_detalle['Proveedor']} | "
                    f"Monto Total: MXN {factura_detalle['Monto Total (MXN)']:,.2f} | Estado: {factura_detalle['Estado de Pago']}",
                ln=True
            )
            pdf.ln(10)

        # Sección: Levantamiento
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, txt="Etapa 1: Levantamiento", ln=True)
        pdf.set_font("Arial", size=10)
        if "df_levantamiento" in locals() and not df_levantamiento.empty:
            for _, row in df_levantamiento.iterrows():
                pdf.cell(0, 10, txt=f"- Proyecto: {row['Nombre Proyecto']} | Estado: {row['Estado Levantamiento']}", ln=True)
            pdf.ln(10)

        # Sección: Cotización
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, txt="Etapa 2: Cotización", ln=True)
        pdf.set_font("Arial", size=10)
        if "df_cotizacion" in locals() and not df_cotizacion.empty:
            for _, row in df_cotizacion.iterrows():
                pdf.cell(
                    0, 10,
                    txt=f"Producto: {row['Producto']} | Costo Unitario: MXN {row['Costo Unitario (MXN)']:,.2f} | "
                        f"Cantidad: {row['Cantidad']} | Costo Total: MXN {row['Costo Total (MXN)']:,.2f}",
                    ln=True
                )
            pdf.ln(10)

        # Sección: Cronograma
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, txt="Etapa 3: Programación de Obra", ln=True)
        pdf.set_font("Arial", size=10)
        if "cronograma_df" in locals() and not cronograma_df.empty:
            for _, row in cronograma_df.iterrows():
                pdf.cell(
                    0, 10,
                    txt=f"Actividad: {row['Actividad']} | Duración: {row['Duración (días)']} días | "
                        f"Costo Estimado: MXN {row['Costo Estimado (MXN)']:,.2f}",
                    ln=True
                )
            pdf.ln(10)

        return pdf

    # Generar y descargar el PDF
    if st.button("Generar Reporte PDF"):
        pdf = generar_reporte_pdf()
        pdf_path = "reporte_completo.pdf"
        pdf.output(pdf_path)
        with open(pdf_path, "rb") as file:
            btn = st.download_button(
                label="Descargar Reporte PDF",
                data=file,
                file_name="reporte_completo.pdf",
                mime="application/pdf"
            )
        st.success("¡Reporte PDF generado correctamente!")
