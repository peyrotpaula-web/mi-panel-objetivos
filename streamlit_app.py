import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. CONFIGURACIÓN GENERAL
st.set_page_config(page_title="Sistema de Gestión Comercial", layout="wide")

# Colores para el ranking de marcas
COLORES_MARCAS = {
    "PAMPAWAGEN": "#001E50", "FORTECAR": "#102C54", "GRANVILLE": "#FFCE00",
    "CITROEN SN": "#E20613", "OPENCARS": "#00A1DF", "RED SECUNDARIA": "#4B4B4B", "OTRAS": "#999999"
}

# 2. MENÚ LATERAL
st.sidebar.title("🚀 Menú de Navegación")
pagina = st.sidebar.radio("Seleccione el Panel:", 
                         ["Panel de Objetivos Sucursales", "Ranking de Asesores 🥇"])

st.sidebar.divider()

# =========================================================
# PÁGINA 1: PANEL DE OBJETIVOS SUCURSALES
# =========================================================
if pagina == "Panel de Objetivos Sucursales":
    st.title("📊 Panel de Control de Objetivos")
    
    uploaded_file = st.file_uploader("Sube el archivo de Objetivos (N1, N2, Logrado)", type=["xlsx"], key="obj_uploader")

    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            df.columns = [str(c).strip() for c in df.columns]
            col_obj, col_n1, col_n2, col_log = df.columns[0], df.columns[1], df.columns[2], df.columns[3]

            # Clasificación de Marcas
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
            opciones_marcas = ["GRUPO TOTAL"] + sorted(df_suc['Marca'].unique().tolist())
            marca_sel = st.sidebar.selectbox("Seleccionar Empresa:", opciones_marcas)

            df_final = df_suc if marca_sel == "GRUPO TOTAL" else df_suc[df_suc['Marca'] == marca_sel].copy()
            df_final['%_int'] = (df_final[col_log] / df_final[col_n1] * 100).fillna(0).round(0).astype(int)
            
            # Gráfico de Barras Principal
            st.subheader(f"📍 Rendimiento: {marca_sel}")
            fig_bar = px.bar(df_final, x=col_obj, y=[col_log, col_n1, col_n2], barmode='group',
                             color_discrete_sequence=["#00CC96", "#636EFA", "#AB63FA"], text_auto=True)
            st.plotly_chart(fig_bar, use_container_width=True)

            # Ranking de Marcas Ordenado
            if marca_sel == "GRUPO TOTAL":
                st.write("### 🏆 Ranking de Cumplimiento por Marca")
                ranking_m = df_final.groupby('Marca').agg({col_log: 'sum', col_n1: 'sum'}).reset_index()
                ranking_m['%'] = (ranking_m[col_log] / ranking_m[col_n1] * 100).round(0).astype(int)
                ranking_m = ranking_m.sort_values('%', ascending=True) # Ascending=True para que el mayor quede arriba en horizontal
                fig_rank = px.bar(ranking_m, x='%', y='Marca', orientation='h', text_auto=True,
                                  color='Marca', color_discrete_map=COLORES_MARCAS)
                st.plotly_chart(fig_rank, use_container_width=True)

        except Exception as e:
            st.error(f"Error en objetivos: {e}")

# =========================================================
# PÁGINA 2: RANKING DE ASESORES
# =========================================================
elif pagina == "Ranking de Asesores 🥇":
    st.title("🏆 Ranking de Asesores Comercial")
    
    c1, c2 = st.columns(2)
    with c1:
        file_u45 = st.file_uploader("Archivo U45 (Ventas)", type=["xlsx", "xls", "csv"], key="u45")
    with c2:
        file_u53 = st.file_uploader("Archivo U53 (Planes)", type=["xlsx", "xls", "csv"], key="u53")

    if file_u45 and file_u53:
        try:
            # PROCESAMIENTO U45
            df45 = pd.read_csv(file_u45) if file_u45.name.endswith('.csv') else pd.read_excel(file_u45)
            df45.columns = [str(c).strip() for c in df45.columns]
            df45 = df45.dropna(subset=['Vendedor', 'Tipo'])
            df45 = df45[(df45['Estad'] != 'A') & (df45['Tipo'] != 'AC')]
            
            # Clasificación U45
            df45['VN'] = df45['Tipo'].apply(lambda x: 1 if str(x).strip().upper() in ['O', 'OP'] else 0)
            df45['VO'] = df45['Tipo'].apply(lambda x: 1 if str(x).strip().upper() == 'O2' else 0)
            df45['ADJ'] = df45['Tipo'].apply(lambda x: 1 if str(x).strip().upper() == 'PL' else 0)
            df45['VE'] = df45['Tipo'].apply(lambda x: 1 if str(x).strip().upper() == 'VE' else 0)
            
            # Tomas VO (Columna AN: 'Tas. vo')
            def es_toma(valor):
                v = str(valor).strip().replace('.0', '')
                return 1 if v not in ['nan', '0', '0.0', 'None', ''] else 0
            df45['TOMA_VO'] = df45['Tas. vo'].apply(es_toma)
            
            u45_final = df45[['Vendedor', 'Nombre concesionario', 'VN', 'VO', 'ADJ', 'VE', 'TOMA_VO']].copy()
            u45_final.columns = ['asesor', 'Sucursal', 'VN', 'VO', 'ADJ', 'VE', 'TOMA_VO']

            # PROCESAMIENTO U53
            df53 = pd.read_csv(file_u53) if file_u53.name.endswith('.csv') else pd.read_excel(file_u53)
            df53.columns = [str(c).strip() for c in df53.columns]
            df53 = df53.dropna(subset=['Vendedor'])
            df53 = df53[df53['Estado'] != 'AN']
            u53_final = df53[['Vendedor', 'Origen']].copy()
            u53_final['PDA'] = 1
            u53_final.columns = ['asesor', 'Sucursal', 'PDA']

            # CONSOLIDACIÓN
            consolidado = pd.concat([u45_final, u53_final], ignore_index=True).fillna(0)
            consolidado['asesor'] = consolidado['asesor'].str.strip().upper()

            # Filtro Lateral
            suc_list = ["TODAS"] + sorted(consolidado['Sucursal'].unique().tolist())
            sel_suc = st.sidebar.selectbox("Filtrar por Sucursal:", suc_list, key="suc_ranking")
            if sel_suc != "TODAS":
                consolidado = consolidado[consolidado['Sucursal'] == sel_suc]

            # Ranking
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
            res.columns = ['Ranking', 'Asesor', 'VN', 'VO', 'PDA', 'ADJ', 'VE', 'TOTAL', 'TOMAS VO', 'Sucursal']

            st.dataframe(res, use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"Error en ranking: {e}")
