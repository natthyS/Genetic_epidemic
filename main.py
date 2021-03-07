import numpy as np
import pandas as pd
import utils.utils as utils
from genetic import f_adaptacion, seleccion, reproduccion, mutation
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
grafi = 50       # cada cuantos pasos guardo el valor de adaptación para graficarlos

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
  list_mej_adap = []                   # Lista con las mejores adaptaciones por generación
  list_generations = []                 # Lista para guardar el contador de las mejores generaciones 
                                  # y las que se va a graficar

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
      bina_temp[i, :], bina_temp[i+1, :]  = reproduccion(n_tp, parametros['pr'], poblacion_actual, id1, id2)
    
    # Mutación
    bina_temp = mutation(N_ind_dead,n_tp, parametros['pm'], bina_temp)

    #Guardar la mejor adaptación
    ada_mejor = np.amax(f_adapta)
    indice = np.argmax(f_adapta)
    if ada_mejor > ada_mejor_h:
      list_mej_adap.append(ada_mejor)                  # Guardo el historial del ada mejor
      list_generations.append(current_step)                     # Guardo la generacion actual
      ada_mejor_h = ada_mejor                     # Guardo el mejor valor de adaptación
      mejor = np.copy(poblacion_actual[indice,:]) # Guardo el mejor individuo en binarios

    #Guardar para graficar
    if current_step%grafi == 0:
      logging.info('paso actual: {} adapta mejor: {}'.format(current_step,ada_mejor))    
      list_mej_adap.append(ada_mejor)
      list_generations.append(current_step)

    # Ordenar por valor de adaptación (mayor a menor)
    poblacion_actual = poblacion_actual[np.argsort(f_adapta)]
    poblacion_actual = np.flip(poblacion_actual, axis=0)

    # Matar a los menos aptos
    poblacion_actual[-N_ind_dead:,:] = bina_temp
    
    #Incrementar el current_step
    current_step += 1

    # Create a dictionary with the variables to plot results
    meta_results = {
      'list_mej_adap': list_mej_adap,
      'list_generations': list_generations
    }

  return mejor, meta_results