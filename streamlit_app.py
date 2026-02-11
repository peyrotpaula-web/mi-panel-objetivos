import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# CONFIGURACIÓN INICIAL
# =========================================================
st.set_page_config(page_title="Sistema Comercial Grupo", layout="wide")

def limpiar_texto(t):
    return " ".join(str(t).split()).replace(".", "").strip().upper()

# Maestro de Asesores Global
maestro_asesores = {
    "1115 JORGE ZORRO": "GRANVILLE TRELEW", "1114 FACUNDO BOTAZZI": "FORTECAR SAN NICOLAS",
    "1090 FACUNDO BLAIOTTA": "GRANVILLE JUNIN", "843 JUAN ANDRES SILVA": "FORTECAR TRENQUE LAUQUEN",
    "682 TOMAS VILLAMIL SOUBLE": "PAMPAWAGEN SANTA ROSA", "980 NAVARRO RAFAEL": "PAMPAWAGEN SANTA ROSA",
    "912 NICOLAS MARCHIORI": "FORTECAR SAN NICOLAS", "467 FABIAN LOSCERTALES": "PAMPAWAGEN GENERAL PICO",
    "45 LAURA CASSANITI": "FORTECAR JUNIN", "1051 MARTIN GALOTTI": "FORTECAR OLAVARRIA",
    "784 GUSTAVO RIVAS": "GRANVILLE TRELEW", "899 ELIAS LANGONE": "FORTECAR TRENQUE LAUQUEN",
    "897 CONSTANZA NATTINO": "PAMPAWAGEN GENERAL PICO", "930 NICOLAS SCHNEIDER": "PAMPAWAGEN SANTA ROSA",
    "962 GONZALO EZEQUIEL TORRES": "GRANVILLE COMODORO", "1089 ANGEL AUGUSTO FRANCO": "GRANVILLE TRELEW",
    "1081 GASTON ACTIS": "PAMPAWAGEN SANTA ROSA", "596 MARINO JOAQUIN": "FORTECAR CHIVILCOY",
    "916 MATIAS NICOLAS JACCOUD": "FORTECAR PERGAMINO", "902 AGUSTINA BARRIOS": "FORTECAR OLAVARRIA",
    "1091 NORBERTO ALESSO": "FORTECAR PERGAMINO", "477 CARLOS MANFREDINI": "GRANVILLE SAN NICOLAS",
    "748 HERNAN MAXIMILIANO NOLASCO": "GRANVILLE PERGAMINO", "401 JOSE JUAN": "GRANVILLE JUNIN",
    "409 IGNACIO SOSA": "FORTECAR PERGAMINO", "774 CRISTIAN BRIGNANI": "FORTECAR CHIVILCOY",
    "913 NICOLAS MALDONADO": "GRANVILLE CITROEN SAN NICOLAS", "462 JORGE FERRAIUOLO": "FORTECAR JUNIN",
    "931 JUAN IGNACIO SORAIZ": "FORTECAR OLAVARRIA", "648 VALENTINA DIAZ REBICHINI": "PAMPAWAGEN GENERAL PICO",
    "977 OLIVIA ZUCARELLI": "OPENCARS JUNIN", "1004 JOSE LUIS CIARROCCHI": "FORTECAR JUNIN",
    "1097 NICOLAS CIALDO": "FORTECAR CHIVILCOY", "16 DANILO ROBLEDO": "GRANVILLE PERGAMINO",
    "1003 JUAN IGNACIO ARCE": "OPENCARS JUNIN", "1048 BRUNO VIGNALE": "OPENCARS JUNIN",
    "961 FRANCO BRAVO": "FORTECAR OLAVARRIA", "751 SANTIAGO CARRERE": "GRANVILLE SAN NICOLAS",
    "1047 GISELL LLANOS": "GRANVILLE COMODORO", "1088 FRANCO VEGA": "GRANVILLE PERGAMINO",
    "402 CRISTIAN LOPEZ": "FORTECAR JUNIN", "1080 CRISTIAN ESCALANTE": "FORTECAR NUEVE DE JULIO",
    "1021 JUAN ANDRES BRIZUELA": "GRANVILLE COMODORO", "458 OSCAR TAVANI": "GRANVILLE SAN NICOLAS",
    "781 SILVANA CHAMINE": "GRANVILLE MADRYN", "1109 JULIETA DOWNES": "FORTECAR SAN NICOLAS",
    "476 POLIZZI PABLO ANDRES": "FORTECAR PERGAMINO", "950 SOFIA DIAMELA FERNANDEZ": "GRANVILLE JUNIN",
    "1099 GASTON SENOSEAIN": "PAMPAWAGEN SANTA ROSA", "1108 FLORENCIA HAESLER": "FORTECAR SAN NICOLAS",
    "968 RODRIGO JULIAN RIOS": "GRANVILLE MADRYN", "974 CIELO QUIROGA": "OPENCARS SAN NICOLAS",
    "786 RICHARD FORMANTEL ALBORNOZ": "GRANVILLE COMODORO", "601 SOSA JUAN CARLOS": "FORTECAR CHIVILCOY",
    "1104 CELIA FABIANA GONZALEZ": "GRANVILLE CITROEN SAN NICOLAS", "1050 MANUEL SORAIZ": "FORTECAR OLAVARRIA",
    "1100 CAMPODONICO MAGALI": "FORTECAR NUEVE DE JULIO", "1112 AGUSTINA AUZA": "GRANVILLE MADRYN",
    "1111 DAMIAN PARRONDO": "GRANVILLE MADRYN", "1101 RODRIGO BACCHIARRI": "GRANVILLE TRELEW",
    "SS SANTIAGO SERVIDIA": "GRANVILLE MADRYN", "41 TOMAS DI NUCCI": "FORTECAR JUNIN",
    "414 CLAUDIO SANCHEZ": "RED SECUNDARIA", "986 RUBEN JORGE LARRIPA": "RED SECUNDARIA",
    "1031 ADRIAN FERNANDO SANCHEZ": "RED SECUNDARIA", "G GERENCIA MARC AS": "GERENCIA",
    "MARTIN POTREBICA": "FORTECAR NUEVE DE JULIO", "1116 MELINA BENITEZ": "FORTECAR NUEVE DE JULIO",
    "1119 ROMAN GAVINO": "FORTECAR NUEVE DE JULIO", "658 BRUNO GONZALEZ": "PAMPAWAGEN GENERAL PICO",
    "1118 BRENDA AGUIRRE": "FORTECAR OLAVARRIA",
    "FEDERICO RUBINO": "SUCURSAL VIRTUAL", "GERMAN CALVO": "SUCURSAL VIRTUAL",
    "JAZMIN BERAZATEGUI": "SUCURSAL VIRTUAL", "LUISANA LEDESMA": "SUCURSAL VIRTUAL",
    "CAMILA GARCIA": "SUCURSAL VIRTUAL", "CARLA VALLEJO": "SUCURSAL VIRTUAL",
    "PILAR ALCOBA": "SUCURSAL VIRTUAL", "ROCIO FERNANDEZ": "SUCURSAL VIRTUAL"
}

