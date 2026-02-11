import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. CONFIGURACIÓN BASE
st.set_page_config(page_title="Gestión Comercial Grupo", layout="wide")

# Maestro de Asesores (Copia fiel del tuyo)
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

def limpiar_texto(t):
    return " ".join(str(t).split()).replace(".", "").strip().upper()

# NAVEGACIÓN
pagina = st.sidebar.radio("Seleccionar Panel:", ["Panel de Objetivos Sucursales", "Ranking de Asesores 🥇", "Cumplimiento de Objetivos 🎯"])

# =========================================================
# OPCIÓN 1: PANEL DE OBJETIVOS (CÓDIGO ORIGINAL RECUPERADO)
# =========================================================
if pagina == "Panel de Objetivos Sucursales":
    st.title("📊 Panel de Control de Objetivos Sucursales")
    COLORES_MARCAS = {"PAMPAWAGEN": "#001E50", "FORTECAR": "#102C54", "GRANVILLE": "#FFCE00", "CITROEN SN": "#E20613", "OPENCARS": "#00A1DF", "RED SECUNDARIA": "#4B4B4B", "OTRAS": "#999999"}
    uploaded_file = st.file_uploader("Sube el archivo Excel de Objetivos", type=["xlsx"], key="panel_obj")
    
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            df.columns = [str(c).strip() for c in df.columns]
            col_obj, col_n1, col_n2, col_log = df.columns[0], df.columns[1], df.columns[2], df.columns[3]
            df['Marca'] = "OTRAS"
            marca_actual = "OTRAS"
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
            df_final['%_txt'] = df_final['%_int'].astype(str) + "%"
            st.subheader(f"📍 Resumen: {marca_sel}")
            t_log, t_n1, t_n2 = df_final[col_log].sum(), df_final[col_n1].sum(), df_final[col_n2].sum()
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Logrado", int(t_log)); c2.metric("Nivel 1", int(t_n1)); c3.metric("Nivel 2", int(t_n2)); c4.metric("% Global", f"{int((t_log/t_n1*100)) if t_n1>0 else 0}%")
            fig_bar = px.bar(df_final, x=col_obj, y=[col_log, col_n1, col_n2], barmode='group', color_discrete_sequence=["#00CC96", "#636EFA", "#AB63FA"], text_auto=True)
            st.plotly_chart(fig_bar, use_container_width=True)
            st.table(df_final[[col_obj, '%_txt']].set_index(col_obj))
        except Exception as e: st.error(f"Error: {e}")

# =========================================================
# OPCIÓN 2: RANKING (RESTAURADO AL LOGRADO ANTERIORMENTE)
# =========================================================
elif pagina == "Ranking de Asesores 🥇":
    st.title("🏆 Ranking de Asesores Comercial")
    c1, c2 = st.columns(2)
    with c1: u45 = st.file_uploader("Archivo U45", type=["xlsx", "xls", "csv"], key="u45_main")
    with c2: u53 = st.file_uploader("Archivo U53", type=["xlsx", "xls", "csv"], key="u53_main")
    if u45 and u53:
        try:
            def leer(f): 
                if f.name.endswith('.csv'): return pd.read_csv(f)
                return pd.read_excel(f, engine='xlrd' if f.name.endswith('.xls') else None)
            df45_raw, df53_raw = leer(u45), leer(u53)
            # Procesamiento U45
            c_v_45 = df45_raw.columns[4]; c_t_45 = next((c for c in df45_raw.columns if "TIPO" in str(c).upper()), "Tipo")
            c_e_45 = next((c for c in df45_raw.columns if "ESTAD" in str(c).upper()), "Estad")
            df45 = df45_raw[(df45_raw[c_e_45] != 'A') & (df45_raw[c_t_45] != 'AC')].copy()
            df45['KEY'] = df45[c_v_45].apply(limpiar_texto)
            u45_sum = df45.groupby('KEY').apply(lambda x: pd.Series({'VN': (x[c_t_45].isin(['O', 'OP'])).sum(), 'VO': (x[c_t_45].isin(['O2','O2R'])).sum(), 'ADJ': (x[c_t_45]=='PL').sum(), 'VE': (x[c_t_45]=='VE').sum()})).reset_index()
            # Procesamiento U53
            c_v_53 = df53_raw.columns[0]; df53 = df53_raw.copy(); df53['KEY'] = df53[c_v_53].apply(limpiar_texto)
            u53_sum = df53.groupby('KEY').size().reset_index(name='PDA')
            # Union
            ranking = pd.merge(u45_sum, u53_sum, on='KEY', how='outer').fillna(0)
            maestro_limpio = {limpiar_texto(k): v for k, v in maestro_asesores.items()}
            ranking['Sucursal'] = ranking['KEY'].map(maestro_limpio)
            ranking = ranking.dropna(subset=['Sucursal']).copy()
            ranking['TOTAL'] = ranking['VN'] + ranking['VO'] + ranking['ADJ'] + ranking['VE'] + ranking['PDA']
            ranking = ranking.sort_values('TOTAL', ascending=False).reset_index(drop=True)
            # Podio
            cols = st.columns(3)
            for i in range(min(3, len(ranking))):
                with cols[i]: st.metric(f"Pos {i+1} - {ranking.iloc[i]['KEY']}", f"{int(ranking.iloc[i]['TOTAL'])} u.")
            st.divider()
            st.dataframe(ranking[['KEY', 'VN', 'VO', 'PDA', 'TOTAL', 'Sucursal']], use_container_width=True)
        except Exception as e: st.error(f"Error procesando Ranking: {e}")

