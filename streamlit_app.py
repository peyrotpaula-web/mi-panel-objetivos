import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# Configuración de la página
st.set_page_config(page_title="Dashboard de Ventas Pro", layout="wide")

st.title("🚀 Panel de Control de Objetivos")
st.markdown("Sube tu Excel diario para actualizar los gráficos y descargar reportes.")

# 1. CARGA DE ARCHIVO
uploaded_file = st.file_uploader("Arrastra tu archivo Excel aquí", type=["xlsx"])

if uploaded_file:
    try:
        # Procesamiento y Limpieza
        df = pd.read_excel(uploaded_file)
        df.columns = [str(c).strip() for c in df.columns]
        df.iloc[:, 0] = df.iloc[:, 0].ffill() 
        
        # Identificación de columnas por posición
        col_empresa = df.columns[0]
        col_sucursal = df.columns[1]
        col_n1 = df.columns[2]
        col_n2 = df.columns[3]
        col_logrado = df.columns[4]

        # Filtrar sucursales reales (quitar totales)
        df_sucursales = df[~df[col_sucursal].str.contains("TOTAL", na=False, case=False)].dropna(subset=[col_sucursal])

        # 2. BARRA LATERAL (Filtros y Exportación)
        st.sidebar.header("⚙️ Configuración")
        empresas = df_sucursales[col_empresa].unique()
        seleccion = st.sidebar.multiselect("Filtrar Empresas:", empresas, default=list(empresas))
        
        df_filtrado = df_sucursales[df_sucursales[col_empresa].isin(seleccion)]

        # Botón de Descarga de Datos Filtrados
        st.sidebar.divider()
        st.sidebar.subheader("📥 Exportar")
        
        def to_excel(df_to_download):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_to_download.to_excel(writer, index=False, sheet_name='Reporte')
            return output.getvalue()

        excel_data = to_excel(df_filtrado)
        st.sidebar.download_button(
            label="Descargar Reporte en Excel",
            data=excel_data,
            file_name=f'reporte_objetivos.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        # 3. CUADRO DE MANDO (KPIs)
        t_logrado = df_filtrado[col_logrado].sum()
        t_n1 = df_filtrado[col_n1].sum()
        progreso = (t_logrado / t_n1 * 100) if t_n1 > 0 else 0

        st.subheader("📌 Resumen General de Selección")
        c1, c2, c3 = st.columns(3)
        c1.metric("Unidades Logradas", f"{t_logrado}")
        c2.metric("Meta Nivel 1", f"{t_n1}")
        c3.metric("% Cumplimiento", f"{progreso:.1f}%", delta=f"{progreso-100:.1f}% vs Meta")

        st.divider()

        # 4. GRÁFICOS DIDÁCTICOS
        col_a, col_b = st.columns(2)

        with col_a:
            st.write("### 📊 Comparativa de Niveles por Sucursal")
            fig_bar = px.bar(df_filtrado, x=col_sucursal, y=[col_logrado, col_n1, col_n2],
                             barmode='group', color_discrete_sequence=["#1f77b4", "#ff7f0e", "#2ca02c"])
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_b:
            st.write("### 🎯 Ranking de Cumplimiento (%)")
            df_filtrado['perc'] = (df_filtrado[col_logrado] / df_filtrado[col_n1] * 100)
            fig_rank = px.bar(df_filtrado.sort_values('perc'), x='perc', y=col_sucursal, 
                              orientation='h', color='perc', color_continuous_scale="RdYlGn")
            st.plotly_chart(fig_rank, use_container_width=True)

        # 5. TABLA DE DATOS FINAL
        st.subheader("📝 Detalle de Sucursales")
        st.dataframe(df_filtrado.style.background_gradient(cmap='YlGn', subset=[df.columns[5]]), use_container_width=True)

    except Exception as e:
        st.error(f"Error: Asegúrate de que el Excel tenga el formato correcto. Detalles: {e}")
else:
    st.info("👋 Por favor, sube el archivo Excel para activar el panel.")
