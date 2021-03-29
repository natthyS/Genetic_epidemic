import math 

def get_surv_and_dead(p_sup, N_indv):
    if int((1-p_sup) *N_indv)%2 == 0:
        N_ind_dead = int((1-p_sup) *N_indv) 
    else: 
        N_ind_dead = int((1-p_sup) *N_indv)+1
    
    N_ind_sup = N_indv - N_ind_dead

    return N_ind_sup, N_ind_dead


def get_len_parameters(precision = 2, intervalo = (0,1 )):
    l_inf, l_sup = intervalo
    len_param = math.log(((l_sup-l_inf)*(10**precision)),2)
    len_param = math.ceil(len_param)

    return len_param



