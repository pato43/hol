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

cotizacion_data = pd.DataFrame({
    "Recurso": ["Materiales", "Mano de Obra", "Tiempo Estimado"],
    "Costo": [50000, 30000, 20000],
})

materiales = {
    "Material": ["Cemento", "Varilla", "Grava", "Arena"],
    "Cantidad Comprada": [100, 50, 30, 40],
    "Cantidad Presupuestada": [120, 50, 30, 50],
    "Ubicación": ["CDMX", "Puebla", "Guadalajara", "Querétaro"],
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
tabs = st.tabs([
    "Resumen", "Cotizaciones", "Materiales", "Predicciones", "Pagos", "Facturas", "Timeline", "Riesgos"
])

# --------------------- Pestaña: Resumen ---------------------
with tabs[0]:
    st.subheader("Resumen de Proyectos")
    selected_project = st.selectbox("Selecciona un Proyecto", df_proyectos["Nombre Proyecto"])
    project_info = df_proyectos[df_proyectos["Nombre Proyecto"] == selected_project].iloc[0]

    col1, col2 = st.columns(2)
    col1.metric("Estado Actual", project_info["Estado Actual"])
    col1.metric("Avance (%)", f"{project_info['Avance (%)']}%")
    col2.metric("Irregularidades Detectadas", project_info["Irregularidades Detectadas"])
    col2.metric("Fecha Fin Estimada", project_info["Fecha Fin Estimada"])

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

    st.markdown("**Ubicaciones de los Materiales:**")
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

# --------------------- Pestaña: Predicciones ---------------------
with tabs[3]:
    st.subheader("Predicciones de Avance y Duración")

    st.markdown("**Modelo: Regresión Lineal y Polinómica**")

    # Crear modelos de regresión con datos simulados
    reg_model = LinearRegression()
    x_train = np.array(range(10)).reshape(-1, 1)  # Simula un conjunto de datos
    y_train = np.random.uniform(50, 150, size=10)  # Resultados aleatorios
    reg_model.fit(x_train, y_train)

    poly_model = make_pipeline(PolynomialFeatures(2), LinearRegression())
    poly_model.fit(x_train, y_train)

    user_input = st.slider("Ingresa un avance (%):", min_value=0, max_value=100, step=5)
    pred_lineal = reg_model.predict([[user_input]])[0]
    pred_poli = poly_model.predict([[user_input]])[0]

    col1, col2 = st.columns(2)
    col1.metric("Duración Lineal Estimada", f"{pred_lineal:.2f} días")
    col2.metric("Duración Polinómica Estimada", f"{pred_poli:.2f} días")

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

    st.markdown("**Distribución de Pagos:**")
    fig_pie = px.pie(
        pagos,
        values="Pagos Realizados",
        names="Etapa",
        title="Distribución de Pagos Realizados"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

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

        pdf.cell(200, 10

=f"Monto Total: ${monto:,.2f}", ln=True)

        nombre_archivo = f"Factura_{cliente.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
        pdf.output(nombre_archivo)
        return nombre_archivo

    if st.button("Generar Factura"):
        if cliente and concepto and monto > 0:
            archivo_factura = generar_factura(cliente, concepto, monto)
            with open(archivo_factura, "rb") as file:
                st.download_button(
                    label="Descargar Factura", data=file, file_name=archivo_factura, mime="application/pdf"
                )
        else:
            st.warning("Por favor, completa todos los campos antes de generar la factura.")

# --------------------- Pestaña: Timeline ---------------------
with tabs[6]:
    st.subheader("Línea de Tiempo del Proyecto")

    st.markdown("**Progreso del Proyecto Seleccionado:**")
    timeline_data = {
        "Etapa": ["Levantamiento", "Cotización", "Compra de Materiales", "Ejecución", "Entrega"],
        "Fecha Inicio": ["2023-01-01", "2023-01-15", "2023-02-01", "2023-03-01", "2023-12-15"],
        "Fecha Fin": ["2023-01-14", "2023-01-31", "2023-02-28", "2023-12-14", "2023-12-31"],
    }
    df_timeline = pd.DataFrame(timeline_data)
    st.dataframe(df_timeline, use_container_width=True)

    fig_timeline = px.timeline(
        df_timeline,
        x_start="Fecha Inicio",
        x_end="Fecha Fin",
        y="Etapa",
        title="Línea de Tiempo del Proyecto",
    )
    st.plotly_chart(fig_timeline, use_container_width=True)

# --------------------- Pestaña: Riesgos ---------------------
with tabs[7]:
    st.subheader("Gestión de Riesgos e Irregularidades")

    st.markdown("**Irregularidades Detectadas por Proyecto:**")
    fig_irregularidades = px.bar(
        df_proyectos,
        x="Nombre Proyecto",
        y="Irregularidades Detectadas",
        title="Irregularidades Detectadas por Proyecto",
    )
    st.plotly_chart(fig_irregularidades, use_container_width=True)

    st.markdown("**Simulación de Riesgos:**")
    prob_riesgo = st.slider("Probabilidad de Riesgo (%)", min_value=0, max_value=100, step=5)
    impacto = st.slider("Impacto Estimado ($)", min_value=1000, max_value=50000, step=1000)

    riesgo_estimado = prob_riesgo / 100 * impacto
    st.metric("Riesgo Estimado", f"${riesgo_estimado:,.2f}")

  
