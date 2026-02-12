import streamlit as st
import pandas as pd
from io import BytesIO

# Configuración inicial
st.set_page_config(page_title="Sistema Comercial Grupo", layout="wide")

def limpiar_texto(t):
    return " ".join(str(t).split()).replace(".", "").strip().upper()

# Maestro de Asesores completo
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

pag = st.sidebar.radio("Navegación", ["Panel de Objetivos", "Ranking de Asesores 🥇", "Cumplimiento"])

# --- SECCIÓN RANKING (INTOCABLE) ---
if pag == "Ranking de Asesores 🥇":
    st.title("🏆 Ranking de Asesores")
    c1, c2 = st.columns(2)
    u45 = c1.file_uploader("Subir U45", type=["xlsx", "xls", "csv"], key="u45_rank")
    u53 = c2.file_uploader("Subir U53", type=["xlsx", "xls", "csv"], key="u53_rank")

    if u45 and u53:
        try:
            def leer(f):
                if f.name.endswith(".csv"): return pd.read_csv(f)
                return pd.read_excel(f, engine="xlrd" if f.name.endswith(".xls") else None)
            d45, d53 = leer(u45), leer(u53)
            c_ase = d45.columns[4]; c_tip = next(c for c in d45.columns if "TIPO" in str(c).upper())
            c_est = next(c for c in d45.columns if "ESTAD" in str(c).upper())
            c_tom = next((c for c in d45.columns if "TAS. VO" in str(c).upper()), None)
            df45 = d45[(d45[c_est] != "A") & (d45[c_tip] != "AC")].copy()
            df45["KEY"] = df45[c_ase].apply(limpiar_texto)
            res = df45.groupby("KEY").apply(lambda x: pd.Series({
                "VN": int(x[c_tip].isin(["O", "OP"]).sum()), "VO": int(x[c_tip].isin(["O2","O2R"]).sum()),
                "ADJ": int((x[c_tip] == "PL").sum()), "VE": int((x[c_tip] == "VE").sum()),
                "TOMA": int(x[c_tom].apply(lambda v: 1 if str(v).strip() not in ["0", "0.0", "nan", "None", "", "0,0"] else 0).sum()) if c_tom else 0
            })).reset_index()
            d53["KEY"] = d53[d53.columns[0]].apply(limpiar_texto)
            pda = d53.groupby("KEY").size().reset_index(name="PDA")
            df = pd.merge(res, pda, on="KEY", how="outer").fillna(0)
            ml = {limpiar_texto(k): v for k, v in maestro_asesores.items()}
            df["Sucursal"] = df["KEY"].map(ml); df = df.dropna(subset=["Sucursal"]).copy()
            for c in ["VN", "VO", "PDA", "ADJ", "VE", "TOMA"]: df[c] = df[c].astype(int)
            df["TOTAL"] = df["VN"] + df["VO"] + df["ADJ"] + df["VE"] + df["PDA"]
            st.session_state["v_mem"] = df.groupby("Sucursal")["TOTAL"].sum().to_dict()
            
            def prio(s):
                if s == "GERENCIA": return 2
                return 1 if s == "RED SECUNDARIA" else 0
            df["P"] = df["Sucursal"].apply(prio); df = df.sort_values(by=["P", "TOTAL", "TOMA"], ascending=[True, False, False]).reset_index(drop=True)
            
            st.write("### 🎖️ Cuadro de Honor")
            pc = st.columns(3)
            meds = ["🥇", "🥈", "🥉"]; cols_b = ["#FFD700", "#C0C0C0", "#CD7F32"]
            for i in range(min(3, len(df))):
                a = df.iloc[i]
                with pc[i]:
                    st.markdown(f'''<div style="text-align:center;border:3px solid {cols_b[i]};border-radius:10px;padding:15px;background-color:#f8f9fa;min-height:160px;">
                        <h2 style="margin:0;">{meds[i]}</h2><b style="display:block;margin:10px 0;font-size:16px;">{a["KEY"]}</b>
                        <h1 style="color:#1f77b4;margin:0;">{a["TOTAL"]} <small style="font-size:15px;">unid.</small></h1>
                        <p style="color:gray;font-size:13px;margin-top:5px;">{a["Sucursal"]}</p></div>''', unsafe_allow_html=True)
            
            st.divider()
            f1, f2 = st.columns(2); f_suc = f1.multiselect("Filtrar Sucursal:", sorted(df["Sucursal"].unique())); f_ase = f2.text_input("Buscar Asesor:")
            rf = df.copy()
            if f_suc: rf = rf[rf["Sucursal"].isin(f_suc)]
            if f_ase: rf = rf[rf["KEY"].str.contains(f_ase.upper())]
            
            rf["Rank"] = [f"🥇 1°" if i==0 else f"🥈 2°" if i==1 else f"🥉 3°" if i==2 else f"{i+1}°" for i in range(len(rf))]
            disp = rf[["Rank", "KEY", "VN", "VO", "PDA", "ADJ", "VE", "TOTAL", "TOMA", "Sucursal"]].rename(columns={"KEY":"Asesor"})
            def styler(row):
                base = ['text-align: center'] * len(row)
                if row["Sucursal"] == "SUCURSAL VIRTUAL": return [x + "; color: #1a73e8;" for x in base]
                if row["Sucursal"] == "RED SECUNDARIA": return [x + "; color: #8e44ad;" for x in base]
                return base
            st.dataframe(disp.style.apply(styler, axis=1), use_container_width=True, hide_index=True)
            
            df_c = rf[rf["Sucursal"] != "SUCURSAL VIRTUAL"]
            sumas = {"VN": int(df_c["VN"].sum()), "VO": int(df_c["VO"].sum()), "PDA": int(df_c["PDA"].sum()), "ADJ": int(df_c["ADJ"].sum()), "VE": int(df_c["VE"].sum()), "TOTAL": int(df_c["TOTAL"].sum()), "TOMA": int(df_c["TOMA"].sum())}
            st.markdown("---")
            l, r = st.columns([1.5, 5])
            with l: st.subheader("TOTAL GENERAL")
            with r: st.table(pd.DataFrame([sumas]).assign(Idx="").set_index("Idx"))
        except Exception as e: st.error(f"Error: {e}")

