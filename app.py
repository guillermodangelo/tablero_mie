import streamlit as st
import pandas as pd
import statsmodels.api as sm

st.set_page_config(page_title='Test')

st.title("Test 🇺🇾")

desc = """
Aplicación para comparar datos
demográficos de los migrantes internos en Uruguay,
según los datos del Censo INE 2011.

*Desarrollada por Guillermo D'Angelo.*
"""

st.caption(desc)

@st.cache(persist=True)
def cargar_dd_deptos():
    dd_deptos = pd.read_csv('data/dd_deptos.csv', sep=';', decimal=',')
    dd_deptos.loc[dd_deptos.largo_limite.isna(), 'largo_limite'] = 0.0001
    dd_deptos['largo_limite_km'] = dd_deptos.largo_limite/1000

    return dd_deptos
    
dd = cargar_dd_deptos()

#prodSim = sm.load('data/restringido_origen_mvo.pickle')

nom_depto = [
    'Montevideo', 'Artigas', 'Canelones',
    'Cerro Largo', 'Colonia', 'Durazno',
    'Flores', 'Florida', 'Lavalleja',
    'Maldonado', 'Paysandú', 'Río Negro',
    'Rivera', 'Rocha', 'Salto', 'San José',
    'Soriano', 'Tacuarembó', 'Treinta y Tres'
    ]


edad = st.slider('Aumento edad', 0.0, 5.0, value=1.2)

st.write(edad)