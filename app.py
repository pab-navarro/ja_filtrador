import streamlit as st
import sqlite3
import pandas as pd

# Función para obtener las opciones de filtrado desde una tabla
def get_filter_options(table_name, column_name):
    conn = sqlite3.connect('articulos.db')
    query = f"SELECT DISTINCT {column_name}, Code FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    # Añadir una opción en blanco
    df = pd.concat([pd.DataFrame({column_name: [''], 'Code': [None]}), df], ignore_index=True)
    return df

# Función para obtener los datos filtrados de la tabla 'articles'
def get_filtered_data(filters):
    conn = sqlite3.connect('articulos.db')
    query = '''
    SELECT a.*
    FROM articles a
    LEFT JOIN appointment ap ON a.Number_of_appointments = ap.Code
    LEFT JOIN years y ON a.YEAR = y.Code
    LEFT JOIN area_of_knowledge ak ON a.Code_Area_of_Knowledge = ak.Code
    LEFT JOIN keyword k ON a.Code_Keyword = k.Code
    LEFT JOIN JCR_rank jr ON a.Code_JCR_RANK = jr.Code
    WHERE 1=1
    '''
    params = []
    if filters['Appointment']:
        query += " AND ap.Code IN ({})".format(','.join('?' * len(filters['Appointment'])))
        params.extend(filters['Appointment'])
    if filters['Year']:
        query += " AND y.Code IN ({})".format(','.join('?' * len(filters['Year'])))
        params.extend(filters['Year'])
    if filters['Area_of_Knowledge']:
        query += " AND ak.Code IN ({})".format(','.join('?' * len(filters['Area_of_Knowledge'])))
        params.extend(filters['Area_of_Knowledge'])
    if filters['Keyword']:
        query += " AND k.Code IN ({})".format(','.join('?' * len(filters['Keyword'])))
        params.extend(filters['Keyword'])
    if filters['JCR_RANK']:
        query += " AND jr.Code IN ({})".format(','.join('?' * len(filters['JCR_RANK'])))
        params.extend(filters['JCR_RANK'])
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

# Título de la aplicación
st.markdown("<h1 style='text-align: center;'>Article Filter</h1>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Obtener las opciones de filtrado desde las tablas
appointment_options = get_filter_options('appointment', 'Appointment')
year_options = get_filter_options('years', 'Year')
area_of_knowledge_options = get_filter_options('area_of_knowledge', 'Code_Area_of_Knowledge')
keyword_options = get_filter_options('keyword', 'Keyword')
jcr_rank_options = get_filter_options('JCR_rank', 'JCR_RANK')

# Crear columnas para los filtros
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
col5 = st.columns(1)

with col1:
    selected_appointments = st.multiselect('Select the number of appointments:', appointment_options['Appointment'])
with col2:
    selected_years = st.multiselect('Select the year:', year_options['Year'])
with col3:
    selected_area_of_knowledges = st.multiselect('Select the knowledge area:', area_of_knowledge_options['Code_Area_of_Knowledge'])
with col4:
    selected_keywords = st.multiselect('Select the Keyword:', keyword_options['Keyword'])
with col5[0]:
    selected_jcr_ranks = st.multiselect('Select the JCR rank:', jcr_rank_options['JCR_RANK'])

# Obtener los códigos seleccionados
filters = {
    'Appointment': appointment_options.loc[appointment_options['Appointment'].isin(selected_appointments), 'Code'].tolist() if selected_appointments else [],
    'Year': year_options.loc[year_options['Year'].isin(selected_years), 'Code'].tolist() if selected_years else [],
    'Area_of_Knowledge': area_of_knowledge_options.loc[area_of_knowledge_options['Code_Area_of_Knowledge'].isin(selected_area_of_knowledges), 'Code'].tolist() if selected_area_of_knowledges else [],
    'Keyword': keyword_options.loc[keyword_options['Keyword'].isin(selected_keywords), 'Code'].tolist() if selected_keywords else [],
    'JCR_RANK': jcr_rank_options.loc[jcr_rank_options['JCR_RANK'].isin(selected_jcr_ranks), 'Code'].tolist() if selected_jcr_ranks else [],
}

# Mostrar los datos filtrados o todos los datos si no se selecciona ningún filtro
st.markdown("<br>", unsafe_allow_html=True)
data = get_filtered_data(filters)
st.dataframe(data, use_container_width=True, hide_index=True)