# --- SECCIÓN CUMPLIMIENTO (RESTAURADA Y ROBUSTA) ---
elif pag == "Cumplimiento":
    st.title("🎯 Cumplimiento de Objetivos")
    obj_file = st.file_uploader("Subir Objetivos (Excel)", type=["xlsx"], key="obj_cump")
    
    if obj_file:
        if not st.session_state["v_mem"]:
            st.warning("⚠️ Primero subí los archivos en 'Ranking de Asesores' para tener las ventas actuales.")
        else:
            try:
                df_raw = pd.read_excel(obj_file)
                # Tomamos solo las 3 primeras columnas sin importar el nombre original
                df_obj = df_raw.iloc[:, :3].copy()
                df_obj.columns = ["Sucursal", "Obj N1", "Obj N2"]
                
                ventas_actuales = st.session_state["v_mem"]
                res_data = []

                for _, row in df_obj.iterrows():
                    suc_nombre = str(row["Sucursal"])
                    suc_key = limpiar_texto(suc_nombre)
                    obj1 = row["Obj N1"]
                    obj2 = row["Obj N2"]
                    logrado = ventas_actuales.get(suc_key, 0)
                    
                    cump1 = (logrado / obj1 * 100) if obj1 > 0 else 0
                    cump2 = (logrado / obj2 * 100) if obj2 > 0 else 0
                    
                    res_data.append({
                        "Sucursal": suc_nombre,
                        "Nivel 1": obj1,
                        "Nivel 2": obj2,
                        "Logrado": logrado,
                        "% Nivel 1": cump1,
                        "% Nivel 2": cump2,
                        "Faltan N1": max(0, obj1 - logrado),
                        "Faltan N2": max(0, obj2 - logrado)
                    })
                
                df_res = pd.DataFrame(res_data)

                def semaforo(val):
                    if val < 80: return 'color: red;'
                    elif 80 <= val < 100: return 'color: orange;'
                    return 'color: green;'

                st.dataframe(
                    df_res.style.format({
                        "% Nivel 1": "{:.1f}%", "% Nivel 2": "{:.1f}%",
                        "Nivel 1": "{:,.0f}", "Nivel 2": "{:,.0f}",
                        "Logrado": "{:,.0f}", "Faltan N1": "{:,.0f}", "Faltan N2": "{:,.0f}"
                    }).applymap(semaforo, subset=["% Nivel 1", "% Nivel 2"]),
                    use_container_width=True, hide_index=True
                )
            except Exception as e:
                st.error(f"Error al procesar el archivo: {e}")

elif pag == "Panel de Objetivos":
    st.title("📊 Panel de Objetivos")
