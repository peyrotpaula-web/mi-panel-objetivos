import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# Configuración de página
st.set_page_config(page_title="Sistema Comercial Grupo", layout="wide")

def limpiar_texto(t):
    return " ".join(str(t).split()).replace(".", "").strip().upper()

# Maestro de Asesores
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

if "ventas_sucursal_memoria" not in st.session_state:
    st.session_state["ventas_sucursal_memoria"] = {}

menu = st.sidebar.radio("Seleccionar Panel:", ["Panel de Objetivos Sucursales", "Ranking de Asesores 🥇", "Cumplimiento de Objetivos 🎯"])

# --- PANEL OBJETIVOS ---
if menu == "Panel de Objetivos Sucursales":
    st.title("📊 Panel de Objetivos")
    f = st.file_uploader("Subir Excel de Objetivos", type=["xlsx"])
    if f:
        try:
            df = pd.read_excel(f)
            df.columns = [str(c).strip() for c in df.columns]
            c_obj, c_n1, c_n2, c_log = df.columns[0], df.columns[1], df.columns[2], df.columns[3]
            df["Marca"] = "OTRAS"
            m_act = "OTRAS"
            for i, r in df.iterrows():
                t = str(r[c_obj]).upper()
                if "OPENCARS" in t: m_act = "OPENCARS"
                elif "PAMPAWAGEN" in t: m_act = "PAMPAWAGEN"
                elif "FORTECAR" in t: m_act = "FORTECAR"
                elif "GRANVILLE" in t: m_act = "GRANVILLE"
                elif "CITROEN" in t: m_act = "CITROEN SN"
                elif "RED" in t: m_act = "RED SECUNDARIA"
                df.at[i, "Marca"] = m_act
            df_s = df[~df[c_obj].str.contains("TOTAL", na=False, case=False)].dropna(subset=[c_n1]).copy()
            m_sel = st.sidebar.selectbox("Empresa:", ["GRUPO TOTAL"] + sorted(df_s["Marca"].unique().tolist()))
            df_f = df_s if m_sel == "GRUPO TOTAL" else df_s[df_s["Marca"] == m_sel].copy()
            df_f["%"] = (df_f[c_log] / df_f[c_n1] * 100).fillna(0).round(0).astype(int)
            st.plotly_chart(px.bar(df_f, x=c_obj, y=[c_log, c_n1, c_n2], barmode="group", text_auto=True), use_container_width=True)
            st.table(df_f[[c_obj, c_log, c_n1, "%"]].set_index(c_obj))
        except Exception as e: st.error(f"Error: {e}")

# --- RANKING ---
elif menu == "Ranking de Asesores 🥇":
    st.title("🏆 Ranking de Asesores")
    c1, c2 = st.columns(2)
    u45 = c1.file_uploader("Archivo U45", type=["xlsx", "xls", "csv"])
    u53 = c2.file_uploader("Archivo U53", type=["xlsx", "xls", "csv"])
    
    if u45 and u53:
        try:
            def l_f(file):
                if file.name.endswith(".csv"): return pd.read_csv(file)
                return pd.read_excel(file, engine="xlrd" if file.name.endswith(".xls") else None)
            d45r, d53r = l_f(u45), l_f(u53)
            cv45 = d45r.columns[4]
            ct45 = next(c for c in d45r.columns if "TIPO" in str(c).upper())
            ce45 = next(c for c in d45r.columns if "ESTAD" in str(c).upper())
            co45 = next((c for c in d45r.columns if "TAS. VO" in str(c).upper()), None)
            d45f = d45r[(d45r[ce45] != "A") & (d45r[ct45] != "AC")].copy()
            d45f["KEY"] = d45f[cv45].apply(limpiar_texto)
            res = d45f.groupby("KEY").apply(lambda x: pd.Series({
                "VN": int((x[ct45].isin(["O", "OP"])).sum()), "VO": int((x[ct45].isin(["O2","O2R"])).sum()),
                "ADJ": int((x[ct45] == "PL").sum()), "VE": int((x[ct45] == "VE").sum()),
                "TOMA_VO": int(x[co45].apply(lambda v: 1 if str(v).strip() not in ["0", "0.0", "nan", "None", "", "0,0"] else 0).sum()) if co45 else 0
            })).reset_index()
            d53r["KEY"] = d53r[d53r.columns[0]].apply(limpiar_texto)
            pda = d53r.groupby("KEY").size().reset_index(name="PDA")
            df = pd.merge(res, pda, on="KEY", how="outer").fillna(0)
            ml = {limpiar_texto(k): v for k, v in maestro_asesores.items()}
            df["Sucursal"] = df["KEY"].map(ml)
            df = df.dropna(subset=["Sucursal"]).copy()
            for c in ["VN", "VO", "PDA", "ADJ", "VE", "TOMA_VO"]: df[c] = df[c].astype(int)
            df["TOTAL"] = df["VN"] + df["VO"] + df["ADJ"] + df["VE"] + df["PDA"]
            st.session_state["ventas_sucursal_memoria"] = df.groupby("Sucursal")["TOTAL"].sum().to_dict()
            
            def p_ord(s):
                if s == "GERENCIA": return 2
                if s == "RED SECUNDARIA": return 1
                return 0
            df["P"] = df["Sucursal"].apply(p_ord)
            df = df.sort_values(by=["P", "TOTAL", "TOMA_VO"], ascending=[True, False, False]).reset_index(drop=True)

            # Podio
            st.write("## 🎖️ Cuadro de Honor")
            pc = st.columns(3)
            meds = ["🥇", "🥈", "🥉"]
            cols_b = ["#FFD700", "#C0C0C0", "#CD7F32"]
            for i in range(min(3, len(df))):
                a = df.iloc[i]
                with pc[i]:
                    st.markdown(f'<div style="text-align: center; border: 2px solid {cols_b[i]}; border-radius: 10px; padding: 10px; background-color: #f0f2f6;"><h3>{meds[i]} {a["KEY"]}</h3><h2>{a["TOTAL"]} u.</h2><p>{a["Sucursal"]}</p></div>', unsafe_allow_html=True)

            st.divider()
            f_suc = st.multiselect("Filtrar Sucursal:", sorted(df["Sucursal"].unique()))
            rf = df[df["Sucursal"].isin(f_suc)] if f_suc else df.copy()
            
            # Formateo de Rank para la tabla
            rf["Rank"] = [f"🥇 1°" if i==0 else f"🥈 2°" if i==1 else f"🥉 3°" if i==2 else f"{i+1}°" for i in range(len(rf))]
            disp = rf[["Rank", "KEY", "VN", "VO", "PDA", "ADJ", "VE", "TOTAL", "TOMA_VO", "Sucursal"]].rename(columns={"KEY": "Asesor"})
            
            def est_filas(row):
                s = ["text-align: center"] * len(row)
                if row["Sucursal"] == "SUCURSAL VIRTUAL": s = [x + "; color: #1a73e8" for x in s]
                elif row["Sucursal"] == "RED SECUNDARIA": s = [x + "; color: #8e44ad" for x in s]
                return s

            st.dataframe(disp.style.apply(est_filas, axis=1), use_container_width=True, hide_index=True)
            
            # Totales y Descarga
            df_v = rf[rf["Sucursal"] != "SUCURSAL VIRTUAL"]
            t_d = {"Rank": "", "Asesor": "TOTAL GENERAL", "VN": df_v["VN"].sum(), "VO": df_v["VO"].sum(), "PDA": df_v["PDA"].sum(), "ADJ": df_v["ADJ"].sum(), "VE": df_v["VE"].sum(), "TOTAL": df_v
