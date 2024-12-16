import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from fpdf import FPDF  # Librería para generar PDFs

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

# Barra lateral con pestañas
tabs = st.sidebar.radio(
    "Navegación por etapas:",
    ("Inicio", "Etapa 1: Levantamiento", "Etapa 2: Cotización", 
     "Etapa 3: Programación de Obra", "Anomalías y Alertas", "Generar Reporte PDF")
)

# Función para generar PDF
def generar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Reporte de Seguimiento de Proyectos", ln=True, align="C")
    pdf.cell(200, 10, txt="Generado por Holman Service México", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=10)

    # Ejemplo: Datos de levantamiento en el PDF
    pdf.cell(0, 10, txt="Resumen de Levantamiento:", ln=True)
    for i, row in df_levantamiento.iterrows():
        pdf.cell(0, 10, txt=f"- Proyecto: {row['Nombre Proyecto']} | Estado: {row['Estado Levantamiento']}", ln=True)
    pdf.output("reporte_seguimiento.pdf")
    st.success("¡Reporte PDF generado correctamente! Descarga el archivo desde la carpeta de ejecución.")

# Pestaña: Inicio
if tabs == "Inicio":
    st.subheader("📌 Introducción")
    st.markdown("""
    Este dashboard permite supervisar las etapas principales de un proyecto:
    - **Levantamiento de Información**
    - **Cotización**
    - **Programación y Ejecución de Obra**
    - **Detección de Anomalías y Alertas**
    Utiliza los gráficos interactivos y herramientas disponibles para analizar el progreso.
    """)

# Pestaña: Levantamiento
elif tabs == "Etapa 1: Levantamiento":
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

# Pestaña: Generar Reporte PDF
elif tabs == "Generar Reporte PDF":
    st.subheader("Generar Reporte PDF")
    st.markdown("""
    Haz clic en el botón para generar un reporte en formato PDF con los datos actuales de levantamiento.
    """)
    if st.button("Generar Reporte PDF"):
        generar_pdf()
# --------------------- Etapa 2: Cotización ---------------------
st.header("Etapa 2: Cotización")

st.markdown(
    """
    En esta etapa se lleva a cabo un análisis detallado de los costos asociados al proyecto, considerando los materiales, 
    mano de obra, equipos y otros insumos necesarios. 
    """
)

# Mostrar tabla de cotización
st.markdown("### Tabla de Costos por Concepto")
cotizacion = {
    "Concepto": ["Materiales", "Mano de Obra", "Equipos", "Transporte", "Imprevistos"],
    "Costo Unitario (MXN)": [50000, 30000, 15000, 8000, 5000],
    "Cantidad": [20, 15, 10, 5, 1],
    "Costo Total (MXN)": [1000000, 450000, 150000, 40000, 5000],
}

cotizacion_df = pd.DataFrame(cotizacion)
cotizacion_df["Costo Total (MXN)"] = (
    cotizacion_df["Costo Unitario (MXN)"] * cotizacion_df["Cantidad"]
)

st.dataframe(cotizacion_df)

# Mostrar costos totales
st.markdown("### Costo Total del Proyecto")
costo_total = cotizacion_df["Costo Total (MXN)"].sum()
st.write(f"El costo total estimado del proyecto es **MXN {costo_total:,.2f}**.")

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

# --------------------- Etapa 3: Programación de Obra ---------------------
st.header("Etapa 3: Programación de Obra")

st.markdown(
    """
    Esta etapa organiza las actividades y tiempos del proyecto en un cronograma estructurado, asegurando 
    una ejecución eficiente y controlada.
    """
)

# Mostrar cronograma
st.markdown("### Cronograma de Actividades")
cronograma = {
    "Actividad": [
        "Preparación del Terreno",
        "Adquisición de Materiales",
        "Construcción de Cimientos",
        "Estructura Principal",
        "Acabados Finales",
    ],
    "Duración (días)": [10, 15, 20, 30, 25],
    "Inicio Estimado": [
        "2025-01-01",
        "2025-01-11",
        "2025-01-26",
        "2025-02-15",
        "2025-03-17",
    ],
    "Fin Estimado": [
        "2025-01-10",
        "2025-01-25",
        "2025-02-14",
        "2025-03-16",
        "2025-04-10",
    ],
}

