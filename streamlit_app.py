import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Sistema de Gestión Comercial", layout="wide")

# 2. MENÚ LATERAL
st.sidebar.title("🚀 Menú de Navegación")
pagina = st.sidebar.radio("Seleccione el Panel:", 
                         ["Panel de Objetivos Sucursales", "Ranking de Asesores 🥇"])

# =========================================================
# SECCIÓN 1: PANEL DE OBJETIVOS (TAL CUAL EL ANTERIOR)
# =========================================================
if pagina == "Panel de Objetivos Sucursales":
    st.title("📊 Panel de Control de Objetivos Sucursales")
    
    uploaded_file = st.file_uploader("Sube tu archivo de Objetivos (Excel)", type=["xlsx"], key="objetivos_p1")

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        # Limpieza de nombres de columnas
        df.columns = [str(c).strip() for c in df.columns]
        col_suc, col_n1, col_n2, col_log = df.columns[0], df.columns[1], df.columns[2], df.columns[3]

        # Cálculos Globales para los indicadores del PDF
        total_n1 = df[col_n1].sum()
        total_n2 = df[col_n2].sum()
        total_logrado = df[col_log].sum()
        cumplimiento_global = int((total_logrado / total_n1) * 100) if total_n1 > 0 else 0

        # Métrica de Resumen (Cabecera tal cual el PDF)
        st.subheader("Resumen de Gestión: GRUPO TOTAL")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Logrado Total", f"{total_logrado}")
        m2.metric("Objetivo N1", f"{total_n1}")
        m3.metric("Objetivo N2", f"{total_n2}")
        m4.metric("% Global (N1)", f"{cumplimiento_global}%")

        st.divider()

        # Gráfico de Barras Triple por Sucursal
        fig = go.Figure()
        # Barra Logrado (Verde)
        fig.add_trace(go.Bar(x=df[col_suc], y=df[col_log], name='Logrado', marker_color='#00CC96', text=df[col_log], textposition='auto'))
        # Barra Nivel 1 (Azul)
        fig.add_trace(go.Bar(x=df[col_suc], y=df[col_n1], name='Nivel 1', marker_color='#636EFA', text=df[col_n1], textposition='auto'))
        # Barra Nivel 2 (Violeta)
        fig.add_trace(go.Bar(x=df[col_suc], y=df[col_n2], name='Nivel 2', marker_color='#AB63FA', text=df[col_n2], textposition='auto'))

        fig.update_layout(title="Rendimiento por Sucursal", barmode='group', height=500, margin=dict(t=50, b=100))
        st.plotly_chart(fig, use_container_width=True)

        # Tabla de Semáforos (Rendimiento por Sucursal)
        st.subheader("Detalle de Cumplimiento")
        df['% Cumplimiento'] = (df[col_log] / df[col_n1] * 100).fillna(0).round(1)
        
        def color_semaforo(val):
            if val >= 100: color = "green"
            elif val >= 80: color = "orange"
            else: color = "red"
            return f'background-color: {color}; color: white; font-weight: bold'

        st.dataframe(df.style.applymap(color_semaforo, subset=['% Cumplimiento']), use_container_width=True)