# =========================================================
# OPCIÓN 3: CUMPLIMIENTO (NUEVO - SINCRONIZADO)
# =========================================================
elif pagina == "Cumplimiento de Objetivos 🎯":
    st.title("🎯 Cumplimiento de Objetivos (Sincronizado)")
    st.info("Sube los archivos para ver la tabla de objetivos con los datos de 'Logrado' actualizados automáticamente.")
    c1, c2, c3 = st.columns(3)
    with c1: f45 = st.file_uploader("U45", type=["xlsx", "xls", "csv"], key="u45_cump")
    with c2: f53 = st.file_uploader("U53", type=["xlsx", "xls", "csv"], key="u53_cump")
    with c3: f_meta = st.file_uploader("Archivo Objetivos", type=["xlsx"], key="meta_cump")
    
    if f45 and f53 and f_meta:
        try:
            # 1. Obtener Ventas de los archivos reales
            d45 = pd.read_excel(f45) if f45.name.endswith('xlsx') else pd.read_csv(f45)
            d53 = pd.read_excel(f53) if f53.name.endswith('xlsx') else pd.read_csv(f53)
            maestro_limpio = {limpiar_texto(k): v for k, v in maestro_asesores.items()}
            d45['Sucursal'] = d45.iloc[:, 4].apply(limpiar_texto).map(maestro_limpio)
            d53['Sucursal'] = d53.iloc[:, 0].apply(limpiar_texto).map(maestro_limpio)
            ventas_por_sucursal = pd.concat([d45['Sucursal'], d53['Sucursal']]).value_counts().to_dict()
            
            # 2. Leer archivo de cumplimiento
            df_m = pd.read_excel(f_meta)
            df_m.columns = [str(c).strip() for c in df_m.columns]
            col_suc = df_m.columns[0]; col_log = df_m.columns[3]
            
            # 3. Actualizar columna Logrado
            for idx, row in df_m.iterrows():
                suc_txt = str(row[col_suc]).strip().upper()
                if "TOTAL" in suc_txt:
                    # Si es una fila de TOTAL, dejamos que el Excel sume o lo calculamos luego
                    continue
                # Buscamos si la sucursal del excel está en nuestras ventas reales
                for suc_real, cant in ventas_por_sucursal.items():
                    if str(suc_real).upper() in suc_txt:
                        df_m.at[idx, col_log] = cant
            
            # 4. Mostrar exactamente como el archivo
            st.write("### 📊 Tabla de Objetivos Actualizada")
            st.dataframe(df_m.fillna(0), use_container_width=True, hide_index=True)
        except Exception as e: st.error(f"Error en cumplimiento: {e}")