cronograma_df = pd.DataFrame(cronograma)
st.dataframe(cronograma_df)

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

# --------------------- Etapa 4: Ejecución y Monitoreo ---------------------
st.subheader("Etapa 4: Ejecución y Monitoreo")
st.markdown("En esta sección se realiza el seguimiento de la ejecución de los proyectos y se detectan posibles anomalías.")

# Simulación de datos para la etapa de ejecución
ejecucion_data = {
    "ID Proyecto": [1, 2, 3],
    "Nombre Proyecto": ["Edificio Corporativo A", "Planta Industrial B", "Residencial C"],
    "Progreso (%)": [100, 65, 30],
    "Desviación Presupuesto (%)": [5, -2, 10],
    "Retraso Días": [0, 5, 15],
    "Estado General": ["Finalizado", "En Progreso", "Retrasado"],
}
df_ejecucion = pd.DataFrame(ejecucion_data)

# Mostrar tabla de ejecución
st.markdown("### Información de Ejecución por Proyecto")
st.dataframe(df_ejecucion, use_container_width=True)

# Gráfico de progreso por proyecto
fig_ejecucion = px.bar(
    df_ejecucion,
    x="Nombre Proyecto",
    y="Progreso (%)",
    title="Progreso de Ejecución por Proyecto",
    color="Estado General",
    color_discrete_map={
        "Finalizado": "green",
        "En Progreso": "orange",
        "Retrasado": "red",
    },
    text_auto=True,
)
st.plotly_chart(fig_ejecucion, use_container_width=True)

# Filtro para seleccionar un proyecto específico
selected_ejecucion = st.selectbox("Selecciona un Proyecto para Detallar Ejecución", df_ejecucion["Nombre Proyecto"])

detalle_ejecucion = df_ejecucion[df_ejecucion["Nombre Proyecto"] == selected_ejecucion].iloc[0]
st.markdown(f"""
**Proyecto:** {detalle_ejecucion['Nombre Proyecto']}  
**Progreso:** {detalle_ejecucion['Progreso (%)']}%  
**Desviación Presupuesto:** {detalle_ejecucion['Desviación Presupuesto (%)']}%  
**Retraso:** {detalle_ejecucion['Retraso Días']} días  
**Estado General:** {detalle_ejecucion['Estado General']}
""")

# Advertencias sobre anomalías en ejecución
anomalías = df_ejecucion[(df_ejecucion["Desviación Presupuesto (%)"].abs() > 10) | (df_ejecucion["Retraso Días"] > 10)]
if not anomalías.empty:
    st.warning(f"⚠️ Se detectaron {len(anomalías)} anomalías en la ejecución de los proyectos.")
    st.dataframe(anomalías, use_container_width=True)

# --------------------- Detección de Anomalías ---------------------
st.subheader("Detección de Anomalías y Alertas")
st.markdown("En esta sección se generan alertas automáticas basadas en datos simulados para identificar posibles problemas en tiempo real.")

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

# --------------------- Generar Reporte en PDF ---------------------
st.subheader("Generación de Reporte en PDF")
st.markdown("Puedes generar un reporte del seguimiento de proyectos, incluyendo gráficos e información relevante.")

from fpdf import FPDF

def generar_reporte_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Título
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Reporte de Seguimiento de Proyectos", ln=True, align="C")
    pdf.ln(10)
    
    # Sección de Ejecución
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt="Etapa 4: Ejecución y Monitoreo", ln=True)
    pdf.set_font("Arial", size=10)
    for index, row in df_ejecucion.iterrows():
        pdf.cell(200, 10, txt=f"Proyecto: {row['Nombre Proyecto']}, Progreso: {row['Progreso (%)']}%, Retraso: {row['Retraso Días']} días, Estado: {row['Estado General']}", ln=True)
    pdf.ln(10)
    
    # Sección de Alertas
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt="Detección de Anomalías", ln=True)
    pdf.set_font("Arial", size=10)
    for index, row in df_alertas.iterrows():
        pdf.cell(200, 10, txt=f"Proyecto: {row['Nombre Proyecto']}, Tipo: {row['Tipo Anomalía']}, Nivel: {row['Nivel de Alerta']}", ln=True)

    # Guardar PDF
    pdf.output("reporte_proyectos.pdf")
    st.success("Reporte generado exitosamente: 'reporte_proyectos.pdf'")

