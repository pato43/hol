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
# --------------------- Parte 3: Programación de la Obra y Ejecución ---------------------
# Corrección y ampliación para incluir las etapas de "Programación de la Obra" y "Ejecución"

st.subheader("Etapa 3: Programación de la Obra")
st.markdown("En esta sección se gestiona la programación detallada de las obras asociadas a cada proyecto.")

# Simulación de datos para la etapa de programación de obra
programacion_data = {
    "ID Proyecto": [1, 2, 3],
    "Nombre Proyecto": ["Edificio Corporativo A", "Planta Industrial B", "Residencial C"],
    "Fecha Inicio Programación": ["2023-01-21", "2023-03-01", "2023-04-06"],
    "Fecha Fin Programación": ["2023-01-30", "2023-03-10", "2023-04-15"],
    "Estado Programación": ["Completado", "En Progreso", "Pendiente"],
}
df_programacion = pd.DataFrame(programacion_data)

# Conversión de fechas a formato datetime
df_programacion["Fecha Inicio Programación"] = pd.to_datetime(df_programacion["Fecha Inicio Programación"])
df_programacion["Fecha Fin Programación"] = pd.to_datetime(df_programacion["Fecha Fin Programación"])

# Mostrar tabla de programación de obra
st.markdown("### Información de Programación de Obra por Proyecto")
st.dataframe(df_programacion, use_container_width=True)

# Gráfico de progreso en la programación
fig_programacion = px.timeline(
    df_programacion,
    x_start="Fecha Inicio Programación",
    x_end="Fecha Fin Programación",
    y="Nombre Proyecto",
    title="Cronograma de Programación de Obra",
    color="Estado Programación",
    color_discrete_map={
        "Completado": "green",
        "En Progreso": "orange",
        "Pendiente": "red",
    },
)
fig_programacion.update_yaxes(categoryorder="total ascending")
st.plotly_chart(fig_programacion, use_container_width=True)

# Detalle de proyectos en programación
selected_programacion = st.selectbox("Selecciona un Proyecto para Detallar Programación", df_programacion["Nombre Proyecto"])

detalle_programacion = df_programacion[df_programacion["Nombre Proyecto"] == selected_programacion].iloc[0]
st.markdown(f"""
**Proyecto:** {detalle_programacion['Nombre Proyecto']}  
**Inicio de Programación:** {detalle_programacion['Fecha Inicio Programación'].strftime('%d-%m-%Y')}  
**Fin Estimado:** {detalle_programacion['Fecha Fin Programación'].strftime('%d-%m-%Y')}  
**Estado:** {detalle_programacion['Estado Programación']}
""")

# Mensaje de advertencia para programaciones pendientes
pendientes_programacion = len(df_programacion[df_programacion["Estado Programación"] == "Pendiente"])
if pendientes_programacion > 0:
    st.warning(f"Hay {pendientes_programacion} proyecto(s) pendiente(s) de programación.")

# --------------------- Etapa 4: Ejecución ---------------------
st.subheader("Etapa 4: Ejecución")
st.markdown("Esta sección detalla el progreso de la ejecución de cada obra, incluyendo fechas y estados.")

# Simulación de datos para la etapa de ejecución
ejecucion_data = {
    "ID Proyecto": [1, 2, 3],
    "Nombre Proyecto": ["Edificio Corporativo A", "Planta Industrial B", "Residencial C"],
    "Fecha Inicio Ejecución": ["2023-02-01", "2023-03-11", "2023-04-16"],
    "Fecha Fin Ejecución": ["2023-03-01", "2023-04-20", "2023-05-30"],
    "Estado Ejecución": ["Completado", "En Progreso", "Pendiente"],
    "Porcentaje Avance (%)": [100, 60, 0],
}
df_ejecucion = pd.DataFrame(ejecucion_data)

# Conversión de fechas a formato datetime
df_ejecucion["Fecha Inicio Ejecución"] = pd.to_datetime(df_ejecucion["Fecha Inicio Ejecución"])
df_ejecucion["Fecha Fin Ejecución"] = pd.to_datetime(df_ejecucion["Fecha Fin Ejecución"])

