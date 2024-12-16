# --------------------- Parte 1: Levantamiento ---------------------
# Corrección y ampliación para incluir la etapa de "Levantamiento"

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Título principal del Dashboard
st.title("Dashboard de Seguimiento de Proyectos - Holman Service México")
st.sidebar.title("Menú de Navegación")
st.sidebar.markdown("Selecciona una etapa del proceso")

# Sección de Levantamiento
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
selected_levantamiento = st.selectbox("Selecciona un Proyecto para Detallar Levantamiento", df_levantamiento["Nombre Proyecto"])

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
# --------------------- Parte 2: Cotización ---------------------
# Corrección y ampliación para incluir la etapa de "Cotización"

st.subheader("Etapa 2: Cotización")
st.markdown("En esta sección se detalla el progreso de las cotizaciones asociadas a cada proyecto.")

# Simulación de datos para la etapa de cotización
cotizacion_data = {
    "ID Proyecto": [1, 2, 3],
    "Nombre Proyecto": ["Edificio Corporativo A", "Planta Industrial B", "Residencial C"],
    "Costo Estimado (MXN)": [500000, 1200000, 750000],
    "Fecha Inicio Cotización": ["2023-01-11", "2023-02-21", "2023-03-26"],
    "Fecha Fin Cotización": ["2023-01-20", "2023-02-28", "2023-04-05"],
    "Estado Cotización": ["Completado", "En Progreso", "Pendiente"],
}
df_cotizacion = pd.DataFrame(cotizacion_data)

# Conversión de fechas a formato datetime
df_cotizacion["Fecha Inicio Cotización"] = pd.to_datetime(df_cotizacion["Fecha Inicio Cotización"])
df_cotizacion["Fecha Fin Cotización"] = pd.to_datetime(df_cotizacion["Fecha Fin Cotización"])

# Mostrar tabla de cotización
st.markdown("### Información de Cotización por Proyecto")
st.dataframe(df_cotizacion, use_container_width=True)

# Gráfico de costo estimado por proyecto
fig_cotizacion = px.bar(
    df_cotizacion,
    x="Nombre Proyecto",
    y="Costo Estimado (MXN)",
    title="Costo Estimado por Proyecto",
    labels={"Costo Estimado (MXN)": "Costo en MXN"},
    text_auto=True,
    color="Estado Cotización",
    color_discrete_map={
        "Completado": "green",
        "En Progreso": "orange",
        "Pendiente": "red",
    }
)
st.plotly_chart(fig_cotizacion, use_container_width=True)

# Filtro para seleccionar proyectos específicos en la etapa de cotización
selected_cotizacion = st.selectbox("Selecciona un Proyecto para Detallar Cotización", df_cotizacion["Nombre Proyecto"])

# Mostrar información detallada del proyecto seleccionado
detalle_cotizacion = df_cotizacion[df_cotizacion["Nombre Proyecto"] == selected_cotizacion].iloc[0]
st.markdown(f"""
**Proyecto:** {detalle_cotizacion['Nombre Proyecto']}  
**Costo Estimado:** ${detalle_cotizacion['Costo Estimado (MXN)']:,.2f}  
**Inicio:** {detalle_cotizacion['Fecha Inicio Cotización'].strftime('%d-%m-%Y')}  
**Fin Estimado:** {detalle_cotizacion['Fecha Fin Cotización'].strftime('%d-%m-%Y')}  
**Estado:** {detalle_cotizacion['Estado Cotización']}
""")

# Mensaje de advertencia para cotizaciones pendientes
total_pendientes_cotizacion = len(df_cotizacion[df_cotizacion["Estado Cotización"] == "Pendiente"])
if total_pendientes_cotizacion > 0:
    st.warning(f"Hay {total_pendientes_cotizacion} proyecto(s) pendiente(s) de cotización.")
