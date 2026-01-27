import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. CONFIGURACIÓN INICIAL
st.set_page_config(page_title="Sistema Comercial Consolidado", layout="wide")

# 2. MENÚ LATERAL DE NAVEGACIÓN
st.sidebar.title("🚀 Panel de Control")
pagina = st.sidebar.radio("Seleccione una herramienta:", 
                         ["Panel de Objetivos Sucursales", "Ranking de Asesores 🥇"])

st.sidebar.divider()

# =========================================================
# PÁGINA 1: PANEL DE OBJETIVOS (Tu código anterior)
# =========================================================
if pagina == "Panel de Objetivos Sucursales":
    st.title("📊 Panel de Control de Objetivos")
    
    # AQUÍ PEGA TODO EL CÓDIGO QUE YA TENÍAS DEL PANEL DE OBJETIVOS
    # (El que procesa el Excel con barras verdes, azules y genera PDF)
    st.info("Sube el archivo de objetivos para visualizar el rendimiento por sucursal.")
    # [Pega aquí el bloque de código de la primera app]


# =========================================================
# PÁGINA 2: RANKING DE ASESORES (El nuevo código)
# =========================================================
elif pagina == "Ranking de Asesores 🥇":
    st.title("🏆 Ranking de Asesores Comercial")
    st.markdown("Consolidado Neto U45 y U53 (Sin Anulados y con Tomas de VO)")

    col1, col2 = st.columns(2)
    with col1:
        file_u45 = st.file_uploader("Archivo U45 (Ventas)", type=["xlsx", "xls", "csv"], key="u45")
    with col2:
        file_u53 = st.file_uploader("Archivo U53 (Planes)", type=["xlsx", "xls", "csv"], key="u53")

    if file_u45 and file_u53:
        try:
            # PROCESAMIENTO U45
            df45 = pd.read_csv(file_u45) if file_u45.name.endswith('.csv') else pd.read_excel(file_u45)
            df45.columns = [str(c).strip() for c in df45.columns]
            df45 = df45.dropna(subset=['Vendedor', 'Tipo'])
            df45 = df45[(df45['Estad'] != 'A') & (df45['Tipo'] != 'AC')]
            
            df45['VN'] = df45['Tipo'].apply(lambda x: 1 if str(x).strip().upper() in ['O', 'OP'] else 0)
            df45['VO'] = df45['Tipo'].apply(lambda x: 1 if str(x).strip().upper() == 'O2' else 0)
            df45['ADJ'] = df45['Tipo'].apply(lambda x: 1 if str(x).strip().upper() == 'PL' else 0)
            df45['VE'] = df45['Tipo'].apply(lambda x: 1 if str(x).strip().upper() == 'VE' else 0)
            
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
            sel_suc = st.sidebar.selectbox("Filtrar por Sucursal:", suc_list)
            if sel_suc != "TODAS":
                consolidado = consolidado[consolidado['Sucursal'] == sel_suc]

            ranking = consolidado.groupby(['asesor', 'Sucursal']).sum().reset_index()
            ranking['Total'] = ranking['VN'] + ranking['VO'] + ranking['PDA'] + ranking['ADJ'] + ranking['VE']
            ranking = ranking.sort_values(by='Total', ascending=False).reset_index(drop=True)
            
            def asignar_puesto(i):
                if i == 0: return "🥇 1°"
                if i == 1: return "🥈 2°"
                if i == 2: return "🥉 3°"
                return f"{i+1}°"
            ranking.insert(0, 'Ranking', [asignar_puesto(i) for i in range(len(ranking))])

            resultado = ranking[['Ranking', 'asesor', 'VN', 'VO', 'PDA', 'ADJ', 'VE', 'Total', 'TOMA_VO', 'Sucursal']]
            resultado.columns = ['Ranking', 'Asesor', 'VN (O/OP)', 'VO (O2)', 'PDA', 'ADJ (PL)', 'VE', 'TOTAL VENTAS', 'TOMAS VO', 'Sucursal']

            st.dataframe(resultado, use_container_width=True, hide_index=True)
            st.download_button("📥 Descargar CSV", resultado.to_csv(index=False).encode('utf-8-sig'), "ranking.csv", "text/csv")

        except Exception as e:
            st.error(f"Error: {e}")
