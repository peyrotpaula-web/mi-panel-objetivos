import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

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

if 'ventas_sucursal_memoria' not in st.session_state:
    st.session_state['ventas_sucursal_memoria'] = {}

pagina = st.sidebar.radio("Seleccionar Panel:", ["Panel de Objetivos Sucursales", "Ranking de Asesores 🥇", "Cumplimiento de Objetivos 🎯"])

# =========================================================
# OPCIÓN 1: PANEL DE OBJETIVOS
# =========================================================
if pagina == "Panel de Objetivos Sucursales":
    st.title("📊 Panel de Control de Objetivos Sucursales")
    uploaded_file = st.file_uploader("Sube el archivo Excel de Objetivos", type=["xlsx"])
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            df.columns = [str(c).strip() for c in df.columns]
            col_obj, col_n1, col_n2, col_log = df.columns[0], df.columns[1], df.columns[2], df.columns[3]
            df['Marca'] = "OTRAS"; marca_actual = "OTRAS"
            for i, row in df.iterrows():
                texto = str(row[col_obj]).upper()
                if "OPENCARS" in texto: marca_actual = "OPENCARS"
                elif "PAMPAWAGEN" in texto: marca_actual = "PAMPAWAGEN"
                elif "FORTECAR" in texto: marca_actual = "FORTECAR"
                elif "GRANVILLE" in texto: marca_actual = "GRANVILLE"
                elif "CITROEN" in texto: marca_actual = "CITROEN SN"
                elif "RED" in texto: marca_actual = "RED SECUNDARIA"
                df.at[i, 'Marca'] = marca_actual
            df_suc = df[~df[col_obj].str.contains("TOTAL", na=False, case=False)].dropna(subset=[col_n1]).copy()
            marca_sel = st.sidebar.selectbox("Empresa:", ["GRUPO TOTAL"] + sorted(df_suc['Marca'].unique().tolist()))
            df_f = df_suc if marca_sel == "GRUPO TOTAL" else df_suc[df_suc['Marca'] == marca_sel].copy()
            df_f['%_int'] = (df_f[col_log] / df_f[col_n1] * 100).fillna(0).round(0).astype(int)
            st.subheader(f"📍 Resumen: {marca_sel}")
            fig = px.bar(df_f, x=col_obj, y=[col_log, col_n1, col_n2], barmode='group', text_auto=True)
            st.plotly_chart(fig, use_container_width=True)
            st.table(df_f[[col_obj, col_log, col_n1, '%_int']].set_index(col_obj))
        except Exception as e: st.error(f"Error: {e}")