# Botón para generar PDF
if st.button("Generar Reporte PDF"):
    generar_reporte_pdf()
# --------------------- Etapa 5: Predicción y Análisis Futuro ---------------------
st.subheader("Etapa 5: Predicción y Análisis Futuro")
st.markdown(
    "En esta sección se presentan predicciones basadas en datos históricos y modelos de machine learning. "
    "Estos resultados te ayudarán a anticipar posibles problemas o proyecciones de desempeño."
)

# Simulación de datos históricos para la predicción
historico_data = {
    "Mes": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre"],
    "Progreso Promedio (%)": [5, 15, 25, 35, 45, 55, 65, 75, 85, 95],
    "Desviación Promedio (%)": [2, 3, 1, -2, -1, 4, 2, -3, 5, 0],
}
df_historico = pd.DataFrame(historico_data)

# Mostrar datos históricos
st.markdown("### Datos Históricos de Proyectos")
st.dataframe(df_historico, use_container_width=True)

# Gráfico histórico
fig_historico = px.line(
    df_historico,
    x="Mes",
    y="Progreso Promedio (%)",
    title="Progreso Promedio Mensual (Histórico)",
    markers=True,
    line_shape="spline",
)
st.plotly_chart(fig_historico, use_container_width=True)

# Modelo predictivo usando datos simulados
from sklearn.linear_model import LinearRegression
import numpy as np

# Preparación de datos para el modelo
meses = np.arange(1, len(df_historico) + 1).reshape(-1, 1)
progreso = df_historico["Progreso Promedio (%)"].values

# Entrenar el modelo
modelo = LinearRegression()
modelo.fit(meses, progreso)

# Predicción para los próximos 6 meses
meses_futuros = np.arange(len(df_historico) + 1, len(df_historico) + 7).reshape(-1, 1)
predicciones = modelo.predict(meses_futuros)

# Crear DataFrame de predicciones
futuro_data = {
    "Mes Futuro": ["Noviembre", "Diciembre", "Enero (2025)", "Febrero (2025)", "Marzo (2025)", "Abril (2025)"],
    "Predicción Progreso (%)": predicciones.round(2),
}
df_futuro = pd.DataFrame(futuro_data)

# Mostrar tabla de predicciones
st.markdown("### Predicciones de Progreso Futuro")
st.dataframe(df_futuro, use_container_width=True)

# Gráfico de predicciones
fig_predicciones = px.line(
    x=["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre"] + futuro_data["Mes Futuro"],
    y=list(progreso) + list(predicciones),
    title="Progreso Histórico y Predicciones Futuras",
    markers=True,
    labels={"x": "Mes", "y": "Progreso (%)"},
)
fig_predicciones.update_traces(line_shape="spline")
st.plotly_chart(fig_predicciones, use_container_width=True)

# Análisis adicional
st.markdown(
    f"Se estima que el progreso promedio alcanzará el {predicciones[-1]:.2f}% en abril de 2025, basado en datos históricos. "
    "Es importante ajustar estrategias si las desviaciones presupuestarias continúan aumentando."
)


# --------------------- Alertas Predictivas ---------------------
st.subheader("Alertas Predictivas Basadas en Modelos")
st.markdown("Basándonos en las predicciones, generamos alertas automáticas sobre posibles riesgos futuros.")

# Definir alertas basadas en predicciones
umbral_alerta = 90  # Progreso menor al 90% como alerta
alertas_predicciones = [
    {"Mes": mes, "Predicción Progreso (%)": progreso}
    for mes, progreso in zip(futuro_data["Mes Futuro"], predicciones)
    if progreso < umbral_alerta
]

# Mostrar alertas si existen
if alertas_predicciones:
    st.warning(f"⚠️ Se detectaron {len(alertas_predicciones)} meses con progreso estimado por debajo del umbral del {umbral_alerta}%.")
    st.table(alertas_predicciones)
else:
    st.success("✅ No se detectaron alertas basadas en las predicciones actuales.")

