import numpy as np
from sklearn.metrics import jaccard_score

def jaccard_index_ind(current_population, index):

    # indentifica el mejor individuo de la población (mayor adaptación por generación)
    individual = current_population[index]
    # elimina el mejor individuo de la población
    current_population_wt_best = np.delete(current_population, index, axis = 0)
    # longitud de población sin mejor individuo
    len_aux_pop = current_population_wt_best.shape[0]
    # crea población auxiliar con mejor individuo del tamaño de la población sin mejor individuo
    arrays = [individual for _ in range(len_aux_pop)]
    aux_pop = np.stack(arrays, axis=0)
    # calcula el jaccard_score entre la población actual y la población auxiliar
    j_score = jaccard_score(aux_pop, current_population_wt_best, average='samples')

    return j_score


def jaccard_index_population(current_population):
    
    # Obtengo el numero de individuos en la poblacion actual
    num_indv = current_population.shape[0]

    # Get the jaccard_index per each pair of individuals
    mean_jaccard = 0
    counter = 0
    for i in range(num_indv):
        for j in range(num_indv):
            if (i != j) and (i > j):
                mean_jaccard += jaccard_score(current_population[i],current_population[j])
                counter += 1

    mean_jaccard = mean_jaccard / counter

    return mean_jaccard


def sorensen_index_population(current_population):

    # Obtengo el numero de individuos en la poblacion actual
    num_indv = current_population.shape[0]

    # Get the sorensen_index per each pair of individuals
    mean_sorensen = 0
    counter = 0
    for i in range(num_indv):
        for j in range(num_indv):
            if (i != j) and (i > j):
                jaccard_metric = jaccard_score(current_population[i],current_population[j])
                mean_sorensen += (2*jaccard_metric) / (1 + jaccard_metric)
                counter += 1

    mean_sorensen = mean_sorensen / counter

    return mean_sorensen