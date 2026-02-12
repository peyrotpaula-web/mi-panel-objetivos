import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# Configuración inicial
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

if "v_memoria" not in st.session_state:
    st.session_state["v_memoria"] = {}

pag = st.sidebar.radio("Navegación", ["Panel de Objetivos", "Ranking de Asesores 🥇", "Cumplimiento"])

# --- OBJETIVOS ---
if pag == "Panel de Objetivos":
    st.title("📊 Panel de Objetivos")
    f_obj = st.file_uploader("Subir Excel", type=["xlsx"])
    if f_obj:
        try:
            df = pd.read_excel(f_obj)
            df.columns = [str(c).strip() for c in df.columns]
            c_o, c_n1, c_n2, c_l = df.columns[0], df.columns[1], df.columns[2], df.columns[3]
            df["Marca"] = "OTRAS"; m_a = "OTRAS"
            for i, r in df.iterrows():
                t = str(r[c_o]).upper()
                if "OPENCARS" in t: m_a = "OPENCARS"
                elif "PAMPAWAGEN" in t: m_a = "PAMPAWAGEN"
                elif "FORTECAR" in t: m_a = "FORTECAR"
                elif "GRANVILLE" in t: m_a = "GRANVILLE"
                df.at[i, "Marca"] = m_a
            df_s = df[~df[c_o].str.contains("TOTAL", na=False, case=False)].dropna(subset=[c_n1]).copy()
            st.plotly_chart(px.bar(df_s, x=c_o, y=[c_l, c_n1], barmode="group", text_auto=True))
            st.table(df_s[[c_o, c_l, c_n1]])
        except Exception as e: st.error(f"Error: {e}")