# Mostrar tabla de ejecución
st.markdown("### Información de Ejecución por Proyecto")
st.dataframe(df_ejecucion, use_container_width=True)

# Gráfico de avance de ejecución
fig_ejecucion = px.bar(
    df_ejecucion,
    x="Nombre Proyecto",
    y="Porcentaje Avance (%)",
    title="Avance de Ejecución por Proyecto",
    color="Estado Ejecución",
    color_discrete_map={
        "Completado": "green",
        "En Progreso": "orange",
        "Pendiente": "red",
    },
    text="Porcentaje Avance (%)",
)
st.plotly_chart(fig_ejecucion, use_container_width=True)

# Detalle de proyectos en ejecución
selected_ejecucion = st.selectbox("Selecciona un Proyecto para Detallar Ejecución", df_ejecucion["Nombre Proyecto"])

detalle_ejecucion = df_ejecucion[df_ejecucion["Nombre Proyecto"] == selected_ejecucion].iloc[0]
st.markdown(f"""
**Proyecto:** {detalle_ejecucion['Nombre Proyecto']}  
**Inicio de Ejecución:** {detalle_ejecucion['Fecha Inicio Ejecución'].strftime('%d-%m-%Y')}  
**Fin Estimado:** {detalle_ejecucion['Fecha Fin Ejecución'].strftime('%d-%m-%Y')}  
**Estado:** {detalle_ejecucion['Estado Ejecución']}  
**Porcentaje de Avance:** {detalle_ejecucion['Porcentaje Avance (%)']}%
""")

# Mensaje de advertencia para ejecuciones pendientes
pendientes_ejecucion = len(df_ejecucion[df_ejecucion["Estado Ejecución"] == "Pendiente"])
if pendientes_ejecucion > 0:
    st.warning(f"Hay {pendientes_ejecucion} proyecto(s) pendiente(s) de ejecución.")
# --------------------- Parte 4: Entrega y Pagos/Seguimiento ---------------------
# Corrección y ampliación para incluir las etapas de "Entrega" y "Pagos y Seguimiento"

st.subheader("Etapa 5: Entrega")
st.markdown("En esta etapa se detallan las fechas, responsables y estatus de la entrega de cada proyecto.")

# Simulación de datos para la etapa de entrega
entrega_data = {
    "ID Proyecto": [1, 2, 3],
    "Nombre Proyecto": ["Edificio Corporativo A", "Planta Industrial B", "Residencial C"],
    "Fecha Inicio Entrega": ["2023-03-02", "2023-04-21", "2023-06-01"],
    "Fecha Fin Entrega": ["2023-03-10", "2023-05-01", "2023-06-10"],
    "Estado Entrega": ["Completado", "En Progreso", "Pendiente"],
    "Responsable Entrega": ["Arq. Pérez", "Ing. López", "Arq. Martínez"],
}
df_entrega = pd.DataFrame(entrega_data)

# Conversión de fechas a formato datetime
df_entrega["Fecha Inicio Entrega"] = pd.to_datetime(df_entrega["Fecha Inicio Entrega"])
df_entrega["Fecha Fin Entrega"] = pd.to_datetime(df_entrega["Fecha Fin Entrega"])

# Mostrar tabla de entrega
st.markdown("### Información de Entrega por Proyecto")
st.dataframe(df_entrega, use_container_width=True)

# Gráfico de progreso de entrega
fig_entrega = px.timeline(
    df_entrega,
    x_start="Fecha Inicio Entrega",
    x_end="Fecha Fin Entrega",
    y="Nombre Proyecto",
    title="Cronograma de Entrega",
    color="Estado Entrega",
    color_discrete_map={
        "Completado": "green",
        "En Progreso": "orange",
        "Pendiente": "red",
    },
)
fig_entrega.update_yaxes(categoryorder="total ascending")
st.plotly_chart(fig_entrega, use_container_width=True)

