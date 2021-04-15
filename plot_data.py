import pandas as pd 
import numpy as np
from utils.plot_utils import plot_adaptacion_2, plot_model_2, plot_dead_2

# Load Pichincha data
df = pd.read_csv("stuff/data/data_norm_2020.csv")
datos = df['Pichincha']
datos = np.clip(datos,0, float('inf'))
datos = np.cumsum(datos)
#Parametros del modelo teorico
I0 = 1                              # numero inicial de infectados

#Parametros del modelo teorico
Np_AG = 3228233                     # Población estimada de Quito
# vector inicial para resolver ecuaciones diferenciales
y_initial = [Np_AG, 0, I0, 0, 0] 

# Plot adaptation

for exp in range (1,31):
    for inte in range(2): 
        direction = 'stuff/experiments/crossover_testvariation_results_sheet_crossover/experiment_{}_execution_{}_iterations.csv'.format(exp,inte)
        #direction = 'stuff/experiments/crossover_testvariation_results_sheet_crossover_5/experiment_{}_execution_{}_iterations.csv'.format(exp,inte)
        data = pd.read_csv(direction)
        adapta = data['best_adapta']
        interation = data['iteration']
        experiment_name = "sheet_crossover_exp_{}_inter_{}".format(exp,inte)
        
        plot_adaptacion_2(interation,adapta, experiment_name)


# Plot dead and theoretical model 
direct = 'stuff/experiments/crossover_testvariation_results_sheet_crossover/crossover_testvariation_results.csv'
#direct = 'stuff/experiments/crossover_testvariation_results_sheet_crossover_5/crossover_testvariation_results.csv'
results = pd.read_csv(direct)
n_const = ['sigma', 'gamma', 'beta','f']
val_const = []
for exp in range(30):
    for const in n_const: 
        val_const.append(results[const][exp]) 
    #print('values ', val_const)
    n_exp = 'exp_{}'.format(exp+1)
    plot_model_2 (datos, y_initial, val_const, n_exp)
    plot_dead_2(datos, y_initial, val_const, n_exp)
    val_const.clear()
