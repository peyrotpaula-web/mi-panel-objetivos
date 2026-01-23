import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# Configuración de página
st.set_page_config(page_title="Dashboard Ejecutivo", layout="wide")

st.title("📊 Panel de Control Gerencial")
st.markdown("_Para exportar a **PDF**: Presiona **Ctrl + P** (Windows) o **Cmd + P** (Mac) y selecciona 'Guardar como PDF'_")

uploaded_file = st.file_uploader("Sube el archivo Excel", type=["xlsx"])

if uploaded_file:
    try:
        # 1. PROCESAMIENTO
        df = pd.read_excel(uploaded_file)
        df.columns = [str(c).strip() for c in df.columns]
        col_obj, col_n1, col_n2, col_log = df.columns[0], df.columns[1], df.columns[2], df.columns[3]

        # Lógica de asignación de Marcas
        df['Marca'] = None
        marca_actual = "OTRAS"
        for i, row in df.iterrows():
            texto = str(row[col_obj]).upper()
            if "OPENCARS" in texto: marca_actual = "OPENCARS"
            elif "PAMPAWAGEN" in texto: marca_actual = "PAMPAWAGEN"
            elif "FORTECAR" in texto: marca_actual = "FORTECAR"
            elif "GRANVILLE" in texto: marca_actual = "GRANVILLE"
            elif "CITROEN" in texto: marca_actual = "CITROEN SN"
            elif "RED" in texto: marca_actual = "RED SECUNDARIA"
            df.at[i, 'Marca'] = marca_actual

        # Filtrar sucursales
        df_suc = df[~df[col_obj].str.contains("TOTAL", na=False, case=False)].copy()
        df_suc = df_suc.dropna(subset=[col_n1])
        df_suc['%_int'] = (df_suc[col_log] / df_suc[col_n1] * 100).round(0).astype(int)
        df_suc['%_txt'] = df_suc['%_int'].astype(str) + "%"

        # 2. KPIs GLOBALES
        t_log, t_n1, t_n2 = df_suc[col_log].sum(), df_suc[col_n1].sum(), df_suc[col_n2].sum()
        cumpl_global = int((t_log/t_n1)*100) if t_n1 > 0 else 0

        # 3. BARRA LATERAL - SOLO EXCEL
        st.sidebar.header("📥 Descargas")
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_suc[[col_obj, col_log, col_n1, col_n2, '%_txt', 'Marca']].to_excel(writer, index=False)
        st.sidebar.download_button("Descargar Datos (Excel)", data=output.getvalue(), file_name="reporte_ventas.xlsx")

        # 4. INTERFAZ VISUAL (KPIs)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Logrado Total", f"{int(t_log)} un.")
        c2.metric("Objetivo N1", f"{int(t_n1)} un.")
        c3.metric("Objetivo N2", f"{int(t_n2)} un.")
        c4.metric("% Global", f"{cumpl_global}%")

        st.divider()

        # 5. GRÁFICOS PRINCIPALES
        col_bar, col_marca = st.columns([2, 1])
        
        with col_bar:
            st.write("### 🏢 Comparativa General por Sucursal")
            fig_suc = px.bar(df_suc, x=col_obj, y=[col_log, col_n1, col_n2], barmode='group',
                             color_discrete_sequence=["#00CC96", "#636EFA", "#AB63FA"],
                             labels={'value': 'Unidades', 'variable': 'Referencia'})
            st.plotly_chart(fig_suc, use_container_width=True)

        with col_marca:
            st.write("### 🌡️ Termómetro de Avance")
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number", value = cumpl_global,
                number = {'suffix': "%"},
                gauge = {'axis': {'range': [0, 120]}, 'bar': {'color': "#323232"},
                         'steps': [{'range': [0, 80], 'color': "#FF4B4B"},
                                   {'range': [80, 100], 'color': "#F9D71C"},
                                   {'range': [100, 120], 'color': "#00CC96"}]}))
            fig_gauge.update_layout(height=280, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig_gauge, use_container_width=True)

        # 6. MATRIZ TOP/BOTTOM (Sin números de índice)
        st.divider()
        st.write("### 🏆 Matriz de Cumplimiento (Nivel 1)")
        col_l, col_a = st.columns(2)
        
        with col_l:
            st.success("✨ Líderes (>= 80%)")
            df_lideres = df_suc[df_suc['%_int'] >= 80].sort_values('%_int', ascending=False)[[col_obj, '%_txt']]
            df_lideres.columns = ["Sucursal", "Cumplimiento"]
            st.table(df_lideres.assign(blank='').set_index('blank')) # Hack para quitar índice
            
        with col_a:
            st.error("⚠️ Alerta (< 80%)")
            df_alerta = df_suc[df_suc['%_int'] < 80].sort_values('%_int')[[col_obj, '%_txt']]
            df_alerta.columns = ["Sucursal", "Cumplimiento"]
            st.table(df_alerta.assign(blank='').set_index('blank'))

        # 7. HEATMAP (SEMÁFORO)
        st.divider()
        st.write("### 🚥 Semáforo Visual de Sucursales")
        df_heat = df_suc.sort_values('%_int', ascending=True)
        
        fig_heat = px.imshow([df_heat['%_int'].values], 
                             x=df_heat[col_obj], 
                             color_continuous_scale="RdYlGn", 
                             text_auto=True,
                             aspect="auto")
        
        # Agregar el símbolo % al texto sobre las barras
        fig_heat.update_traces(texttemplate="%{z}%")
        fig_heat.update_xaxes(side="top")
        st.plotly_chart(fig_heat, use_container_width=True)

    except Exception as e:
        st.error(f"Error en el procesamiento: {e}")
else:
    st.info("👋 Sube el archivo Excel para visualizar el panel de control.")