# Detalle de proyectos en entrega
selected_entrega = st.selectbox("Selecciona un Proyecto para Detallar Entrega", df_entrega["Nombre Proyecto"])

detalle_entrega = df_entrega[df_entrega["Nombre Proyecto"] == selected_entrega].iloc[0]
st.markdown(f"""
**Proyecto:** {detalle_entrega['Nombre Proyecto']}  
**Inicio de Entrega:** {detalle_entrega['Fecha Inicio Entrega'].strftime('%d-%m-%Y')}  
**Fin Estimado:** {detalle_entrega['Fecha Fin Entrega'].strftime('%d-%m-%Y')}  
**Estado:** {detalle_entrega['Estado Entrega']}  
**Responsable:** {detalle_entrega['Responsable Entrega']}
""")

# Mensaje de advertencia para entregas pendientes
pendientes_entrega = len(df_entrega[df_entrega["Estado Entrega"] == "Pendiente"])
if pendientes_entrega > 0:
    st.warning(f"Hay {pendientes_entrega} proyecto(s) pendiente(s) de entrega.")

# --------------------- Etapa 6: Pagos y Seguimiento ---------------------
st.subheader("Etapa 6: Pagos y Seguimiento")
st.markdown("Aquí se monitorean los pagos realizados, pendientes y el seguimiento de los mismos.")

# Simulación de datos para la etapa de pagos y seguimiento
pagos_data = {
    "ID Proyecto": [1, 2, 3],
    "Nombre Proyecto": ["Edificio Corporativo A", "Planta Industrial B", "Residencial C"],
    "Monto Total": [500000, 1200000, 750000],
    "Monto Pagado": [500000, 600000, 0],
    "Monto Pendiente": [0, 600000, 750000],
    "Fecha Último Pago": ["2023-03-15", "2023-04-25", None],
    "Estado Pagos": ["Pagado", "Parcial", "Pendiente"],
}
df_pagos = pd.DataFrame(pagos_data)

# Conversión de fechas a formato datetime, manejo de valores nulos
df_pagos["Fecha Último Pago"] = pd.to_datetime(df_pagos["Fecha Último Pago"], errors="coerce")

# Mostrar tabla de pagos y seguimiento
st.markdown("### Información de Pagos por Proyecto")
st.dataframe(df_pagos, use_container_width=True)

# Gráfico de pagos por estado
fig_pagos = px.pie(
    df_pagos,
    names="Estado Pagos",
    values="Monto Total",
    title="Distribución del Estado de Pagos",
    color="Estado Pagos",
    color_discrete_map={
        "Pagado": "green",
        "Parcial": "orange",
        "Pendiente": "red",
    },
)
st.plotly_chart(fig_pagos, use_container_width=True)

# Detalle de pagos por proyecto
selected_pagos = st.selectbox("Selecciona un Proyecto para Detallar Pagos", df_pagos["Nombre Proyecto"])

detalle_pagos = df_pagos[df_pagos["Nombre Proyecto"] == selected_pagos].iloc[0]
ultimo_pago = (
    detalle_pagos["Fecha Último Pago"].strftime('%d-%m-%Y')
    if pd.notna(detalle_pagos["Fecha Último Pago"])
    else "No realizado"
)
st.markdown(f"""
**Proyecto:** {detalle_pagos['Nombre Proyecto']}  
**Monto Total:** ${detalle_pagos['Monto Total']:,.2f}  
**Monto Pagado:** ${detalle_pagos['Monto Pagado']:,.2f}  
**Monto Pendiente:** ${detalle_pagos['Monto Pendiente']:,.2f}  
**Último Pago Realizado:** {ultimo_pago}  
**Estado:** {detalle_pagos['Estado Pagos']}
""")

# Mensaje de advertencia para pagos pendientes
pendientes_pagos = len(df_pagos[df_pagos["Estado Pagos"] == "Pendiente"])
if pendientes_pagos > 0:
    st.warning(f"Hay {pendientes_pagos} proyecto(s) con pagos pendientes.")
