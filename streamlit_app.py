import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Panel de Ventas Real", layout="wide")

st.title("📊 Control de Objetivos - Datos Verificados")

uploaded_file = st.file_uploader("Sube tu archivo .xlsx", type=["xlsx"])

if uploaded_file:
    try:
        # 1. Leer archivo y limpiar
        df = pd.read_excel(uploaded_file)
        df.columns = [str(c).strip() for c in df.columns]
        
        # Identificar columnas clave por posición para evitar errores de nombres
        # Según tu archivo: Col 2=Sucursal, Col 3=Nivel1, Col 4=Nivel2, Col 5=Logrado
        col_sucursal = df.columns[1]
        col_n1 = df.columns[2]
        col_n2 = df.columns[3]
        col_logrado = df.columns[4]

        # --- FILTRADO DE SEGURIDAD ---
        # Solo nos quedamos con las sucursales reales. 
        # Descartamos cualquier fila que diga "TOTAL" o esté vacía.
        df_sucursales = df[
            (df[col_sucursal].notna()) & 
            (~df[col_sucursal].str.contains("TOTAL", na=False, case=False)) &
            (df[col_sucursal] != "")
        ].copy()

        # 2. CÁLCULO MANUAL (Sin duplicados)
        total_logrado = df_sucursales[col_logrado].sum()
        total_n1 = df_sucursales[col_n1].sum()
        total_n2 = df_sucursales[col_n2].sum()
        cumplimiento = (total_logrado / total_n1 * 100) if total_n1 > 0 else 0

        # --- DISEÑO DEL PANEL ---
        st.subheader("📌 Totales Reales (Suma de Sucursales)")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Logrado Total", f"{int(total_logrado)}")
        c2.metric("Objetivo Nivel 1", f"{int(total_n1)}")
        c3.metric("Objetivo Nivel 2", f"{int(total_n2)}")
        c4.metric("% Cumplimiento", f"{cumplimiento:.1f}%")

        st.divider()

        # 3. GRÁFICOS
        col_izq, col_der = st.columns(2)

        with col_izq:
            st.write("### 🏢 Rendimiento por Sucursal")
            fig_bar = px.bar(df_sucursales, x=col_sucursal, y=[col_logrado, col_n1],
                             barmode='group', labels={'value': 'Unidades', 'variable': 'Tipo'},
                             color_discrete_sequence=["#0088FE", "#FFBB28"])
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_der:
            st.write("### 📈 Porcentaje de Avance")
            df_sucursales['%'] = (df_sucursales[col_logrado] / df_sucursales[col_n1] * 100)
            fig_rank = px.bar(df_sucursales.sort_values('%'), x='%', y=col_sucursal, 
                              orientation='h', color='%', color_continuous_scale="RdYlGn")
            st.plotly_chart(fig_rank, use_container_width=True)

        # 4. TABLA DE AUDITORÍA (Para que verifiques fila por fila)
        with st.expander("🔍 Ver desglose de sucursales sumadas"):
            st.write("El sistema solo está sumando estas filas para evitar duplicar totales:")
            st.table(df_sucursales[[col_sucursal, col_logrado, col_n1, col_n2]])

    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
else:
    st.info("Sube el archivo Excel para ver los datos correctos.")
