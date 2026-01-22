import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Dashboard de Objetivos", layout="wide")

st.title("📊 Monitor de Objetivos: Nivel 1 vs Nivel 2")

uploaded_file = st.file_uploader("Sube tu archivo .xlsx", type=["xlsx"])

if uploaded_file:
    # 1. Limpieza de datos (específica para tu formato)
    df = pd.read_excel(uploaded_file)
    df.columns = [c.strip() for c in df.columns]
    df.iloc[:, 0] = df.iloc[:, 0].ffill() # Rellenar nombres de empresas
    
    empresa_col = df.columns[0]
    sucursal_col = df.columns[1]
    
    # Separamos los Totales de las Sucursales
    df_sucursales = df[~df[sucursal_col].str.contains("TOTAL", na=False)].copy()
    df_totales = df[df[sucursal_col].str.contains("TOTAL", na=False)].copy()

    # 2. Selector de Sucursal para el Termómetro
    st.sidebar.header("Filtros")
    sucursal_seleccionada = st.sidebar.selectbox("Selecciona una Sucursal para ver detalle:", df_sucursales[sucursal_col].unique())
    
    datos_suc = df_sucursales[df_sucursales[sucursal_col] == sucursal_seleccionada].iloc[0]

    # 3. Visualización de Termómetro (Gauge Chart)
    st.subheader(f"Estado de cumplimiento: {sucursal_seleccionada}")
    
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = datos_suc['Logrado h/21/01'],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Progreso hacia Nivel 2", 'font': {'size': 24}},
        delta = {'reference': datos_suc['Nivel 1'], 'position': "top", 'relative': False},
        gauge = {
            'axis': {'range': [None, datos_suc['Nivel 2']], 'tickwidth': 1},
            'bar': {'color': "#1f77b4"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, datos_suc['Nivel 1']], 'color': '#ffcfcf'}, # Rojo hasta Nivel 1
                {'range': [datos_suc['Nivel 1'], datos_suc['Nivel 2']], 'color': '#e1ffcf'}], # Verde hasta Nivel 2
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': datos_suc['Nivel 1']}}))

    st.plotly_chart(fig_gauge, use_container_width=True)

    # 4. Comparativa General
    st.divider()
    st.subheader("Comparativo por Concesionarios")
    
    # Gráfico de barras comparando niveles
    fig_comp = px.bar(df_sucursales, 
                     x=sucursal_col, 
                     y=['Logrado h/21/01', 'Nivel 1', 'Nivel 2'],
                     barmode='group',
                     color_discrete_map={
                         'Logrado h/21/01': '#1f77b4',
                         'Nivel 1': '#ff7f0e',
                         'Nivel 2': '#2ca02c'
                     })
    st.plotly_chart(fig_comp, use_container_width=True)

    # 5. Tabla con formato de colores
    st.subheader("Planilla Detallada")
    st.dataframe(df_sucursales.style.background_gradient(subset=['% logrado del Nivel 1'], cmap='RdYlGn'))

else:
    st.info("👋 Por favor, sube el archivo Excel para activar el termómetro de ventas.")
