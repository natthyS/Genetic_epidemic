from genetic.main import main_loop
import pandas as pd
import utils.plot_utils as plot_utils

# Parametros ajustables
N_indv = 20          # Número de individuos(par)
N_pasos = 2000       # Numero de pasos de la simulación; número de generacions
p_repro = 0.95       # probabilidad de reproducción, la mayorio del tiempo es fijo
p_muta = 0.4         # probabilidad de mutación
p_sup = 0.10         # probabilidad de supervivencia o porcentaje que se conserva de la generacion previa
cross_mode = 'bt_wt_par'# tipo de crossover (reproduccion) 
                     # bt_par : crossover between parameters
                     # wt_par : crossover within parameters
                     # bt_wt_par : crossover between and within parameters
                     # bk_par : crossover in one point
 
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
  'i0' : I0,
  'xmode' : cross_mode 
}

# Execute the main loop algorithm
mejor_individuo, meta_results = main_loop(data, parametros)
# Print mejor_individio y su adaptación 

print ('Mejor adaptación : ', max(meta_results['l_mej_adap']))

plot_utils.plot_adaptacion(meta_results['l_generations'], 
                          meta_results['l_mej_adap'],
                          **parametros)