# =========================================================
# SECCIÓN 2: RANKING DE ASESORES (NUEVO)
# =========================================================
elif pagina == "Ranking de Asesores 🥇":
    st.title("🏆 Ranking de Asesores Comercial")
    st.info("Sube los archivos U45 y U53 para procesar el ranking de medallas.")

    c1, c2 = st.columns(2)
    with c1:
        file_u45 = st.file_uploader("Archivo U45 (Ventas)", type=["xlsx", "xls", "csv"], key="u45_p2")
    with c2:
        file_u53 = st.file_uploader("Archivo U53 (Planes)", type=["xlsx", "xls", "csv"], key="u53_p2")

    if file_u45 and file_u53:
        try:
            # PROCESAMIENTO U45
            df45 = pd.read_csv(file_u45) if file_u45.name.endswith('.csv') else pd.read_excel(file_u45)
            df45.columns = [str(c).strip() for c in df45.columns]
            
            # Filtros U45: No Anuladas (S: Estad != A), No tipos AC (R: Tipo)
            df45 = df45.dropna(subset=['Vendedor', 'Tipo'])
            df45 = df45[(df45['Estad'] != 'A') & (df45['Tipo'] != 'AC')]
            
            # Clasificación U45
            df45['VN'] = df45['Tipo'].apply(lambda x: 1 if str(x).strip().upper() in ['O', 'OP'] else 0)
            df45['VO'] = df45['Tipo'].apply(lambda x: 1 if str(x).strip().upper() == 'O2' else 0)
            df45['ADJ'] = df45['Tipo'].apply(lambda x: 1 if str(x).strip().upper() == 'PL' else 0)
            df45['VE'] = df45['Tipo'].apply(lambda x: 1 if str(x).strip().upper() == 'VE' else 0)
            
            # Lógica Tomas VO (AN: 'Tas. vo')
            def es_toma(valor):
                v = str(valor).strip().replace('.0', '')
                return 1 if v not in ['nan', '0', '0.0', 'None', ''] else 0
            df45['TOMA_VO'] = df45['Tas. vo'].apply(es_toma)
            
            u45_final = df45[['Vendedor', 'Nombre concesionario', 'VN', 'VO', 'ADJ', 'VE', 'TOMA_VO']].copy()
            u45_final.columns = ['asesor', 'Sucursal', 'VN', 'VO', 'ADJ', 'VE', 'TOMA_VO']

            # PROCESAMIENTO U53 (PDA)
            df53 = pd.read_csv(file_u53) if file_u53.name.endswith('.csv') else pd.read_excel(file_u53)
            df53.columns = [str(c).strip() for c in df53.columns]
            df53 = df53.dropna(subset=['Vendedor'])
            df53 = df53[df53['Estado'] != 'AN'] # Filtrar anulados PDA
            
            u53_final = df53[['Vendedor', 'Origen']].copy()
            u53_final['PDA'] = 1
            u53_final.columns = ['asesor', 'Sucursal', 'PDA']

            # CONSOLIDACIÓN
            consolidado = pd.concat([u45_final, u53_final], ignore_index=True).fillna(0)
            consolidado['asesor'] = consolidado['asesor'].str.strip().upper()

            # Filtro Lateral de Sucursal (Solo para el Ranking)
            suc_list = ["TODAS"] + sorted(consolidado['Sucursal'].unique().tolist())
            sel_suc = st.sidebar.selectbox("Filtrar Sucursal (Ranking):", suc_list)
            if sel_suc != "TODAS":
                consolidado = consolidado[consolidado['Sucursal'] == sel_suc]

            ranking = consolidado.groupby(['asesor', 'Sucursal']).sum().reset_index()
            ranking['Total'] = ranking['VN'] + ranking['VO'] + ranking['PDA'] + ranking['ADJ'] + ranking['VE']
            ranking = ranking.sort_values(by='Total', ascending=False).reset_index(drop=True)
            
            def asignar_puesto(i):
                if i == 0: return "🥇 1°"
                elif i == 1: return "🥈 2°"
                elif i == 2: return "🥉 3°"
                return f"{i+1}°"
            ranking.insert(0, 'Ranking', [asignar_puesto(i) for i in range(len(ranking))])

            res = ranking[['Ranking', 'asesor', 'VN', 'VO', 'PDA', 'ADJ', 'VE', 'Total', 'TOMA_VO', 'Sucursal']]
            res.columns = ['Ranking', 'Asesor', 'VN', 'VO', 'PDA', 'ADJ', 'VE', 'TOTAL VENTAS', 'TOMAS VO', 'Sucursal']

            st.dataframe(res, use_container_width=True, hide_index=True)
            st.download_button("📥 Descargar Ranking CSV", res.to_csv(index=False).encode('utf-8-sig'), "ranking.csv", "text/csv")

        except Exception as e:
            st.error(f"Error en ranking: {e}")
