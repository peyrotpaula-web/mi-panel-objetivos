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
# OPCIÓN 2: RANKING DE ASESORES (UNIFICADO POR HOJA 1)
# =========================================================
elif pagina == "Ranking de Asesores 🥇":
    st.title("🏆 Ranking de Asesores Comercial")
    
    c1, c2 = st.columns(2)
    with c1:
        u45 = st.file_uploader("Archivo U45 (Ventas)", type=["xlsx", "xls", "csv"], key="u45_key")
    with c2:
        u53 = st.file_uploader("Archivo U53 (Planes)", type=["xlsx", "xls", "csv"], key="u53_key")

    if u45 and u53:
        try:
            # --- FUNCIÓN PARA LEER HOJA 1 ---
            def leer_hoja_1(file):
                if file.name.endswith('.csv'):
                    return pd.read_csv(file)
                # Intenta leer "Hoja 1", si no existe lee la primera pestaña
                xls = pd.ExcelFile(file, engine='xlrd' if file.name.endswith('.xls') else None)
                nombre_hoja = "Hoja 1" if "Hoja 1" in xls.sheet_names else xls.sheet_names[0]
                return xls.parse(nombre_hoja)

            # --- PROCESAR U45 ---
            df45 = leer_hoja_1(u45)
            df45 = df45.loc[:, ~df45.columns.duplicated()]
            
            # Mapeo de columnas U45
            col_vend_45 = df45.columns[4] # Columna E
            col_suc_45 = next((c for c in df45.columns if "CONCESIONARIO" in str(c).upper() or "SUCURSAL" in str(c).upper()), df45.columns[10])
            col_tipo_45 = next((c for c in df45.columns if "TIPO" in str(c).upper()), df45.columns[17])
            col_estad_45 = next((c for c in df45.columns if "ESTAD" in str(c).upper()), df45.columns[18])
            col_tasa_45 = next((c for c in df45.columns if "TAS. VO" in str(c).upper()), None)

            # Filtros U45 y limpieza de nombres
            df45[col_vend_45] = df45[col_vend_45].astype(str).str.strip().str.upper()
            df45 = df45[(df45[col_estad_45] != 'A') & (df45[col_tipo_45] != 'AC')].dropna(subset=[col_vend_45])
            
            # Cálculos U45
            df45['VN'] = df45[col_tipo_45].apply(lambda x: 1 if str(x).upper() in ['O', 'OP'] else 0)
            df45['VO'] = df45[col_tipo_45].apply(lambda x: 1 if str(x).upper() == 'O2' else 0)
            df45['ADJ'] = df45[col_tipo_45].apply(lambda x: 1 if str(x).upper() == 'PL' else 0)
            df45['VE'] = df45[col_tipo_45].apply(lambda x: 1 if str(x).upper() == 'VE' else 0)
            df45['TOMA_VO'] = df45[col_tasa_45].apply(lambda x: 1 if str(x).strip().upper() not in ['0', '0.0', 'NAN', 'NONE', '', '0,0'] else 0) if col_tasa_45 else 0

            # --- PROCESAR U53 ---
            df53 = leer_hoja_1(u53)
            df53 = df53.loc[:, ~df53.columns.duplicated()]
            
            col_vend_53 = "Asesor" if "Asesor" in df53.columns else df53.columns[0] # Columna A
            col_suc_53 = next((c for c in df53.columns if "ORIGEN" in str(c).upper() or "SUCURSAL" in str(c).upper()), df53.columns[3])
            col_est_53 = next((c for c in df53.columns if "ESTADO" in str(c).upper()), None)
            
            # Filtros U53 y limpieza
            df53[col_vend_53] = df53[col_vend_53].astype(str).str.strip().str.upper()
            if col_est_53:
                df53 = df53[df53[col_est_53] != 'AN']

            # --- CONSOLIDACIÓN MAESTRA ---
            # 1. Crear diccionario de Asesor -> Sucursal (priorizando U45 que suele ser más completo)
            dict_sucursales = pd.concat([
                df45[[col_vend_45, col_suc_45]].rename(columns={col_vend_45:'Asesor', col_suc_45:'Sucursal'}),
                df53[[col_vend_53, col_suc_53]].rename(columns={col_vend_53:'Asesor', col_suc_53:'Sucursal'})
            ]).drop_duplicates(subset=['Asesor'], keep='first').set_index('Asesor')['Sucursal'].to_dict()

            # 2. Preparar datos para sumar
            u45_datos = df45[[col_vend_45, 'VN', 'VO', 'ADJ', 'VE', 'TOMA_VO']].rename(columns={col_vend_45:'Asesor'})
            u53_datos = df53[[col_vend_53]].rename(columns={col_vend_53:'Asesor'})
            u53_datos['PDA'] = 1
            
            # 3. Unir y Sumar
            final = pd.concat([u45_datos, u53_datos], sort=False).fillna(0)
            ranking = final.groupby('Asesor').sum().reset_index()
            
            # 4. Reasignar la sucursal única
            ranking['Sucursal'] = ranking['Asesor'].map(dict_sucursales)
            
            # 5. Totales y Medallas
            ranking['TOTAL'] = ranking['VN'] + ranking['VO'] + ranking['PDA'] + ranking['ADJ'] + ranking['VE']
            ranking = ranking.sort_values('TOTAL', ascending=False).reset_index(drop=True)
            ranking.insert(0, 'Ranking', [f"🥇 1°" if i==0 else f"🥈 2°" if i==1 else f"🥉 3°" if i==2 else f"{i+1}°" for i in range(len(ranking))])

            st.write(f"### 🏆 Ranking de Asesores (Consolidado por Sucursal)")
            st.dataframe(ranking[['Ranking', 'Asesor', 'VN', 'VO', 'PDA', 'ADJ', 'VE', 'TOTAL', 'TOMA_VO', 'Sucursal']], 
                         hide_index=True, use_container_width=True)
