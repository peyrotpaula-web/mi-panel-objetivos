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
# OPCIÓN 1: PANEL DE OBJETIVOS (INTACTO)
# =========================================================
if pagina == "Panel de Objetivos Sucursales":
    st.title("📊 Panel de Control de Objetivos Sucursales")
    uploaded_file = st.file_uploader("Sube el archivo Excel de Objetivos", type=["xlsx"], key="obj_panel_key")
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
            df_final = df_suc if marca_sel == "GRUPO TOTAL" else df_suc[df_suc['Marca'] == marca_sel].copy()
            df_final['%_int'] = (df_final[col_log] / df_final[col_n1] * 100).fillna(0).round(0).astype(int)
            st.subheader(f"📍 Resumen: {marca_sel}")
            fig_bar = px.bar(df_final, x=col_obj, y=[col_log, col_n1, col_n2], barmode='group', color_discrete_sequence=["#00CC96", "#636EFA", "#AB63FA"], text_auto=True)
            st.plotly_chart(fig_bar, use_container_width=True)
            st.table(df_final[[col_obj, col_log, col_n1, '%_int']].set_index(col_obj))
        except Exception as e: st.error(f"Error: {e}")

# =========================================================
# OPCIÓN 2: RANKING (AJUSTES DE ORDEN Y DESCARGA)
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

            # Lógica de Prioridad: 0: Normal, 1: Red Secundaria, 2: Gerencia
            def asignar_prioridad(suc):
                if suc == "GERENCIA": return 2
                if suc == "RED SECUNDARIA": return 1
                return 0

            ranking_base['Prioridad'] = ranking_base['Sucursal'].apply(asignar_prioridad)
            ranking_base = ranking_base.sort_values(by=['Prioridad', 'TOTAL', 'TOMA_VO'], ascending=[True, False, False]).reset_index(drop=True)

            col_f1, col_f2 = st.columns(2)
            with col_f1: filtro_sucursal = st.multiselect("Filtrar por Sucursal:", sorted(ranking_base['Sucursal'].unique()))
            with col_f2: filtro_asesor = st.text_input("Buscar Asesor:")

            ranking = ranking_base.copy()
            if filtro_sucursal: ranking = ranking[ranking['Sucursal'].isin(filtro_sucursal)]
            if filtro_asesor: ranking = ranking[ranking['KEY'].str.contains(filtro_asesor.upper())]

            # TABLA PRINCIPAL
            ranks = [f"🥇 1°" if i==0 else f"🥈 2°" if i==1 else f"🥉 3°" if i==2 else f"{i+1}°" for i in range(len(ranking))]
            ranking['Rank'] = ranks
            final_display = ranking[['Rank', 'KEY', 'VN', 'VO', 'PDA', 'ADJ', 'VE', 'TOTAL', 'TOMA_VO', 'Sucursal']].rename(columns={'KEY': 'Asesor'})
            
            def color_y_centrado(row):
                styles = ['text-align: center'] * len(row)
                if row['Sucursal'] == "SUCURSAL VIRTUAL": styles = [s + '; color: #1a73e8' for s in styles]
                elif row['Sucursal'] == "RED SECUNDARIA": styles = [s + '; color: #8e44ad' for s in styles]
                elif row['Sucursal'] == "GERENCIA": styles = [s + '; color: #e67e22' for s in styles]
                return styles

            st.dataframe(final_display.style.apply(color_y_centrado, axis=1), use_container_width=True, hide_index=True)
            
            # TOTALES
            df_v = ranking[ranking['Sucursal'] != "SUCURSAL VIRTUAL"]
            totales = pd.DataFrame({'Métrica': ['TOTAL'], 'VN': [df_v['VN'].sum()], 'VO': [df_v['VO'].sum()], 'PDA': [df_v['PDA'].sum()], 'ADJ': [df_v['ADJ'].sum()], 'VE': [df_v['VE'].sum()], 'TOTAL': [df_v['TOTAL'].sum()], 'TOMA_VO': [df_v['TOMA_VO'].sum()]}).set_index('Métrica')
            st.table(totales.style.set_properties(**{'text-align': 'center'}))

            # BOTÓN DE DESCARGA CON TOTALES
            df_csv = pd.concat([final_display, totales.reset_index().rename(columns={'Métrica':'Asesor'})]).fillna("")
            st.download_button(label="📥 Descargar Ranking CSV", data=df_csv.to_csv(index=False).encode('utf-8'), file_name='ranking_comercial.csv', mime='text/csv')

        except Exception as e: st.error(f"Error: {e}")

