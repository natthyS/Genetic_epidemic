from main import *
import pandas as pd
import utils.plot_utils as plot_utils

# Parametros ajustables
N_indv = 100         # Número de individuos(par)
N_pasos = 1000       # Numero de pasos de la simulación; número de generacions
p_repro = 0.95       # probabilidad de reproducción, la mayorio del tiempo es fijo
p_muta = 0.5         # probabilidad de mutación
p_sup = 0.10         # probabilidad de supervivencia o porcentaje que se conserva de la generacion previa

#Parametros del modelo teorico
I0 = 7                              # numero inicial de infectados

# Load the data from .csv
df = pd.read_csv("stuff/data/data_norm_2020.csv")
data = df['Acu-Pichincha']

# Plot the best adaptation per generation
parametros = {
  'inds' : N_indv,
  'steps' : N_pasos,
  'pr' : p_repro,
  'pm' : p_muta,
  'ps' : p_sup,
  'i0' : I0
}

# Execute the main loop algorithm
mejor_individuo, meta_results = main_loop(data, parametros)

plot_utils.plot_adaptacion(meta_results['list_generations'], 
                          meta_results['list_mej_adap'],
                          **parametros)
