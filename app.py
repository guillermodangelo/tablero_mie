import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.metrics import r2_score, mean_squared_error

st.set_page_config(page_title='Test')

st.title("Modelo de interacción espacial para migraciones internas 🇺🇾")

desc = """
A partir de un modelo de interacción espacial restringido en origen, esta app permite
modificar las variables usadas para la estimación, simulando escenarios de migración
interna a futuro, si se mantuvieran las relaciones entre las variables del modelo calibrado.

Para el desarrollo del modelo se usaron datos del Censo INE 2011.

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

factor_edad = st.slider('Factor de aumento de la edad promedio en destino 🧓', 0.0, 5.0, value=1.0)

factor_pbi = st.slider('Factor de aumento del PBI en destino (millardos) 💸', 0.0, 5.0, value=1.0)



dd_new = dd.copy()

dd_new['log_edad_promedio_des'] = np.log(factor_edad * dd_new.edad_prom_des)
dd_new['log_pbi_destino_millardos'] = np.log(factor_pbi * dd_new.pbi_destino_millardos)


def print_scores_simple(ground_truth, estimation):
    "Imprime r cuadrado y error mínimo cuadrático de un modelo"
    r2 = r2_score(ground_truth, estimation)
    rmse = mean_squared_error(ground_truth, estimation, squared=False)
    
    st.write("r² = " + round(r2, 4).astype(str))
    st.write("RMSE = " + round(rmse, 4).astype(str))


actual_counts = dd.personas_mig
new_pred = round(prodSim.predict(dd_new)).astype(int)


st.markdown('**Métricas del modelo estimado:**')

print_scores_simple(actual_counts, new_pred)



# matriz de los valores estimados
dd['prodsimest'] = new_pred

matriz = pd.pivot_table(dd,
                        values='prodsimest',
                        index ='nom_depto_orig',
                        columns='nom_depto_des',
                        fill_value=0,
                        aggfunc=sum,
                        margins=True,
                        margins_name='Total')

st.subheader("Matriz de datos estimados 📉")

st.write(matriz)

