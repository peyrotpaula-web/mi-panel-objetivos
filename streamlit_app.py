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

# Maestro de Asesores Global (Se mantiene igual)
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

# --- CAMBIO 1: AJUSTE DE ORDEN EN EL FILTRO LATERAL ---
pagina = st.sidebar.radio("Seleccionar Panel:", [
    "Ranking de Asesores 🥇", 
    "Cumplimiento de Objetivos 🎯", 
    "Panel de Objetivos Sucursales"
])

# =========================================================
# OPCIÓN 1: RANKING
# =========================================================
if pagina == "Ranking de Asesores 🥇":
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

            if not filtro_sucursal and not filtro_asesor:
                st.write("## 🎖️ Cuadro de Honor")
                podio_cols = st.columns(3); meds, cols_p = ["🥇", "🥈", "🥉"], ["#FFD700", "#C0C0C0", "#CD7F32"]
                for i in range(min(3, len(ranking))):
                    asesor = ranking.iloc[i]
                    with podio_cols[i]:
                        st.markdown(f'<div style="text-align: center; border: 2px solid {cols_p[i]}; border-radius: 15px; padding: 15px; background-color: #f9f9f9;"><h1 style="margin: 0;">{meds[i]}</h1><p style="font-weight: bold; margin: 5px 0;">{asesor["KEY"]}</p><h2 style="color: #1f77b4; margin: 0;">{asesor["TOTAL"]} <small>u.</small></h2><span style="font-size: 0.8em; color: gray;">{asesor["Sucursal"]}</span></div>', unsafe_allow_html=True)
                st.divider()

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
            
            df_v = ranking[ranking['Sucursal'] != "SUCURSAL VIRTUAL"]
            totales = pd.DataFrame({'Rank': ['-'], 'Asesor': ['TOTAL'], 'VN': [df_v['VN'].sum()], 'VO': [df_v['VO'].sum()], 'PDA': [df_v['PDA'].sum()], 'ADJ': [df_v['ADJ'].sum()], 'VE': [df_v['VE'].sum()], 'TOTAL': [df_v['TOTAL'].sum()], 'TOMA_VO': [df_v['TOMA_VO'].sum()], 'Sucursal': ['-']})
            st.table(totales.set_index('Asesor').style.set_properties(**{'text-align': 'center'}))

            df_csv = pd.concat([final_display, totales]).fillna("")
            st.download_button(label="📥 Descargar Ranking CSV", data=df_csv.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig'), file_name='ranking_comercial.csv', mime='text/csv')

        except Exception as e: st.error(f"Error: {e}")

# =========================================================
# OPCIÓN 2: CUMPLIMIENTO
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
                suc_excel = limpiar_texto(row[cols[0]])
                if "TOTAL" in suc_excel: continue
                for s_mem, val in ventas_reales.items():
                    s_mem_limpia = limpiar_texto(s_mem)
                    if s_mem_limpia in suc_excel or suc_excel in s_mem_limpia:
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
            df_m["Faltante N1"] = (df_m[cols[1]] - df_m[cols[3]]).apply(lambda x: x if x > 0 else 0)
            df_m["Faltante N2"] = (df_m[cols[2]] - df_m[cols[3]]).apply(lambda x: x if x > 0 else 0)

            def resaltar_totales(row):
                if "TOTAL" in str(row[cols[0]]).upper():
                    return ['font-weight: bold; background-color: #f0f2f6'] * len(row)
                return [''] * len(row)

            def semaforo_fuente(val):
                if val >= 1.0: color = '#28a745'
                elif val >= 0.8: color = '#fd7e14'
                else: color = '#dc3545'
                return f'color: {color}; font-weight: bold; text-align: center'

            st.write("### ✅ Resumen de Cumplimiento")
            df_final = df_m[[cols[0], cols[1], cols[2], cols[3], col_pct_n1, col_pct_n2, "Faltante N1", "Faltante N2"]]
            
            estilo_df = df_final.style.apply(resaltar_totales, axis=1) \
                .map(semaforo_fuente, subset=[col_pct_n1, col_pct_n2]) \
                .format({
                    cols[1]: "{:,.0f}", cols[2]: "{:,.0f}", cols[3]: "{:,.0f}",
                    col_pct_n1: "{:.1%}", col_pct_n2: "{:.1%}",
                    "Faltante N1": "{:,.0f}", "Faltante N2": "{:,.0f}"
                })

            # --- CAMBIO 2: AJUSTE DE ALTURA PARA ELIMINAR DOBLE BARRA ---
            # Se agrega 'height' para que el contenedor sea lo suficientemente grande y no cree scroll interno
            st.dataframe(estilo_df, use_container_width=True, hide_index=True, height=(len(df_final) + 1) * 36)
            
        except Exception as e: st.error(f"Error: {e}")

# =========================================================
# OPCIÓN 3: PANEL DE OBJETIVOS SUCURSALES (DINÁMICO)
# =========================================================
elif pagina == "Panel de Objetivos Sucursales":
    st.title("📊 Panel de Control de Objetivos Sucursales")
    
    # 1. Recuperar datos procesados del Panel 2
    # Buscamos en el estado de la sesión si ya existe el DataFrame procesado
    # Para que esto funcione, en el Panel 2 deberías guardar: st.session_state['df_cumplimiento_final'] = df_m
    
    if 'ventas_sucursal_memoria' not in st.session_state:
        st.warning("⚠️ No hay datos de ventas. Por favor, carga los archivos en el panel 'Ranking de Asesores'.")
        st.stop()

    # Nota: Para máxima precisión, este panel requiere que el archivo de objetivos 
    # ya haya sido cargado y procesado en la pestaña "Cumplimiento de Objetivos".
    # Intentamos obtener df_m (el cuadro del panel 2)
    
    # Si no quieres navegar al panel 2 para que cargue, podemos disparar la lectura aquí si el archivo está presente
    f_meta = st.file_uploader("Sube el archivo de Objetivos para alimentar este panel", type=["xlsx"], key="panel3_uploader")
    
    if f_meta:
        try:
            # --- PROCESAMIENTO IGUAL AL PANEL 2 ---
            df_m = pd.read_excel(f_meta)
            df_m.columns = [str(c).strip() for c in df_m.columns]
            cols = df_m.columns # 0:Sucursal, 1:N1, 2:N2, 3:Logrado
            
            # Limpieza y cruce (reutilizando tu lógica del Panel 2)
            ventas_reales = st.session_state.get('ventas_sucursal_memoria', {})
            df_m[cols[3]] = 0
            for idx, row in df_m.iterrows():
                suc_excel = limpiar_texto(row[cols[0]])
                if "TOTAL" in suc_excel: continue
                for s_mem, val in ventas_reales.items():
                    if limpiar_texto(s_mem) in suc_excel or suc_excel in limpiar_texto(s_mem):
                        df_m.at[idx, cols[3]] = val

            # Cálculos de Totales por Marca
            marcas_lista = ["OPENCARS", "PAMPAWAGEN", "GRANVILLE", "FORTECAR"]
            inicio = 0
            for idx, row in df_m.iterrows():
                nombre_fila = str(row[cols[0]]).upper()
                if "TOTAL" in nombre_fila and any(m in nombre_fila for m in marcas_lista):
                    df_m.at[idx, cols[3]] = df_m.iloc[inicio:idx, 3].sum()
                    inicio = idx + 1

            # --- CÁLCULOS ESPECÍFICOS PARA LOS GRÁFICOS ---
            # Filtrar solo sucursales (quitar totales para las barras)
            df_sucursales = df_m[~df_m[cols[0]].str.contains("TOTAL", case=False, na=False)].copy()
            df_sucursales["% N1"] = (df_sucursales[cols[3]] / df_sucursales[cols[1]]).fillna(0)
            df_sucursales["% N2"] = (df_sucursales[cols[3]] / df_sucursales[cols[2]]).fillna(0)
            
            # Datos Globales (del Total General)
            total_gen_row = df_m[df_m[cols[0]].str.contains("TOTAL GENERAL", case=False, na=False)]
            if not total_gen_row.empty:
                log_tot = total_gen_row[cols[3]].values[0] [cite: 4, 113]
                obj_n1 = total_gen_row[cols[1]].values[0] [cite: 5]
                obj_n2 = total_gen_row[cols[2]].values[0] [cite: 7, 9]
                pct_n1 = (log_tot / obj_n1) if obj_n1 > 0 else 0 [cite: 10]
                pct_n2 = (log_tot / obj_n2) if obj_n2 > 0 else 0

            # ---------------------------------------------------------
            # 1. TARJETAS (5 Unidades)
            # ---------------------------------------------------------
            st.subheader("Resumen de Gestión: GRUPO TOTAL") [cite: 2]
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Logrado Total", f"{log_tot}") [cite: 3, 4]
            c2.metric("Objetivo N1", f"{obj_n1}") [cite: 5]
            c3.metric("Objetivo N2", f"{obj_n2}") [cite: 7, 9]
            c4.metric("% Global (N1)", f"{pct_n1:.0%}") [cite: 8, 10]
            c5.metric("% Global (N2)", f"{pct_n2:.0%}")

            st.divider()

            # ---------------------------------------------------------
            # 2. RENDIMIENTO POR SUCURSAL (Barras Agrupadas)
            # ---------------------------------------------------------
            st.subheader("Rendimiento por Sucursal") [cite: 6]
            fig_rend = px.bar(df_sucursales, x=cols[0], y=[cols[3], cols[1], cols[2]],
                             barmode='group',
                             labels={'value': 'Unidades', 'variable': 'Tipo'},
                             color_discrete_map={cols[3]: '#00CC96', cols[1]: '#636EFA', cols[2]: '#AB63FA'}) [cite: 15, 16, 18]
            st.plotly_chart(fig_rend, use_container_width=True)

            # ---------------------------------------------------------
            # 3. RANKING POR MARCA Y TERMÓMETRO
            # ---------------------------------------------------------
            col_rank, col_termo = st.columns([2, 1])
            
            with col_rank:
                st.subheader("Ranking de Cumplimiento por Marca (Obj N1)") [cite: 82]
                df_marcas = df_m[df_m[cols[0]].str.contains("TOTAL", case=False) & 
                                 ~df_m[cols[0]].str.contains("GENERAL", case=False)].copy()
                df_marcas["%"] = (df_marcas[cols[3]] / df_marcas[cols[1]] * 100) [cite: 90, 91, 92, 93, 94, 106]
                df_marcas = df_marcas.sort_values("%", ascending=True)
                
                fig_marca = px.bar(df_marcas, x="%", y=cols[0], orientation='h', 
                                  text=df_marcas["%"].apply(lambda x: f'{x:.0f}%')) [cite: 104]
                st.plotly_chart(fig_marca, use_container_width=True)

            with col_termo:
                st.subheader("Avance Global") [cite: 105]
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = pct_n1 * 100,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    gauge = {
                        'axis': {'range': [0, 120]},
                        'bar': {'color': "black"},
                        'steps': [
                            {'range': [0, 80], 'color': "#ff4b4b"},
                            {'range': [80, 90], 'color': "#ffa500"},
                            {'range': [90, 120], 'color': "#00CC96"}]
                    })) [cite: 108, 109, 110, 112, 113, 115]
                st.plotly_chart(fig_gauge, use_container_width=True)

            # ---------------------------------------------------------
            # 4. MATRIZ DE CUMPLIMIENTO (REGLA 90%)
            # ---------------------------------------------------------
            st.subheader("Matriz de Cumplimiento (Faltantes N1 y N2)") [cite: 116]
            
            # Líderes >= 90%
            lideres = df_sucursales[df_sucursales["% N1"] >= 0.9].copy() [cite: 117]
            # Alerta < 90%
            alerta = df_sucursales[df_sucursales["% N1"] < 0.9].copy() [cite: 118]
            
            m1, m2 = st.columns(2)
            with m1:
                st.success("🟢 Líderes (>= 90%)") [cite: 117]
                st.dataframe(lideres[[cols[0], "% N1", "Faltante N1", "Faltante N2"]].style.format({"% N1": "{:.0%}"}), hide_index=True) [cite: 119]
            with m2:
                st.error("🔴 Alerta (< 90%)") [cite: 118]
                st.dataframe(alerta[[cols[0], "% N1", "Faltante N1", "Faltante N2"]].style.format({"% N1": "{:.0%}"}), hide_index=True) [cite: 119]

            # ---------------------------------------------------------
            # 5. SEMÁFORO DE CUMPLIMIENTO
            # ---------------------------------------------------------
            st.subheader("Semáforo de Cumplimiento") [cite: 120]
            df_semaforo = df_sucursales.sort_values("% N1", ascending=False)
            
            fig_heat = px.imshow([df_semaforo["% N1"] * 100],
                                x=df_semaforo[cols[0]],
                                color_continuous_scale='RdYlGn',
                                aspect="auto",
                                text_auto=".0f") [cite: 123, 124, 125, 126, 127]
            st.plotly_chart(fig_heat, use_container_width=True)

        except Exception as e:
            st.error(f"Error procesando el panel dinámico: {e}")
