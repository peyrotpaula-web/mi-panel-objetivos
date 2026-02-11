import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Sistema Comercial Grupo", layout="wide")

# 2. MENÚ LATERAL
st.sidebar.title("🚀 Menú de Gestión")
pagina = st.sidebar.radio("Seleccione el Panel:", 
                         ["Panel de Objetivos Sucursales", 
                          "Ranking de Asesores 🥇", 
                          "Cumplimiento de Objetivos 🎯"])

st.sidebar.divider()

# MAESTRO DE ASESORES (Compartido para Opción 2 y 3)
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

# =========================================================
# OPCIÓN 1: PANEL DE OBJETIVOS (ORIGINAL)
# =========================================================
if pagina == "Panel de Objetivos Sucursales":
    # (Aquí va tu código original de la Opción 1 intacto)
    st.title("📊 Panel de Control de Objetivos Sucursales")
    uploaded_file = st.file_uploader("Sube el archivo Excel de Objetivos", type=["xlsx"], key="obj_key")
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            st.write("Archivo cargado con éxito.")
            # ... resto de tu lógica original ...
        except Exception as e:
            st.error(f"Error: {e}")

# =========================================================
# OPCIÓN 2: RANKING DE ASESORES
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

            df45_raw = leer_archivo(u45)
            df53_raw = leer_archivo(u53)

            # --- PROCESAMIENTO ---
            c_v_45 = df45_raw.columns[4]
            c_t_45 = next((c for c in df45_raw.columns if "TIPO" in str(c).upper()), "Tipo")
            c_e_45 = next((c for c in df45_raw.columns if "ESTAD" in str(c).upper()), "Estad")
            c_vo_45 = next((c for c in df45_raw.columns if "TAS. VO" in str(c).upper()), None)

            df45 = df45_raw[(df45_raw[c_e_45] != 'A') & (df45_raw[c_t_45] != 'AC')].copy()
            df45['KEY'] = df45[c_v_45].apply(limpiar_texto)

            u45_sum = df45.groupby('KEY').apply(lambda x: pd.Series({
                'VN': int((x[c_t_45].isin(['O', 'OP'])).sum()),
                'VO': int((x[c_t_45].isin(['O2','O2R'])).sum()),
                'ADJ': int((x[c_t_45] == 'PL').sum()),
                'VE': int((x[c_t_45] == 'VE').sum()),
                'TOMA_VO': int(x[c_vo_45].apply(lambda v: 1 if str(v).strip() not in ['0', '0.0', 'nan', 'None', '', '0,0'] else 0).sum()) if c_vo_45 else 0
            })).reset_index()

            c_v_53 = df53_raw.columns[0]
            df53 = df53_raw.copy()
            df53['KEY'] = df53[c_v_53].apply(limpiar_texto)
            u53_sum = df53.groupby('KEY').size().reset_index(name='PDA')

            ranking_base = pd.merge(u45_sum, u53_sum, on='KEY', how='outer').fillna(0)
            maestro_limpio = {limpiar_texto(k): v for k, v in maestro_asesores.items()}
            ranking_base['Sucursal'] = ranking_base['KEY'].map(maestro_limpio)
            ranking_base = ranking_base.dropna(subset=['Sucursal']).copy()

            ranking_base['TOTAL'] = ranking_base['VN'] + ranking_base['VO'] + ranking_base['ADJ'] + ranking_base['VE'] + ranking_base['PDA']
            ranking_base = ranking_base.sort_values(by=['TOTAL'], ascending=False).reset_index(drop=True)

            # --- TABLA ---
            ranks = ["🥇 1°" if i==0 else "🥈 2°" if i==1 else "🥉 3°" if i==2 else f"{i+1}°" for i in range(len(ranking_base))]
            ranking_base['Rank'] = ranks
            st.dataframe(ranking_base[['Rank', 'KEY', 'VN', 'VO', 'PDA', 'TOTAL', 'Sucursal']], use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"Error: {e}")

