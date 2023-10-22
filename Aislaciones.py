import streamlit as st
import pyodbc
import pandas as pd



def load_data():
    try:
        conn_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                    r'DBQ=Y:\Entity\GPI\G_200_Site_Incahuasi\05_PRODUCCION\01. REPORTES\1.1. Diarios\15 Libro de Novedades\1.-Programa\Base de Datos\LIBRONOVEDADES_be.accdb;'
                    r'Mode=Read;')
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
        
            d[nombre] = pd.read_sql('select * from [Aislacion de Proceso]', conn)
        
    except Exception as e:
        st.write("error is: {}".format(e))

    return d
         
d = load_data()
