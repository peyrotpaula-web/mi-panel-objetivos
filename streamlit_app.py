import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(page_title="Dashboard Ejecutivo", layout="wide")

st.title("📊 Panel de Control Gerencial")

uploaded_file = st.file_uploader("Sube el archivo Excel", type=["xlsx"])

if uploaded_file:
    try:
        # 1. PROCESAMIENTO
        df = pd.read_excel(uploaded_file)
        df.columns = [str(c).strip() for c in df.columns]
        col_obj, col_n1, col_n2, col_log = df.columns[0], df.columns[1], df.columns[2], df.columns[3]

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

        df_suc = df[~df[col_obj].str.contains("TOTAL", na=False, case=False)].copy()
        df_suc = df_suc.dropna(subset=[col_n1])
        df_suc['%'] = (df_suc[col_log] / df_suc[col_n1] * 100).round(0).astype(int)

        # 2. KPIs
        t_log, t_n1, t_n2 = df_suc[col_log].sum(), df_suc[col_n1].sum(), df_suc[col_n2].sum()
        cumpl_global = int((t_log/t_n1)*100)

        # 3. BARRA LATERAL - DESCARGAS Y COMPARTIR
        st.sidebar.header("📥 Exportar y Compartir")
        
        # Botón Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_suc[[col_obj, col_log, col_n1, col_n2, '%', 'Marca']].to_excel(writer, index=False)
        st.sidebar.download_button("Descargar Datos (Excel)", data=output.getvalue(), file_name="reporte_ventas.xlsx")

        # Texto para WhatsApp
        st.sidebar.subheader("📱 WhatsApp")
        texto_wsp = f"*REPORTE DIARIO DE VENTAS*\n\n" \
                    f"✅ Logrado: {int(t_log)} un.\n" \
                    f"🎯 Meta N1: {int(t_n1)} un.\n" \
                    f"📊 Cumplimiento: {cumpl_global}%\n\n" \
                    f"*Líderes:* {', '.join(df_suc[df_suc['%'] >= 80][col_obj].tolist()[:3])}"
        st.sidebar.text_area("Copia este texto para WhatsApp:", texto_wsp, height=150)

        # 4. INTERFAZ VISUAL (KPIs)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Logrado Total", f"{int(t_log)}")
        c2.metric("Objetivo N1", f"{int(t_n1)}")
        c3.metric("Objetivo N2", f"{int(t_n2)}")
        c4.metric("% Global", f"{cumpl_global}%")

        st.divider()

        # 5. GRÁFICOS
        col_bar, col_marca = st.columns([2, 1])
        with col_bar:
            st.write("### 🏢 Comparativa General")
            fig_suc = px.bar(df_suc, x=col_obj, y=[col_log, col_n1, col_n2], barmode='group',
                             color_discrete_sequence=["#00CC96", "#636EFA", "#AB63FA"])
            st.plotly_chart(fig_suc, use_container_width=True)

        with col_marca:
            st.write("### 🌡️ Avance Global")
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number", value = cumpl_global,
                number = {'suffix': "%"},
                gauge = {'axis': {'range': [0, 120]}, 'bar': {'color': "#323232"},
                         'steps': [{'range': [0, 80], 'color': "#FF4B4B"},
                                   {'range': [80, 100], 'color': "#F9D71C"},
                                   {'range': [100, 120], 'color': "#00CC96"}]}))
            fig_gauge.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig_gauge, use_container_width=True)

        # 6. MATRIZ TOP/BOTTOM
        st.divider()
        col_l, col_a = st.columns(2)
        with col_l:
            st.success("✨ Líderes (>= 80%)")
            st.table(df_suc[df_suc['%'] >= 80].sort_values('%', ascending=False)[[col_obj, '%']])
        with col_a:
            st.error("⚠️ Alerta (< 80%)")
            st.table(df_suc[df_suc['%'] < 80].sort_values('%')[[col_obj, '%']])

        # 7. HEATMAP
        st.write("### 🚥 Semáforo de Cumplimiento")
        fig_heat = px.imshow([df_suc['%'].values], x=df_suc[col_obj], color_continuous_scale="RdYlGn", text_auto=True)
        st.plotly_chart(fig_heat, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Sube el archivo para activar las funciones de exportación.")
