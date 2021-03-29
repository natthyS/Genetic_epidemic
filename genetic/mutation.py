
import logging
import numpy as np
import random

def mutation_in_point(ind):
    """[Function performances a mutation in ONE point on the entire chromosome]

    Args:
        ind ([array]): [individual to mutate]

    Returns:
        ind [array]: [mutated indivual]
    """    
    # logging.info("Shape ind: {}".format(ind.shape))
    n_tp = ind.shape[0]
    k = np.random.randint(n_tp)# número aleatorio = indice dónde se hará la mutación
    ind[k] = (ind[k] + 1) % 2

    return ind

def mutation_in_four_point(ind):
    """[Function performances a mutation in FOUR different points on the entire chromosome]

    Args:
        ind ([array]): [individual to mutate]

    Returns:
        ind [array]: [mutated indivual]
    """    
    n_tp = ind.shape[0]
    indices = sorted( random.sample(range(0, n_tp), 4) ) 

    for k in indices:
        ind[k] = (ind[k] + 1) % 2

    return ind