# Memoria de sesión
if 'ventas_sucursal_memoria' not in st.session_state:
    st.session_state['ventas_sucursal_memoria'] = {}

# MENU
pagina = st.sidebar.radio("Seleccionar Panel:", 
                         ["Panel de Objetivos Sucursales", "Ranking de Asesores 🥇", "Cumplimiento de Objetivos 🎯"])

# =========================================================
# OPCIÓN 1: PANEL DE OBJETIVOS (NUTRIDO DE CUMPLIMIENTO)
# =========================================================
if pagina == "Panel de Objetivos Sucursales":
    st.title("📊 Panel de Control de Objetivos Sucursales")

    if 'df_cumplimiento_procesado' not in st.session_state:
        st.warning("⚠️ No hay datos disponibles. Por favor, realiza primero los siguientes pasos:\n1. Ve al panel **Ranking de Asesores** y sube los archivos U45 y U53.\n2. Ve al panel **Cumplimiento de Objetivos** y sube el archivo de metas.")
    else:
        df_base = st.session_state['df_cumplimiento_procesado'].copy()
        cols_b = df_base.columns # 0: Sucursal, 1: N1, 2: N2, 3: Logrado, 4: %N1, 5: %N2
        
        # Filtros de datos
        df_suc = df_base[~df_base[cols_b[0]].str.contains("TOTAL", na=False, case=False)].copy()
        df_totales = df_base[df_base[cols_b[0]].str.contains("TOTAL GENERAL", na=False, case=False)].iloc[0]

        # --- 1. RESUMEN DE GESTIÓN (5 TARJETAS) ---
        st.subheader("📌 Resumen de Gestión Global")
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Logrado Total", f"{int(df_totales[cols_b[3]])} u.")
        c2.metric("Objetivo N1", f"{int(df_totales[cols_b[1]])} u.")
        c3.metric("Objetivo N2", f"{int(df_totales[cols_b[2]])} u.")
        c4.metric("% Logrado N1", f"{df_totales[cols_b[4]]:.1%}")
        c5.metric("% Logrado N2", f"{df_totales[cols_b[5]]:.1%}")

        st.divider()

        # --- 2. RENDIMIENTO POR SUCURSAL (Logrado, N1, N2) ---
        st.subheader("📍 Rendimiento Detallado por Sucursal")
        fig_perf = px.bar(df_suc, x=cols_b[0], y=[cols_b[3], cols_b[1], cols_b[2]],
                         barmode='group', labels={'value': 'Unidades', 'variable': 'Métrica'},
                         color_discrete_sequence=["#28a745", "#636EFA", "#AB63FA"], text_auto=True)
        st.plotly_chart(fig_perf, use_container_width=True)

        col_left, col_right = st.columns(2)

        with col_left:
            # --- 3. RANKING CUMPLIMIENTO N1 ---
            st.subheader("🥇 Ranking Cumplimiento N1")
            df_rank_n1 = df_suc.sort_values(cols_b[4], ascending=False)
            fig_n1 = px.bar(df_rank_n1, x=cols_b[4], y=cols_b[0], orientation='h', 
                            color=cols_b[4], color_continuous_scale='RdYlGn', text_auto='.1%')
            st.plotly_chart(fig_n1, use_container_width=True)

        with col_right:
            # --- 4. MATRIZ DE FALTANTES ---
            st.subheader("📉 Unidades Faltantes para Meta")
            df_suc['Falta N1'] = (df_suc[cols_b[1]] - df_suc[cols_b[3]]).clip(lower=0)
            df_suc['Falta N2'] = (df_suc[cols_b[2]] - df_suc[cols_b[3]]).clip(lower=0)
            st.table(df_suc[[cols_b[0], 'Falta N1', 'Falta N2']].set_index(cols_b[0]))

        # --- 5. SEMÁFORO DE CUMPLIMIENTO ---
        st.subheader("🚦 Semáforo de Estado Operativo")
        def color_semaforo(val):
            color = 'red' if val < 0.8 else 'orange' if val < 1.0 else 'green'
            return f'background-color: {color}; color: white; font-weight: bold'

        st.dataframe(df_suc[[cols_b[0], cols_b[3], cols_b[4], cols_b[5]]].style.applymap(
            color_semaforo, subset=[cols_b[4], cols_b[5]]
        ).format({cols_b[4]: "{:.1%}", cols_b[5]: "{:.1%}"}), use_container_width=True, hide_index=True)

