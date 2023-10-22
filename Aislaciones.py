import streamlit as st
import pyodbc


st.title('AISLACIONES DE PROCESO Y ELECTRICAS')
# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return pyodbc.connect(
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=Y:\Entity\GPI\G_200_Site_Incahuasi\05_PRODUCCION\01. REPORTES\1.1. Diarios\15 Libro de Novedades\1.-Programa\Base de Datos\LIBRONOVEDADES_be.accdb;'
        r'Mode=Read;'
         
    )

conn = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.

def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from [Aislacion de Proceso]")
