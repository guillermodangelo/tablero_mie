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


st.sidebar.title(
    'Elija factores de ponderación para modificar el escenario de migración interna'
    )

factor_pob = st.sidebar.slider(
    'Factor de aumento o reducción la población en destino (miles de personas) 🤰', 0.0, 2.0, value=1.0
    )

factor_edad = st.sidebar.slider(
    'Factor de aumento de la edad promedio en destino 🧓', 1.0, 5.0, value=1.0
    )

factor_pbi = st.sidebar.slider(
    'Factor de aumento del PBI en destino (millardos) 💸', 1.0, 3.0, value=1.0
    )

factor_ocup = st.sidebar.slider(
    'Factor de aumento o reducción del porcentaje de ocupados en destino 🛠', 0.01, 3.0, value=1.0
    )

# factor_pob = st.slider('Factor de aumento o reducción la población en destino (miles de personas) 🤰', 0.0, 2.5, value=1.0)
# factor_edad = st.slider('Factor de aumento de la edad promedio en destino 🧓', 1.0, 5.0, value=1.0)
# factor_pbi = st.slider('Factor de aumento del PBI en destino (millardos) 💸', 1.0, 3.0, value=1.0)
# factor_ocup = st.slider('Factor de aumento o reducción del porcentaje de ocupados en destino 🛠', 0.01, 3.0, value=1.0)

dd_new = dd.copy()

dd_new['log_pob_destino_k'] = np.log(factor_pob * dd_new.pob_destino_k)
dd_new['log_edad_promedio_des'] = np.log(factor_edad * dd_new.edad_prom_des)
dd_new['log_pbi_destino_millardos'] = np.log(factor_pbi * dd_new.pbi_destino_millardos)
dd_new['log_porc_ocupados_des'] = np.log(factor_ocup * dd_new.porc_ocupados_des)


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
st.subheader("Matriz de datos estimados 📉")

dd['prodsimest'] = new_pred

dd['depto_origen'] = dd['depto_origen'].astype(str).str.zfill(3)
dd['depto_destino'] = dd['depto_destino'].astype(str).str.zfill(3)

matriz = pd.pivot_table(dd,
                        values='prodsimest',
                        index ='depto_origen',
                        columns='depto_destino',
                        fill_value=0,
                        aggfunc=sum,
                        margins=True)

var_names = nom_depto + ['Total']

matriz.columns = var_names
matriz = matriz.rename(index = dict(zip(matriz.index,  var_names)))

st.write(matriz)



