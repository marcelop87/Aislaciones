import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(layout="wide")
   
file = st.sidebar.file_uploader("Upload a data set in CSV or EXCEL format", type=["csv","xlsx"])

@st.cache_data
def load_data(file):
   CAP = pd.read_excel(file, sheet_name='CAP')  
   CAE = pd.read_excel(file, sheet_name='CAE') 
   return CAP, CAE

if file is not None:
   CAP, CAE = load_data(file)  
   
   CAP_largo = CAP[CAP['LP']==True]
   CAP_corto = CAP[CAP['Tipo']=='Corto Plazo']
    
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
            st.dataframe(CAP_largo.style.hide(axis=“index”))
            st.write('**Asilaciones de Proceso Corto Plazo**')
            st.dataframe(CAP_corto.style.hide(axis=“index”))
         
        with col2:
             st.write('**Asilaciones Electricas Largo Plazo**')
             st.dataframe(CAE_largo.style.hide(axis="index"))
             st.write('**Asilaciones Electricas Corto Plazo**')
             st.dataframe(CAE_corto.style.hide(axis="index"))
        
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
