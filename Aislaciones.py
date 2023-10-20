import streamlit as st
import pyodbc
import pandas as pd
import plotly.express as px


st.set_page_config(layout="wide")

conn_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=Y:\Entity\GPI\G_200_Site_Incahuasi\05_PRODUCCION\01. REPORTES\1.1. Diarios\15 Libro de Novedades\1.-Programa\Base de Datos\LIBRONOVEDADES_be.accdb;'
            r'Mode=Read;'
            )
conn = pyodbc.connect(conn_str)

cursor = conn.cursor()
aislaciones = [i.table_name for i in cursor.tables(tableType='TABLE')]
print(aislaciones)

for j in cursor.tables(tableType='VIEW'):
    print(j.table_name)
    

lista = ['CAP', 'CAE']
d={}
for aislacion, nombre in zip(aislaciones[:2], lista):
#Run SQL statement
    cursor.execute(f'select * from [{aislacion}]')

#get one row
    one_row = cursor.fetchone()

#get all rows
    rows = cursor.fetchall()
      
    d[nombre] = pd.read_sql(f'select * from [{aislacion}]', conn)

df_CAP = d['CAP']
df_CAE = d['CAE']
# df_Equipos = d['Equipos_Disponibles']
# df_Libro = d['Libro_de_novedades']


CAP = df_CAP[df_CAP['Des-Aislacion']==False]
CAP['Fecha'] = CAP['Fecha'].dt.date
CAP_largo = CAP[CAP['LP']==True]
CAP_corto = CAP[CAP['Tipo']=='Corto Plazo']

df_CAE.dropna(subset='Numero', inplace=True)

CAE = df_CAE[(df_CAE['Des-Aislacion']==False) & df_CAE['CAE']==True]
CAE['Fecha'] = CAE['Fecha'].dt.date

CAE_largo = CAE[CAE['LP']==True]
CAE_corto = CAE[CAE['Tipo']=='Corto Plazo']

st.title('AISLACIONES DE PROCESO Y ELECTRICAS')

with st.container():
    
    column1, column2 = st.columns(2)
    
    with column1:
        st.header('AISLACIONES DE PROCESO')
        col1, col2, col3 = st.columns(3)
        
        col1.metric("**TOTAL**", len(CAP))
        col2.metric("**Largo Plazo**", len(CAP_largo))
        col3.metric("**Corto Plazo**", len(CAP_corto))
     
    with column2:
        st.header('AISLACIONES DE ELECTRICAS')
        col1, col2, col3 = st.columns(3)
         
        col1.metric("**TOTAL**", len(CAE))
        col2.metric("**Largo Plazo**", len(CAE_largo))
        col3.metric("**Corto Plazo**", len(CAE_corto))

with st.expander('Ver detalle'):
    
    col1, col2= st.columns(2)
    with col1:
        st.write('**Asilaciones de Proceso Largo Plazo**')
        st.dataframe(CAP_largo, hide_index=True)
        st.write('**Asilaciones de Proceso Corto Plazo**')
        st.dataframe(CAP_corto, hide_index=True)
     
    with col2:
         st.write('**Asilaciones Electricas Largo Plazo**')
         st.dataframe(CAE_largo, hide_index=True)
         st.write('**Asilaciones Electricas Corto Plazo**')
         st.dataframe(CAE_corto, hide_index=True)
    
with st.container():
    
    col1, col2= st.columns(2)
    
    with col1:
        fig = px.histogram(CAP, x='Sistema', text_auto= True, color='Sistema')
        fig.update_traces(textfont_size=20, textangle=0, textposition="outside", cliponaxis=False, showlegend=False)
        st.plotly_chart(fig)
        
    with col2:
        fig = px.histogram(CAE, x='Sistema', text_auto= True, color='Sistema')
        fig.update_traces(textfont_size=20, textangle=0, textposition="outside", cliponaxis=False, showlegend=False)
        st.plotly_chart(fig)
