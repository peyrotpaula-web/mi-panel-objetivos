import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard Estratégico de Ventas", layout="wide")

st.title("📊 Monitor Estratégico: Análisis de Brechas y Rendimiento")

uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

if uploaded_file:
    try:
        # 1. Carga y Limpieza
        df = pd.read_excel(uploaded_file)
        df.columns = [str(c).strip() for c in df.columns]
        
        col_obj = df.columns[0]
        col_n1 = df.columns[1]
        col_n2 = df.columns[2]
        col_log = df.columns[3]

        # 2. Asignación de Marcas Ampliada
        df['Marca'] = None
        marca_actual = "Otras"
        
        for i, row in df.iterrows():
            texto = str(row[col_obj]).upper()
            if "OPENCARS" in texto: marca_actual = "OPENCARS"
            elif "PAMPAWAGEN" in texto: marca_actual = "PAMPAWAGEN"
            elif "FORTECAR" in texto: marca_actual = "FORTECAR"
            elif "GRANVILLE" in texto: marca_actual = "GRANVILLE"
            elif "CITROEN" in texto: marca_actual = "CITROEN"
            elif "PEUGEOT" in texto: marca_actual = "PEUGEOT"
            elif "RED" in texto: marca_actual = "RED"
            df.at[i, 'Marca'] = marca_actual

        # 3. Filtrado de Sucursales
        df_suc = df[~df[col_obj].str.contains("TOTAL", na=False, case=False)].copy()
        df_suc = df_suc.dropna(subset=[col_n1])
        df_suc['%_Cumplimiento'] = (df_suc[col_log] / df_suc[col_n1] * 100).round(1)
        df_suc['Gap_N1'] = df_suc[col_n1] - df_suc[col_log]

        # 4. Sidebar y Filtros
        st.sidebar.header("Análisis por Marca")
        marcas = ["TODAS"] + sorted(df_suc['Marca'].unique().tolist())
        sel_marca = st.sidebar.selectbox("Seleccionar Marca:", marcas)

        df_final = df_suc if sel_marca == "TODAS" else df_suc[df_suc['Marca'] == sel_marca]

        # 5. KPIs Principales
        t_log = df_final[col_log].sum()
        t_n1 = df_final[col_n1].sum()
        cumpl_total = (t_log / t_n1 * 100) if t_n1 > 0 else 0

        c1, c2, c3 = st.columns(3)
        c1.metric("Ventas Totales", f"{int(t_log)} un.")
        c2.metric("Meta Nivel 1", f"{int(t_n1)} un.")
        c3.metric("% Cumplimiento Marca", f"{cumpl_total:.1f}%")

        st.divider()

        # 6. ANÁLISIS DE DISPERSIÓN (Scatter Plot)
        st.subheader("🎯 Dispersión: Objetivo vs. Logrado")
        fig_disp = px.scatter(df_final, x=col_n1, y=col_log, text=col_obj, 
                             size=col_log, color='%_Cumplimiento',
                             labels={col_n1: 'Objetivo Nivel 1', col_log: 'Logrado Real'},
                             color_continuous_scale="RdYlGn",
                             title="Posicionamiento de Sucursales")
        st.plotly_chart(fig_disp, use_container_width=True)

        # 7. MATRIZ TOP VS BOTTOM Y GAP CHART
        col_mat, col_gap = st.columns(2)

        with col_mat:
            st.write("### 🏆 Matriz Top vs Bottom (Rendimiento)")
            df_sorted = df_final.sort_values('%_Cumplimiento', ascending=False)
            top_3 = df_sorted.head(3)[[col_obj, '%_Cumplimiento']]
            bottom_3 = df_sorted.tail(3)[[col_obj, '%_Cumplimiento']]
            
            st.success("**Top 3 Sucursales**")
            st.table(top_3)
            st.error("**Bottom 3 Sucursales**")
            st.table(bottom_3)

        with col_gap:
            st.write("### 📉 Brecha (Gap) para alcanzar Nivel 1")
            # Bullet chart simplificado con barras
            fig_gap = px.bar(df_final.sort_values('Gap_N1', ascending=True), 
                            x='Gap_N1', y=col_obj, 
                            orientation='h',
                            title="Unidades faltantes para Nivel 1",
                            color_discrete_sequence=['#FF4B4B'])
            st.plotly_chart(fig_gap, use_container_width=True)

        # 8. ANÁLISIS COMPARATIVO ENTRE MARCAS (Solo si selecciona TODAS)
        if sel_marca == "TODAS":
            st.divider()
            st.subheader("📊 Comparativo Inter-Marcas")
            df_marcas = df_suc.groupby('Marca').agg({col_log:'sum', col_n1:'sum'}).reset_index()
            df_marcas['%'] = (df_marcas[col_log] / df_marcas[col_n1] * 100).round(1)
            
            fig_marcas = px.bar(df_marcas, x='Marca', y='%', color='Marca',
                               text='%', title="% Cumplimiento por Empresa")
            st.plotly_chart(fig_marcas, use_container_width=True)

    except Exception as e:
        st.error(f"Error en los datos: {e}")
else:
    st.info("👋 Esperando el archivo 'archivo 2.xlsx' para iniciar el análisis profundo.")
