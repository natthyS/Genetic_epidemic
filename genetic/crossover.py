import numpy as np
import random


def croosover_in_point(p_1, p_2, t_p):
    """[This function crosses only one point of the entire chromosome (one point for all 4 parameters)]

    Args:
        p_1 ([np.array]): [patern_1]
        p_2 ([np.array]): [patern_2]
        t_p ([int]): [size of parameter]

    Returns:
        hijo1, hijo2 [np.array]: [hijo 1 y hijo 2]
    """    

    k = np.random.randint(1, t_p * 4)            # valor donde se partira el cromosoma para la reproducción
    hijo1 = np.concatenate( (p_1[:k], p_2[k:]) ) # Se combinan los dos padres para dar un hijo
    hijo2 = np.concatenate( (p_2[:k], p_1[k:]) ) # Se combinan los dos padres para dar el otro hijo
    
        #k = 12
        #hijo1 = np.concatenate( (p_1[:12], p_2[12:]) )
        #hijo2 = np.concatenate( (p_2[:12], p_1[12:]) )
    
    
    return hijo1, hijo2
    
def crossover_wt_par(p_1, p_2, t_p):
    """[This function crosses within a part of each parameter which comes from two parents individuals]

    Args:
        p_1 ([np.array]): [patern_1]
        p_2 ([np.array]): [patern_1]
        t_p ([int]): [size of parameter]

    Returns:
        hijo1, hijo2 [np.array]: [hijo 1 y hijo 2]
    """  
  
    # generar 4 números aleatorios de 1 a 7 que corresponde a las posiciones a variar en cada parametro del cromosoma
    cambio = np.random.randint(1,t_p,size=(4) )
   
    # crear listas vacias para cada cromosoma hijo
    crom_h1 = []
    crom_h2 = []

    for i in range(4): 
        crom_h1 += [p_1[t_p*i:t_p*i+cambio[i]], p_2[t_p*i+cambio[i]:t_p*(i+1)]]
        crom_h2 += [p_2[t_p*i:t_p*i+cambio[i]], p_1[t_p*i+cambio[i]:t_p*(i+1)]]
        # i = 0; cambio[0] = 2
        # crom_h1 += [p_1[0:2], p_2[2:7]]
        # crom_h2 += [p_2[0:2], p_1[2:7]]
        # i = 1; cambio[1] = 4
        # crom_h1 += [p_1[7:11], p_2[11:14]]
        # crom_h2 += [p_2[7:11], p_1[11:14]]
        #.
        #.

    hijo1 = np.concatenate(tuple(crom_h1))
    hijo2 = np.concatenate(tuple(crom_h2)) 

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
    #numero de parámetros a cambiar del 1 al 3
    num_par = np.random.randint(1,4)
    
    # posiciones a cambiar de acuerdo al num_par (0,1,2,3)
    cambiar = random.sample(range(0,4),num_par)

    #cada hijo es una copia de un padre
    hijo_1 = np.copy(parent_1)
    hijo_2 = np.copy(parent_2)

    
    for x in cambiar:
        step = x*t_p
        hijo_1[step: step+t_p] = parent_2[step: step+t_p]
        hijo_2[step: step+t_p] = parent_1[step: step+t_p]

        # num_par = 2
        # cambiar = [0,2]
        # x = 0
        # step = 0
        # hijo_1[0: 7] = parent_2[0: 7]
        # hijo_2[0: 7] = parent_1[0: 7]
        # x = 2
        # step = 14
        # hijo_1[14: 21] = parent_2[14:21]
        # hijo_2[14: 21] = parent_1[14:21]
          
    return hijo_1, hijo_2

def crossover_in_four_points(parent_1, parent_2, n_tp):
    """[This function performs a crossover in 4 different point in the chromosomes of the parents.
        Randomly selected point over the entire chromosome lenght range. 
        Point selection does not consider the lenght of each parameter ]

    Args:
        parent_1 (np.array): [parent_1]
        parent_2 (np.array): [parent_2]
        n_tp ([int]): [total chromosome size]

    Returns:
         hijo1, hijo2 [np.array]: [hijo 1 y hijo 2]
    """            
    # parent_1 = np.squeeze(parent_1, axis=0)
    # parent_2 = np.squeeze(parent_2, axis=0)
    
    # reproducción a cuatro puntos
    k1,k2,k3,k4 = sorted( random.sample(range(3, n_tp-1), 4) ) #no tomo los extremos
    #????? por qué desde 3?
    ceros = np.zeros(n_tp)
    mascara1 = np.concatenate( (parent_1[:k1], ceros[k1:k2], parent_1[k2:k3], ceros[k3:k4], parent_1[k4: ]) )
    mascara2 = np.concatenate( (ceros[:k1], parent_1[k1:k2], ceros[k2:k3], parent_1[k3:k4], ceros[k4: ]) )
    mascara3 = np.concatenate( (parent_2[ :k1], ceros[k1:k2], parent_2[k2:k3], ceros[k3:k4], parent_2[ k4: ]) )
    mascara4 = np.concatenate( (ceros[:k1], parent_2[k1:k2], ceros[k2:k3], parent_2[k3:k4], ceros[k4: ]) )
    hijo1 = mascara1 + mascara4 # Se combinan los dos padres para dar un hijo
    hijo2 = mascara2 + mascara3   # Se combinan los dos padres para dar el otro hijo
    return hijo1, hijo2
