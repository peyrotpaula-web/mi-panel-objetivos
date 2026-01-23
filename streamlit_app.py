import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# 1. CONFIGURACIÓN Y TÍTULO CORREGIDO
st.set_page_config(page_title="Dashboard Objetivos", layout="wide")

st.markdown("""
    <style>
    @media print {
        /* Ocultar elementos de control que no van en el reporte */
        .stButton, .stFileUploader, .stSidebar, header, footer, [data-testid="stToolbar"], .stMarkdown {
            display: none !important;
        }
        /* Mostrar el título y el contenido */
        .main .block-container {
            padding: 0 !important;
            margin: 0 !important;
        }
        /* Forzar visibilidad de gráficos */
        .stPlotlyChart {
            visibility: visible !important;
            display: block !important;
            page-break-inside: avoid !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Título con la 'S' agregada
st.title("📊 Panel de Control de Objetivos Sucursales")

uploaded_file = st.file_uploader("Sube el archivo Excel", type=["xlsx"])

if uploaded_file:
    try:
        # 2. PROCESAMIENTO
        df = pd.read_excel(uploaded_file)
        df.columns = [str(c).strip() for c in df.columns]
        col_obj, col_n1, col_n2, col_log = df.columns[0], df.columns[1], df.columns[2], df.columns[3]

        # Lógica de Marcas
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
        
        st.sidebar.header("🔍 Filtros")
        opciones_marcas = ["GRUPO TOTAL"] + sorted(df_suc['Marca'].unique().tolist())
        marca_sel = st.sidebar.selectbox("Seleccionar Empresa:", opciones_marcas)

        df_final = df_suc if marca_sel == "GRUPO TOTAL" else df_suc[df_suc['Marca'] == marca_sel].copy()
        df_final['%_int'] = (df_final[col_log] / df_final[col_n1] * 100).round(0).astype(int)
        df_final['%_txt'] = df_final['%_int'].astype(str) + "%"

        # 3. DASHBOARD (Diseño Estático para PDF)
        st.header(f"Reporte: {marca_sel}")
        t_log, t_n1, t_n2 = df_final[col_log].sum(), df_final[col_n1].sum(), df_final[col_n2].sum()
        cumpl_global = int((t_log/t_n1)*100) if t_n1 > 0 else 0

        st.info(f"📈 **Estado Actual:** {int(t_log)} unidades logradas de una meta de {int(t_n1)} (Cumplimiento: {cumpl_global}%)")
        
        # Gráficos configurados como IMÁGENES para el PDF
        st.write("### 🏢 Rendimiento por Sucursal")
        fig = px.bar(df_final, x=col_obj, y=[col_log, col_n1, col_n2], barmode='group',
                     color_discrete_sequence=["#00CC96", "#636EFA", "#AB63FA"])
        st.plotly_chart(fig, use_container_width=True, config={'staticPlot': True})

        c_l, c_r = st.columns(2)
        with c_l:
            st.write("### 🌡️ Avance Global")
            fig_g = go.Figure(go.Indicator(mode="gauge+number", value=cumpl_global, number={'suffix': "%"},
                                           gauge={'axis': {'range': [0, 120]}, 'bar': {'color': "#323232"},
                                                  'steps': [{'range': [0, 80], 'color': "#FF4B4B"},
                                                            {'range': [80, 100], 'color': "#F9D71C"},
                                                            {'range': [100, 120], 'color': "#00CC96"}]}))
            fig_g.update_layout(height=300)
            st.plotly_chart(fig_g, use_container_width=True, config={'staticPlot': True})
        
        with c_r:
            st.write("### 🏆 Líderes de Cumplimiento")
            df_l = df_final[df_final['%_int'] >= 80].sort_values('%_int', ascending=False)[[col_obj, '%_txt']]
            st.dataframe(df_l, hide_index=True, use_container_width=True)

        st.write("### 🚥 Semáforo de Objetivos")
        df_h = df_final.sort_values('%_int', ascending=False)
        fig_h = px.imshow([df_h['%_int'].values], x=df_h[col_obj], color_continuous_scale="RdYlGn", text_auto=True)
        fig_h.update_traces(texttemplate="%{z}%")
        fig_h.update_layout(height=200)
        st.plotly_chart(fig_h, use_container_width=True, config={'staticPlot': True})

        # BOTÓN FINAL CON SCRIPT DE FOCO
        st.divider()
        st.button("📄 GENERAR REPORTE PDF", help="Usa Ctrl+P si la ventana no abre automáticamente")
        st.components.v1.html("""
            <script>
            setTimeout(function() {
                window.parent.focus();
                window.parent.print();
            }, 1000);
            </script>
        """, height=0)

    except Exception as e:
        st.error(f"Error: {e}")
