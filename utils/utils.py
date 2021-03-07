def get_surv_and_dead(p_sup, N_indv):
    if int((1-p_sup) *N_indv)%2 == 0:
        N_ind_dead = int((1-p_sup) *N_indv) 
    else: 
        N_ind_dead = int((1-p_sup) *N_indv)+1
        N_ind_sup = N_indv - N_ind_dead

    return N_ind_sup, N_ind_dead