# --- RANKING ---
elif pag == "Ranking de Asesores 🥇":
    st.title("🏆 Ranking Comercial")
    col1, col2 = st.columns(2)
    u45 = col1.file_uploader("Archivo U45", type=["xlsx", "xls", "csv"])
    u53 = col2.file_uploader("Archivo U53", type=["xlsx", "xls", "csv"])

    if u45 and u53:
        try:
            def leer(arch):
                if arch.name.endswith(".csv"): return pd.read_csv(arch)
                return pd.read_excel(arch, engine="xlrd" if arch.name.endswith(".xls") else None)
            d45, d53 = leer(u45), leer(u53)
            
            # Procesar datos
            c_asesor = d45.columns[4]
            c_tipo = next(c for c in d45.columns if "TIPO" in str(c).upper())
            c_est = next(c for c in d45.columns if "ESTAD" in str(c).upper())
            c_toma = next((c for c in d45.columns if "TAS. VO" in str(c).upper()), None)
            
            df45 = d45[(d45[c_est] != "A") & (d45[c_tipo] != "AC")].copy()
            df45["KEY"] = df45[c_asesor].apply(limpiar_texto)
            
            res = df45.groupby("KEY").apply(lambda x: pd.Series({
                "VN": int(x[c_tipo].isin(["O", "OP"]).sum()),
                "VO": int(x[c_tipo].isin(["O2","O2R"]).sum()),
                "ADJ": int((x[c_tipo] == "PL").sum()),
                "VE": int((x[c_tipo] == "VE").sum()),
                "TOMA": int(x[c_toma].apply(lambda v: 1 if str(v).strip() not in ["0", "0.0", "nan", "None", "", "0,0"] else 0).sum()) if c_toma else 0
            })).reset_index()
            
            d53["KEY"] = d53[d53.columns[0]].apply(limpiar_texto)
            pda = d53.groupby("KEY").size().reset_index(name="PDA")
            df = pd.merge(res, pda, on="KEY", how="outer").fillna(0)
            
            m_l = {limpiar_texto(k): v for k, v in maestro_asesores.items()}
            df["Sucursal"] = df["KEY"].map(m_l)
            df = df.dropna(subset=["Sucursal"]).copy()
            
            for c in ["VN", "VO", "PDA", "ADJ", "VE", "TOMA"]: df[c] = df[c].astype(int)
            df["TOTAL"] = df["VN"] + df["VO"] + df["ADJ"] + df["VE"] + df["PDA"]
            st.session_state["v_memoria"] = df.groupby("Sucursal")["TOTAL"].sum().to_dict()

            # Orden Gerencia al final
            def prio(s):
                if s == "GERENCIA": return 2
                return 1 if s == "RED SECUNDARIA" else 0
            df["P"] = df["Sucursal"].apply(prio)
            df = df.sort_values(by=["P", "TOTAL", "TOMA"], ascending=[True, False, False]).reset_index(drop=True)

            # Podio original
            st.write("## 🎖️ Cuadro de Honor")
            pc = st.columns(3); meds = ["🥇", "🥈", "🥉"]; cols_b = ["#FFD700", "#C0C0C0", "#CD7F32"]
            for i in range(min(3, len(df))):
                a = df.iloc[i]
                with pc[i]:
                    st.markdown(f'''<div style="text-align:center;border:3px solid {cols_b[i]};border-radius:15px;padding:15px;background-color:#f8f9fa;">
                        <h1 style="margin:0;">{meds[i]}</h1><h3 style="margin:5px;">{a["KEY"]}</h3>
                        <h2 style="color:#1f77b4;margin:0;">{a["TOTAL"]} <small>u.</small></h2>
                        <p style="color:gray;">{a["Sucursal"]}</p></div>''', unsafe_allow_html=True)

            st.divider()
            # Filtros restaurados
            f_col1, f_col2 = st.columns(2)
            f_suc = f_col1.multiselect("Filtrar Sucursal:", sorted(df["Sucursal"].unique()))
            f_ase = f_col2.text_input("Buscar por nombre de Asesor:")
            
            rf = df.copy()
            if f_suc: rf = rf[rf["Sucursal"].isin(f_suc)]
            if f_ase: rf = rf[rf["KEY"].str.contains(f_ase.upper())]

            # Tabla
            rf["Rank"] = [f"🥇 1°" if i==0 else f"🥈 2°" if i==1 else f"🥉 3°" if i==2 else f"{i+1}°" for i in range(len(rf))]
            disp = rf[["Rank", "KEY", "VN", "VO", "PDA", "ADJ", "VE", "TOTAL", "TOMA", "Sucursal"]].rename(columns={"KEY":"Asesor"})
            
            def styler(row):
                s = ['text-align: center'] * len(row)
                if row["Sucursal"] == "SUCURSAL VIRTUAL": s = [x + "; color: #1a73e8" for x in s]
                elif row["Sucursal"] == "RED SECUNDARIA": s = [x + "; color: #8e44ad" for x in s]
                return s
            st.dataframe(disp.style.apply(styler, axis=1), use_container_width=True, hide_index=True)

            # Totales y Descarga
            df_v = rf[rf["Sucursal"] != "SUCURSAL VIRTUAL"]
            t_row = {"Rank": "", "Asesor": "TOTAL GENERAL", "VN": df_v["VN"].sum(), "VO": df_v["VO"].sum(), "PDA": df_v["PDA"].sum(), "ADJ": df_v["ADJ"].sum(), "VE": df_v["VE"].sum(), "TOTAL": df_v["TOTAL"].sum(), "TOMA": df_v["TOMA"].sum(), "Sucursal": ""}
            df_tot = pd.DataFrame([t_row])
            st.table(df_tot.set_index("Rank"))

            output = BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                pd.concat([disp, df_tot]).to_excel(writer, index=False, sheet_name="Ranking")
            st.download_button("📥 Descargar Ranking Completo (Excel)", output.getvalue(), "ranking_asesores.xlsx")

        except Exception as e: st.error(f"Error: {e}")

# --- CUMPLIMIENTO ---
elif pag == "Cumplimiento":
    st.title("🎯 Cumplimiento")
    v_r = st.session_state.get("v_memoria", {})
    f_m = st.file_uploader("Metas Excel", type=["xlsx"])
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
            dfm["%"] = (dfm[c[3]] / dfm[c[1]]).fillna(0)
            st.dataframe(dfm.style.format({"%": "{:.1%}"}), use_container_width=True, hide_index=True)
        except Exception as e: st.error(f"Error: {e}")