# =========================================================
# OPCIÓN 3: CUMPLIMIENTO DE OBJETIVOS (EL NUEVO BLOQUE)
# =========================================================
elif pagina == "Cumplimiento de Objetivos 🎯":
    st.title("🎯 Cumplimiento de Objetivos por Sucursal")
    st.info("Carga los archivos U45, U53 y el archivo de Objetivos para ver el avance por sucursal.")

    c1, c2, c3 = st.columns(3)
    with c1: u45_obj = st.file_uploader("Archivo U45", type=["xlsx", "xls", "csv"], key="u45_o")
    with c2: u53_obj = st.file_uploader("Archivo U53", type=["xlsx", "xls", "csv"], key="u53_o")
    with c3: u_meta = st.file_uploader("Archivo de Objetivos", type=["xlsx", "csv"], key="meta_o")

    if u45_obj and u53_obj and u_meta:
        try:
            def leer(f):
                if f.name.endswith('.csv'): return pd.read_csv(f)
                return pd.read_excel(f)

            df45_raw, df53_raw, df_meta = leer(u45_obj), leer(u53_obj), leer(u_meta)
            
            # --- PROCESAR VENTAS REALES ---
            maestro_limpio = {limpiar_texto(k): v for k, v in maestro_asesores.items()}
            
            # U45 (Ventas)
            c_v_45 = df45_raw.columns[4]
            c_t_45 = next((c for c in df45_raw.columns if "TIPO" in str(c).upper()), "Tipo")
            c_e_45 = next((c for c in df45_raw.columns if "ESTAD" in str(c).upper()), "Estad")
            df45_f = df45_raw[(df45_raw[c_e_45] != 'A') & (df45_raw[c_t_45] != 'AC')].copy()
            df45_f['Sucursal'] = df45_f[c_v_45].apply(limpiar_texto).map(maestro_limpio)
            
            # U53 (PDA)
            c_v_53 = df53_raw.columns[0]
            df53_raw['Sucursal'] = df53_raw[c_v_53].apply(limpiar_texto).map(maestro_limpio)
            
            # Sumar todo por sucursal
            real_45 = df45_f.groupby('Sucursal').size()
            real_53 = df53_raw.groupby('Sucursal').size()
            ventas_totales = (real_45.add(real_53, fill_value=0)).reset_index(name='Logrado')

            # --- PROCESAR TABLA DE OBJETIVOS ---
            # Normalizamos nombres de columnas del archivo cargado
            df_meta.columns = [c.strip() for c in df_meta.columns]
            col_suc_meta = df_meta.columns[0] # "OBJETIVOS"
            col_n1_meta = "Nivel 1" # O el nombre que tenga la columna de objetivo
            
            # Limpiamos nombres de sucursales en la meta para cruzar
            df_meta['Sucursal_Clean'] = df_meta[col_suc_meta].apply(limpiar_texto)
            ventas_totales['Sucursal_Clean'] = ventas_totales['Sucursal'].apply(limpiar_texto)

            # Unimos los datos
            df_final = pd.merge(df_meta, ventas_totales[['Sucursal_Clean', 'Logrado']], 
                                left_on='Sucursal_Clean', right_on='Sucursal_Clean', how='left').fillna(0)

            # Cálculos solicitados
            df_final['Faltan'] = (df_final[col_n1_meta] - df_final['Logrado']).clip(lower=0)
            df_final['%'] = (df_final['Logrado'] / df_final[col_n1_meta].replace(0, 1) * 100).round(1)

            # Selección de columnas final (limpia)
            resultado = df_final[[col_suc_meta, col_n1_meta, 'Logrado', 'Faltan', '%']].rename(columns={col_suc_meta: 'Sucursal', col_n1_meta: 'Objetivo'})

            # --- ESTILO Y SEMÁFORO ---
            def aplicar_semaforo(row):
                val = row['%']
                if val >= 100: color = '#28a745' # Verde
                elif val >= 80: color = '#fd7e14' # Naranja
                else: color = '#dc3545' # Rojo
                
                estilos = ['text-align: center'] * len(row)
                estilos[4] = f'text-align: center; color: {color}; font-weight: bold'
                return estilos

            st.write("### 📊 Tabla de Cumplimiento")
            st.dataframe(
                resultado.style.apply(aplicar_semaforo, axis=1),
                use_container_width=True,
                hide_index=True
            )

        except Exception as e:
            st.error(f"Error en Opción 3: {e}")
