import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Panel de Ventas Preciso", layout="wide")

st.title("📊 Control de Objetivos - Datos Verificados")

uploaded_file = st.file_uploader("Sube tu archivo .xlsx", type=["xlsx"])

if uploaded_file:
    try:
        # 1. Leer y limpiar básico
        df = pd.read_excel(uploaded_file)
        df.columns = [str(c).strip() for c in df.columns]
        
        # Rellenar la columna de Empresa (columna 0)
        df.iloc[:, 0] = df.iloc[:, 0].ffill()
        
        # Nombres de columnas por posición para evitar errores de fecha
        col_empresa = df.columns[0]
        col_sucursal = df.columns[1]
        col_n1 = df.columns[2]
        col_n2 = df.columns[3]
        col_logrado = df.columns[4]

        # --- LÓGICA DE FILTRADO PRECISA ---
        # 2. Separar Sucursales de Totales
        # Filtramos filas que contienen "TOTAL" (mayúsculas o minúsculas)
        es_fila_total = df[col_sucursal].str.contains("TOTAL", na=False, case=False)
        
        df_sucursales = df[~es_fila_total].dropna(subset=[col_sucursal])
        df_totales = df[es_fila_total]

        # 3. CÁLCULO DE TOTALES (Usando las filas TOTAL del Excel para máxima precisión)
        # Sumamos solo las filas que dicen "TOTAL" por marca para el KPI global
        total_logrado_real = df_sucursales[col_logrado].sum()
        total_n1_real = df_sucursales[col_n1].sum()
        total_n2_real = df_sucursales[col_n2].sum()
        
        cumplimiento_global = (total_logrado_real / total_n1_real) * 100 if total_n1_real > 0 else 0

        # --- INTERFAZ ---
        st.subheader("📈 Resumen Consolidado Real")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Logrado (Suma Sucursales)", f"{int(total_logrado_real)}")
        k2.metric("Objetivo Nivel 1", f"{int(total_n1_real)}")
        k3.metric("Objetivo Nivel 2", f"{int(total_n2_real)}")
        k4.metric("% Cumplimiento Total", f"{cumplimiento_global:.1f}%")

        st.divider()

        # 4. GRÁFICOS (Solo con datos de sucursales, sin totales que distorsionen)
        col_izq, col_der = st.columns(2)

        with col_izq:
            st.write("### 🏢 Comparativa por Sucursal")
            fig_bar = px.bar(df_sucursales, 
                             x=col_sucursal, 
                             y=[col_logrado, col_n1],
                             barmode='group',
                             title="Logrado vs Nivel 1",
                             color_discrete_sequence=["#007bff", "#ffc107"])
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_der:
            st.write("### 🏆 Top Cumplimiento (%)")
            df_sucursales['%_logro'] = (df_sucursales[col_logrado] / df_sucursales[col_n1]) * 100
            fig_ranking = px.bar(df_sucursales.sort_values('%_logro'), 
                                 x='%_logro', y=col_sucursal, 
                                 orientation='h',
                                 color='%_logro',
                                 color_continuous_scale="RdYlGn")
            st.plotly_chart(fig_ranking, use_container_width=True)

        # 5. TABLA DE CONTROL (Muestra los datos tal cual el Excel para auditar)
        st.subheader("🔍 Auditoría de Datos (Planilla Filtrada)")
        st.dataframe(df_sucursales[[col_empresa, col_sucursal, col_logrado, col_n1, col_n2]], use_container_width=True)

    except Exception as e:
        st.error(f"Error al procesar los datos: {e}")
else:
    st.info("Sube el archivo para verificar los totales.")
