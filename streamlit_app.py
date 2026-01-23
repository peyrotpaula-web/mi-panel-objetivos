import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# 1. CONFIGURACIÓN Y ESTILO
st.set_page_config(page_title="Dashboard Objetivos", layout="wide")

COLORES_MARCAS = {
    "PAMPAWAGEN": "#001E50", "FORTECAR": "#102C54", "GRANVILLE": "#FFCE00",
    "CITROEN SN": "#E20613", "OPENCARS": "#00A1DF", "RED SECUNDARIA": "#4B4B4B", "OTRAS": "#999999"
}

st.markdown("""
    <style>
    @media print {
        .stButton, .stFileUploader, .stSidebar, header, footer, [data-testid="stToolbar"] { display: none !important; }
        .main .block-container { padding-top: 1rem !important; max-width: 100% !important; }
        .element-container { margin-bottom: 2rem !important; page-break-inside: avoid !important; }
        .stPlotlyChart { visibility: visible !important; display: block !important; }
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Panel de Control de Objetivos Sucursales")

uploaded_file = st.file_uploader("Sube el archivo Excel", type=["xlsx"])

if uploaded_file:
    try:
        # 2. PROCESAMIENTO
        df = pd.read_excel(uploaded_file)
        df.columns = [str(c).strip() for c in df.columns]
        col_obj, col_n1, col_n2, col_log = df.columns[0], df.columns[1], df.columns[2], df.columns[3]

        df['Marca'] = "OTRAS"
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
        st.sidebar.header("🔍 Filtros")
        opciones_marcas = ["GRUPO TOTAL"] + sorted(df_suc['Marca'].unique().tolist())
        marca_sel = st.sidebar.selectbox("Seleccionar Empresa:", opciones_marcas)

        df_final = df_suc if marca_sel == "GRUPO TOTAL" else df_suc[df_suc['Marca'] == marca_sel].copy()
        df_final['%_int'] = (df_final[col_log] / df_final[col_n1] * 100).round(0).astype(int)
        df_final['%_txt'] = df_final['%_int'].astype(str) + "%"
        
        # Cálculo de Faltantes
        def calc_faltante(logrado, objetivo):
            diff = objetivo - logrado
            return f"{int(diff)} un." if diff > 0 else "✅ Logrado"

        df_final['Faltante N1'] = df_final.apply(lambda x: calc_faltante(x[col_log], x[col_n1]), axis=1)
        df_final['Faltante N2'] = df_final.apply(lambda x: calc_faltante(x[col_log], x[col_n2]), axis=1)

        # --- DASHBOARD ---
        st.subheader(f"📍 Resumen de Gestión: {marca_sel}")
        t_log, t_n1, t_n2 = df_final[col_log].sum(), df_final[col_n1].sum(), df_final[col_n2].sum()
        cumpl_global = int((t_log/t_n1)*100) if t_n1 > 0 else 0

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Logrado Total", f"{int(t_log)}")
        c2.metric("Objetivo N1", f"{int(t_n1)}")
        c3.metric("Objetivo N2", f"{int(t_n2)}")
        c4.metric("% Global (N1)", f"{cumpl_global}%")

        st.divider()

        # Gráfico de Barras Sucursales
        st.write("### 🏢 Rendimiento por Sucursal")
        fig_bar = px.bar(df_final, x=col_obj, y=[col_log, col_n1, col_n2], barmode='group',
                         color_discrete_sequence=["#00CC96", "#636EFA", "#AB63FA"], text_auto=True)
        fig_bar.update_traces(textposition='outside')
        st.plotly_chart(fig_bar, use_container_width=True, config={'staticPlot': True})

        # Ranking de Marcas (Ordenado de Mayor a Menor)
        if marca_sel == "GRUPO TOTAL":
            st.write("### 🏆 Ranking de Cumplimiento por Marca (Objetivo Nivel 1)")
            ranking = df_final.groupby('Marca').agg({col_log: 'sum', col_n1: 'sum'}).reset_index()
            ranking['%'] = (ranking[col_log] / ranking[col_n1] * 100).round(0).astype(int)
            ranking['text_label'] = ranking['%'].astype(str) + "%"
            
            # ORDENAR DE MAYOR A MENOR
            ranking = ranking.sort_values('%', ascending=True) # Ascending True porque Plotly invierte el orden en barras horizontales
            
            fig_rank = px.bar(ranking, x='%', y='Marca', orientation='h', text='text_label',
                              color='Marca', color_discrete_map=COLORES_MARCAS)
            fig_rank.update_layout(showlegend=False, xaxis_title="Porcentaje de Cumplimiento")
            st.plotly_chart(fig_rank, use_container_width=True, config={'staticPlot': True})

        # Termómetro
        st.write("### 🌡️ Avance Global")
        fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=cumpl_global, number={'suffix': "%"},
                                           gauge={'axis': {'range': [0, 120]}, 'bar': {'color': "#323232"},
                                                  'steps': [{'range': [0, 80], 'color': "#FF4B4B"},
                                                            {'range': [80, 100], 'color': "#F9D71C"},
                                                            {'range': [100, 120], 'color': "#00CC96"}]}))
        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True, config={'staticPlot': True})

        st.divider()

        # Matriz
        st.write("### 🏆 Matriz de Cumplimiento (Faltantes N1 y N2)")
        col_l, col_a = st.columns(2)
        cols_mostrar = [col_obj, '%_txt', 'Faltante N1', 'Faltante N2']
        
        with col_l:
            st.success("✨ Líderes (>= 80%)")
            df_l = df_final[df_final['%_int'] >= 80].sort_values('%_int', ascending=False)[cols_mostrar]
            st.table(df_l.set_index(col_obj))
        with col_a:
            st.error("⚠️ Alerta (< 80%)")
            df_a = df_final[df_final['%_int'] < 80].sort_values('%_int')[cols_mostrar]
            st.table(df_a.set_index(col_obj))

        st.divider()
        st.write("### 🚥 Semáforo de Cumplimiento")
        df_heat = df_final.sort_values('%_int', ascending=False)
        fig_heat = px.imshow([df_heat['%_int'].values], x=df_heat[col_obj], color_continuous_scale="RdYlGn", text_auto=True)
        fig_heat.update_traces(texttemplate="%{z}%")
        st.plotly_chart(fig_heat, use_container_width=True, config={'staticPlot': True})

        st.write("---")
        if st.button("📄 GENERAR REPORTE PDF"):
            st.components.v1.html("<script>window.parent.print();</script>", height=0)

    except Exception as e:
        st.error(f"Error: {e}")
