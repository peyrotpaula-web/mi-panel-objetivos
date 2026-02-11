import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Sistema Comercial Grupo", layout="wide")

# 2. MENÚ LATERAL
st.sidebar.title("🚀 Menú de Gestión")
pagina = st.sidebar.radio("Seleccione el Panel:", 
                         ["Panel de Objetivos Sucursales", "Ranking de Asesores 🥇", "Cumplimiento de Objetivos 🎯"])

# MAESTRO DE ASESORES (Tu lista original e intacta)
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
# OPCIÓN 1: PANEL DE OBJETIVOS SUCURSALES (Archivo Nuevo)
# =========================================================
if pagina == "Panel de Objetivos Sucursales":
    st.title("📊 Panel de Control de Objetivos")
    u_meta = st.file_uploader("Subir archivo 'cumplimiento de objetivos'", type=["xlsx"], key="u_meta_1")

    if u_meta:
        try:
            df = pd.read_excel(u_meta)
            # Limpiar nombres de columnas (quita espacios extras)
            df.columns = [str(c).strip() for c in df.columns]
            
            # Identificar columnas por posición para evitar errores de nombres
            col_suc = df.columns[0]   # OBJETIVOS
            col_n1 = df.columns[1]    # Nivel 1
            col_log = df.columns[3]   # Logrado

            # Convertir a números y limpiar filas vacías
            df[col_n1] = pd.to_numeric(df[col_n1], errors='coerce').fillna(0)
            df[col_log] = pd.to_numeric(df[col_log], errors='coerce').fillna(0)
            
            # Filtrar filas de totales y vacíos
            df_plot = df[~df[col_suc].str.contains("TOTAL", na=False, case=False)].copy()
            df_plot = df_plot[df_plot[col_n1] > 0] # Solo sucursales con objetivo

            st.write("### 🏢 Rendimiento por Sucursal")
            fig = px.bar(df_plot, x=col_suc, y=[col_log, col_n1], 
                         barmode='group', text_auto=True,
                         labels={'value': 'Unidades', 'variable': 'Métrica'})
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(df_plot[[col_suc, col_n1, col_log]], use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"Hubo un problema al leer el archivo: {e}")

# =========================================================
# OPCIÓN 2: RANKING (Tu código original mantenido)
# =========================================================
elif pagina == "Ranking de Asesores 🥇":
    st.title("🏆 Ranking de Asesores Comercial")
    
    c1, c2 = st.columns(2)
    with c1: u45 = st.file_uploader("Archivo U45", type=["xlsx", "xls", "csv"], key="u45_f")
    with c2: u53 = st.file_uploader("Archivo U53", type=["xlsx", "xls", "csv"], key="u53_f")

    if u45 and u53:
        try:
            def leer_archivo(file):
                if file.name.endswith('.csv'): return pd.read_csv(file)
                return pd.read_excel(file, engine='xlrd' if file.name.endswith('.xls') else None)

            df45_raw = leer_archivo(u45)
            df53_raw = leer_archivo(u53)

            # --- PROCESAMIENTO (TU LÓGICA ORIGINAL) ---
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
            ranking_base['Prioridad'] = ranking_base['Sucursal'].apply(lambda x: 1 if x == "RED SECUNDARIA" else 0)
            ranking_base = ranking_base.sort_values(by=['Prioridad', 'TOTAL', 'TOMA_VO'], ascending=[True, False, False]).reset_index(drop=True)

            # --- PODIO ---
            st.write("## 🎖️ Cuadro de Honor")
            podio_cols = st.columns(3)
            medallas_p, colores_podio = ["🥇", "🥈", "🥉"], ["#FFD700", "#C0C0C0", "#CD7F32"]
            for i in range(3):
                if i < len(ranking_base):
                    asesor = ranking_base.iloc[i]
                    with podio_cols[i]:
                        st.markdown(f'<div style="text-align: center; border: 2px solid {colores_podio[i]}; border-radius: 15px; padding: 15px; background-color: #f9f9f9;"><h1 style="margin: 0;">{medallas_p[i]}</h1><p style="font-weight: bold; margin: 5px 0;">{asesor["KEY"]}</p><h2 style="color: #1f77b4; margin: 0;">{int(asesor["TOTAL"])} <small>u.</small></h2><span style="font-size: 0.8em; color: gray;">{asesor["Sucursal"]}</span></div>', unsafe_allow_html=True)

            st.divider()
            st.dataframe(ranking_base[['KEY', 'VN', 'VO', 'PDA', 'ADJ', 'VE', 'TOTAL', 'Sucursal']], use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"Error: {e}")

# =========================================================
# OPCIÓN 3: CUMPLIMIENTO (Cruzando U45+U53 vs Excel Metas)
# =========================================================
elif pagina == "Cumplimiento de Objetivos 🎯":
    st.title("🎯 Cumplimiento: Real vs Objetivos")
    
    col1, col2, col3 = st.columns(3)
    with col1: u45_o = st.file_uploader("U45", type=["xlsx", "csv"], key="c_u45")
    with col2: u53_o = st.file_uploader("U53", type=["xlsx", "csv"], key="c_u53")
    with col3: meta_o = st.file_uploader("Archivo Metas", type=["xlsx"], key="c_meta")

    if u45_o and u53_o and meta_o:
        try:
            # 1. Procesar Ventas Reales
            d45 = pd.read_excel(u45_o) if u45_o.name.endswith('xlsx') else pd.read_csv(u45_o)
            d53 = pd.read_excel(u53_o) if u53_o.name.endswith('xlsx') else pd.read_csv(u53_o)
            
            maestro_limpio = {limpiar_texto(k): v for k, v in maestro_asesores.items()}

            # Contar U45
            c_v_45 = d45.columns[4]
            d45['Sucursal'] = d45[c_v_45].apply(limpiar_texto).map(maestro_limpio)
            real45 = d45.groupby('Sucursal').size()

            # Contar U53
            c_v_53 = d53.columns[0]
            d53['Sucursal'] = d53[c_v_53].apply(limpiar_texto).map(maestro_limpio)
            real53 = d53.groupby('Sucursal').size()

            # Sumar ambos
            reales = (real45.add(real53, fill_value=0)).reset_index(name='Ventas_Reales')
            reales['Sucursal_Clean'] = reales['Sucursal'].apply(limpiar_texto)

            # 2. Procesar Metas
            df_m = pd.read_excel(meta_o)
            df_m.columns = [str(c).strip() for c in df_m.columns]
            col_suc_meta = df_m.columns[0]
            col_obj_n1 = df_m.columns[1]
            
            df_m['Sucursal_Clean'] = df_m[col_suc_meta].apply(limpiar_texto)
            
            # 3. Unir
            final = pd.merge(df_m, reales[['Sucursal_Clean', 'Ventas_Reales']], on='Sucursal_Clean', how='left').fillna(0)
            
            # Calcular indicadores
            final['Objetivo'] = pd.to_numeric(final[col_obj_n1], errors='coerce').fillna(0)
            final['Logrado'] = final['Ventas_Reales'].astype(int)
            final['%'] = (final['Logrado'] / final['Objetivo'].replace(0,1) * 100).round(1)

            # Mostrar solo filas con objetivos reales
            final_view = final[final['Objetivo'] > 0][[col_suc_meta, 'Objetivo', 'Logrado', '%']]
            
            st.write("### 📊 Tabla de Cumplimiento")
            st.dataframe(final_view.style.highlight_max(axis=0), use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"Error en el cruce de datos: {e}")
