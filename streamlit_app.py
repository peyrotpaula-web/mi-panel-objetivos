import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# CONFIGURACIÓN INICIAL
# =========================================================
st.set_page_config(page_title="Sistema Comercial Grupo", layout="wide")

def limpiar_texto(t):
    return " ".join(str(t).split()).replace(".", "").strip().upper()

# Maestro de Asesores Global (INTACTO)
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
    "409 IGNACIO SOSA": "FORTECAR PERGAMINO", "774 ELIAS LANGONE": "FORTECAR CHIVILCOY", # Ajustado nombre
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

if 'df_final_procesado' not in st.session_state:
    st.session_state['df_final_procesado'] = None

pagina = st.sidebar.radio("Seleccionar Panel:", [
    "Ranking de Asesores 🥇", 
    "Cumplimiento de Objetivos 🎯", 
    "Panel de Objetivos Sucursales"
])

# =========================================================
# OPCIÓN 1: RANKING (SIN CAMBIOS)
# =========================================================
if pagina == "Ranking de Asesores 🥇":
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

            ranking_base['Prioridad'] = ranking_base['Sucursal'].apply(lambda x: 2 if x=="GERENCIA" else 1 if x=="RED SECUNDARIA" else 0)
            ranking_base = ranking_base.sort_values(by=['Prioridad', 'TOTAL', 'TOMA_VO'], ascending=[True, False, False]).reset_index(drop=True)

            final_display = ranking_base[['KEY', 'VN', 'VO', 'PDA', 'ADJ', 'VE', 'TOTAL', 'TOMA_VO', 'Sucursal']].rename(columns={'KEY': 'Asesor'})
            st.dataframe(final_display, use_container_width=True, hide_index=True)
        except Exception as e: st.error(f"Error: {e}")

# =========================================================
# OPCIÓN 2: CUMPLIMIENTO (SÓLO GUARDADO DE DATOS)
# =========================================================
elif pagina == "Cumplimiento de Objetivos 🎯":
    st.title("🎯 Cumplimiento de Objetivos")
    ventas_reales = st.session_state.get('ventas_sucursal_memoria', {})
    f_meta = st.file_uploader("Sube el archivo 'cumplimiento de objetivos.xlsx'", type=["xlsx"])
    if f_meta:
        try:
            df_m = pd.read_excel(f_meta)
            df_m.columns = [str(c).strip() for c in df_m.columns]
            cols = df_m.columns
            df_m[cols[3]] = 0 
            
            for idx, row in df_m.iterrows():
                suc_excel = limpiar_texto(row[cols[0]])
                if "TOTAL" in suc_excel: continue
                for s_mem, val in ventas_reales.items():
                    if limpiar_texto(s_mem) in suc_excel or suc_excel in limpiar_texto(s_mem):
                        df_m.at[idx, cols[3]] = val

            marcas = ["OPENCARS", "PAMPAWAGEN", "GRANVILLE", "FORTECAR"]
            inicio = 0
            for idx, row in df_m.iterrows():
                nombre_fila = str(row[cols[0]]).upper()
                if "TOTAL" in nombre_fila and any(m in nombre_fila for m in marcas):
                    df_m.at[idx, cols[3]] = df_m.iloc[inicio:idx, 3].sum()
                    inicio = idx + 1

            idx_total_general = df_m[df_m[cols[0]].str.contains("TOTAL GENERAL", na=False, case=False)].index
            if not idx_total_general.empty:
                suma_m = df_m[(df_m[cols[0]].str.contains("TOTAL", case=False)) & (df_m[cols[0]].str.contains("|".join(marcas), case=False))][cols[3]].sum()
                suma_r = df_m[(df_m[cols[0]].str.contains("RED SECUNDARIA", case=False)) & (~df_m[cols[0]].str.contains("TOTAL GENERAL", case=False))][cols[3]].sum()
                df_m.at[idx_total_general[0], cols[3]] = suma_m + suma_r

            df_m[cols[1]] = pd.to_numeric(df_m[cols[1]], errors='coerce').fillna(0).astype(int)
            df_m[cols[2]] = pd.to_numeric(df_m[cols[2]], errors='coerce').fillna(0).astype(int)
            
            df_m["% N1"] = (df_m[cols[3]] / df_m[cols[1]]).fillna(0)
            df_m["% N2"] = (df_m[cols[3]] / df_m[cols[2]]).fillna(0)
            df_m["Faltante N1"] = (df_m[cols[1]] - df_m[cols[3]]).apply(lambda x: x if x > 0 else 0)
            df_m["Faltante N2"] = (df_m[cols[2]] - df_m[cols[3]]).apply(lambda x: x if x > 0 else 0)

            st.session_state['df_final_procesado'] = df_m.copy()
            st.dataframe(df_m[[cols[0], cols[1], cols[2], cols[3], "% N1", "% N2"]].style.format({"% N1": "{:.1%}", "% N2": "{:.1%}"}), use_container_width=True, hide_index=True)
        except Exception as e: st.error(f"Error: {e}")

