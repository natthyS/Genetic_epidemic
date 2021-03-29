from genetic.main import main_loop
import pandas as pd
from utils.plot_utils import plot_adaptacion, plot_dead, plot_model
import numpy as np
import random
import utils.utils as utils
import logging


# Init a same seed to all the experiments
SEED = 1000
np.random.seed(SEED)
random.seed(SEED)

# Parametros ajustables
N_indv = 10          # Número de individuos(par)
N_pasos = 100        # Numero de pasos de la simulación; número de generacions
p_repro = 0.95       # probabilidad de reproducción, la mayorio del tiempo es fijo
p_muta = 0.4         # probabilidad de mutación
p_sup = 0.2         # probabilidad de supervivencia o porcentaje que se conserva de la generacion previa
# n_surv = utils.get_surv_and_dead(p_sup, N_indv)
n_surv = 1            # Numero de sobrevivientes
cross_mode = 'bk4_par'  # tipo de crossover (reproduccion) 
                        # bt_par : crossover between parameters
                        # wt_par : crossover within parameters
                        # bt_wt_par : crossover between and within parameters
                        # bk1_par : crossover in one point
                        # bk4_par : crossover in four points
muta_mode = 'm4_point'  # tipo de mutacion
                        # m1_point: mutacion en 1 solo punto
                        # m4_point: mutacion en 4 puntos
                        # 
select_mode = 'st_wheel' # tipo de seleccion
                         # st_lib: seleccion con la libreria random
                         # st_wheel: selecction con la funcion implementada de ruleta                        
precision = 2       # precision for decoding one parameter
 
#Parametros para ajustar los cromosomas
n_p = 4             # número de parametros a ajustar
t_p = utils.get_len_parameters(precision)  # tamaño del parámetro(bits/Tamaño)

#Parametros del modelo teorico
I0 = 1                              # numero inicial de infectados

#Parametros del modelo teorico
Np_AG = 3228233                     # Población estimada de Quito
# vector inicial para resolver ecuaciones diferenciales
y_initial = [Np_AG, 0, I0, 0, 0] 

# Load the data from .csv
df = pd.read_csv("stuff/data/data_norm_2020.csv")
data = df['Acu-Pichincha']

# Plot the best adaptation per generation
parametros = {
  'inds' : N_indv,
  'steps' : N_pasos,
  'pr' : p_repro,
  'pm' : p_muta,
  'nsurv' : n_surv,
  'i0' : I0,
  'xmode' : cross_mode,
  'mutamode' : muta_mode,
  'select_mode' : select_mode,
  'y_initial': y_initial,
  'n_p' : n_p, 
  't_p' : t_p
}

# Execute the main loop algorithm
mejor_individuo, meta_results = main_loop(data, parametros)
# Print mejor_individio y su adaptación 

logging.info('Mejor adaptación : {}'.format(max(meta_results['l_mej_adap'])))

del parametros['y_initial']
del parametros['n_p']
del parametros['t_p']
del parametros['mutamode']
plot_adaptacion(meta_results['l_generations'], 
                          meta_results['l_mej_adap'],
                          **parametros)

# plot_model(mejor_individuo, y_initial, t_p, n_p, data,
#                           **parametros)

# plot_dead(mejor_individuo, y_initial, t_p, n_p, data,
#                           **parametros)                          
