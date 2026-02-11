import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# CONFIGURACIÓN INICIAL
# =========================================================
st.set_page_config(page_title="Sistema Comercial Grupo", layout="wide")

def limpiar_texto(t):
    return " ".join(str(t).split()).replace(".", "").strip().upper()

# Maestro de Asesores Global (Completo)
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

# Inicialización de memoria de sesión
if 'ventas_sucursal_memoria' not in st.session_state:
    st.session_state['ventas_sucursal_memoria'] = {}
if 'df_cumplimiento_procesado' not in st.session_state:
    st.session_state['df_cumplimiento_procesado'] = None

pagina = st.sidebar.radio("Seleccionar Panel:", 
                         ["Panel de Objetivos Sucursales", "Ranking de Asesores 🥇", "Cumplimiento de Objetivos 🎯"])

# =========================================================
# OPCIÓN 1: PANEL DE OBJETIVOS (AUTOMATIZADO)
# =========================================================
if pagina == "Panel de Objetivos Sucursales":
    st.title("📊 Panel de Control de Objetivos Sucursales")

    if st.session_state['df_cumplimiento_procesado'] is None:
        st.warning("⚠️ Sin datos disponibles. Por favor, primero carga archivos en 'Ranking' y procesa metas en 'Cumplimiento'.")
    else:
        df_base = st.session_state['df_cumplimiento_procesado'].copy()
        cols = df_base.columns
        
        # Filtros: Sucursales y Totales
        df_suc = df_base[~df_base[cols[0]].str.contains("TOTAL", na=False, case=False)].copy()
        df_tot = df_base[df_base[cols[0]].str.contains("TOTAL GENERAL", na=False, case=False)].iloc[0]

        # 1. RESUMEN DE GESTIÓN (5 TARJETAS)
        st.subheader("📌 Resumen de Gestión Global")
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Logrado Total", f"{int(df_tot[cols[3]])} u.")
        c2.metric("Objetivo N1", f"{int(df_tot[cols[1]])} u.")
        c3.metric("Objetivo N2", f"{int(df_tot[cols[2]])} u.")
        c4.metric("% Logrado N1", f"{df_tot[cols[4]]:.1%}")
        c5.metric("% Logrado N2", f"{df_tot[cols[5]]:.1%}")

        st.divider()

        # 2. RENDIMIENTO POR SUCURSAL
        st.subheader("📍 Rendimiento Detallado por Sucursal")
        fig_perf = px.bar(df_suc, x=cols[0], y=[cols[3], cols[1], cols[2]],
                         barmode='group', labels={'value': 'Unidades', 'variable': 'Métrica'},
                         color_discrete_sequence=["#28a745", "#636EFA", "#AB63FA"], text_auto=True)
        st.plotly_chart(fig_perf, use_container_width=True)

        col_l, col_r = st.columns(2)
        with col_l:
            st.subheader("🥇 Ranking Cumplimiento N1")
            df_r = df_suc.sort_values(cols[4], ascending=True)
            fig_r = px.bar(df_r, x=cols[4], y=cols[0], orientation='h', 
                          color=cols[4], color_continuous_scale='RdYlGn', text_auto='.1%')
            st.plotly_chart(fig_r, use_container_width=True)

        with col_r:
            st.subheader("📉 Unidades Faltantes para Meta")
            df_suc['Falta N1'] = (df_suc[cols[1]] - df_suc[cols[3]]).clip(lower=0)
            df_suc['Falta N2'] = (df_suc[cols[2]] - df_suc[cols[3]]).clip(lower=0)
            st.table(df_suc[[cols[0], 'Falta N1', 'Falta N2']].set_index(cols[0]))

        # 3. SEMÁFORO
        st.subheader("🚦 Semáforo de Cumplimiento")
        def s_color(v):
            c = 'red' if v < 0.8 else 'orange' if v < 1.0 else 'green'
            return f'background-color: {c}; color: white; font-weight: bold'
        
        st.dataframe(df_suc[[cols[0], cols[3], cols[4], cols[5]]].style.map(
            s_color, subset=[cols[4], cols[5]]
        ).format({cols[4]: "{:.1%}", cols[5]: "{:.1%}"}), use_container_width=True, hide_index=True)

