  import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Profesional", layout="wide")

st.title("📊 Monitor de Objetivos Dinámico")

uploaded_file = st.file_uploader("Sube el archivo 'archivo 2.xlsx'", type=["xlsx"])

if uploaded_file:
    try:
        # 1. Cargar datos
        df = pd.read_excel(uploaded_file)
        df.columns = [str(c).strip() for c in df.columns]
        
        # Identificar columnas
        col_obj = df.columns[0]
        col_n1 = df.columns[1]
        col_n2 = df.columns[2]
        col_log = df.columns[3]

        # 2. Asignar Marca a cada fila (Detectar a qué empresa pertenece cada sucursal)
        # Creamos una columna auxiliar 'Marca' basada en los totales
        df['Marca'] = None
        marca_actual = "Otras"
        
        # Lógica para identificar marcas basado en la estructura de tu Excel
        for i, row in df.iterrows():
            texto = str(row[col_obj]).upper()
            if "OPENCARS" in texto: marca_actual = "OPENCARS"
            elif "PAMPAWAGEN" in texto: marca_actual = "PAMPAWAGEN"
            elif "CITROEN" in texto: marca_actual = "CITROEN"
            elif "PEUGEOT" in texto: marca_actual = "PEUGEOT"
            df.at[i, 'Marca'] = marca_actual

        # 3. FILTRADO: Quitar filas de TOTAL para los cálculos
        df_sucursales = df[~df[col_obj].str.contains("TOTAL", na=False, case=False)].copy()
        df_sucursales = df_sucursales.dropna(subset=[col_n1])

        # 4. BARRA LATERAL: Filtro de Marca
        st.sidebar.header("Filtros")
        lista_marcas = ["TODAS"] + sorted(df_sucursales['Marca'].unique().tolist())
        filtro_marca = st.sidebar.selectbox("Seleccionar Empresa:", lista_marcas)

        if filtro_marca != "TODAS":
            df_final = df_sucursales[df_sucursales['Marca'] == filtro_marca]
        else:
            df_final = df_sucursales

        # 5. CÁLCULOS
        t_logrado = df_final[col_log].sum()
        t_n1 = df_final[col_n1].sum()
        t_n2 = df_final[col_n2].sum()
        cumplimiento = (t_logrado / t_n1 * 100) if t_n1 > 0 else 0

        # --- INTERFAZ ---
        st.subheader(f"📌 Resumen: {filtro_marca}")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Logrado", f"{int(t_logrado)}")
        c2.metric("Meta Nivel 1", f"{int(t_n1)}")
        c3.metric("Meta Nivel 2", f"{int(t_n2)}")
        c4.metric("% Cumplimiento", f"{cumplimiento:.1f}%")

        st.divider()

        # 6. GRÁFICOS
        col_a, col_b = st.columns(2)

        with col_a:
            st.write("### 🏢 Unidades por Sucursal")
            fig_bar = px.bar(df_final, x=col_obj, y=[col_log, col_n1, col_n2],
                             barmode='group', 
                             color_discrete_sequence=["#00BCFF", "#323232", "#00F0A0"],
                             labels={'value': 'Unidades', 'variable': 'Nivel'})
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_b:
            st.write("### 📈 Avance sobre Nivel 1")
            df_final['%'] = (df_final[col_log] / df_final[col_n1] * 100)
            fig_rank = px.bar(df_final.sort_values('%'), x='%', y=col_obj, 
                              orientation='h', color='%', color_continuous_scale="RdYlGn")
            st.plotly_chart(fig_rank, use_container_width=True)

        # 7. TABLA DE VERIFICACIÓN
        st.subheader("📋 Detalle de Datos")
        st.dataframe(df_final[[col_obj, col_log, col_n1, col_n2, 'Marca']], use_container_width=True)

    except Exception as e:
        st.error(f"Error en el procesamiento: {e}")
else:
    st.info("👋 Sube el nuevo archivo Excel para activar el panel con filtros.")
