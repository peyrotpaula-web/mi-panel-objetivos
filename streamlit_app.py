import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Sistema Comercial", layout="wide")

def clean(t):
    return " ".join(str(t).split()).replace(".", "").strip().upper()

# Maestro de Asesores (Simplificado para evitar errores de carga)
MAESTRO = {
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
    "1031 ADRIAN FERNANDO SANCHEZ": "RED SECUNDARIA", "MARTIN POTREBICA": "FORTECAR NUEVE DE JULIO", 
    "1116 MELINA BENITEZ": "FORTECAR NUEVE DE JULIO", "1119 ROMAN GAVINO": "FORTECAR NUEVE DE JULIO", 
    "658 BRUNO GONZALEZ": "PAMPAWAGEN GENERAL PICO", "1118 BRENDA AGUIRRE": "FORTECAR OLAVARRIA",
    "FEDERICO RUBINO": "SUCURSAL VIRTUAL", "GERMAN CALVO": "SUCURSAL VIRTUAL",
    "JAZMIN BERAZATEGUI": "SUCURSAL VIRTUAL", "LUISANA LEDESMA": "SUCURSAL VIRTUAL",
    "CAMILA GARCIA": "SUCURSAL VIRTUAL", "CARLA VALLEJO": "SUCURSAL VIRTUAL",
    "PILAR ALCOBA": "SUCURSAL VIRTUAL", "ROCIO FERNANDEZ": "SUCURSAL VIRTUAL"
}

# Persistencia de datos
if 'ventas_mem' not in st.session_state: st.session_state['ventas_mem'] = {}
if 'df_final' not in st.session_state: st.session_state['df_final'] = None

menu = st.sidebar.radio("Panel:", ["Panel Sucursales", "Ranking Asesores", "Cumplimiento"])

# --- PANEL 1: SUCURSALES ---
if menu == "Panel Sucursales":
    st.title("📊 Control de Objetivos")
    if st.session_state['df_final'] is None:
        st.info("Cargue datos en Ranking y Cumplimiento primero.")
    else:
        df = st.session_state['df_final']
        cols = df.columns
        tot = df[df[cols[0]].str.contains("TOTAL GENERAL", na=False)].iloc[0]
        sucs = df[~df[cols[0]].str.contains("TOTAL", na=False)].copy()

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Logrado", f"{int(tot[cols[3]])}")
        c2.metric("Meta N1", f"{int(tot[cols[1]])}")
        c3.metric("Meta N2", f"{int(tot[cols[2]])}")
        c4.metric("% N1", f"{tot[cols[4]]:.1%}")
        c5.metric("% N2", f"{tot[cols[5]]:.1%}")

        fig = px.bar(sucs, x=cols[0], y=[cols[3], cols[1], cols[2]], barmode='group', text_auto=True)
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("📉 Faltantes para Meta")
        sucs['Falta N1'] = (sucs[cols[1]] - sucs[cols[3]]).clip(0)
        sucs['Falta N2'] = (sucs[cols[2]] - sucs[cols[3]]).clip(0)
        st.table(sucs[[cols[0], 'Falta N1', 'Falta N2']].set_index(cols[0]))

# --- PANEL 2: RANKING ---
elif menu == "Ranking Asesores":
    st.title("🏆 Ranking")
    u45 = st.file_uploader("U45", type=["xlsx", "xls", "csv"])
    u53 = st.file_uploader("U53", type=["xlsx", "xls", "csv"])
    
    if u45 and u53:
        def load(f): return pd.read_csv(f) if f.name.endswith('csv') else pd.read_excel(f)
        try:
            d45, d53 = load(u45), load(u53)
            # Buscar columnas por posición o nombre
            idx_v = d45.columns[4]
            idx_t = next(x for x in d45.columns if "TIPO" in str(x).upper())
            idx_e = next(x for x in d45.columns if "ESTAD" in str(x).upper())
            
            d45 = d45[(d45[idx_e] != 'A') & (d45[idx_t] != 'AC')].copy()
            d45['K'] = d45[idx_v].apply(clean)
            
            res = d45.groupby('K').apply(lambda x: pd.Series({
                'V': (x[idx_t].isin(['O','OP','O2','O2R','PL','VE'])).sum()
            })).reset_index()
            
            d53['K'] = d53[d53.columns[0]].apply(clean)
            p = d53.groupby('K').size().reset_index(name='P')
            
            m = pd.merge(res, p, on='K', how='outer').fillna(0)
            m_l = {clean(k): v for k, v in MAESTRO.items()}
            m['Suc'] = m['K'].map(m_l)
            m = m.dropna(subset=['Suc'])
            m['TOTAL'] = m['V'] + m['P']
            
            st.session_state['ventas_mem'] = m.groupby('Suc')['TOTAL'].sum().to_dict()
            st.dataframe(m.sort_values('TOTAL', ascending=False), use_container_width=True)
            st.success("Ventas guardadas.")
        except Exception as e: st.error(f"Error: {e}")

# --- PANEL 3: CUMPLIMIENTO ---
elif menu == "Cumplimiento":
    st.title("🎯 Objetivos")
    v = st.session_state.get('ventas_mem', {})
    f = st.file_uploader("Metas", type=["xlsx"])
    if f:
        try:
            df = pd.read_excel(f)
            df.columns = [str(x).strip() for x in df.columns]
            c = df.columns
            df[c[3]] = 0
            
            for i, r in df.iterrows():
                n = str(r[c[0]]).upper()
                if "TOTAL" in n: continue
                for s, val in v.items():
                    if s.upper() in n: df.at[i, c[3]] = val

            marcas = ["OPENCARS", "PAMPAWAGEN", "GRANVILLE", "FORTECAR"]
            ptr = 0
            for i, r in df.iterrows():
                if "TOTAL" in str(r[c[0]]).upper() and any(m in str(r[c[0]]).upper() for m in marcas):
                    df.at[i, c[3]] = df.iloc[ptr:i, 3].sum()
                    ptr = i + 1

            itg = df[df[c[0]].str.contains("TOTAL GENERAL", na=False, case=False)].index
            if not itg.empty:
                sm = df[(df[c[0]].str.contains("TOTAL", case=False)) & (df[c[0]].str.contains("|".join(marcas), case=False))][c[3]].sum()
                sr = df[df[c[0]].str.contains("RED SECUNDARIA", case=False) & ~df[c[0]].str.contains("TOTAL GENERAL", case=False)][c[3]].sum()
                df.at[itg[0], c[3]] = sm + sr

            df[c[4]] = (df[c[3]] / df[c[1]].replace(0,1)).fillna(0)
            df[c[5]] = (df[c[3]] / df[c[2]].replace(0,1)).fillna(0)
            
            st.session_state['df_final'] = df
            
            def style_c(v):
                col = '#28a745' if v >= 1.0 else '#fd7e14' if v >= 0.8 else '#dc3545'
                return f'background-color: {col}; color: white'
            
            st.dataframe(df.style.map(style_c, subset=[c[4], c[5]]).format({c[4]:"{:.1%}", c[5]:"{:.1%}"}), use_container_width=True)
        except Exception as e: st.error(f"Error: {e}")
