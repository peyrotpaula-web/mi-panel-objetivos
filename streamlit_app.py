import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard Ejecutivo de Ventas", layout="wide")

st.title("📊 Panel de Control Gerencial")

uploaded_file = st.file_uploader("Sube el archivo 'archivo 2.xlsx'", type=["xlsx"])

if uploaded_file:
    try:
        # 1. CARGA Y PROCESAMIENTO
        df = pd.read_excel(uploaded_file)
        df.columns = [str(c).strip() for c in df.columns]
        
        col_obj = df.columns[0]
        col_n1 = df.columns[1]
        col_n2 = df.columns[2]
        col_log = df.columns[3]

        # Lógica para asignar Marcas dinámicamente
        df['Marca'] = None
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

        # Filtrar solo sucursales (quitar filas de TOTAL)
        df_suc = df[~df[col_obj].str.contains("TOTAL", na=False, case=False)].copy()
        df_suc = df_suc.dropna(subset=[col_n1])
        
        # Cálculo de porcentaje sin decimales para visualización
        df_suc['%'] = (df_suc[col_log] / df_suc[col_n1] * 100).round(0).astype(int)

        # 2. TARJETAS DE TOTALES (KPIs)
        t_log = df_suc[col_log].sum()
        t_n1 = df_suc[col_n1].sum()
        t_n2 = df_suc[col_n2].sum()
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Logrado Total", f"{int(t_log)} un.")
        c2.metric("Objetivo N1", f"{int(t_n1)} un.")
        c3.metric("Objetivo N2", f"{int(t_n2)} un.")
        c4.metric("% Global", f"{(t_log/t_n1*100):.0f}%")

        st.divider()

        # 3. GRÁFICOS PRINCIPALES
        col_bar, col_marca = st.columns([2, 1])

        with col_bar:
            st.write("### 🏢 Comparativa: Logrado vs Nivel 1 vs Nivel 2")
            # Agregamos col_n2 a la lista de y
            fig_suc = px.bar(df_suc, x=col_obj, y=[col_log, col_n1, col_n2], 
                             barmode='group',
                             color_discrete_sequence=["#00CC96", "#636EFA", "#AB63FA"],
                             labels={'value': 'Unidades', 'variable': 'Referencia'})
            st.plotly_chart(fig_suc, use_container_width=True)

        with col_marca:
            st.write("### 🏭 Unidades por Marca")
            df_m = df_suc.groupby('Marca')[[col_log, col_n1]].sum().reset_index()
            fig_m = px.bar(df_m, x='Marca', y=col_log, color='Marca', text_auto=True)
            fig_m.update_layout(showlegend=False)
            st.plotly_chart(fig_m, use_container_width=True)

        st.divider()

        # 4. MATRIZ DE RENDIMIENTO (Líderes y Alertas)
        st.write("### 🏆 Matriz de Cumplimiento Nivel 1")
        col_l, col_a = st.columns(2)
        
        with col_l:
            st.success("✨ Líderes de Cumplimiento (>= 80%)")
            # Mostramos el porcentaje como entero
            df_lideres = df_suc[df_suc['%'] >= 80].sort_values('%', ascending=False)[[col_obj, '%']]
            st.table(df_lideres.style.format({"%": "{}%"}))
            
        with col_a:
            st.error("⚠️ Sucursales en Alerta (< 80%)")
            df_alerta = df_suc[df_suc['%'] < 80].sort_values('%')[[col_obj, '%']]
            st.table(df_alerta.style.format({"%": "{}%"}))

        st.divider()

        # 5. TERMÓMETRO Y HEATMAP
        col_ter, col_heat = st.columns([1, 2])

        with col_ter:
            st.write("### 🌡️ Termómetro Grupo")
            progreso_global = (t_log/t_n1*100)
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number", value = progreso_global,
                number = {'suffix': "%", 'valueformat': '.0f'},
                gauge = {'axis': {'range': [0, 120]}, 
                         'bar': {'color': "#323232"},
                         'steps': [{'range': [0, 80], 'color': "#FF4B4B"},
                                   {'range': [80, 100], 'color': "#F9D71C"},
                                   {'range': [100, 120], 'color': "#00CC96"}]}))
            fig_gauge.update_layout(height=300)
            st.plotly_chart(fig_gauge, use_container_width=True)

        with col_heat:
            st.write("### 🚥 Semáforo de Cumplimiento (Heatmap)")
            # Heatmap con valores enteros
            fig_heat = px.imshow([df_suc['%'].values], 
                                 x=df_suc[col_obj], 
                                 labels=dict(color="Cumplimiento %"),
                                 color_continuous_scale="RdYlGn", 
                                 text_auto=True)
            fig_heat.update_xaxes(side="top")
            st.plotly_chart(fig_heat, use_container_width=True)

    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
else:
    st.info("👋 Por favor, sube tu archivo Excel para generar el panel avanzado.")
