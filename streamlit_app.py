import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Panel de Control Oficial", layout="wide")

st.title("📊 Monitor de Objetivos Dinámico")
st.markdown("Los datos se calculan sumando únicamente las sucursales individuales para evitar duplicados.")

uploaded_file = st.file_uploader("Sube el archivo 'archivo 2.xlsx'", type=["xlsx"])

if uploaded_file:
    try:
        # 1. Cargar datos
        df = pd.read_excel(uploaded_file)
        df.columns = [str(c).strip() for c in df.columns]
        
        # Identificar columnas (Basado en tu nuevo archivo)
        # Col 0: OBJETIVOS, Col 1: Nivel 1, Col 2: Nivel 2, Col 3: Logrado
        col_sucursal = df.columns[0]
        col_n1 = df.columns[1]
        col_n2 = df.columns[2]
        col_logrado = df.columns[3]

        # 2. FILTRADO CRUCIAL: Quitar filas de TOTAL y filas vacías
        # Solo procesamos filas que NO digan "TOTAL"
        df_sucursales = df[
            (df[col_sucursal].notna()) & 
            (~df[col_sucursal].str.contains("TOTAL", na=False, case=False))
        ].copy()

        # Convertir a números por seguridad
        df_sucursales[col_n1] = pd.to_numeric(df_sucursales[col_n1], errors='coerce').fillna(0)
        df_sucursales[col_n2] = pd.to_numeric(df_sucursales[col_n2], errors='coerce').fillna(0)
        df_sucursales[col_logrado] = pd.to_numeric(df_sucursales[col_logrado], errors='coerce').fillna(0)

        # 3. CÁLCULOS GLOBALES REALES
        total_logrado = df_sucursales[col_logrado].sum()
        total_n1 = df_sucursales[col_n1].sum()
        total_n2 = df_sucursales[col_n2].sum()
        cumplimiento = (total_logrado / total_n1 * 100) if total_n1 > 0 else 0

        # --- INTERFAZ DEL PANEL ---
        st.subheader("📌 Resumen Ejecutivo")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Unidades Logradas", f"{int(total_logrado)}")
        c2.metric("Meta Nivel 1", f"{int(total_n1)}")
        c3.metric("Meta Nivel 2", f"{int(total_n2)}")
        c4.metric("% Cumplimiento", f"{cumplimiento:.1f}%")

        st.divider()

        # 4. GRÁFICOS DINÁMICOS
        col_a, col_b = st.columns(2)

        with col_a:
            st.write("### 🏢 Logrado vs Meta por Sucursal")
            # Gráfico de barras comparativo
            fig_bar = px.bar(df_sucursales, x=col_sucursal, y=[col_logrado, col_n1],
                             barmode='group', 
                             color_discrete_map={col_logrado: "#00BCFF", col_n1: "#323232"},
                             labels={'value': 'Unidades', 'variable': 'Categoría'})
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_b:
            st.write("### 🏆 Ranking de Cumplimiento")
            df_sucursales['%'] = (df_sucursales[col_logrado] / df_sucursales[col_n1] * 100)
            fig_rank = px.bar(df_sucursales.sort_values('%'), x='%', y=col_sucursal, 
                              orientation='h', color='%', color_continuous_scale="RdYlGn")
            st.plotly_chart(fig_rank, use_container_width=True)

        # 5. TABLA DE CONTROL FINAL
        st.subheader("📋 Planilla de Verificación")
        st.dataframe(df_sucursales[[col_sucursal, col_logrado, col_n1, col_n2]], use_container_width=True)

    except Exception as e:
        st.error(f"Ocurrió un error al leer el archivo: {e}")
else:
    st.info("👋 Por favor, sube tu archivo 'archivo 2.xlsx' para ver el panel actualizado.")
