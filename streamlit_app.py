import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# CONFIGURACIÓN E IDENTIDAD
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
    "1118 BRENDA AGUIRRE": "FORTECAR OLAVARRIA"
}

# Inicialización de memoria
if 'ventas_sucursal_memoria' not in st.session_state:
    st.session_state['ventas_sucursal_memoria'] = {}

pagina = st.sidebar.radio("Seleccionar Panel:", 
                         ["Panel de Objetivos Sucursales", "Ranking de Asesores 🥇", "Cumplimiento de Objetivos 🎯"])

# =========================================================
# OPCIÓN 1: PANEL DE OBJETIVOS (AUTOMATIZADO)
# =========================================================
if pagina == "Panel de Objetivos Sucursales":
    st.title("📊 Panel de Control de Objetivos Sucursales")

    if 'df_cumplimiento_procesado' not in st.session_state:
        st.warning("⚠️ Sin datos. Sigue este orden:\n1. Ve a **Ranking** y sube archivos.\n2. Ve a **Cumplimiento** y sube metas.")
    else:
        df_base = st.session_state['df_cumplimiento_procesado']
        c = df_base.columns
        
        df_suc = df_base[~df_base[c[0]].str.contains("TOTAL", na=False, case=False)].copy()
        df_totales = df_base[df_base[c[0]].str.contains("TOTAL GENERAL", na=False, case=False)].iloc[0]

        # 1. Resumen
        st.subheader("📌 Resumen Global")
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Logrado Total", f"{int(df_totales[c[3]])}")
        m2.metric("Objetivo N1", f"{int(df_totales[c[1]])}")
        m3.metric("Objetivo N2", f"{int(df_totales[c[2]])}")
        m4.metric("% N1", f"{df_totales[c[4]]:.1%}")
        m5.metric("% N2", f"{df_totales[c[5]]:.1%}")

        st.divider()

        # 2. Rendimiento y Ranking
        st.subheader("📍 Rendimiento por Sucursal")
        fig = px.bar(df_suc, x=c[0], y=[c[3], c[1], c[2]], barmode='group',
                     color_discrete_sequence=["#28a745", "#636EFA", "#AB63FA"], text_auto=True)
        st.plotly_chart(fig, use_container_width=True)

        ca, cb = st.columns(2)
        with ca:
            st.subheader("🥇 Cumplimiento N1 (%)")
            fig_r = px.bar(df_suc.sort_values(c[4]), x=c[4], y=c[0], orientation='h', 
                           color=c[4], color_continuous_scale='RdYlGn', text_auto='.1%')
            st.plotly_chart(fig_r, use_container_width=True)
        with cb:
            st.subheader("📉 Unidades Faltantes")
            df_suc['Falta N1'] = (df_suc[c[1]] - df_suc[c[3]]).clip(lower=0)
            df_suc['Falta N2'] = (df_suc[c[2]] - df_suc[c[3]]).clip(lower=0)
            st.table(df_suc[[c[0], 'Falta N1', 'Falta N2']].set_index(c[0]))