# =========================================================
# OPCIÓN 2: RANKING (INTACTO)
# =========================================================
elif pagina == "Ranking de Asesores 🥇":
    st.title("🏆 Ranking de Asesores Comercial")
    c1, c2 = st.columns(2)
    with c1: u45 = st.file_uploader("Archivo U45", type=["xlsx", "xls", "csv"], key="u45_final")
    with c2: u53 = st.file_uploader("Archivo U53", type=["xlsx", "xls", "csv"], key="u53_final")
    
    if u45 and u53:
        try:
            def leer_archivo(file):
                if file.name.endswith('.csv'): return pd.read_csv(file)
                return pd.read_excel(file, engine='xlrd' if file.name.endswith('.xls') else None)
            df45_raw, df53_raw = leer_archivo(u45), leer_archivo(u53)

            c_v_45 = df45_raw.columns[4]; c_t_45 = next((c for c in df45_raw.columns if "TIPO" in str(c).upper()), "Tipo")
            c_e_45 = next((c for c in df45_raw.columns if "ESTAD" in str(c).upper()), "Estad")
            c_vo_45 = next((c for c in df45_raw.columns if "TAS. VO" in str(c).upper()), None)

            df45 = df45_raw[(df45_raw[c_e_45] != 'A') & (df45_raw[c_t_45] != 'AC')].copy()
            df45['KEY'] = df45[c_v_45].apply(limpiar_texto)

            u45_sum = df45.groupby('KEY').apply(lambda x: pd.Series({
                'VN': int((x[c_t_45].isin(['O', 'OP'])).sum()), 'VO': int((x[c_t_45].isin(['O2','O2R'])).sum()),
                'ADJ': int((x[c_t_45] == 'PL').sum()), 'VE': int((x[c_t_45] == 'VE').sum()),
                'TOMA_VO': int(x[c_vo_45].apply(lambda v: 1 if str(v).strip() not in ['0', '0.0', 'nan', 'None', '', '0,0'] else 0).sum()) if c_vo_45 else 0
            })).reset_index()

            c_v_53 = df53_raw.columns[0]; df53 = df53_raw.copy(); df53['KEY'] = df53[c_v_53].apply(limpiar_texto)
            u53_sum = df53.groupby('KEY').size().reset_index(name='PDA')

            ranking_base = pd.merge(u45_sum, u53_sum, on='KEY', how='outer').fillna(0)
            maestro_limpio = {limpiar_texto(k): v for k, v in maestro_asesores.items()}
            ranking_base['Sucursal'] = ranking_base['KEY'].map(maestro_limpio)
            ranking_base = ranking_base.dropna(subset=['Sucursal']).copy()

            for c in ['VN', 'VO', 'PDA', 'ADJ', 'VE', 'TOMA_VO']: ranking_base[c] = ranking_base[c].astype(int)
            ranking_base['TOTAL'] = ranking_base['VN'] + ranking_base['VO'] + ranking_base['ADJ'] + ranking_base['VE'] + ranking_base['PDA']
            
            st.session_state['ventas_sucursal_memoria'] = ranking_base.groupby('Sucursal')['TOTAL'].sum().to_dict()

            ranking_base['Prioridad'] = ranking_base['Sucursal'].apply(lambda x: 1 if x == "RED SECUNDARIA" else 0)
            ranking_base = ranking_base.sort_values(by=['Prioridad', 'TOTAL', 'TOMA_VO'], ascending=[True, False, False]).reset_index(drop=True)

            st.write("### 🔍 Buscador y Filtros")
            col_f1, col_f2 = st.columns(2)
            with col_f1: filtro_sucursal = st.multiselect("Filtrar por Sucursal:", sorted(ranking_base['Sucursal'].unique()))
            with col_f2: filtro_asesor = st.text_input("Buscar Asesor:")

            ranking = ranking_base.copy()
            if filtro_sucursal: ranking = ranking[ranking['Sucursal'].isin(filtro_sucursal)]
            if filtro_asesor: ranking = ranking[ranking['KEY'].str.contains(filtro_asesor.upper())]

            if not filtro_sucursal and not filtro_asesor:
                st.write("## 🎖️ Cuadro de Honor")
                podio_cols = st.columns(3); meds, cols_p = ["🥇", "🥈", "🥉"], ["#FFD700", "#C0C0C0", "#CD7F32"]
                for i in range(min(3, len(ranking))):
                    asesor = ranking.iloc[i]
                    with podio_cols[i]: st.markdown(f'<div style="text-align: center; border: 2px solid {cols_p[i]}; border-radius: 15px; padding: 15px; background-color: #f9f9f9;"><h1 style="margin: 0;">{meds[i]}</h1><p style="font-weight: bold; margin: 5px 0;">{asesor["KEY"]}</p><h2 style="color: #1f77b4; margin: 0;">{asesor["TOTAL"]} <small>u.</small></h2><span style="font-size: 0.8em; color: gray;">{asesor["Sucursal"]}</span></div>', unsafe_allow_html=True)

            st.divider()
            ranks = [f"🥇 1°" if i==0 else f"🥈 2°" if i==1 else f"🥉 3°" if i==2 else f"{i+1}°" for i in range(len(ranking))]
