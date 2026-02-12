import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# Configuración base
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
    "1119 ROMAN GAVINO": "FORTECAR NUEVE DE JULIO", "658 BRUNO GONALEZ": "PAMPAWAGEN GENERAL PICO",
    "1118 BRENDA AGUIRRE": "FORTECAR OLAVARRIA",
    "FEDERICO RUBINO": "SUCURSAL VIRTUAL", "GERMAN CALVO": "SUCURSAL VIRTUAL",
    "JAZMIN BERAZATEGUI": "SUCURSAL VIRTUAL", "LUISANA LEDESMA": "SUCURSAL VIRTUAL",
    "CAMILA GARCIA": "SUCURSAL VIRTUAL", "CARLA VALLEJO": "SUCURSAL VIRTUAL",
    "PILAR ALCOBA": "SUCURSAL VIRTUAL", "ROCIO FERNANDEZ": "SUCURSAL VIRTUAL"
}

if "v_mem" not in st.session_state:
    st.session_state["v_mem"] = {}

pag = st.sidebar.radio("Menu", ["Panel Objetivos", "Ranking Asesores", "Cumplimiento"])

# --- PANEL OBJETIVOS ---
if pag == "Panel Objetivos":
    st.title("Panel de Objetivos")
    f = st.file_uploader("Excel Objetivos", type=["xlsx"])
    if f:
        try:
            df = pd.read_excel(f)
            df.columns = [str(c).strip() for c in df.columns]
            c_o, c_n1, c_n2, c_l = df.columns[0], df.columns[1], df.columns[2], df.columns[3]
            df["Marca"] = "OTRAS"
            m_a = "OTRAS"
            for i, r in df.iterrows():
                t = str(r[c_o]).upper()
                if "OPENCARS" in t: m_a = "OPENCARS"
                elif "PAMPAWAGEN" in t: m_a = "PAMPAWAGEN"
                elif "FORTECAR" in t: m_a = "FORTECAR"
                elif "GRANVILLE" in t: m_a = "GRANVILLE"
                elif "CITROEN" in t: m_a = "CITROEN SN"
                elif "RED" in t: m_a = "RED SECUNDARIA"
                df.at[i, "Marca"] = m_a
            df_s = df[~df[c_o].str.contains("TOTAL", na=False, case=False)].dropna(subset=[c_n1]).copy()
            m_s = st.sidebar.selectbox("Empresa", ["GRUPO TOTAL"] + sorted(df_s["Marca"].unique().tolist()))
            df_f = df_s if m_s == "GRUPO TOTAL" else df_s[df_s["Marca"] == m_s].copy()
            st.plotly_chart(px.bar(df_f, x=c_o, y=[c_l, c_n1, c_n2], barmode="group", text_auto=True))
            st.table(df_f[[c_o, c_l, c_n1]].set_index(c_o))
        except Exception as e: st.error(f"Error: {e}")