# =========================================================
# OPCIÓN 3: PANEL DE OBJETIVOS SUCURSALES (CORREGIDO)
# =========================================================
elif pagina == "Panel de Objetivos Sucursales":
    st.title("📊 Panel de Control de Objetivos Sucursales")
    
    if st.session_state['df_final_procesado'] is None:
        st.warning("⚠️ Sin datos. Completa el Panel 2 primero.")
    else:
        df_m = st.session_state['df_final_procesado']
        cols = df_m.columns

        # 1. TARJETAS (KPIs) - CORRECCIÓN DE PORCENTAJES
        fila_total = df_m[df_m[cols[0]].str.contains("TOTAL GENERAL", case=False, na=False)].iloc[0]
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Logrado Total", f"{int(fila_total[cols[3]])}")
        c2.metric("Objetivo N1", f"{int(fila_total[cols[1]])}")
        c3.metric("Objetivo N2", f"{int(fila_total[cols[2]])}")
        c4.metric("% Cumpl. N1", f"{fila_total['% N1']:.1%}")
        c5.metric("% Cumpl. N2", f"{fila_total['% N2']:.1%}")

        st.divider()

        # 2. RENDIMIENTO POR SUCURSAL (CON NÚMEROS EN BARRAS)
        st.subheader("Rendimiento por Sucursal")
        df_suc = df_m[~df_m[cols[0]].str.contains("TOTAL", case=False, na=False)].copy()
        fig_barras = px.bar(
            df_suc, x=cols[0], y=[cols[3], cols[1], cols[2]],
            barmode='group', text_auto=True, # Muestra los números en las barras
            color_discrete_map={cols[3]: '#00CC96', cols[1]: '#636EFA', cols[2]: '#AB63FA'}
        )
        st.plotly_chart(fig_barras, use_container_width=True)

        # 3. RANKING MARCA Y TERMÓMETRO
        col_l, col_r = st.columns([2, 1])
        with col_l:
            st.subheader("Ranking de Cumplimiento por Marca")
            df_marcas = df_m[df_m[cols[0]].str.contains("TOTAL", case=False) & ~df_m[cols[0]].str.contains("GENERAL", case=False)].copy()
            df_marcas = df_marcas.sort_values("% N1", ascending=True)
            fig_m = px.bar(df_marcas, x="% N1", y=cols[0], orientation='h', text_auto='.1%',
                          color="% N1", color_continuous_scale='RdYlGn')
            st.plotly_chart(fig_m, use_container_width=True)

        with col_r:
            st.subheader("Avance Global N1")
            fig_g = go.Figure(go.Indicator(mode="gauge+number", value=fila_total["% N1"]*100,
                gauge={'axis': {'range': [0, 110]}, 'bar': {'color': "black"},
                       'steps': [{'range': [0, 80], 'color': "#ff4b4b"}, {'range': [80, 90], 'color': "#ffa500"}, {'range': [90, 110], 'color': "#00CC96"}]}))
            st.plotly_chart(fig_g, use_container_width=True)

        # 4. MATRIZ DE CUMPLIMIENTO (90%)
        st.subheader("Matriz de Cumplimiento")
        m1, m2 = st.columns(2)
        with m1:
            st.success("🟢 Líderes (>= 90% N1)")
            st.dataframe(df_suc[df_suc["% N1"] >= 0.9][[cols[0], "% N1", "Faltante N1", "Faltante N2"]].style.format({"% N1": "{:.1%}"}), hide_index=True, use_container_width=True)
        with m2:
            st.error("🔴 Alerta (< 90% N1)")
            st.dataframe(df_suc[df_suc["% N1"] < 0.9][[cols[0], "% N1", "Faltante N1", "Faltante N2"]].style.format({"% N1": "{:.1%}"}), hide_index=True, use_container_width=True)

        # 5. SEMÁFORO
        st.subheader("Semáforo de Cumplimiento de Sucursales")
        df_sem = df_suc.sort_values("% N1", ascending=False)
        fig_s = px.imshow([df_sem["% N1"]*100], x=df_sem[cols[0]], color_continuous_scale='RdYlGn', text_auto=".0f")
        st.plotly_chart(fig_s, use_container_width=True)
