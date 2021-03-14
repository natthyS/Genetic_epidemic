import numpy as np
import pandas as pd
import utils.utils as utils
from utils.metrics import jaccard_index_ind, jaccard_index_population, sorensen_index_population
from genetic.genetic import f_adaptacion, seleccion, reproduccion, mutation
import logging
log_format = '%(asctime)s | (line %(lineno)d %(filename)s) | [%(levelname)s]: %(message)s'
logging.basicConfig(format= log_format, level=logging.INFO)

#Parametros del modelo teorico
Np_AG = 3228233                     # Población estimada de Quito

# Parametros para ajustar el cromosoma
n_p = 4             # número de parametros a ajustar
t_p = 7             # tamaño del parámetro(bits/Tamaño)
n_tp = n_p * t_p    # tamaño total del cromosoma
x_min = 0           # valor min y max de cada parametro
x_max = 1


# Parametros de resultados
grafi = 5           # cada cuantos pasos guardo el valor de adaptación para graficarlos


def main_loop(data, parametros):

  # vector inicial para resolver ecuaciones diferenciales
  y_initial = [Np_AG, 0, parametros['i0'], 0, 0]   

  # Get survived individuals and dead individuals
  N_ind_sup, N_ind_dead = utils.get_surv_and_dead(parametros['ps'], parametros['inds'])

  # Población inicial en números binarios
  p_bina = np.random.randint(2, size=(parametros['inds'], n_tp) ) 

  # Inicializaciones
  current_step = 0                # contador de paso actual
  ada_mejor = -1.0                # Adaptacion del mejor individuo
  ada_mejor_h = -1.0              # Adaptación del mejor individuo en la historia

  # Create a dictionary with the variables to plot results
  meta_results = {
    'l_mej_adap': [],
    'l_generations': [],
    'l_mej_ind': [],
    'l_jaccard_ind' : [],
    'l_jaccard_pop' : [],
    'l_sorensen_pop' : [],
    'l_adaptations' : []
  }

  # Temporales y Auxiliares
  mejor =  np.random.randint(2, size=(n_tp) ) 
  bina_temp = np.zeros((N_ind_dead,n_tp), dtype=int)

  # Main Loop
  poblacion_actual = p_bina
  while (ada_mejor < 0.999) and (current_step< parametros['steps']) :

    # obtenemos el valor de adaptacion por individuo
    f_adapta = f_adaptacion(poblacion_actual, data, parametros['inds'], x_min, x_max, t_p, n_p, y_initial)
    
    #Ciclo de reproducción
    for i in range(0,N_ind_dead ,2):
      id1, id2 = seleccion(f_adapta)
      bina_temp[i, :], bina_temp[i+1, :]  = reproduccion(parametros['pr'], poblacion_actual, id1, id2, parametros['xmode'], t_p)
      
    
    # Mutación
    bina_temp = mutation(N_ind_dead,n_tp, parametros['pm'], bina_temp)

    #Actualizo la mejor adaptación
    ada_mejor = np.amax(f_adapta)
    indice = np.argmax(f_adapta)
    if ada_mejor > ada_mejor_h:
      ada_mejor_h = ada_mejor                     # Guardo el mejor valor de adaptación
      mejor = np.copy(poblacion_actual[indice,:]) # Guardo el mejor individuo en binarios
    
    #Guardar para graficar
    if current_step%grafi == 0:
      meta_results['l_mej_adap'].append(ada_mejor)
      meta_results['l_generations'].append(current_step)
      meta_results['l_mej_ind'].append(mejor)
      meta_results['l_adaptations'].append(f_adapta) # n, bins, patches = plt.hist(f_adapta)

      meta_results['l_jaccard_ind'].append(jaccard_index_ind(poblacion_actual, indice))
      meta_results['l_jaccard_pop'].append(jaccard_index_population(poblacion_actual))
      meta_results['l_sorensen_pop'].append(sorensen_index_population(poblacion_actual))
      
      logging.info('Step: {} AdaBest : {} JaccI: {:.4f} JaccP: {:.4f} SorsP: {:.4f}'.format(
                                    current_step,
                                    meta_results['l_mej_adap'][-1],
                                    meta_results['l_jaccard_ind'][-1],
                                    meta_results['l_jaccard_pop'][-1],
                                    meta_results['l_sorensen_pop'][-1]
                                    ))    


    # Matar a los menos aptos
    poblacion_actual[-N_ind_dead:,:] = bina_temp
    
    #Incrementar el current_step
    current_step += 1

  return mejor, meta_results