# =========================================================
# OPCIÓN 3: CUMPLIMIENTO (COLUMNAS FALTANTES Y SEMÁFORO FUENTE)
# =========================================================
elif pagina == "Cumplimiento de Objetivos 🎯":
    st.title("🎯 Cumplimiento de Objetivos")
    ventas_reales = st.session_state.get('ventas_sucursal_memoria', {})
    if not ventas_reales:
        st.warning("⚠️ Sube primero los archivos en el panel de Ranking para ver datos aquí.")
    
    f_meta = st.file_uploader("Sube el archivo 'cumplimiento de objetivos.xlsx'", type=["xlsx"])
    if f_meta:
        try:
            df_m = pd.read_excel(f_meta)
            df_m.columns = [str(c).strip() for c in df_m.columns]
            cols = df_m.columns
            df_m[cols[3]] = 0 # Logrado
            
            for idx, row in df_m.iterrows():
                suc_ex = str(row[cols[0]]).upper()
                if "TOTAL" in suc_ex: continue
                for s_mem, val in ventas_reales.items():
                    if s_mem.upper() in suc_ex:
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
                suma_marcas = df_m[(df_m[cols[0]].str.contains("TOTAL", case=False)) & (df_m[cols[0]].str.contains("|".join(marcas), case=False))][cols[3]].sum()
                suma_red = df_m[(df_m[cols[0]].str.contains("RED SECUNDARIA", case=False)) & (~df_m[cols[0]].str.contains("TOTAL GENERAL", case=False))][cols[3]].sum()
                df_m.at[idx_total_general[0], cols[3]] = suma_marcas + suma_red

            df_m[cols[1]] = pd.to_numeric(df_m[cols[1]], errors='coerce').fillna(0).astype(int)
            df_m[cols[2]] = pd.to_numeric(df_m[cols[2]], errors='coerce').fillna(0).astype(int)
            df_m[cols[3]] = df_m[cols[3]].astype(int)
            
            col_pct_n1, col_pct_n2 = "% N1", "% N2"
            df_m[col_pct_n1] = (df_m[cols[3]] / df_m[cols[1]]).replace([float('inf'), -float('inf')], 0).fillna(0)
            df_m[col_pct_n2] = (df_m[cols[3]] / df_m[cols[2]]).replace([float('inf'), -float('inf')], 0).fillna(0)

            # NUEVAS COLUMNAS: FALTANTES
            df_m["Faltante N1"] = (df_m[cols[1]] - df_m[cols[3]]).apply(lambda x: x if x > 0 else 0)
            df_m["Faltante N2"] = (df_m[cols[2]] - df_m[cols[3]]).apply(lambda x: x if x > 0 else 0)

            # --- ESTILOS ---
            def resaltar_totales(row):
                if "TOTAL" in str(row[cols[0]]).upper():
                    return ['font-weight: bold; background-color: #f0f2f6'] * len(row)
                return [''] * len(row)

            def semaforo_fuente(val):
                if val >= 1.0: color = '#28a745' # Verde
                elif val >= 0.8: color = '#fd7e14' # Naranja
                else: color = '#dc3545' # Rojo
                return f'color: {color}; font-weight: bold; text-align: center'

            st.write("### ✅ Resumen de Cumplimiento")
            # Selección de columnas final
            df_final = df_m[[cols[0], cols[1], cols[2], cols[3], col_pct_n1, col_pct_n2, "Faltante N1", "Faltante N2"]]
            
            estilo_df = df_final.style.apply(resaltar_totales, axis=1) \
                .map(semaforo_fuente, subset=[col_pct_n1, col_pct_n2]) \
                .format({
                    cols[1]: "{:,.0f}", cols[2]: "{:,.0f}", cols[3]: "{:,.0f}",
                    col_pct_n1: "{:.1%}", col_pct_n2: "{:.1%}",
                    "Faltante N1": "{:,.0f}", "Faltante N2": "{:,.0f}"
                })

            st.dataframe(estilo_df, use_container_width=True, hide_index=True)
            
        except Exception as e: st.error(f"Error: {e}")