# =========================================================
# OPCIÓN 2: RANKING (ORDEN GERENCIA AL FINAL Y EXPORTAR)
# =========================================================
elif pagina == "Ranking de Asesores 🥇":
    st.title("🏆 Ranking de Asesores Comercial")
    c1, c2 = st.columns(2)
    with c1: u45 = st.file_uploader("Archivo U45", type=["xlsx", "xls", "csv"], key="u45")
    with c2: u53 = st.file_uploader("Archivo U53", type=["xlsx", "xls", "csv"], key="u53")
    
    if u45 and u53:
        try:
            def leer(f):
                if f.name.endswith('.csv'): return pd.read_csv(f)
                return pd.read_excel(f, engine='xlrd' if f.name.endswith('.xls') else None)
            d45_raw, d53_raw = leer(u45), leer(u53)

            c_v = d45_raw.columns[4]
            c_t = next((c for c in d45_raw.columns if "TIPO" in str(c).upper()), "Tipo")
            c_e = next((c for c in d45_raw.columns if "ESTAD" in str(c).upper()), "Estad")
            c_vo = next((c for c in d45_raw.columns if "TAS. VO" in str(c).upper()), None)

            df45 = d45_raw[(d45_raw[c_e] != 'A') & (d45_raw[c_t] != 'AC')].copy()
            df45['KEY'] = df45[c_v].apply(limpiar_texto)

            res = df45.groupby('KEY').apply(lambda x: pd.Series({
                'VN': int((x[c_t].isin(['O', 'OP'])).sum()), 'VO': int((x[c_t].isin(['O2','O2R'])).sum()),
                'ADJ': int((x[c_t] == 'PL').sum()), 'VE': int((x[c_t] == 'VE').sum()),
                'TOMA_VO': int(x[c_vo].apply(lambda v: 1 if str(v).strip() not in ['0', '0.0', 'nan', 'None', '', '0,0'] else 0).sum()) if c_vo else 0
            })).reset_index()

            d53_raw['KEY'] = d53_raw[d53_raw.columns[0]].apply(limpiar_texto)
            pda = d53_raw.groupby('KEY').size().reset_index(name='PDA')

            df = pd.merge(res, pda, on='KEY', how='outer').fillna(0)
            m_l = {limpiar_texto(k): v for k, v in maestro_asesores.items()}
            df['Sucursal'] = df['KEY'].map(m_l)
            df = df.dropna(subset=['Sucursal']).copy()

            for c in ['VN', 'VO', 'PDA', 'ADJ', 'VE', 'TOMA_VO']: df[c] = df[c].astype(int)
            df['TOTAL'] = df['VN'] + df['VO'] + df['ADJ'] + df['VE'] + df['PDA']
            st.session_state['ventas_sucursal_memoria'] = df.groupby('Sucursal')['TOTAL'].sum().to_dict()

            # --- AJUSTE: ORDENAMIENTO (GERENCIA AL FINAL) ---
            def prioridad(s):
                if s == "GERENCIA": return 2
                if s == "RED SECUNDARIA": return 1
                return 0
            df['P'] = df['Sucursal'].apply(prioridad)
            df = df.sort_values(by=['P', 'TOTAL', 'TOMA_VO'], ascending=[True, False, False]).reset_index(drop=True)

            st.write("### 🔍 Buscador y Filtros")
            col_f1, col_f2 = st.columns(2)
            with col_f1: f_suc = st.multiselect("Filtrar Sucursal:", sorted(df['Sucursal'].unique()))
            with col_f2: f_ase = st.text_input("Buscar Asesor:")

            rf = df.copy()
            if f_suc: rf = rf[rf['Sucursal'].isin(f_suc)]
            if f_ase: rf = rf[rf['KEY'].str.contains(f_ase.upper())]

            # PODIO
            if not f_suc and not f_ase:
                st.write("## 🎖️ Cuadro de Honor")
                cols = st.columns(3); meds = ["🥇", "🥈", "🥉"]
                for i in range(min(3, len(rf))):
                    a = rf.iloc[i]
                    with cols[i]: st.info(f"{meds[i]} {a['KEY']}\n\n**{a['TOTAL']} u.** ({a['Sucursal']})")

            st.divider()
            ranks = [f"{i+1}°" for i in range(len(rf))]
            rf['Rank'] = ranks
            disp = rf[['Rank', 'KEY', 'VN', 'VO', 'PDA', 'ADJ', 'VE', 'TOTAL', 'TOMA_VO', 'Sucursal']].rename(columns={'KEY': 'Asesor'})
            
            def estilos(row):
                st_list = ['text-align: center'] * len(row)
                if row['Sucursal'] == "SUCURSAL VIRTUAL": st_list = [s + '; color: #1a73e8' for s in st_list]
                elif row['Sucursal'] == "RED SECUNDARIA": st_list = [s + '; color: #8e44ad' for s in st_list]
                return st_list

            st.dataframe(disp.style.apply(estilos, axis=1), use_container_width=True, hide_index=True)
            
            # TOTALES
            df_v = rf[rf['Sucursal'] != "SUCURSAL VIRTUAL"]
            t_data = {'Rank': '', 'Asesor': 'TOTAL GENERAL', 'VN': df_v['VN'].sum(), 'VO': df_v['VO'].sum(), 'PDA': df_v['PDA'].sum(), 'ADJ': df_v['ADJ'].sum(), 'VE': df_v['VE'].sum(), 'TOTAL': df_v['TOTAL'].sum(), 'TOMA_VO': df_v['TOMA_VO'].sum(), 'Sucursal': ''}
            df_t = pd.DataFrame([t_data]).set_index('Rank')
            st.table(df_t.style.set_properties(**{'text-align': 'center', 'font-weight': 'bold'}))

            # --- AJUSTE: DESCARGA EXCEL CON TOTAL ---
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                pd.concat([disp.set_index('Rank'), df_t]).to_excel(writer, sheet_name='Ranking')
            st.download_button(label="📥 Descargar Ranking (Excel)", data=output.getvalue(), file_name="ranking.xlsx")

        except Exception as e: st.error(f"Error: {e}")

# =========================================================
# OPCIÓN 3: CUMPLIMIENTO
# =========================================================
elif pagina == "Cumplimiento de Objetivos 🎯":
    st.title("🎯 Cumplimiento de Objetivos")
    ventas = st.session_state.get('ventas_sucursal_memoria', {})
    f_meta = st.file_uploader("Sube el archivo Excel", type=["xlsx"])
    if f_meta:
        try:
            df_m = pd.read_excel(f_meta)
            df_m.columns = [str(c).strip() for c in df_m.columns]
            c = df_m.columns
            df_m[c[3]] = 0
            for i, r in df_m.iterrows():
                s_ex = str(r[c[0]]).upper()
                if "TOTAL" not in s_ex:
                    for sm, v in ventas.items():
                        if sm.upper() in s_ex: df_m.at[i, c[3]] = v
            marcas = ["OPENCARS", "PAMPAWAGEN", "GRANVILLE", "FORTECAR"]
            ini = 0
            for i, r in df_m.iterrows():
                n = str(r[c[0]]).upper()
                if "TOTAL" in n and any(m in n for m in marcas):
                    df_m.at[i, c[3]] = df_m.iloc[ini:i, 3].sum()
                    ini = i + 1
            idx_tg = df_m[df_m[c[0]].str.contains("TOTAL GENERAL", na=False, case=False)].index
            if not idx_tg.empty:
                s_m = df_m[(df_m[c[0]].str.contains("TOTAL", case=False)) & (df_m[c[0]].str.contains("|".join(marcas), case=False))][c[3]].sum()
                s_r = df_m[(df_m[c[0]].str.contains("RED SECUNDARIA", case=False)) & (~df_m[c[0]].str.contains("TOTAL GENERAL", case=False))][c[3]].sum()
                df_m.at[idx_tg[0], c[3]] = s_m + s_r
            df_m["% N1"] = (df_m[c[3]] / df_m[c[1]]).replace([float('inf')], 0).fillna(0)
            df_m["% N2"] = (df_m[c[3]] / df_m[c[2]]).replace([float('inf')], 0).fillna(0)
            st.dataframe(df_m[[c[0], c[1], c[2], c[3], "% N1", "% N2"]].style.format({c[1]: "{:,.0f}", c[2]: "{:,.0f}", c[3]: "{:,.0f}", "% N1": "{:.1%}", "% N2": "{:.1%}"}), use_container_width=True, hide_index=True)
        except Exception as e: st.error(f"Error: {e}")
