import numpy as np
import random


def croosover_in_point(p_1, p_2, t_p):
    k = np.random.randint(1, t_p * 4) # valor donde se partira el cromosoma para la reproducción
    hijo1 = np.concatenate( (p_1[:k], p_2[k:]) ) # Se combinan los dos padres para dar un hijo
    hijo2 = np.concatenate( (p_2[:k], p_1[k:]) ) # Se combinan los dos padres para dar el otro hijo
    
    return hijo1, hijo2

def crossover_wt_par(p_1, p_2, t_p):
    """[This function performs a crossover some portions of parameters (within parameter) of two parent individuals]

    Args:
        p_1 ([np.array]): [patern_1]
        p_2 ([np.array]): [patern_1]
        t_p ([int]): [size of parameter]

    Returns:
        hijo1, hijo2 [np.array]: [hijo 1 y hijo 2]
    """  
  
    #print('Este es p_1: ', p_1)
    #print('Este es p_2: ', p_2)
  
    cambio = np.random.randint(1,t_p,size=(4) )
    #print(cambio)
    
    crom_h1 = []
    crom_h2 = []
    for i in range(4): 
        crom_h1 += [p_1[t_p*i:t_p*i+cambio[i]], p_2[t_p*i+cambio[i]:t_p*(i+1)]]
        crom_h2 += [p_2[t_p*i:t_p*i+cambio[i]], p_1[t_p*i+cambio[i]:t_p*(i+1)]]

    hijo1 = np.concatenate(tuple(crom_h1))
    hijo2 = np.concatenate(tuple(crom_h2)) 

    #print('Este es h_1: ', hijo1)
    #print('Este es h_2: ', hijo2)

    return hijo1, hijo2

def crossover_bt_par(parent_1, parent_2, t_p): 
    """This function performs a crossover between parameters of two parent individuals.
       The idea is interchange the parts of the cromosomas, which correspond to an
       specific parameter.

    Args:
        parent_1 (np.array): [parent_1]
        parent_2 (np.array): [parent_2]
        t_p (int): [size of parameter]
    Returns:
        hijo1, hijo2 [np.array]: [hijo 1 y hijo 2]
    """
    #print('Esta es parent_1: ',parent_1)
    #print('Esta es parent_2: ',parent_2)

    num_par = np.random.randint(1,4)
    #print(num_par)
    cambiar = random.sample(range(0,4),num_par)

    hijo_1 = np.copy(parent_1)
    hijo_2 = np.copy(parent_2)

        
    #   print('Posiciones a cambiar', cambiar)

    for x in cambiar:
        step = x*t_p
        hijo_1[step: step+t_p] = parent_2[step: step+t_p]
        hijo_2[step: step+t_p] = parent_1[step: step+t_p]

    #   print('Este es el h_1', hijo_1)
    #   print('Este es el h_2', hijo_2)
    return hijo_1, hijo_2