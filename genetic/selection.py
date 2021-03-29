import random
import numpy as np
import logging

def seleccion_roulette( f_ad ):
    s_total = sum(f_ad)
    f_adapt_acu = 0.0
    rand_n = s_total * np.random.rand()

    # Select the first individual
    i = 0
    while(rand_n > f_adapt_acu):
        f_adapt_acu += f_ad[i]
        i += 1
    ind1 = i-1

    # Select the second individual
    fin = False
    while(not fin):
        i = 0
        f_adapt_acu = 0.0
        rand_n = s_total * np.random.rand()
        while( rand_n > f_adapt_acu ):
            f_adapt_acu += f_ad[i]
            i += 1
        ind2 = i - 1
        if(ind2 != ind1): 
            fin = True

    return ind1, ind2


def selection_random_library(f_adapta):
    
    #create array of index per individual
    indexes = np.arange(f_adapta.shape[0]) 
    
    ind1 = random.choices(indexes, weights = f_adapta)[0]
    ind2 = random.choices(indexes, weights = f_adapta)[0]

    while (ind1 == ind2):
        ind2 = random.choices(indexes, weights = f_adapta)[0]

    return ind1, ind2
