﻿import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.metrics import r2_score, mean_squared_error

st.set_page_config(page_title='Test')

st.title("Test 🇺🇾")

desc = """
Aplicación para comparar datos
demográficos de los migrantes internos en Uruguay,
según los datos del Censo INE 2011.

*Desarrollada por Guillermo D'Angelo.*
"""

st.caption(desc)

def cargar_dd_deptos():
    dd_deptos = pd.read_csv('data/dd_deptos.csv', sep=';', decimal=',')
    dd_deptos.loc[dd_deptos.largo_limite.isna(), 'largo_limite'] = 0.0001
    dd_deptos['largo_limite_km'] = dd_deptos.largo_limite/1000

    return dd_deptos


dd = cargar_dd_deptos()

prodSim = sm.load('data/restringido_origen_mvo.pickle')

nom_depto = [
    'Montevideo',
    'Artigas',
    'Canelones',
    'Cerro Largo',
    'Colonia',
    'Durazno',
    'Flores',
    'Florida',
    'Lavalleja',
    'Maldonado',
    'Paysandú',
    'Río Negro',
    'Rivera',
    'Rocha',
    'Salto',
    'San José',
    'Soriano',
    'Tacuarembó',
    'Treinta y Tres'
    ]

factor_edad = st.slider('Aumento edad', 0.0, 5.0, value=1.2)

factor_pbi = st.slider('Aumento PBI', 0.0, 5.0, value=1.2)



dd_new = dd.copy()

dd_new['log_edad_promedio_des'] = np.log(factor_edad * dd_new.edad_prom_des)
st.write(dd_new['log_edad_promedio_des'])
st.write(prodSim.summary())


dd_new['log_pbi_destino_millardos'] = np.log(factor_pbi * dd_new.pbi_destino_millardos)
st.write(dd_new['log_pbi_destino_millardos'])
st.write(prodSim.summary())


def print_scores_simple(ground_truth, estimation):
    "Imprime r cuadrado y error mínimo cuadrático de un modelo"
    r2 = r2_score(ground_truth, estimation)
    rmse = mean_squared_error(ground_truth, estimation, squared=False)
    
    st.write("R² = " + round(r2, 4).astype(str))
    st.write("RMSE = " + round(rmse, 4).astype(str))


actual_counts = dd.personas_mig
new_pred = prodSim.predict(dd_new)

#predicted_counts = new_pred.summary_frame()['mean'].round(0).astype(int)

st.write(actual_counts)

st.write(new_pred)


print_scores_simple(actual_counts, new_pred)

title = 'Groud truth vs. estimaciones'
subtitle = 'MIE restringido en origen con Mvdeo.'

