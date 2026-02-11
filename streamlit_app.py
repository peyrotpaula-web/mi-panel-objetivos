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
# OPCIÓN 2: RANKING CON ASESORES VIRTUALES (SIN SUMAR TOTAL)
# =========================================================
elif pagina == "Ranking de Asesores 🥇":
    st.title("🏆 Ranking de Asesores Comercial")
    
    # 1. Lista de Asesores Virtuales para validación
    asesores_virtuales = [
        "FEDERICO RUBINO", "GERMAN CALVO", "JAZMIN BERAZATEGUI", 
        "LUISANA LEDESMA", "CAMILA GARCIA", "CARLA VALLEJO", 
        "PILAR ALCOBA", "ROCIO FERNANDEZ"
    ]

    # Maestro extendido (incluimos los virtuales para que el mapeo de sucursal funcione)
    maestro_asesores.update({v: "SUCURSAL VIRTUAL" for v in asesores_virtuales})

    c1, c2 = st.columns(2)
    with c1: u45 = st.file_uploader("Archivo U45", type=["xlsx", "xls", "csv"], key="u45_v3")
    with c2: u53 = st.file_uploader("Archivo U53", type=["xlsx", "xls", "csv"], key="u53_v3")

    if u45 and u53:
        try:
            def leer_archivo(file):
                if file.name.endswith('.csv'): return pd.read_csv(file)
                return pd.read_excel(file, engine='xlrd' if file.name.endswith('.xls') else None)

            df45_raw = leer_archivo(u45)
            df53_raw = leer_archivo(u53)

            def limpiar_texto(t):
                return " ".join(str(t).split()).replace(".", "").strip().upper()

            # --- A. PROCESAMIENTO ASESORES ESTÁNDAR ---
            c_v_45 = df45_raw.columns[4] # Columna E (Asesor estándar)
            c_t_45 = df45_raw.columns[17] # Columna R (Tipo)
            c_e_45 = next((c for c in df45_raw.columns if "ESTAD" in str(c).upper()), "Estad")
            c_vo_45 = next((c for c in df45_raw.columns if "TAS. VO" in str(c).upper()), None)
            
            df45_std = df45_raw[(df45_raw[c_e_45] != 'A') & (df45_raw[c_t_45] != 'AC')].copy()
            df45_std['KEY'] = df45_std[c_v_45].apply(limpiar_texto)
            
            u45_std_sum = df45_std.groupby('KEY').apply(lambda x: pd.Series({
                'VN': int((x[c_t_45].isin(['O', 'OP'])).sum()),
                'VO': int((x[c_t_45].isin(['O2','O2R'])).sum()),
                'ADJ': int((x[c_t_45] == 'PL').sum()),
                'VE': int((x[c_t_45] == 'VE').sum()),
                'TOMA_VO': int(x[c_vo_45].apply(lambda v: 1 if str(v).strip() not in ['0', '0.0', 'nan', 'None', '', '0,0'] else 0).sum()) if c_vo_45 else 0
            })).reset_index()

            # --- B. NUEVA PARTE: PROCESAMIENTO ASESORES VIRTUALES ---
            # En U45 buscar en Columna BK (Vendedor Compartido - índice 62 aprox, mejor por nombre)
            c_compartido = df45_raw.columns[62] # Columna BK
            
            df45_virt = df45_raw[(df45_raw[c_e_45] != 'A') & (df45_raw[c_t_45] != 'AC')].copy()
            df45_virt['KEY'] = df45_virt[c_compartido].apply(limpiar_texto)
            # Filtrar solo si el nombre está en nuestra lista de virtuales
            df45_virt = df45_virt[df45_virt['KEY'].isin(asesores_virtuales)]

            u45_virt_sum = df45_virt.groupby('KEY').apply(lambda x: pd.Series({
                'VN': int((x[c_t_45].isin(['O', 'OP'])).sum()),
                'VO': int((x[c_t_45].isin(['O2','O2R'])).sum()),
                'ADJ': int((x[c_t_45] == 'PL').sum()),
                'VE': int((x[c_t_45] == 'VE').sum()),
                'TOMA_VO': 0 # Virtuales no suelen tomar usados según consigna
            })).reset_index()

            # En U53 buscar en Columna D (Origen - índice 3)
            c_origen_53 = df53_raw.columns[3]
            df53_all = df53_raw.copy()
            
            # PDA Estándar (Columna A)
            df53_all['KEY_STD'] = df53_all[df53_raw.columns[0]].apply(limpiar_texto)
            u53_std = df53_all.groupby('KEY_STD').size().reset_index(name='PDA')
            u53_std.rename(columns={'KEY_STD': 'KEY'}, inplace=True)

            # PDA Virtuales (Columna D)
            df53_all['KEY_VIRT'] = df53_all[c_origen_53].apply(limpiar_texto)
            u53_virt = df53_all[df53_all['KEY_VIRT'].isin(asesores_virtuales)].groupby('KEY_VIRT').size().reset_index(name='PDA')
            u53_virt.rename(columns={'KEY_VIRT': 'KEY'}, inplace=True)

            # --- C. UNIFICACIÓN ---
            # Combinamos std y virtuales (evitando duplicados de nombres si un virtual apareciera en columna E)
            df_final_std = pd.merge(u45_std_sum, u53_std, on='KEY', how='outer').fillna(0)
            df_final_virt = pd.merge(u45_virt_sum, u53_virt, on='KEY', how='outer').fillna(0)
            
            # Marcamos quién es quién antes de concatenar
            df_final_std['Es_Virtual'] = False
            df_final_virt['Es_Virtual'] = True
            
            ranking = pd.concat([df_final_std, df_final_virt], ignore_index=True)
            
            # Mapeo de sucursal
            maestro_limpio = {limpiar_texto(k): v for k, v in maestro_asesores.items()}
            ranking['Sucursal'] = ranking['KEY'].map(maestro_limpio)
            ranking = ranking.dropna(subset=['Sucursal']).copy()

            # --- D. LÓGICA DE TOTALES Y PRIORIDADES ---
            for c in ['VN', 'VO', 'PDA', 'ADJ', 'VE', 'TOMA_VO']:
                ranking[c] = ranking[c].astype(int)

            # IMPORTANTE: El total solo suma si NO es virtual
            ranking['TOTAL'] = ranking.apply(
                lambda x: (x['VN'] + x['VO'] + x['ADJ'] + x['VE'] + x['PDA']) if not x['Es_Virtual'] else 0, 
                axis=1
            )
            
            # Para que los virtuales no queden con "0" absoluto en la tabla, creamos una visual de total
            ranking['Total_Visible'] = ranking['VN'] + ranking['VO'] + ranking['ADJ'] + ranking['VE'] + ranking['PDA']

            # Prioridades de orden: 0: Estándar, 1: Virtual, 2: Red Secundaria
            def asignar_prioridad(row):
                if row['Sucursal'] == "RED SECUNDARIA": return 2
                if row['Es_Virtual']: return 1
                return 0

            ranking['Prioridad'] = ranking.apply(asignar_prioridad, axis=1)
            
            # Ordenamos: Prioridad asc, y luego por Total Real (o Visible para virtuales)
            ranking = ranking.sort_values(
                by=['Prioridad', 'TOTAL', 'Total_Visible', 'TOMA_VO'], 
                ascending=[True, False, False, False]
            ).reset_index(drop=True)

            # --- E. VISUALIZACIÓN ---
            # Podio (solo para presenciales)
            st.write("## 🎖️ Cuadro de Honor")
            podio_cols = st.columns(3)
            for i in range(3):
                if i < len(ranking) and ranking.iloc[i]['Prioridad'] == 0:
                    asesor = ranking.iloc[i]
                    with podio_cols[i]:
                        st.metric(label=f"{i+1}° - {asesor['KEY']}", value=f"{asesor['TOTAL']} u.", help=asesor['Sucursal'])

            st.divider()

            # Tabla Final
            icons = [f"🥇 1°" if i==0 else f"🥈 2°" if i==1 else f"🥉 3°" if i==2 else f"{i+1}°" for i in range(len(ranking))]
            ranking.insert(0, 'Rank', icons)

            # Fila de Totales Generales
            # Aquí sumamos solo lo que tiene 'TOTAL' > 0 (los presenciales)
            totales = pd.DataFrame({
                'Rank': [''], 'KEY': ['TOTAL GENERAL'],
                'VN': [ranking['VN'].sum()], 'VO': [ranking['VO'].sum()],
                'PDA': [ranking['PDA'].sum()], 'ADJ': [ranking['ADJ'].sum()],
                'VE': [ranking['VE'].sum()], 'TOTAL': [ranking['TOTAL'].sum()],
                'TOMA_VO': [ranking['TOMA_VO'].sum()], 'Sucursal': ['']
            })

            # Preparamos tabla para mostrar (usamos Total_Visible para que se vea cuánto vendió el virtual)
            ranking_display = ranking[['Rank', 'KEY', 'VN', 'VO', 'PDA', 'ADJ', 'VE', 'Total_Visible', 'TOMA_VO', 'Sucursal']].rename(
                columns={'KEY': 'Asesor', 'Total_Visible': 'Unidades'}
            )
            
            # Ajustamos el nombre de la columna en totales para que coincida en el concat
            totales_display = totales.rename(columns={'TOTAL': 'Unidades'})

            st.write("### 📊 Ranking Comercial Detallado")
            st.info("Nota: Los asesores de 'SUCURSAL VIRTUAL' se muestran en el ranking pero sus unidades no se contabilizan en el Total General.")
            st.dataframe(pd.concat([ranking_display, totales_display], ignore_index=True), use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"Error detallado: {e}")
