# --------------------- Parte 1: Levantamiento ---------------------
# Corrección y ampliación para incluir la etapa de "Levantamiento"

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

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
try:
    df_levantamiento["Fecha Inicio Levantamiento"] = pd.to_datetime(df_levantamiento["Fecha Inicio Levantamiento"])
    df_levantamiento["Fecha Fin Levantamiento"] = pd.to_datetime(df_levantamiento["Fecha Fin Levantamiento"])
except Exception as e:
    st.error(f"Error al convertir fechas: {e}")

# Visualización en Streamlit
st.subheader("Etapa 1: Levantamiento de Información")

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
)

st.plotly_chart(fig_levantamiento, use_container_width=True)

# Filtro para seleccionar proyectos específicos en la etapa de levantamiento
selected_levantamiento = st.selectbox("Selecciona un Proyecto para Detallar Levantamiento", df_levantamiento["Nombre Proyecto"])

# Mostrar información detallada del proyecto seleccionado
detalle_levantamiento = df_levantamiento[df_levantamiento["Nombre Proyecto"] == selected_levantamiento].iloc[0]
st.write(
    f"**Proyecto:** {detalle_levantamiento['Nombre Proyecto']}\n"
    f"**Responsable:** {detalle_levantamiento['Responsable']}\n"
    f"**Inicio:** {detalle_levantamiento['Fecha Inicio Levantamiento'].strftime('%d-%m-%Y')}\n"
    f"**Fin Estimado:** {detalle_levantamiento['Fecha Fin Levantamiento'].strftime('%d-%m-%Y')}\n"
    f"**Estado:** {detalle_levantamiento['Estado Levantamiento']}"
)

# Mensaje de advertencia para proyectos pendientes
total_pendientes = len(df_levantamiento[df_levantamiento["Estado Levantamiento"] == "Pendiente"])
if total_pendientes > 0:
    st.warning(f"Hay {total_pendientes} proyectos pendientes de levantamiento.")
