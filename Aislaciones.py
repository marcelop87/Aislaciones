import streamlit as st
import pyodbc
import pandas as pd

def main():
  container.write(" # Data Analysis and Visualization # ")

  file = st.sidebar.file_uploader("Upload a database")

  options = st.sidebar.radio('Pages',options = ['Data Analysis','Data visualization', 'Data Prediction'])

  if file is not None:
    data = load_data(file)


@st.cache_data
def load_data(file):
    try:
        conn_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                    r'DBQ=file;'
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
         
if __name__ == "__main__":
  main()
