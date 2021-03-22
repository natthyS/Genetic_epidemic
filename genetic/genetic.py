import logging
import numpy as np
import random
from scipy.integrate import odeint
from teoric.utils_equations import Diff_Equ, Diff_Equ_2
from scipy.special import softmax
from genetic.crossover import crossover_wt_par, crossover_bt_par, croosover_in_point
import logging

def f_decodi(individuo, x_min, x_max, t_p, n_p):

  '''
  inputs:
    individuo: vector binario con los parámetros del individuo i de la población
    x_min: extremo inferior de valor a ajustar
    x_max: extremo superior de valor a ajustar
    t_p: tamaño del parámetro(bits/Tamaño)
    n_p: número de parámetros a ajustar

  outputs:
    p: array con números decimales de cada parámetros que estaban en binario
  '''
  #Variables de la función
  p = np.zeros(n_p)
  com = 0 # comienzo del próximo número
  parametro = 0 
  while parametro < n_p :
    vec = individuo[com:com + t_p] # Arreglo con los dígitos del número entero a traves de un slice
    lis = list(vec) # Convierto el vector en una lista de números
    full_str = ''.join([str(elem) for elem in lis]) # Convierto cada elemento de la lista en un string sin separación
    num = int(full_str,2)# Hallo el númnero decimal
    param = x_min + (num *(x_max-x_min)/((2**t_p)-1) ) # encuentro el valor del parámetro
    p[parametro] = param
    parametro += 1
    com += t_p # Es el inicio del slice que corresponde al proximo número
  return p

def f_adaptacion(p_bina, data, N_indv, x_min, x_max, t_p, n_p, y_initial):
  """
  inputs:
    p_bina : Población en números binarios
    data: Datos de muertes acumuladas de Pichincha 2020
    N_indv: Número de individuos(par)
    x_min: extremo inferior de valor a ajustar
    x_max: extremo superior de valor a ajustar
    t_p: tamaño del parámetro(bits/Tamaño)
    n_p: número de a ajustar
   

  outputs:
    f_adap : lista con nuevos valores de adaptación
  """
  dias = list(range(len(data.index)))
  f_adap = np.zeros(N_indv)
  for i in range(0,N_indv):
        sigma, gamma, beta, f = f_decodi(p_bina[i,:], x_min, x_max, t_p, n_p)
        Solve = odeint(Diff_Equ, y_initial, dias, args=(sigma, gamma, beta, f) )
        S,E,I,R,D = [Solve[:,i] for i in range(5)]# lista de 5 arrays 

        f_adap[i] = 1/(1+np.sum(np.square(D-data)))
  return f_adap

def seleccion(f_adapta):
  """
  inputs:
    f_adapta : array list de valores de adapatacion por individuo

  outputs:
    (ind1, ind2) : tupla con indices de los individuos selecionados
  """
  # normalizamos de acuerdo a los valores de adaptacion
  # obtenemos probabilidades por valor de adaptacion
  #norm_f_add = softmax(f_adapta)          
  #norm_f_add = 1/(1 + np.exp(-f_add))  #sigmoid

  #create array of index per individual
  indexes = np.arange(f_adapta.shape[0]) 


  ind1 = random.choices(indexes, weights = f_adapta)
  ind2 = random.choices(indexes, weights = f_adapta)

  # ind1 = np.random.choice(indexes, p = norm_f_add)
  # ind2 = np.random.choice(indexes, p = norm_f_add)

  while (ind1 == ind2):
    # ind2 = np.random.choice(indexes, p = norm_f_add)
    ind2 = random.choices(indexes, weights = f_adapta)
  
  return (ind1, ind2)

def reproduccion(p_repro, p_bina, ind1, ind2, mode, t_p):
  '''
  inputs:
    p_repro: probabilidad de reproducción
    p_bina : Población inicial en números binarios
    ind1, ind2: índices de individuos seleccionados
    t_p: size of parameter

  outputs:
    hijo1, hijo2: individuos producto de reproducción
  '''

  xx = np.random.rand()
  if ( p_repro < xx ): 
    return (p_bina[ind1,:], p_bina[ind2,:])

  if mode == 'bt_par': 
    hijo1, hijo2 = crossover_bt_par(p_bina[ind1,:], p_bina[ind2,:], t_p)

  elif mode == 'wt_par':
    hijo1, hijo2 = crossover_wt_par(p_bina[ind1,:], p_bina[ind2,:], t_p)

  elif mode == 'bt_wt_par': 
    hijo1, hijo2 = crossover_bt_par(p_bina[ind1,:], p_bina[ind2,:], t_p)
    hijo1, hijo2 = crossover_wt_par(hijo1, hijo2, t_p)

  elif mode == 'bk_par':
    hijo1, hijo2 = croosover_in_point(p_bina[ind1,:], p_bina[ind2,:], t_p)

  else: 
    logging.info('El Modo no existente') 
  
  return hijo1, hijo2

def mutation(N_indv, n_tp, p_muta, bt):
  '''
  inputs:
    n_tp: tamaño total del cromosoma
    N_indv:número de individuos
    p_muta: probabilidad de mutación
    bt: matriz auxiliar para guardar a los hijos
  
  output: N/A
  '''
  
  for i in range(N_indv):
    xx = np.random.rand()
    if ( p_muta > xx ): 
      k = np.random.randint(n_tp)# número aleatorio = indice dónde se hará la mutación
      suma = bt[i, k] + 1
      bt[i,k] = suma%2 # El resto de la división entera me garantiza el resultado entre 0 y 1
  return bt