# Generar recomendaciones basadas en análisis
st.markdown("### Recomendaciones")
if alertas_predicciones:
    st.markdown(
        "- **Fortalecer la supervisión:** Aumentar el monitoreo en meses críticos para evitar retrasos.  \n"
        "- **Reasignar recursos:** Priorizar proyectos con desviaciones significativas para garantizar su éxito.  \n"
        "- **Implementar estrategias de mitigación:** Planificar ajustes presupuestarios en caso de incrementos inesperados."
    )
else:
    st.markdown("Las proyecciones actuales son positivas, pero se recomienda mantener las estrategias actuales para evitar riesgos.")

# --------------------- Exportación de Resultados ---------------------
st.subheader("Exportación de Resultados")
st.markdown("Puedes descargar los datos históricos y predicciones en formato CSV.")

# Función para exportar CSV
@st.cache_data
def convertir_csv(df):
    return df.to_csv(index=False).encode("utf-8")

# Botón de descarga
csv_historico = convertir_csv(df_historico)
csv_futuro = convertir_csv(df_futuro)

st.download_button(
    label="Descargar Datos Históricos (CSV)",
    data=csv_historico,
    file_name="datos_historicos.csv",
    mime="text/csv",
)

st.download_button(
    label="Descargar Predicciones Futuras (CSV)",
    data=csv_futuro,
    file_name="predicciones_futuras.csv",
    mime="text/csv",
)
# --------------------- Etapa 6: Evaluación de Riesgos y Detección de Anomalías ---------------------
st.subheader("Etapa 6: Evaluación de Riesgos y Detección de Anomalías")
st.markdown(
    "En esta sección se analizan los riesgos potenciales y se detectan posibles anomalías "
    "en los datos relacionados con gastos e inventarios de los proyectos."
)

# Simulación de datos de gastos e inventarios
data_anomalias = {
    "Proyecto": ["Proyecto A", "Proyecto B", "Proyecto C", "Proyecto D", "Proyecto E"],
    "Gastos Planificados (MXN)": [20000, 30000, 25000, 40000, 15000],
    "Gastos Reales (MXN)": [22000, 45000, 27000, 41000, 20000],
    "Inventario Planificado (unidades)": [100, 150, 120, 180, 80],
    "Inventario Real (unidades)": [95, 140, 110, 200, 75],
}

df_anomalias = pd.DataFrame(data_anomalias)

# Mostrar datos de gastos e inventarios
st.markdown("### Datos de Gastos e Inventarios")
st.dataframe(df_anomalias, use_container_width=True)

# Calcular diferencias y detectar anomalías
df_anomalias["Diferencia Gastos (%)"] = (
    ((df_anomalias["Gastos Reales (MXN)"] - df_anomalias["Gastos Planificados (MXN)"])
     / df_anomalias["Gastos Planificados (MXN)"]) * 100
).round(2)

df_anomalias["Diferencia Inventario (%)"] = (
    ((df_anomalias["Inventario Real (unidades)"] - df_anomalias["Inventario Planificado (unidades)"])
     / df_anomalias["Inventario Planificado (unidades)"]) * 100
).round(2)

# Visualización de anomalías
st.markdown("### Análisis de Desviaciones")
fig_anomalias_gastos = px.bar(
    df_anomalias,
    x="Proyecto",
    y="Diferencia Gastos (%)",
    title="Desviaciones en Gastos por Proyecto",
    color="Diferencia Gastos (%)",
    color_continuous_scale="RdYlGn",
    labels={"Diferencia Gastos (%)": "Diferencia (%)"},
)
st.plotly_chart(fig_anomalias_gastos, use_container_width=True)

fig_anomalias_inventario = px.bar(
    df_anomalias,
    x="Proyecto",
    y="Diferencia Inventario (%)",
    title="Desviaciones en Inventarios por Proyecto",
    color="Diferencia Inventario (%)",
    color_continuous_scale="RdYlBu",
    labels={"Diferencia Inventario (%)": "Diferencia (%)"},
)
st.plotly_chart(fig_anomalias_inventario, use_container_width=True)

# Resaltar proyectos con mayores riesgos
st.markdown("### Proyectos en Riesgo")
proyectos_riesgo = df_anomalias[
    (df_anomalias["Diferencia Gastos (%)"] > 20) | (df_anomalias["Diferencia Inventario (%)"] > 20)
]

