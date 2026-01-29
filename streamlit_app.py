import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Sistema Comercial Grupo", layout="wide")

# 2. MENÚ LATERAL DE NAVEGACIÓN
st.sidebar.title("🚀 Menú de Gestión")
pagina = st.sidebar.radio("Seleccione el Panel:", 
                         ["Panel de Objetivos Sucursales", "Ranking de Asesores 🥇"])

st.sidebar.divider()

# =========================================================
# OPCIÓN 1: TU CÓDIGO ORIGINAL DE OBJETIVOS (INTACTO)
# =========================================================
if pagina == "Panel de Objetivos Sucursales":
    COLORES_MARCAS = {
       "PAMPAWAGEN": "#001E50", "FORTECAR": "#102C54", "GRANVILLE": "#FFCE00",
        "CITROEN SN": "#E20613", "OPENCARS": "#00A1DF", "RED SECUNDARIA": "#4B4B4B", "OTRAS": "#999999"
    }

    st.markdown("""
        <style>
        @media print {
            .stButton, .stFileUploader, .stSidebar, header, footer, [data-testid="stToolbar"] { 
                display: none !important; 
            }
            .main .block-container { 
                padding-top: 1rem !important; 
                max-width: 100% !important; 
            }
            .element-container { 
                margin-bottom: 2.5rem !important; 
                page-break-inside: avoid !important; 
            }
            .stPlotlyChart { 
                visibility: visible !important; 
                display: block !important; 
            }
        }
        </style>
        """, unsafe_allow_html=True)

    st.title("📊 Panel de Control de Objetivos Sucursales")

    uploaded_file = st.file_uploader("Sube el archivo Excel de Objetivos", type=["xlsx"], key="obj_key")

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

            df_suc = df[~df[col_obj].str.contains("TOTAL", na=False, case=False)].copy()
            df_suc = df_suc.dropna(subset=[col_n1])
            
            st.sidebar.header("🔍 Filtros de Análisis")
            opciones_marcas = ["GRUPO TOTAL"] + sorted(df_suc['Marca'].unique().tolist())
            marca_sel = st.sidebar.selectbox("Seleccionar Empresa:", opciones_marcas)

            df_final = df_suc if marca_sel == "GRUPO TOTAL" else df_suc[df_suc['Marca'] == marca_sel].copy()
            df_final['%_int'] = (df_final[col_log] / df_final[col_n1] * 100).round(0).astype(int)
            df_final['%_txt'] = df_final['%_int'].astype(str) + "%"
            
            def calc_faltante(logrado, objetivo):
                diff = objetivo - logrado
                return f"{int(diff)} un." if diff > 0 else "✅ Logrado"

            df_final['Faltante N1'] = df_final.apply(lambda x: calc_faltante(x[col_log], x[col_n1]), axis=1)
            df_final['Faltante N2'] = df_final.apply(lambda x: calc_faltante(x[col_log], x[col_n2]), axis=1)

            st.subheader(f"📍 Resumen de Gestión: {marca_sel}")
            t_log, t_n1, t_n2 = df_final[col_log].sum(), df_final[col_n1].sum(), df_final[col_n2].sum()
            cumpl_global = int((t_log/t_n1)*100) if t_n1 > 0 else 0

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Logrado Total", f"{int(t_log)}")
            c2.metric("Objetivo N1", f"{int(t_n1)}")
            c3.metric("Objetivo N2", f"{int(t_n2)}")
            c4.metric("% Global (N1)", f"{cumpl_global}%")

            st.divider()

            st.write("### 🏢 Rendimiento por Sucursal (Unidades)")
            fig_bar = px.bar(df_final, x=col_obj, y=[col_log, col_n1, col_n2], barmode='group',
                             color_discrete_sequence=["#00CC96", "#636EFA", "#AB63FA"], text_auto=True)
            fig_bar.update_traces(textposition='outside')
            fig_bar.update_layout(xaxis_title="Sucursales", yaxis_title="Cantidad de Unidades")
            st.plotly_chart(fig_bar, use_container_width=True, config={'staticPlot': True})

            if marca_sel == "GRUPO TOTAL":
                st.write("### 🏆 Ranking de Cumplimiento por Marca (Objetivo Nivel 1)")
                ranking = df_final.groupby('Marca').agg({col_log: 'sum', col_n1: 'sum'}).reset_index()
                ranking['%'] = (ranking[col_log] / ranking[col_n1] * 100).round(0).astype(int)
                ranking['text_label'] = ranking['%'].astype(str) + "%"
                ranking = ranking.sort_values('%', ascending=True)
                fig_rank = px.bar(ranking, x='%', y='Marca', orientation='h', text='text_label',
                                  color='Marca', color_discrete_map=COLORES_MARCAS)
                fig_rank.update_layout(showlegend=False, xaxis_title="Porcentaje de Cumplimiento (%)")
                st.plotly_chart(fig_rank, use_container_width=True, config={'staticPlot': True})

            st.write("### 🌡️ Avance Global")
            fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=cumpl_global,
                number={'suffix': "%"},
                gauge={'axis': {'range': [0, 120]}, 'bar': {'color': "#323232"},
                       'steps': [{'range': [0, 80], 'color': "#FF4B4B"},
                                 {'range': [80, 100], 'color': "#F9D71C"},
                                 {'range': [100, 120], 'color': "#00CC96"}]}))
            fig_gauge.update_layout(height=350)
            st.plotly_chart(fig_gauge, use_container_width=True, config={'staticPlot': True})

            st.divider()
            st.write("### 🏆 Matriz de Cumplimiento (Faltantes N1 y N2)")
            col_l, col_a = st.columns(2)
            cols_mostrar = [col_obj, '%_txt', 'Faltante N1', 'Faltante N2']
            
            with col_l:
                st.success("✨ Líderes (>= 80%)")
                df_l = df_final[df_final['%_int'] >= 80].sort_values('%_int', ascending=False)[cols_mostrar]
                st.table(df_l.set_index(col_obj))
            with col_a:
                st.error("⚠️ Alerta (< 80%)")
                df_a = df_final[df_final['%_int'] < 80].sort_values('%_int')[cols_mostrar]
                st.table(df_a.set_index(col_obj))

            st.divider()
            st.write("### 🚥 Semáforo de Cumplimiento")
            df_heat = df_final.sort_values('%_int', ascending=False)
            fig_heat = px.imshow([df_heat['%_int'].values], x=df_heat[col_obj],
                                 color_continuous_scale="RdYlGn", text_auto=True)
            fig_heat.update_traces(texttemplate="%{z}%")
            st.plotly_chart(fig_heat, use_container_width=True, config={'staticPlot': True})

            st.write("---")
            if st.button("📄 GENERAR REPORTE PDF COMPLETO"):
                st.components.v1.html("<script>window.parent.print();</script>", height=0)

        except Exception as e:
            st.error(f"Error al procesar: {e}")

