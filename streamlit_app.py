import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Panel de Control Preciso", layout="wide")

st.title("📊 Monitor de Objetivos Verificado")

uploaded_file = st.file_uploader("Sube tu archivo .xlsx", type=["xlsx"])

if uploaded_file:
    try:
        # 1. Leer archivo y limpiar nombres de columnas
        df = pd.read_excel(uploaded_file)
        df.columns = [str(c).strip() for c in df.columns]
        
        # 2. Identificar columnas clave (buscando por palabra, no por posición)
        col_sucursal = [c for c in df.columns if 'OBJETIVOS' in c][0]
        col_n1 = [c for c in df.columns if 'Nivel 1' in c and 'logrado' not in c.lower()][0]
        col_n2 = [c for c in df.columns if 'Nivel 2' in c and 'logrado' not in c.lower()][0]
        col_logrado = [c for c in df.columns if 'Logrado' in c][0]

        # 3. Separar datos: Sucursales vs Totales de Marca
        # Filas que son TOTALES (ej: TOTAL OC, TOTAL PW)
        df_totales_marcas = df[df[col_sucursal].str.contains("TOTAL", na=False, case=False)]
        
        # Filas que son SUCURSALES (excluimos las que dicen TOTAL)
        df_sucursales = df[~df[col_sucursal].str.contains("TOTAL", na=False, case=False)].dropna(subset=[col_sucursal])

        # 4. CÁLCULO DE KPIs (Sumando solo los TOTALES de cada marca para no duplicar)
        # Esto garantiza que el número sea igual al de tu Excel
        total_n1 = df_totales_marcas[col_n1].sum()
        total_n2 = df_totales_marcas[col_n2].sum()
        total_logrado = df_totales_marcas[col_logrado].sum()
        
        cumplimiento = (total_logrado / total_n1 * 100) if total_n1 > 0 else 0

        # --- VISUALIZACIÓN ---
        st.subheader("📌 Totales Consolidados (Igual al Excel)")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Logrado Total", f"{int(total_logrado)}")
        c2.metric("Objetivo Nivel 1", f"{int(total_n1)}")
        c3.metric("Objetivo Nivel 2", f"{int(total_n2)}")
        c4.metric("% Cumplimiento", f"{cumplimiento:.1f}%")

        st.divider()

        # 5. GRÁFICOS (Usando solo datos de sucursales para que las barras sean correctas)
        col_a, col_b = st.columns(2)

        with col_a:
            st.write("### 🏢 Logro por Sucursal")
            fig_bar = px.bar(df_sucursales, x=col_sucursal, y=[col_logrado, col_n1],
                             barmode='group', labels={'value': 'Unidades', 'variable': 'Tipo'},
                             color_discrete_sequence=["#1f77b4", "#ff7f0e"])
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_b:
            st.write("### 📈 % de Avance Individual")
            df_sucursales['%'] = (df_sucursales[col_logrado] / df_sucursales[col_n1] * 100)
            fig_rank = px.bar(df_sucursales.sort_values('%'), x='%', y=col_sucursal, 
                              orientation='h', color='%', color_continuous_scale="RdYlGn")
            st.plotly_chart(fig_rank, use_container_width=True)

        # 6. TABLA DE VERIFICACIÓN
        with st.expander("Ver detalle de datos procesados"):
            st.write("Datos de sucursales detectados:")
            st.table(df_sucursales[[col_sucursal, col_logrado, col_n1, col_n2]])

    except Exception as e:
        st.error(f"Error técnico: {e}")
else:
    st.info("👋 Esperando archivo Excel para procesar totales...")
