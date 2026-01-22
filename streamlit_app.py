import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Panel Consolidado de Ventas", layout="wide")

st.title("📊 Tablero General de Objetivos")

uploaded_file = st.file_uploader("Sube tu reporte diario (.xlsx)", type=["xlsx"])

if uploaded_file:
    # 1. Procesamiento de datos
    df = pd.read_excel(uploaded_file)
    df.columns = [str(c).strip() for c in df.columns]
    df.iloc[:, 0] = df.iloc[:, 0].ffill() # Rellenar nombres de empresas
    
    col_empresa, col_sucursal, col_n1, col_n2, col_logrado = df.columns[0:5]

    # Separar sucursales de los totales para no duplicar datos en los gráficos
    df_sucursales = df[~df[col_sucursal].str.contains("TOTAL", na=False)].dropna(subset=[col_sucursal])
    
    # 2. SECCIÓN DE KPI GLOBALES (Todo junto)
    total_n1 = df_sucursales[col_n1].sum()
    total_n2 = df_sucursales[col_n2].sum()
    total_logrado = df_sucursales[col_logrado].sum()
    porc_n1 = (total_logrado / total_n1) * 100

    st.subheader("🌐 Resumen Consolidado (Todas las Empresas)")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Logrado Total", f"{total_logrado} un.")
    m2.metric("Objetivo Nivel 1", f"{total_n1} un.")
    m3.metric("Objetivo Nivel 2", f"{total_n2} un.")
    m4.metric("% Cumplimiento N1", f"{porc_n1:.1f}%")

    st.divider()

    # 3. GRÁFICOS COMPARATIVOS
    col_izq, col_der = st.columns(2)

    with col_izq:
        st.write("### 🏆 Logro vs Objetivos por Sucursal")
        fig_barras = px.bar(df_sucursales, 
                            x=col_sucursal, 
                            y=[col_logrado, col_n1, col_n2],
                            barmode='group',
                            title="Comparativa de Unidades",
                            color_discrete_sequence=["#1E88E5", "#FFC107", "#4CAF50"])
        st.plotly_chart(fig_barras, use_container_width=True)

    with col_der:
        st.write("### 📈 % de Avance Nivel 1")
        # Calculamos el % real para el gráfico
        df_sucursales['% Real'] = (df_sucursales[col_logrado] / df_sucursales[col_n1]) * 100
        fig_pct = px.bar(df_sucursales, 
                         x=col_sucursal, 
                         y='% Real',
                         color='% Real',
                         title="Porcentaje de Cumplimiento por Sucursal",
                         color_continuous_scale="RdYlGn",
                         range_y=[0, 120])
        fig_pct.add_hline(y=100, line_dash="dash", line_color="red", annotation_text="Meta N1")
        st.plotly_chart(fig_pct, use_container_width=True)

    # 4. TABLA MAESTRA ÚNICA
    st.divider()
    st.subheader("📋 Detalle Completo de Operaciones")
    
    # Aplicar color a la tabla para identificar rápido quién llegó a la meta
    def color_cumplimiento(val):
        color = 'background-color: #ffcccc' if val < 0.8 else 'background-color: #ccffcc'
        return color

    st.dataframe(df_sucursales.style.format({
        df.columns[5]: "{:.1%}", 
        df.columns[6]: "{:.1%}"
    }).applymap(color_cumplimiento, subset=[df.columns[5]]), use_container_width=True)

else:
    st.info("👋 Bienvenida/o. Sube el archivo Excel para ver el panel unificado.")