# =========================================================
# OPCIÓN 2: RANKING CON LÓGICA ESPECIAL PARA SUCURSAL VIRTUAL
# =========================================================
elif pagina == "Ranking de Asesores 🥇":
    st.title("🏆 Ranking de Asesores Comercial")
    
    # --- MAESTRO DE ASESORES ESTÁNDAR ---
    maestro_asesores = {
        "1115 JORGE ZORRO": "GRANVILLE TRELEW",
        "1114 FACUNDO BOTAZZI": "GRANVILLE CITROEN SAN NICOLAS",
        "1090 FACUNDO BLAIOTTA": "GRANVILLE JUNIN",
        "843 JUAN ANDRES SILVA": "FORTECAR TRENQUE LAUQUEN", 
        "682 TOMAS VILLAMIL SOUBLE": "PAMPAWAGEN SANTA ROSA",
        "980 NAVARRO RAFAEL": "PAMPAWAGEN SANTA ROSA",
        "912 NICOLAS MARCHIORI": "FORTECAR SAN NICOLAS", 
        "467 FABIAN LOSCERTALES": "PAMPAWAGEN GENERAL PICO",
        "45 LAURA CASSANITI": "FORTECAR JUNIN", 
        "1051 MARTIN GALOTTI": "FORTECAR OLAVARRIA",
        "784 GUSTAVO RIVAS": "GRANVILLE TRELEW",
        "899 ELIAS LANGONE": "FORTECAR TRENQUE LAUQUEN",
        "897 CONSTANZA NATTINO": "PAMPAWAGEN GENERAL PICO", 
        "930 NICOLAS SCHNEIDER": "PAMPAWAGEN SANTA ROSA",
        "962 GONZALO EZEQUIEL TORRES": "GRANVILLE COMODORO", 
        "1089 ANGEL AUGUSTO FRANCO": "GRANVILLE TRELEW",
        "1081 GASTON ACTIS": "PAMPAWAGEN SANTA ROSA", 
        "596 MARINO JOAQUIN": "FORTECAR CHIVILCOY",
        "916 MATIAS NICOLAS JACCOUD": "FORTECAR PERGAMINO", 
        "902 AGUSTINA BARRIOS": "FORTECAR OLAVARRIA",
        "1091 NORBERTO ALESSO": "FORTECAR PERGAMINO", 
        "477 CARLOS MANFREDINI": "GRANVILLE SAN NICOLAS",
        "748 HERNAN MAXIMILIANO NOLASCO": "GRANVILLE PERGAMINO", 
        "401 JOSE JUAN": "GRANVILLE JUNIN",
        "409 IGNACIO SOSA": "FORTECAR PERGAMINO", 
        "774 CRISTIAN BRIGNANI": "FORTECAR CHIVILCOY",
        "913 NICOLAS MALDONADO": "FORTECAR SAN NICOLAS", 
        "462 JORGE FERRAIUOLO": "FORTECAR JUNIN", 
        "931 JUAN IGNACIO SORAIZ": "FORTECAR OLAVARRIA",
        "648 VALENTINA DIAZ REBICHINI": "PAMPAWAGEN GENERAL PICO", 
        "977 OLIVIA ZUCARELLI": "OPENCARS JUNIN",
        "1004 JOSE LUIS CIARROCCHI": "FORTECAR JUNIN", 
        "1097 NICOLAS CIALDO": "FORTECAR CHIVILCOY",
        "16 DANILO ROBLEDO": "GRANVILLE PERGAMINO", 
        "1003 JUAN IGNACIO ARCE": "GRANVILLE JUNIN",
        "1048 BRUNO VIGNALE": "OPENCARS JUNIN", 
        "961 FRANCO BRAVO": "FORTECAR OLAVARRIA",
        "751 SANTIAGO CARRERE": "GRANVILLE SAN NICOLAS", 
        "1047 GISELL LLANOS": "GRANVILLE COMODORO",
        "1088 FRANCO VEGA": "GRANVILLE PERGAMINO", 
        "402 CRISTIAN LOPEZ": "FORTECAR JUNIN",
        "1080 CRISTIAN ESCALANTE": "FORTECAR NUEVE DE JULIO", 
        "1021 JUAN ANDRES BRIZUELA": "GRANVILLE COMODORO",
        "458 OSCAR TAVANI": "GRANVILLE SAN NICOLAS", 
        "781 SILVANA CHAMINE": "GRANVILLE MADRYN",
        "1109 JULIETA DOWNES": "FORTECAR SAN NICOLAS",
        "476 POLIZZI PABLO ANDRES": "FORTECAR PERGAMINO", 
        "950 SOFIA DIAMELA FERNANDEZ": "GRANVILLE JUNIN", 
        "1099 GASTON SENOSEAIN": "PAMPAWAGEN SANTA ROSA",
        "1108 FLORENCIA HAESLER": "FORTECAR SAN NICOLAS", 
        "968 RODRIGO JULIAN RIOS": "GRANVILLE MADRYN",
        "974 CIELO QUIROGA": "OPENCARS SAN NICOLAS", 
        "786 RICHARD FORMANTEL ALBORNOZ": "GRANVILLE COMODORO",
        "601 SOSA JUAN CARLOS": "FORTECAR CHIVILCOY", 
        "1104 CELIA FABIANA GONZALEZ": "GRANVILLE CITROEN SAN NICOLAS",
        "1050 MANUEL SORAIZ": "FORTECAR OLAVARRIA", 
        "1100 CAMPODONICO MAGALI": "FORTECAR NUEVE DE JULIO",
        "1112 AGUSTINA AUZA": "GRANVILLE MADRYN", 
        "1111 DAMIAN PARRONDO": "GRANVILLE MADRYN",
        "1101 RODRIGO BACCHIARRI": "GRANVILLE TRELEW",
        "SS SANTIAGO SERVIDIA": "GRANVILLE MADRYN", 
        "41 TOMAS DI NUCCI": "FORTECAR JUNIN",
        "414 CLAUDIO SANCHEZ": "RED SECUNDARIA", 
        "986 RUBEN JORGE LARRIPA": "RED SECUNDARIA",
        "1031 ADRIAN FERNANDO SANCHEZ": "RED SECUNDARIA", 
        "G GERENCIA MARC AS": "GERENCIA"
    }

    # --- LISTA ASESORES VIRTUALES ---
    virtuales = [
        "LEILA BRAVO", "FEDERICO RUBINO", "GERMAN CALVO", 
        "JAZMIN BERAZATEGUI", "LUISANA LEDESMA", "CAMILA GARCIA", 
        "CARLA VALLEJO", "PILAR ALCOBA", "ROCIO FERNANDEZ"
    ]

    c1, c2 = st.columns(2)
    with c1:
        u45 = st.file_uploader("Archivo U45", type=["xlsx", "xls", "csv"], key="u45_v")
    with c2:
        u53 = st.file_uploader("Archivo U53", type=["xlsx", "xls", "csv"], key="u53_v")

    if u45 and u53:
        try:
            def leer_archivo(file):
                if file.name.endswith('.csv'): return pd.read_csv(file)
                return pd.read_excel(file)

            df45_raw = leer_archivo(u45)
            df53_raw = leer_archivo(u53)

            def limpiar(t): return " ".join(str(t).split()).replace(".", "").strip().upper()

            # Columnas U45
            c_v_45 = df45_raw.columns[4] # Vendedor principal
            c_t_45 = next((c for c in df45_raw.columns if "TIPO" in str(c).upper()), "Tipo")
            c_e_45 = next((c for c in df45_raw.columns if "ESTAD" in str(c).upper()), "Estad")
            c_bk_45 = "VENDEDOR COMPARTIDO" # Columna BK
            
            # 1. PROCESAMIENTO ASESORES ESTÁNDAR
            df_std = df45_raw[(df45_raw[c_e_45] != 'A') & (df45_raw[c_t_45] != 'AC')].copy()
            df_std['KEY'] = df_std[c_v_45].apply(limpiar)
            
            res_std = df_std.groupby('KEY').apply(lambda x: pd.Series({
                'VN': (x[c_t_45].isin(['O', 'OP'])).sum(),
                'VO': (x[c_t_45] == 'O2').sum(),
                'ADJ': (x[c_t_45] == 'PL').sum(),
                'VE': (x[c_t_45] == 'VE').sum(),
                'PDA': 0, 'TOMA_VO': 0
            })).reset_index()
            
            # Mapear sucursal y filtrar solo los del maestro estándar
            maestro_limpio = {limpiar(k): v for k, v in maestro_asesores.items()}
            res_std['Sucursal'] = res_std['KEY'].map(maestro_limpio)
            res_std = res_std.dropna(subset=['Sucursal'])

            # 2. PROCESAMIENTO ASESORES VIRTUALES (Lógica BK)
            filas_virtuales = []
            if c_bk_45 in df45_raw.columns:
                df_v = df45_raw[df45_raw[c_e_45] != 'A'].copy() # Solo quito anuladas
                for nombre in virtuales:
                    mask = df_v[c_bk_45].astype(str).str.upper().str.contains(nombre)
                    df_v_n = df_v[mask]
                    filas_virtuales.append({
                        'KEY': nombre,
                        'VN': (df_v_n[c_t_45].isin(['O', 'OP'])).sum(),
                        'VO': (df_v_n[c_t_45] == 'O2').sum(),
                        'ADJ': (df_v_n[c_t_45] == 'PL').sum(),
                        'VE': (df_v_n[c_t_45] == 'VE').sum(),
                        'PDA': 0, 'TOMA_VO': 0,
                        'Sucursal': 'SUCURSAL VIRTUAL'
                    })
            res_virt = pd.DataFrame(filas_virtuales)

            # 3. UNIFICACIÓN PARA EL RANKING
            ranking = pd.concat([res_std, res_virt], ignore_index=True).fillna(0)
            ranking['TOTAL'] = ranking['VN'] + ranking['VO'] + ranking['ADJ'] + ranking['VE']
            ranking = ranking.sort_values(by='TOTAL', ascending=False).reset_index(drop=True)

            # --- CÁLCULO DE TOTALES (SOLO ASESORES ESTÁNDAR) ---
            # Es fundamental filtrar para que los virtuales no sumen al TOTAL GENERAL
            ranking_para_total = ranking[ranking['Sucursal'] != 'SUCURSAL VIRTUAL']
            
            totales = pd.DataFrame({
                'Ranking': [''], 'Asesor': ['TOTAL GENERAL'],
                'VN': [int(ranking_para_total['VN'].sum())],
                'VO': [int(ranking_para_total['VO'].sum())],
                'ADJ': [int(ranking_para_total['ADJ'].sum())],
                'VE': [int(ranking_para_total['VE'].sum())],
                'TOTAL': [int(ranking_para_total['TOTAL'].sum())],
                'TOMA_VO': [0], 'Sucursal': ['']
            })

            # Formateo Final
            ranking.insert(0, 'Rank_Icon', [f"{i+1}°" for i in range(len(ranking))])
            ranking_display = ranking[['Rank_Icon', 'KEY', 'VN', 'VO', 'ADJ', 'VE', 'TOTAL', 'Sucursal']].rename(columns={'Rank_Icon': 'Ranking', 'KEY': 'Asesor'})
            
            # Asegurar enteros
            for c in ['VN', 'VO', 'ADJ', 'VE', 'TOTAL']:
                ranking_display[c] = ranking_display[c].astype(int)

            st.write("### 🏆 Ranking Comercial Oficial")
            st.dataframe(pd.concat([ranking_display, totales], ignore_index=True), use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"Error: {e}")
