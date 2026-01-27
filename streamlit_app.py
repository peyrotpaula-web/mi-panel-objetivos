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
# OPCIÓN 2: RANKING DE ASESORES (LÓGICA E Y A)
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
            # --- PROCESAR U45 (Vendedor en Columna E) ---
            if u45.name.endswith('.csv'):
                df45 = pd.read_csv(u45)
            else:
                df45 = pd.read_excel(u45, engine='xlrd' if u45.name.endswith('.xls') else None)
            
            df45 = df45.loc[:, ~df45.columns.duplicated()]
            
            # Forzamos la identificación de columnas del U45
            # Columna E es el índice 4 (0=A, 1=B, 2=C, 3=D, 4=E)
            col_vend_45 = df45.columns[4] 
            col_tipo_45 = next((c for c in df45.columns if "Tipo" in str(c) or "TIPO" in str(c)), df45.columns[17])
            col_estad_45 = next((c for c in df45.columns if "Estad" in str(c) or "ESTAD" in str(c)), df45.columns[18])
            col_suc_45 = next((c for c in df45.columns if "Nombre concesionario" in str(c) or "CONCESIONARIO" in str(c)), df45.columns[10])
            col_tasa_45 = next((c for c in df45.columns if "TAS. VO" in str(c).upper()), None)

            # Filtros U45
            df45 = df45[(df45[col_estad_45] != 'A') & (df45[col_tipo_45] != 'AC')].dropna(subset=[col_vend_45])
            
            # Conteos U45
            df45['VN'] = df45[col_tipo_45].apply(lambda x: 1 if str(x).upper() in ['O', 'OP'] else 0)
            df45['VO'] = df45[col_tipo_45].apply(lambda x: 1 if str(x).upper() == 'O2' else 0)
            df45['ADJ'] = df45[col_tipo_45].apply(lambda x: 1 if str(x).upper() == 'PL' else 0)
            df45['VE'] = df45[col_tipo_45].apply(lambda x: 1 if str(x).upper() == 'VE' else 0)
            df45['TOMA_VO'] = df45[col_tasa_45].apply(lambda x: 1 if str(x).strip() not in ['0', '0.0', 'nan', 'None', '', '0,0'] else 0) if col_tasa_45 else 0
            
            # --- PROCESAR U53 (Asesor en Columna A) ---
            if u53.name.endswith('.csv'):
                df53 = pd.read_csv(u53)
            else:
                df53 = pd.read_excel(u53, engine='xlrd' if u53.name.endswith('.xls') else None)
            
            df53 = df53.loc[:, ~df53.columns.duplicated()]
            
            # Columna A es el índice 0
            col_vend_53 = "Asesor" if "Asesor" in df53.columns else df53.columns[0]
            col_suc_53 = next((c for c in df53.columns if "Origen" in str(c) or "ORIGEN" in str(c)), df53.columns[3])
            col_est_53 = next((c for c in df53.columns if "Estado" in str(c) or "ESTADO" in str(c)), None)
            
            if col_est_53:
                df53 = df53[df53[col_est_53] != 'AN']
            df53 = df53.dropna(subset=[col_vend_53])

            # --- CONSOLIDAR ---
            # Normalizamos nombres a 'Asesor Final'
            u45_final = df45[[col_vend_45, col_suc_45, 'VN', 'VO', 'ADJ', 'VE', 'TOMA_VO']].rename(columns={col_vend_45:'Asesor_Final', col_suc_45:'Sucursal'})
            u53_final = df53[[col_vend_53, col_suc_53]].rename(columns={col_vend_53:'Asesor_Final', col_suc_53:'Sucursal'})
            u53_final['PDA'] = 1
            
            consolidado = pd.concat([u45_final, u53_final], sort=False).fillna(0)
            
            # Agrupar
            ranking = consolidado.groupby(['Asesor_Final', 'Sucursal']).sum().reset_index()
            ranking['TOTAL'] = ranking['VN'] + ranking['VO'] + ranking['PDA'] + ranking['ADJ'] + ranking['VE']
            ranking = ranking.sort_values('TOTAL', ascending=False).reset_index(drop=True)
            
            # Medallas
            ranking.insert(0, 'Ranking', [f"🥇 1°" if i==0 else f"🥈 2°" if i==1 else f"🥉 3°" if i==2 else f"{i+1}°" for i in range(len(ranking))])
            
            # Renombrar para mostrar
            resultado_ver = ranking.rename(columns={'Asesor_Final': 'Asesor'})
            
            st.write(f"### 🏆 Ranking de Asesores")
            st.dataframe(resultado_ver[['Ranking', 'Asesor', 'VN', 'VO', 'PDA', 'ADJ', 'VE', 'TOTAL', 'TOMA_VO', 'Sucursal']], 
                         hide_index=True, use_container_width=True)

        except Exception as e:
            st.error(f"Error procesando los archivos: {e}")
            st.info("Revisa que el U45 tenga al Vendedor en la columna E y el U53 al Asesor en la columna A.")