# =========================================================
# OPCIÓN 2: RANKING DE ASESORES
# =========================================================
elif pagina == "Ranking de Asesores 🥇":
    st.title("🏆 Ranking de Asesores Comercial")
    col1, col2 = st.columns(2)
    with col1: u45 = st.file_uploader("Archivo U45", type=["xlsx", "xls", "csv"])
    with col2: u53 = st.file_uploader("Archivo U53", type=["xlsx", "xls", "csv"])
    
    if u45 and u53:
        try:
            def cargar(f):
                if f.name.endswith('.csv'): return pd.read_csv(f)
                return pd.read_excel(f)
            
            d45, d53 = cargar(u45), cargar(u53)
            # Detección de columnas
            c_v = d45.columns[4]
            c_t = next(x for x in d45.columns if "TIPO" in str(x).upper())
            c_e = next(x for x in d45.columns if "ESTAD" in str(x).upper())
            c_vo = next((x for x in d45.columns if "TAS. VO" in str(x).upper()), None)

            d45 = d45[(d45[c_e] != 'A') & (d45[c_t] != 'AC')].copy()
            d45['KEY'] = d45[c_v].apply(limpiar_texto)

            # Sumarización
            res = d45.groupby('KEY').apply(lambda x: pd.Series({
                'VN': int((x[c_t].isin(['O', 'OP'])).sum()),
                'VO': int((x[c_t].isin(['O2','O2R'])).sum()),
                'ADJ': int((x[c_t] == 'PL').sum()),
                'VE': int((x[c_t] == 'VE').sum()),
                'TOMA': int(x[c_vo].notnull().sum()) if c_vo else 0
            })).reset_index()

            d53['KEY'] = d53[d53.columns[0]].apply(limpiar_texto)
            pda = d53.groupby('KEY').size().reset_index(name='PDA')

            df = pd.merge(res, pda, on='KEY', how='outer').fillna(0)
            maestro = {limpiar_texto(k): v for k, v in maestro_asesores.items()}
            df['Sucursal'] = df['KEY'].map(maestro)
            df = df.dropna(subset=['Sucursal'])
            df['TOTAL'] = df['VN'] + df['VO'] + df['ADJ'] + df['VE'] + df['PDA']
            
            st.session_state['ventas_sucursal_memoria'] = df.groupby('Sucursal')['TOTAL'].sum().to_dict()
            df = df.sort_values('TOTAL', ascending=False)

            st.write("### 🥇 Ranking General")
            st.dataframe(df[['KEY', 'VN', 'VO', 'PDA', 'TOTAL', 'Sucursal']], use_container_width=True, hide_index=True)
            st.success("Ventas sincronizadas correctamente.")
        except Exception as e:
            st.error(f"Error procesando archivos: {e}")

# =========================================================
# OPCIÓN 3: CUMPLIMIENTO
# =========================================================
elif pagina == "Cumplimiento de Objetivos 🎯":
    st.title("🎯 Cumplimiento de Objetivos")
    ventas = st.session_state.get('ventas_sucursal_memoria', {})
    
    f_meta = st.file_uploader("Sube metas Excel", type=["xlsx"])
    if f_meta:
        try:
            df_m = pd.read_excel(f_meta)
            df_m.columns = [str(x).strip() for x in df_m.columns]
            c = df_m.columns
            df_m[c[3]] = 0 

            # Mapeo de ventas
            for i, r in df_m.iterrows():
                nom = str(r[c[0]]).upper()
                if "TOTAL" in nom: continue
                for suc, val in ventas.items():
                    if suc.upper() in nom: df_m.at[i, c[3]] = val

            # Totales por Marca
            marcas = ["OPENCARS", "PAMPAWAGEN", "GRANVILLE", "FORTECAR"]
            ptr = 0
            for i, r in df_m.iterrows():
                if "TOTAL" in str(r[c[0]]).upper() and any(m in str(r[c[0]]).upper() for m in marcas):
                    df_m.at[i, c[3]] = df_m.iloc[ptr:i, 3].sum()
                    ptr = i + 1

            # Total General
            idx_tg = df_m[df_m[c[0]].str.contains("TOTAL GENERAL", na=False, case=False)].index
            if not idx_tg.empty:
                s_m = df_m[(df_m[c[0]].str.contains("TOTAL", case=False)) & (df_m[c[0]].str.contains("|".join(marcas), case=False))][c[3]].sum()
                s_r = df_m[df_m[c[0]].str.contains("RED SECUNDARIA", case=False) & ~df_m[c[0]].str.contains("TOTAL GENERAL", case=False)][c[3]].sum()
                df_m.at[idx_tg[0], c[3]] = s_m + s_r

            # Cálculos finales
            df_m[c[1]] = pd.to_numeric(df_m[c[1]], errors='coerce').fillna(0).astype(int)
            df_m[c[2]] = pd.to_numeric(df_m[c[2]], errors='coerce').fillna(0).astype(int)
            df_m[c[4]] = (df_m[c[3]] / df_m[c[1]]).replace([float('inf')], 0).fillna(0)
            df_m[c[5]] = (df_m[c[3]] / df_m[c[2]]).replace([float('inf')], 0).fillna(0)

            st.session_state['df_cumplimiento_procesado'] = df_m

            def color_st(v):
                color = '#28a745' if v >= 1.0 else '#fd7e14' if v >= 0.8 else '#dc3545'
                return f'background-color: {color}; color: white'

            st.dataframe(df_m.style.map(color_st, subset=[c
