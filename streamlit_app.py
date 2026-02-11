import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Sistema Comercial Grupo", layout="wide")

def limpiar_texto(t):
    return " ".join(str(t).split()).replace(".", "").strip().upper()

# 2. MAESTRO DE ASESORES
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

st.sidebar.title("🚀 Menú de Gestión")
pagina = st.sidebar.radio("Seleccione el Panel:", ["Panel de Objetivos Sucursales", "Ranking de Asesores 🥇", "Cumplimiento de Objetivos 🎯"])

# --- PANEL 1 Y 2 SE MANTIENEN IGUAL (Omitidos aquí por brevedad pero deben ir en tu código completo) ---

if pagina == "Cumplimiento de Objetivos 🎯":
    st.title("🎯 Cumplimiento de Objetivos (Ventas Reales)")
    
    c1, c2, c3 = st.columns(3)
    with c1: u45 = st.file_uploader("Archivo U45", type=["xlsx", "xls", "csv"], key="u45_c")
    with c2: u53 = st.file_uploader("Archivo U53", type=["xlsx", "xls", "csv"], key="u53_c")
    with c3: u_meta = st.file_uploader("Cumplimiento de Objetivos.xlsx", type=["xlsx"], key="meta_c")

    if u45 and u53 and u_meta:
        try:
            # 1. PROCESAR VENTAS REALES (U45 y U53)
            def cargar(f): return pd.read_excel(f) if f.name.endswith('xlsx') else pd.read_csv(f)
            df45, df53 = cargar(u45), cargar(u53)
            
            maestro_limpio = {limpiar_texto(k): v for k, v in maestro_asesores.items()}
            
            # Obtener sucursal de cada venta
            suc_45 = df45.iloc[:, 4].apply(limpiar_texto).map(maestro_limpio)
            suc_53 = df53.iloc[:, 0].apply(limpiar_texto).map(maestro_limpio)
            
            reales = pd.concat([suc_45, suc_53]).value_counts().reset_index()
            reales.columns = ['Nombre_Sucursal', 'Total_Ventas']
            reales['KEY'] = reales['Nombre_Sucursal'].apply(limpiar_texto)

            # 2. PROCESAR EXCEL DE METAS
            df_m = pd.read_excel(u_meta)
            # Aseguramos que tenga al menos 6 columnas
            while len(df_m.columns) < 6:
                df_m[f"Col_{len(df_m.columns)}"] = 0
            
            df_m['KEY'] = df_m.iloc[:, 0].apply(limpiar_texto) # Columna A (Sucursal)
            
            # 3. UNIR Y CALCULAR (SOLO FILAS DE SUCURSALES)
            # Primero ponemos a 0 la columna "Logrado" (Columna D / Indice 3)
            df_m.iloc[:, 3] = 0 
            
            for idx, row in df_m.iterrows():
                key = row['KEY']
                if key in reales['KEY'].values:
                    venta = reales.loc[reales['KEY'] == key, 'Total_Ventas'].values[0]
                    df_m.iloc[idx, 3] = venta

            # 4. CALCULAR FILAS DE "TOTAL"
            # Si la columna A contiene "TOTAL", sumamos lo que esté arriba hasta el anterior TOTAL
            total_indices = df_m[df_m.iloc[:, 0].str.contains("TOTAL", na=False, case=False)].index
            inicio = 0
            for fin in total_indices:
                suma_logrado = df_m.iloc[inicio:fin, 3].sum()
                df_m.iloc[fin, 3] = suma_logrado
                inicio = fin + 1

            # 5. RECALCULAR PORCENTAJES (Col E y F / Indice 4 y 5)
            for i in range(len(df_m)):
                logrado = df_m.iloc[i, 3]
                n1 = pd.to_numeric(df_m.iloc[i, 1], errors='coerce') or 1
                n2 = pd.to_numeric(df_m.iloc[i, 2], errors='coerce') or 1
                df_m.iloc[i, 4] = round((logrado / n1 * 100), 1)
                df_m.iloc[i, 5] = round((logrado / n2 * 100), 1)

            # 6. MOSTRAR RESULTADO
            st.write("### ✅ Tabla de Cumplimiento Actualizada")
            # Quitar la columna KEY antes de mostrar
            display_df = df_m.drop(columns=['KEY'])
            
            # Formatear para que parezca el Excel original
            st.dataframe(display_df.style.format({
                display_df.columns[4]: "{:.1f}%",
                display_df.columns[5]: "{:.1f}%"
            }), use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"Se produjo un error: {e}")
