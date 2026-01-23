import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# 1. CONFIGURACIÓN Y ESTILO PARA REPORTE ÚNICO
st.set_page_config(page_title="Dashboard Objetivos", layout="wide")

# CSS para forzar que todo el panel se vea en el PDF sin cortes extraños
st.markdown("""
    <style>
    @media print {
        /* Ocultar elementos que no deben ir en el PDF */
        .stButton, .stFileUploader, .stSidebar, header, footer, .stDownloadButton {
            display: none !important;
        }
        /* Ajustar el contenedor para que use todo el ancho */
        .main .block-container {
            padding-top: 1rem !important;
            padding-bottom: 0rem !important;
            max-width: 100% !important;
        }
        /* Evitar que los gráficos se corten a la mitad entre páginas */
        .element-container, .stPlotlyChart {
            page-break-inside: avoid !important;
            margin-bottom: 20px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Panel de Control de Objetivo Sucursales")

# Botón disparador de impresión
if st.button("🖨️ PREPARAR PANEL COMPLETO PARA PDF"):
    st.markdown('<script>window.print();</script>', unsafe_allow_html=True)
    st.info("👆 Se abrirá la ventana de impresión. Selecciona 'Guardar como PDF'.")

uploaded_file = st.file_uploader("Sube el archivo Excel", type=["xlsx"])

if uploaded_file:
    try:
        # 2. PROCESAMIENTO DE DATOS
        df = pd.read_excel(uploaded_file)
        df.columns = [str(c).strip() for c in df.columns]
        col_obj, col_n1, col_n2, col_log = df.columns[0], df.columns[1], df.columns[2], df.columns[3]

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

        df_suc = df[~df[col_obj].str.contains("TOTAL", na=False, case=False)].copy()
        df_suc = df_suc.dropna(subset=[col_n1])
        
        # Filtros
        opciones_marcas = ["GRUPO TOTAL"] + sorted(df_suc['Marca'].unique().tolist())
        marca_sel = st.sidebar.selectbox("Seleccionar Empresa:", opciones_marcas)

        df_final = df_suc if marca_sel == "GRUPO TOTAL" else df_suc[df_suc['Marca'] == marca_sel].copy()
        df_final['%_int'] = (df_final[col_log] / df_final[col_n1] * 100).round(0).astype(int)
        df_final['%_txt'] = df_final['%_int'].astype(str) + "%"

        # 3. DASHBOARD VISUAL
        st.subheader(f"📍 Resumen de Gestión: {marca_sel}")
        t_log, t_n1, t_n2 = df_final[col_log].sum(), df_final[col_n1].sum(), df_final[col_n2].sum()
        cumpl_global = int((t_log/t_n1)*100) if t_n1 > 0 else 0

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Logrado", f"{int(t_log)}")
        c2.metric("Meta N1", f"{int(t_n1)}")
        c3.metric("Meta N2", f"{int(t_n2)}")
        c4.metric("% Global", f"{cumpl_global}%")

        st.divider()

        # Gráficos
        col_a, col_b = st.columns([2, 1])
        with col_a:
            st.write("### 🏢 Rendimiento por Sucursal")
            fig = px.bar(df_final, x=col_obj, y=[col_log, col_n1, col_n2], barmode='group',
                         color_discrete_sequence=["#00CC96", "#636EFA", "#AB63FA"])
            st.plotly_chart(fig, use_container_width=True)
        with col_b:
            st.write("### 🌡️ Termómetro")
            fig_g = go.Figure(go.Indicator(mode="gauge+number", value=cumpl_global, number={'suffix': "%"},
                                           gauge={'axis': {'range': [0, 120]}, 'bar': {'color': "#323232"},
                                                  'steps': [{'range': [0, 80], 'color': "#FF4B4B"},
                                                            {'range': [80, 100], 'color': "#F9D71C"},
                                                            {'range': [100, 120], 'color': "#00CC96"}]}))
            fig_g.update_layout(height=280)
            st.plotly_chart(fig_g, use_container_width=True)

        # Tablas y Semáforo
        st.divider()
        st.write("### 🏆 Matriz de Cumplimiento")
        cl, ca = st.columns(2)
        with cl:
            st.success("✨ Líderes (>= 80%)")
            st.table(df_final[df_final['%_int'] >= 80].sort_values('%_int', ascending=False)[[col_obj, '%_txt']].set_index(col_obj))
        with ca:
            st.error("⚠️ Alerta (< 80%)")
            st.table(df_final[df_final['%_int'] < 80].sort_values('%_int')[[col_obj, '%_txt']].set_index(col_obj))

        st.divider()
        st.write("### 🚥 Semáforo Completo")
        df_h = df_final.sort_values('%_int', ascending=False)
        fig_h = px.imshow([df_h['%_int'].values], x=df_h[col_obj], color_continuous_scale="RdYlGn", text_auto=True)
        fig_h.update_traces(texttemplate="%{z}%")
        st.plotly_chart(fig_h, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")
