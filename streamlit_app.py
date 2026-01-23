import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# 1. CONFIGURACIÓN Y ESTILO PARA REPORTE ÚNICO
st.set_page_config(page_title="Dashboard Objetivos", layout="wide")

# CSS para que el PDF salga impecable y ocultar lo innecesario
st.markdown("""
    <style>
    @media print {
        /* Oculta botones, uploader, barra lateral y mensajes de streamlit */
        .stButton, .stFileUploader, .stSidebar, header, footer, .stDownloadButton, .stInfo {
            display: none !important;
        }
        /* Elimina espacios en blanco arriba */
        .main .block-container {
            padding-top: 1rem !important;
            max-width: 100% !important;
        }
        /* Evita que los gráficos se corten entre páginas */
        .element-container, .stPlotlyChart, .stTable {
            page-break-inside: avoid !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Panel de Control de Objetivo Sucursales")

# --- NUEVO BOTÓN DE IMPRESIÓN REFORZADO ---
# Usamos un componente HTML directo para saltar bloqueos del navegador
st.components.v1.html("""
    <button onclick="window.print()" style="
        background-color: #00CC96;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
        font-size: 16px;
        width: 100%;
    ">
        🖨️ CLIC AQUÍ PARA GENERAR PDF DEL PANEL ENTERO
    </button>
    """, height=60)

uploaded_file = st.file_uploader("Sube el archivo Excel", type=["xlsx"])

if uploaded_file:
    try:
        # 2. PROCESAMIENTO DE DATOS
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
        
        # Filtros en Sidebar (no saldrán en el PDF)
        st.sidebar.header("🔍 Filtros")
        opciones_marcas = ["GRUPO TOTAL"] + sorted(df_suc['Marca'].unique().tolist())
        marca_sel = st.sidebar.selectbox("Seleccionar Empresa:", opciones_marcas)

        df_final = df_suc if marca_sel == "GRUPO TOTAL" else df_suc[df_suc['Marca'] == marca_sel].copy()
        df_final['%_int'] = (df_final[col_log] / df_final[col_n1] * 100).round(0).astype(int)
        df_final['%_txt'] = df_final['%_int'].astype(str) + "%"

        # 3. CUERPO DEL DASHBOARD (Esto es lo que irá al PDF)
        st.subheader(f"📍 Resumen de Gestión: {marca_sel}")
        t_log, t_n1, t_n2 = df_final[col_log].sum(), df_final[col_n1].sum(), df_final[col_n2].sum()
        cumpl_global = int((t_log/t_n1)*100) if t_n1 > 0 else 0

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Logrado", f"{int(t_log)}")
        k2.metric("Meta N1", f"{int(t_n1)}")
        k3.metric("Meta N2", f"{int(t_n2)}")
        k4.metric("% Global", f"{cumpl_global}%")

        st.divider()

        c_a, c_b = st.columns([2, 1])
        with c_a:
            st.write("### 🏢 Rendimiento por Sucursal")
            fig = px.bar(df_final, x=col_obj, y=[col_log, col_n1, col_n2], barmode='group',
                         color_discrete_sequence=["#00CC96", "#636EFA", "#AB63FA"])
            st.plotly_chart(fig, use_container_width=True)
        with c_b:
            st.write("### 🌡️ Avance Global")
            fig_g = go.Figure(go.Indicator(mode="gauge+number", value=cumpl_global, number={'suffix': "%"},
                                           gauge={'axis': {'range': [0, 120]}, 'bar': {'color': "#323232"},
                                                  'steps': [{'range': [0, 80], 'color': "#FF4B4B"},
                                                            {'range': [80, 100], 'color': "#F9D71C"},
                                                            {'range': [100, 120], 'color': "#00CC96"}]}))
            fig_g.update_layout(height=280)
            st.plotly_chart(fig_g, use_container_width=True)

        st.divider()
        st.write("### 🏆 Matriz de Cumplimiento")
        ml, ma = st.columns(2)
        with ml:
            st.success("✨ Líderes (>= 80%)")
            st.table(df_final[df_final['%_int'] >= 80].sort_values('%_int', ascending=False)[[col_obj, '%_txt']].set_index(col_obj))
        with ma:
            st.error("⚠️ Alerta (< 80%)")
            st.table(df_final[df_final['%_int'] < 80].sort_values('%_int')[[col_obj, '%_txt']].set_index(col_obj))

        st.divider()
        st.write("### 🚥 Semáforo de Cumplimiento")
        df_h = df_final.sort_values('%_int', ascending=False)
        fig_h = px.imshow([df_h['%_int'].values], x=df_h[col_obj], color_continuous_scale="RdYlGn", text_auto=True)
        fig_h.update_traces(texttemplate="%{z}%")
        st.plotly_chart(fig_h, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")
