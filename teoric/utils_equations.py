def Diff_Equ_2(y_t, t, sigma, gamma, beta, f):
    S, E, I, R, D = y_t
    Nn = S+E+I+R
    dS_dt = -sigma*S
    dE_dt = -gamma*E*I + sigma*S
    dI_dt = gamma*beta*(I**2) -gamma*I
    dR_dt = (1.0-f)*gamma*I
    dD_dt = f*gamma*I
    return [dS_dt, dE_dt, dI_dt, dR_dt, dD_dt]


def Diff_Equ(y_t, t, sigma, gamma, beta, f):
    S, E, I, R, D = y_t
    Nn = S+E+I+R
    dS_dt = -beta*(S/Nn)*I
    dE_dt = +beta*(S/Nn)*I - sigma*E
    dI_dt = sigma*E - gamma*I
    dR_dt = (1.0-f)*gamma*I
    dD_dt = f*gamma*I
    return [dS_dt, dE_dt, dI_dt, dR_dt, dD_dt]