if not proyectos_riesgo.empty:
    st.warning("⚠️ Se identificaron los siguientes proyectos con desviaciones significativas:")
    st.dataframe(proyectos_riesgo, use_container_width=True)
else:
    st.success("✅ No se identificaron proyectos con desviaciones críticas.")

# --------------------- Alertas de Anomalías ---------------------
st.subheader("Alertas de Anomalías")
st.markdown(
    "Con base en las diferencias detectadas, se generarán alertas automáticas "
    "para notificar cualquier anomalía significativa por correo."
)

# Función para detectar anomalías
@st.cache_data
def detectar_anomalias(data):
    alertas = []
    for index, row in data.iterrows():
        if row["Diferencia Gastos (%)"] > 20:
            alertas.append(
                f"Anomalía detectada en {row['Proyecto']}: "
                f"Gastos reales superan en un {row['Diferencia Gastos (%)']}% los planificados."
            )
        if row["Diferencia Inventario (%)"] > 20:
            alertas.append(
                f"Anomalía detectada en {row['Proyecto']}: "
                f"Inventarios reales difieren en un {row['Diferencia Inventario (%)']}% de los planificados."
            )
    return alertas

# Generar alertas
alertas_detectadas = detectar_anomalias(df_anomalias)

if alertas_detectadas:
    for alerta in alertas_detectadas:
        st.error(alerta)

    # Notificación por correo (simulación)
    st.markdown("### Enviar Notificaciones de Anomalías")
    if st.button("Enviar Correo de Alerta"):
        st.success("📧 Correo enviado a rojasalexander10@gmail.com con las anomalías detectadas.")
else:
    st.success("✅ No se detectaron anomalías significativas para alertar.")

# --------------------- Recomendaciones ---------------------
st.subheader("Recomendaciones Basadas en el Análisis")
st.markdown(
    "- **Controlar gastos:** Implementar auditorías frecuentes para mitigar desviaciones.  \n"
    "- **Optimizar inventarios:** Revisar las métricas de planificación para evitar sobrecostos.  \n"
    "- **Automatizar alertas:** Configurar sistemas automáticos para notificaciones en tiempo real."
)

# --------------------- Exportar Resultados de Análisis ---------------------
st.subheader("Exportar Resultados de Análisis")
st.markdown("Descarga los resultados del análisis de riesgos y anomalías en formato CSV.")

# Botón de descarga
csv_anomalias = convertir_csv(df_anomalias)

st.download_button(
    label="Descargar Análisis de Anomalías (CSV)",
    data=csv_anomalias,
    file_name="analisis_anomalias.csv",
    mime="text/csv",
)
# --------------------- Etapa 7: Conclusiones y Próximos Pasos ---------------------
st.header("Conclusiones y Próximos Pasos")
st.markdown(
    "Esta plataforma permite la detección de riesgos y anomalías en tiempo real, "
    "lo que facilita la toma de decisiones para la mejora de procesos y la reducción de costos. "
    "A continuación, se resumen las principales conclusiones y los pasos futuros recomendados:"
)

# Resumen de conclusiones
st.markdown("### Resumen de Conclusiones")
st.write(
    """
    - Se identificaron desviaciones significativas en algunos proyectos, particularmente en los gastos e inventarios.
    - Los gráficos interactivos y las alertas automáticas ofrecen una forma intuitiva de monitorear estas anomalías.
    - La herramienta es versátil y se puede adaptar a diferentes tipos de datos y métricas.
    """
)

# Propuesta de próximos pasos
st.markdown("### Próximos Pasos")
st.write(
    """
    1. **Implementación de Alertas Automáticas**: Configurar un sistema de notificaciones en tiempo real mediante servicios como Twilio o APIs de correo.
    2. **Ampliación de Métricas**: Incluir métricas adicionales, como tiempos de entrega, satisfacción del cliente, o eficiencia operativa.
    3. **Integración con Bases de Datos**: Conectar la plataforma a sistemas de gestión como ERP o CRMs para automatizar la carga de datos.
    4. **Escalabilidad**: Extender el análisis a proyectos más complejos y múltiples equipos.
    """
)


# --------------------- Fin del Dashboard ---------------------
st.success("¡Gracias por usar esta herramienta! Tu retroalimentación es valiosa para continuar mejorando.")
