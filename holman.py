import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
from datetime import datetime
import numpy as np
from sklearn.linear_model import LinearRegression

# --------------------- Inicio del Dashboard ---------------------
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
proyectos = {
    "ID Proyecto": [1, 2, 3],
    "Nombre Proyecto": ["Edificio Corporativo A", "Planta Industrial B", "Residencial C"],
    "Estado Actual": ["Compra de Materiales", "Levantamiento", "Ejecución de la Obra"],
    "Avance (%)": [45, 10, 70],
    "Irregularidades Detectadas": [2, 0, 1],
}
df_proyectos = pd.DataFrame(proyectos)

cotizacion_data = pd.DataFrame({
    "Recurso": ["Materiales", "Mano de Obra", "Tiempo Estimado"],
    "Costo": [50000, 30000, 20000],
})

materiales = {
    "Material": ["Cemento", "Varilla", "Grava", "Arena"],
    "Cantidad Comprada": [100, 50, 30, 40],
    "Cantidad Presupuestada": [120, 50, 30, 50],
}
df_materiales = pd.DataFrame(materiales)

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
tabs = st.tabs(["Resumen", "Cotizaciones", "Materiales", "Predicciones", "Pagos", "Facturas"])

# --------------------- Pestaña: Resumen ---------------------
with tabs[0]:
    st.subheader("Resumen de Proyectos")
    selected_project = st.selectbox("Selecciona un Proyecto", df_proyectos["Nombre Proyecto"])
    project_info = df_proyectos[df_proyectos["Nombre Proyecto"] == selected_project].iloc[0]

    col1, col2 = st.columns(2)
    col1.metric("Estado Actual", project_info["Estado Actual"])
    col1.metric("Avance (%)", f"{project_info['Avance (%)']}%")
    col2.metric("Irregularidades Detectadas", project_info["Irregularidades Detectadas"])

    st.dataframe(df_proyectos, use_container_width=True)

# --------------------- Pestaña: Cotizaciones ---------------------
with tabs[1]:
    st.subheader("Simulador de Costos")

    st.markdown("**Costos actuales por categoría:**")
    fig_cotizaciones = px.bar(
        cotizacion_data, x="Recurso", y="Costo", text="Costo", title="Costos Estimados por Recurso"
    )
    st.plotly_chart(fig_cotizaciones, use_container_width=True)

    st.markdown("**Predicción de Costo Final Estimado:**")
    user_costo_inicial = st.slider("Ingresa un costo inicial:", min_value=100000, max_value=500000, step=5000)
    inflacion = 1.08
    costo_estimado = user_costo_inicial * inflacion
    st.metric("Costo Final Estimado", f"${costo_estimado:,.2f}")

    st.dataframe(df_costos_pred, use_container_width=True)

# --------------------- Pestaña: Materiales ---------------------
with tabs[2]:
    st.subheader("Control de Materiales")

    st.markdown("**Comparativa de Materiales Comprados vs. Presupuestados:**")
    fig_materiales = px.bar(
        df_materiales,
        x="Material",
        y=["Cantidad Comprada", "Cantidad Presupuestada"],
        barmode="group",
        title="Materiales Comprados vs Presupuestados"
    )
    st.plotly_chart(fig_materiales, use_container_width=True)

# --------------------- Pestaña: Predicciones ---------------------
with tabs[3]:
    st.subheader("Predicciones de Avance y Duración")

    st.markdown("**Modelo: Regresión Lineal**")
    reg_model = LinearRegression()
    x_train = df_costos_pred[["Costo Inicial"]]
    y_train = df_costos_pred[["Costo Final Estimado"]]
    reg_model.fit(x_train, y_train)

    user_input = st.slider("Ingresa un avance (%):", min_value=0, max_value=100, step=5)
    pred_duracion = reg_model.predict([[user_input]])[0][0]
    st.metric("Duración Estimada", f"{pred_duracion:.2f} días")

# --------------------- Pestaña: Pagos ---------------------
with tabs[4]:
    st.subheader("Seguimiento de Pagos")

    fig_pagos = px.bar(
        df_pagos,
        x="Etapa",
        y=["Pagos Realizados", "Pagos Pendientes"],
        barmode="group",
        title="Pagos Realizados vs Pendientes"
    )
    st.plotly_chart(fig_pagos, use_container_width=True)

# --------------------- Pestaña: Facturas ---------------------
with tabs[5]:
    st.subheader("Generación Automática de Facturas")

    cliente = st.text_input("Nombre del Cliente")
    concepto = st.text_area("Concepto de la Factura")
    monto = st.number_input("Monto Total", min_value=0.0, step=100.0)

    def generar_factura(cliente, concepto, monto):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(200, 10, txt="Factura", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Fecha: {datetime.now().strftime('%Y-%m-%d')}", ln=True)
        pdf.cell(200, 10, txt=f"Cliente: {cliente}", ln=True)
        pdf.ln(10)

        pdf.cell(200, 10, txt="Detalle:", ln=True)
        pdf.multi_cell(0, 10, concepto)
        pdf.ln(10)

        pdf.cell(200, 10, txt=f"Monto Total: ${monto:,.2f}", ln=True)
        return pdf

    if st.button("Generar Factura"):
        if cliente and concepto and monto > 0:
            factura_pdf = generar_factura(cliente, concepto, monto)
            file_name = f"factura_{cliente.replace(' ', '_')}.pdf"
            factura_pdf.output(file_name)

            with open(file_name, "rb") as pdf_file:
                st.download_button(
                    label="Descargar Factura", data=pdf_file, file_name=file_name, mime="application/pdf"
                )
