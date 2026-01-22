import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Panel de Objetivos", layout="wide")

st.title("📊 Monitor de Objetivos")

uploaded_file = st.file_uploader("Sube tu archivo .xlsx", type=["xlsx"])

if uploaded_file:
    try:
        # Leer Excel
        df = pd.read_excel(uploaded_file)
        
        # 1. Limpieza Automática
        df.columns = [str(c).strip() for c in df.columns]
        df.iloc[:, 0] = df.iloc[:, 0].ffill() 
        
        # Identificar columnas por posición para que no falle con las fechas
        # Col 0: Empresa, Col 1: Sucursal, Col 2: Nivel 1, Col 3: Nivel 2, Col 4: Logrado
        col_empresa = df.columns[0]
        col_sucursal = df.columns[1]
        col_n1 = df.columns[2]
        col_n2 = df.columns[3]
        col_logrado = df.columns[4]

        # Filtrar filas vacías o totales
        df_clean = df.dropna(subset=[col_sucursal]).copy()
        df_sucursales = df_clean[~df_clean[col_sucursal].str.contains("TOTAL", na=False)].copy()

        # 2. Sidebar
        st.sidebar.header("Configuración")
        sucursal = st.sidebar.selectbox("Selecciona Sucursal:", df_sucursales[col_sucursal].unique())
        datos_suc = df_sucursales[df_sucursales[col_sucursal] == sucursal].iloc[0]

        # 3. Gráfico de Termómetro (Gauge)
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = datos_suc[col_logrado],
            title = {'text': f"Progreso: {sucursal}"},
            delta = {'reference': datos_suc[col_n1]},
            gauge = {
                'axis': {'range': [0, datos_suc[col_n2]]},
                'steps': [
                    {'range': [0, datos_suc[col_n1]], 'color': "lightcoral"},
                    {'range': [datos_suc[col_n1], datos_suc[col_n2]], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': datos_suc[col_n1]
                }
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

        # 4. Tabla de Resumen
        st.subheader("Estado General")
        st.table(df_sucursales[[col_empresa, col_sucursal, col_logrado, col_n1, col_n2]])

    except Exception as e:
        st.error(f"Hubo un problema al leer el archivo: {e}")
        st.info("Asegúrate de que el Excel tenga las columnas: Empresa, Sucursal, Nivel 1, Nivel 2, Logrado.")
else:
    st.warning("Esperando archivo Excel...")