# =========================================================
# OPCIÓN 2: RANKING DE ASESORES (DISEÑO ORIGINAL)
# =========================================================
elif pagina == "Ranking de Asesores 🥇":
    st.title("🏆 Ranking de Asesores Comercial")
    c1, c2 = st.columns(2)
    with c1: u45 = st.file_uploader("Archivo U45", type=["xlsx", "xls", "csv"])
    with c2: u53 = st.file_uploader("Archivo U53", type=["xlsx", "xls", "csv"])
    
    if u45 and u53:
        try:
            def leer(f):
                if f.name.endswith('.csv'): return pd.read_csv(f)
                return pd.read_excel(f)
            df45_r, df53_r = leer(u45), leer(u53)

            c_v = df45_r.columns[4]
            c_t = next(c for c in df45_r.columns if "TIPO" in str(c).upper())
            c_e = next(c for c in df45_r.columns if "ESTAD" in str(c).upper())
            c_vo = next((c for c in df45_r.columns if "TAS. VO" in str(c).upper()), None)

            df45 = df45_r[(df45_r[c_e] != 'A') & (df45_r[c_t] != 'AC')].copy()
            df45['KEY'] = df45[c_v].apply(limpiar_texto)

            u45_s = df45.groupby('KEY').apply(lambda x: pd.Series({
                'VN': int((x[c_t].isin(['O', 'OP'])).sum()), 
                'VO': int((x[c_t].isin(['O2','O2R'])).sum()),
                'ADJ': int((x[c_t] == 'PL').sum()), 
                'VE': int((x[c_t] == 'VE').sum()),
                'TOMA_VO': int(x[c_vo].notnull().sum()) if c_vo else 0
            })).reset_index()

            df53_r['KEY'] = df53_r[df53_r.columns[0]].apply(limpiar_texto)
            u53_s = df53_r.groupby('KEY').size().reset_index(name='PDA')

            rank_b = pd.merge(u45_s, u53_s, on='KEY', how='outer').fillna(0)
            m_l = {limpiar_texto(k): v for k, v in maestro_asesores.items()}
            rank_b['Sucursal'] = rank_b['KEY'].map(m_l)
            rank_b = rank_b.dropna(subset=['Sucursal']).copy()

            rank_b['TOTAL'] = rank_b['VN'] + rank_b['VO'] + rank_b['ADJ'] + rank_b['VE'] + rank_b['PDA']
            st.session_state['ventas_sucursal_memoria'] = rank_b.groupby('Sucursal')['TOTAL'].sum().to_dict()

            # Podio
            rank_b = rank_b.sort_values('TOTAL', ascending=False)
            st.write("## 🎖️ Cuadro de Honor")
            p_cols = st.columns(3)
            meds, clrs = ["🥇", "🥈", "🥉"], ["#FFD700", "#C0C0C0", "#CD7F32"]
            for i in range(min(3, len(rank_b))):
                a = rank_b.iloc[i]
                with p_cols[i]:
                    st.markdown(f'<div style="text-align: center; border: 2px solid {clrs[i]}; border-radius: 10px; padding: 10px;"><h1>{meds[i]}</h1><b>{a["KEY"]}</b><h2>{int(a["TOTAL"])} u.</h2></div>', unsafe_allow_html=True)

            st.divider()
            st.dataframe(rank_b[['KEY', 'VN', 'VO', 'PDA', 'TOTAL', 'Sucursal']], use_container_width=True, hide_index=True)
        except Exception as e: st.error(f"Error: {e}")

# =========================================================
# OPCIÓN 3: CUMPLIMIENTO (SISTEMA DE TOTALES)
# =========================================================
elif pagina == "Cumplimiento de Objetivos 🎯":
    st.title("🎯 Cumplimiento de Objetivos")
    v_reales = st.session_state.get('ventas_sucursal_memoria', {})
    f_meta = st.file_uploader("Subir archivo de metas", type=["xlsx"])
    
    if f_meta:
        try:
            df_m = pd.read_excel(f_meta)
            df_m.columns = [str(c).strip() for c in df_m.columns]
            c = df_m.columns
            df_m[c[3]] = 0 
            
            for i, r in df_m.iterrows():
                n = str(r[c[0]]).upper()
                if "TOTAL" in n: continue
                for s_m, val in v_reales.items():
                    if s_m.upper() in n: df_m.at[i, c[3]] = val

            marcas = ["OPENCARS", "PAMPAWAGEN", "GRANVILLE", "FORTECAR"]
            ptr = 0
            for i, r in df_m.iterrows():
                if "TOTAL" in str(r[c[0]]).upper() and any(m in str(r[c[0]]).upper() for m in marcas):
                    df_m.at[i, c[3]] = df_m.iloc[ptr:i, 3].sum()
                    ptr = i + 1

            # Total General corregido
            idx_g = df_m[df_m[c[0]].str.contains("TOTAL GENERAL", na=False, case=False)].index
            if not idx_g.empty:
                s_marcas = df_m[(df_m[c[0]].str.contains("TOTAL", case=False)) & (df_m[c[0]].str.contains("|".join(marcas), case=False))][c[3]].sum()
                s_red = df_m[df_m[c[0]].str.contains("RED SECUNDARIA", case=False) & ~df_m[c[0]].str.contains("TOTAL GENERAL", case=False)][c[3]].sum()
                df_m.at[idx_g[0], c[3]] = s_marcas + s_red

            # Porcentajes
            df_m[c[4]] = (df_m[c[3]] / df_m[c[1]].replace(0,1)).fillna(0)
            df_m[c[5]] = (df_m[c[3]] / df_m[c[2]].replace(0,1)).fillna(0)

            # GUARDAR EN SESIÓN
            st.session_state['df_cumplimiento_procesado'] = df_m

            st.dataframe(df_m.style.format({c[4]:"{:.1%}", c[5]:"{:.1%}"}), use_container_width=True, hide_index=True)
            st.success("✅ Datos procesados. Ya puedes ver el Panel de Objetivos.")
        except Exception as e: st.error(f"Error: {e}")
