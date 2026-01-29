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
# OPCIÓN 2: RANKING PROFESIONAL (FILTRADO ESTRICTO)
# =========================================================
elif pagina == "Ranking de Asesores 🥇":
    st.title("🏆 Ranking de Asesores Comercial")
    
    # Lista de Virtuales
    virtuales = ["LEILA BRAVO", "FEDERICO RUBINO", "GERMAN CALVO", "JAZMIN BERAZATEGUI", 
                 "LUISANA LEDESMA", "CAMILA GARCIA", "CARLA VALLEJO", "PILAR ALCOBA", "ROCIO FERNANDEZ"]

    # Maestro de Asesores Estándar (Nombre: Sucursal)
    maestro_std = {
        "JORGE ZORRO": "GRANVILLE TRELEW", "FACUNDO BOTAZZI": "GRANVILLE CITROEN SAN NICOLAS",
        "FACUNDO BLAIOTTA": "GRANVILLE JUNIN", "JUAN ANDRES SILVA": "FORTECAR TRENQUE LAUQUEN", 
        "TOMAS VILLAMIL SOUBLE": "PAMPAWAGEN SANTA ROSA", "NAVARRO RAFAEL": "PAMPAWAGEN SANTA ROSA",
        "NICOLAS MARCHIORI": "FORTECAR SAN NICOLAS", "FABIAN LOSCERTALES": "PAMPAWAGEN GENERAL PICO",
        "LAURA CASSANITI": "FORTECAR JUNIN", "MARTIN GALOTTI": "FORTECAR OLAVARRIA",
        "GUSTAVO RIVAS": "GRANVILLE TRELEW", "ELIAS LANGONE": "FORTECAR TRENQUE LAUQUEN",
        "CONSTANZA NATTINO": "PAMPAWAGEN GENERAL PICO", "NICOLAS SCHNEIDER": "PAMPAWAGEN SANTA ROSA",
        "GONZALO EZEQUIEL TORRES": "GRANVILLE COMODORO", "ANGEL AUGUSTO FRANCO": "GRANVILLE TRELEW",
        "GASTON ACTIS": "PAMPAWAGEN SANTA ROSA", "MARINO JOAQUIN": "FORTECAR CHIVILCOY",
        "MATIAS NICOLAS JACCOUD": "FORTECAR PERGAMINO", "AGUSTINA BARRIOS": "FORTECAR OLAVARRIA",
        "NORBERTO ALESSO": "FORTECAR PERGAMINO", "CARLOS MANFREDINI": "GRANVILLE SAN NICOLAS",
        "HERNAN MAXIMILIANO NOLASCO": "GRANVILLE PERGAMINO", "JOSE JUAN": "GRANVILLE JUNIN",
        "IGNACIO SOSA": "FORTECAR PERGAMINO", "CRISTIAN BRIGNANI": "FORTECAR CHIVILCOY",
        "NICOLAS MALDONADO": "FORTECAR SAN NICOLAS", "JORGE FERRAIUOLO": "FORTECAR JUNIN", 
        "JUAN IGNACIO SORAIZ": "FORTECAR OLAVARRIA", "VALENTINA DIAZ REBICHINI": "PAMPAWAGEN GENERAL PICO", 
        "OLIVIA ZUCARELLI": "OPENCARS JUNIN", "JOSE LUIS CIARROCCHI": "FORTECAR JUNIN", 
        "NICOLAS CIALDO": "FORTECAR CHIVILCOY", "DANILO ROBLEDO": "GRANVILLE PERGAMINO", 
        "JUAN IGNACIO ARCE": "GRANVILLE JUNIN", "BRUNO VIGNALE": "OPENCARS JUNIN", 
        "FRANCO BRAVO": "FORTECAR OLAVARRIA", "SANTIAGO CARRERE": "GRANVILLE SAN NICOLAS", 
        "GISELL LLANOS": "GRANVILLE COMODORO", "FRANCO VEGA": "GRANVILLE PERGAMINO", 
        "CRISTIAN LOPEZ": "FORTECAR JUNIN", "CRISTIAN ESCALANTE": "FORTECAR NUEVE DE JULIO", 
        "JUAN ANDRES BRIZUELA": "GRANVILLE COMODORO", "OSCAR TAVANI": "GRANVILLE SAN NICOLAS", 
        "SILVANA CHAMINE": "GRANVILLE MADRYN", "JULIETA DOWNES": "FORTECAR SAN NICOLAS",
        "POLIZZI PABLO ANDRES": "FORTECAR PERGAMINO", "SOFIA DIAMELA FERNANDEZ": "GRANVILLE JUNIN", 
        "GASTON SENOSEAIN": "PAMPAWAGEN SANTA ROSA", "FLORENCIA HAESLER": "FORTECAR SAN NICOLAS", 
        "RODRIGO JULIAN RIOS": "GRANVILLE MADRYN", "CIELO QUIROGA": "OPENCARS SAN NICOLAS", 
        "RICHARD FORMANTEL ALBORNOZ": "GRANVILLE COMODORO", "SOSA JUAN CARLOS": "FORTECAR CHIVILCOY", 
        "CELIA FABIANA GONZALEZ": "GRANVILLE CITROEN SAN NICOLAS", "MANUEL SORAIZ": "FORTECAR OLAVARRIA", 
        "CAMPODONICO MAGALI": "FORTECAR NUEVE DE JULIO", "AGUSTINA AUZA": "GRANVILLE MADRYN", 
        "DAMIAN PARRONDO": "GRANVILLE MADRYN", "RODRIGO BACCHIARRI": "GRANVILLE TRELEW",
        "SANTIAGO SERVIDIA": "GRANVILLE MADRYN", "TOMAS DI NUCCI": "FORTECAR JUNIN",
        "CLAUDIO SANCHEZ": "RED SECUNDARIA", "RUBEN JORGE LARRIPA": "RED SECUNDARIA",
        "ADRIAN FERNANDO SANCHEZ": "RED SECUNDARIA", "GERENCIA MARC AS": "GERENCIA"
    }

    c1, c2 = st.columns(2)
    with c1: u45 = st.file_uploader("Subir U45", type=["xlsx","xls"], key="u45_final_fix")
    with c2: u53 = st.file_uploader("Subir U53", type=["xlsx","xls"], key="u53_final_fix")

    if u45 and u53:
        try:
            df45 = pd.read_excel(u45)
            df53 = pd.read_excel(u53)

            def limpiar_txt(t): return str(t).upper().strip()

            # Identificación de columnas
            c_v45 = df45.columns[4]
            c_t45 = next((c for c in df45.columns if "TIPO" in str(c).upper()), "Tipo")
            c_e45 = next((c for c in df45.columns if "ESTAD" in str(c).upper()), "Estad")
            c_vo45 = next((c for c in df45.columns if "TAS. VO" in str(c).upper()), "TAS. VO")
            c_bk = "VENDEDOR COMPARTIDO"

            c_v53_std = df53.columns[0] # Columna A
            c_v53_virt = df53.columns[2] # Columna C (Vendedor PDA para Virtuales)
            c_e53 = next((c for c in df53.columns if "ESTAD" in str(c).upper()), "Estado")

            res_data = []

            # 1. PROCESAR VIRTUALES (Lógica BK y Columna C)
            for v in virtuales:
                # Ventas U45
                m45 = (df45[c_e45] != 'A') & (df45[c_bk].fillna('').apply(limpiar_txt).str.contains(v))
                df_v = df45[m45]
                # PDA U53 (Columna C)
                m53 = (df53[c_e53] != 'AN') & (df53[c_v53_virt].fillna('').apply(limpiar_txt).str.contains(v))
                
                vn, vo = (df_v[c_t45].isin(['O', 'OP'])).sum(), (df_v[c_t45] == 'O2').sum()
                pda, adj, ve = m53.sum(), (df_v[c_t45] == 'PL').sum(), (df_v[c_t45] == 'VE').sum()
                toma = df_v[c_vo45].apply(lambda x: 1 if str(x).strip() not in ['0', '0.0', 'nan', '', '0,0'] else 0).sum()

                if (vn+vo+pda+adj+ve+toma) > 0:
                    res_data.append({'Asesor': v, 'VN': vn, 'VO': vo, 'PDA': pda, 'ADJ': adj, 'VE': ve, 'TOMA_VO': toma, 'Sucursal': 'SUCURSAL VIRTUAL', 'EsVirtual': True})

            # 2. PROCESAR ESTÁNDAR (Filtrado estricto por Maestro)
            for nom, suc in maestro_std.items():
                m45 = (df45[c_e45] != 'A') & (df45[c_t45] != 'AC') & (df45[c_v45].fillna('').apply(limpiar_txt).str.contains(nom))
                df_s = df45[m45]
                m53 = (df53[c_e53] != 'AN') & (df53[c_v53_std].fillna('').apply(limpiar_txt).str.contains(nom))
                
                vn, vo = (df_s[c_t45].isin(['O', 'OP'])).sum(), (df_s[c_t45] == 'O2').sum()
                pda, adj, ve = m53.sum(), (df_s[c_t45] == 'PL').sum(), (df_s[c_t45] == 'VE').sum()
                toma = df_s[c_vo45].apply(lambda x: 1 if str(x).strip() not in ['0', '0.0', 'nan', '', '0,0'] else 0).sum()

                if (vn+vo+pda+adj+ve+toma) > 0:
                    res_data.append({'Asesor': nom, 'VN': vn, 'VO': vo, 'PDA': pda, 'ADJ': adj, 'VE': ve, 'TOMA_VO': toma, 'Sucursal': suc, 'EsVirtual': False})

            ranking = pd.DataFrame(res_data).drop_duplicates(subset=['Asesor'])
            ranking['TOTAL'] = ranking['VN'] + ranking['VO'] + ranking['PDA'] + ranking['ADJ'] + ranking['VE']
            ranking = ranking.sort_values(by=['TOTAL', 'TOMA_VO'], ascending=False).reset_index(drop=True)

            # --- MEDALLAS ---
            def asignar_medalla(i):
                if i == 0: return "🥇 1°"
                if i == 1: return "🥈 2°"
                if i == 2: return "🥉 3°"
                return f"{i+1}°"
            ranking.insert(0, 'Ranking', [asignar_medalla(i) for i in range(len(ranking))])

            # --- TOTALES (Excluyendo Virtuales) ---
            std_f = ranking[ranking['EsVirtual'] == False]
            totales = pd.DataFrame({
                'Ranking': [''], 'Asesor': ['TOTAL GENERAL'], 'VN': [std_f['VN'].sum()], 'VO': [std_f['VO'].sum()],
                'PDA': [std_f['PDA'].sum()], 'ADJ': [std_f['ADJ'].sum()], 'VE': [std_f['VE'].sum()],
                'TOMA_VO': [std_f['TOMA_VO'].sum()], 'TOTAL': [std_f['TOTAL'].sum()], 'Sucursal': ['']
            })

            # Salida final
            col_final = ['Ranking', 'Asesor', 'VN', 'VO', 'PDA', 'ADJ', 'VE', 'TOMA_VO', 'TOTAL', 'Sucursal']
            df_final = pd.concat([ranking[col_final], totales], ignore_index=True).fillna('')
            
            # Limpiar formatos
            for c in ['VN', 'VO', 'PDA', 'ADJ', 'VE', 'TOMA_VO', 'TOTAL']:
                df_final[c] = df_final[c].apply(lambda x: int(x) if x != '' else '')

            st.write("### 🏆 Ranking Comercial Oficial")
            st.dataframe(df_final, use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"Error en el proceso: {e}")