# --- RANKING ---
elif pag == "Ranking Asesores":
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
                "TOMA": int(x[co45].apply(lambda v: 1 if str(v).strip() not in ["0", "0.0", "nan", "None", "", "0,0"] else 0).sum()) if co45 else 0
            })).reset_index()
            d53r["KEY"] = d53r[d53r.columns[0]].apply(limpiar_texto)
            pda = d53r.groupby("KEY").size().reset_index(name="PDA")
            df = pd.merge(res, pda, on="KEY", how="outer").fillna(0)
            ml = {limpiar_texto(k): v for k, v in maestro_asesores.items()}
            df["Sucursal"] = df["KEY"].map(ml)
            df = df.dropna(subset=["Sucursal"]).copy()
            for c in ["VN", "VO", "PDA", "ADJ", "VE", "TOMA"]: df[c] = df[c].astype(int)
            df["TOTAL"] = df["VN"] + df["VO"] + df["ADJ"] + df["VE"] + df["PDA"]
            st.session_state["v_mem"] = df.groupby("Sucursal")["TOTAL"].sum().to_dict()
            
            def p_o(s):
                if s == "GERENCIA": return 2
                return 1 if s == "RED SECUNDARIA" else 0
            df["P"] = df["Sucursal"].apply(p_o)
            df = df.sort_values(by=["P", "TOTAL", "TOMA"], ascending=[True, False, False]).reset_index(drop=True)

            # Podio
            st.write("## 🎖️ Cuadro de Honor")
            pc = st.columns(3)
            meds = ["🥇", "🥈", "🥉"]
            for i in range(min(3, len(df))):
                a = df.iloc[i]
                with pc[i]:
                    st.markdown(f'<div style="text-align:center;border:2px solid gray;padding:10px;border-radius:10px;"><h3>{meds[i]} {a["KEY"]}</h3><h2>{a["TOTAL"]} u.</h2><p>{a["Sucursal"]}</p></div>', unsafe_allow_html=True)

            st.divider()
            f_s = st.multiselect("Filtrar Sucursal", sorted(df["Sucursal"].unique()))
            rf = df[df["Sucursal"].isin(f_s)] if f_s else df.copy()
            
            # Rank texto
            rk_txt = []
            for i in range(len(rf)):
                if i==0: rk_txt.append("🥇 1°")
                elif i==1: rk_txt.append("🥈 2°")
                elif i==2: rk_txt.append("🥉 3°")
                else: rk_txt.append(f"{i+1}°")
            rf["Rank"] = rk_txt
            
            disp = rf[["Rank", "KEY", "VN", "VO", "PDA", "ADJ", "VE", "TOTAL", "TOMA", "Sucursal"]].rename(columns={"KEY":"Asesor"})
            
            def st_f(row):
                s = ["text-align:center"] * len(row)
                if row["Sucursal"] == "SUCURSAL VIRTUAL": s = [x + "; color:#1a73e8" for x in s]
                elif row["Sucursal"] == "RED SECUNDARIA": s = [x + "; color:#8e44ad" for x in s]
                return s

            st.dataframe(disp.style.apply(st_f, axis=1), use_container_width=True, hide_index=True)
            
            # Totales
            df_v = rf[rf["Sucursal"] != "SUCURSAL VIRTUAL"]
            t_r = {"Rank":"", "Asesor":"TOTAL GENERAL", "VN":df_v["VN"].sum(), "VO":df_v["VO"].sum(), "PDA":df_v["PDA"].sum(), "ADJ":df_v["ADJ"].sum(), "VE":df_v["VE"].sum(), "TOTAL":df_v["TOTAL"].sum(), "TOMA":df_v["TOMA"].sum(), "Sucursal":""}
            df_t = pd.DataFrame([t_r])
            st.table(df_t.set_index("Rank"))
            
            # Descarga
            out = BytesIO()
            with pd.ExcelWriter(out, engine="xlsxwriter") as wr:
                pd.concat([disp, df_t]).to_excel(wr, index=False, sheet_name="Ranking")
            st.download_button("📥 Descargar Excel", out.getvalue(), "ranking.xlsx")
        except Exception as e: st.error(f"Error: {e}")

# --- CUMPLIMIENTO ---
elif pag == "Cumplimiento":
    st.title("🎯 Cumplimiento de Objetivos")
    v_r = st.session_state.get("v_mem", {})
    if not v_r: st.warning("Subí primero los archivos en el Ranking")
    f_m = st.file_uploader("Excel Metas", type=["xlsx"])
    if f_m:
        try:
            dfm = pd.read_excel(f_m)
            dfm.columns = [str(c).strip() for c in dfm.columns]
            c = dfm.columns
            dfm[c[3]] = 0
            for idx, r in dfm.iterrows():
                s_e = str(r[c[0]]).upper()
                if "TOTAL" not in s_e:
                    for s_m, v in v_r.items():
                        if s_m.upper() in s_e: dfm.at[idx, c[3]] = v
            marcas = ["OPENCARS", "PAMPAWAGEN", "GRANVILLE", "FORTECAR"]
            ini = 0
            for idx, r in dfm.iterrows():
                n = str(r[c[0]]).upper()
                if "TOTAL" in n and any(m in n for m in marcas):
                    dfm.at[idx, c[3]] = dfm.iloc[ini:idx, 3].sum()
                    ini = idx + 1
            itg = dfm[dfm[c[0]].str.contains("TOTAL GENERAL", na=False, case=False)].index
            if not itg.empty:
                sm = dfm[(dfm[c[0]].str.contains("TOTAL", case=False)) & (dfm[c[0]].str.contains("|".join(marcas), case=False))][c[3]].sum()
                sr = dfm[(dfm[c[0]].str.contains("RED SECUNDARIA", case=False)) & (~dfm[c[0]].str.contains("TOTAL GENERAL", case=False))][c[3]].sum()
                dfm.at[itg[0], c[3]] = sm + sr
            dfm["% N1"] = (dfm[c[3]] / dfm[c[1]]).fillna(0)
            st.dataframe(dfm.style.format({"% N1":"{:.1%}"}), use_container_width=True, hide_index=True)
        except Exception as e: st.error(f"Error: {e}")
