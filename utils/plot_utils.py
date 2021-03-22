from os.path import join
from genetic.genetic import f_decodi
from teoric.utils_equations import Diff_Equ
from genetic.main import x_min, x_max, t_p, n_p
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import os 

def plot_adaptacion(list_generations, list_mej_adap,**parameters):
    path_to_save = "stuff/figures/"
    if not os.path.exists(path_to_save):
        os.mkdir(path_to_save)

    plt.plot(list_generations, list_mej_adap, "bp-", label = 'Valor de Adaptación según Número de Generación')
    plt.legend()

    
    file_name = "adapt"

    for key, value in parameters.items():
        file_name += "_{}-{}".format(key,value)

    file_name += ".jpg"

    plt.savefig(os.path.join(path_to_save,file_name))
    plt.close()


def plot_model(mejor_individuo, y_initial, data, **parameters):
    path_to_save = "stuff/figures/"
    if not os.path.exists(path_to_save):
        os.mkdir(path_to_save)

    dias = list(range(len(data.index)))
    sigma, gamma, beta, f = f_decodi(mejor_individuo, x_min, x_max, t_p, n_p)
    Solve = odeint(Diff_Equ, y_initial, dias, args=(sigma, gamma, beta, f) )
    S,E,I,R,D = [Solve[:,i] for i in range(5)]

    plt.plot(dias, S, 'k--', label="Susceptible")
    plt.plot(dias, E, label="Exposed")
    plt.plot(dias, I, '--', label="Infectious")
    plt.plot(dias, R, label="Recovered")
    plt.plot(dias, D, label="Deceased")
    plt.title('THEORETICAL_MODEL \n sigma: {:.2f} gamma: {:.2f} beta: {:.2f} f: {:.2f}'.format(sigma, gamma, beta, f))
    plt.legend(loc='upper right')
    plt.show()
    
    
    file_name = "Model_plots"

    for key, value in parameters.items():
        file_name += "_{}-{}".format(key,value)

    file_name += ".jpg"

    plt.savefig(os.path.join(path_to_save,file_name))
    plt.close()

def plot_dead(mejor_individuo, y_initial, data, **parameters):
    path_to_save = "stuff/figures/"
    if not os.path.exists(path_to_save):
        os.mkdir(path_to_save)

    dias = list(range(len(data.index)))
    sigma, gamma, beta, f = f_decodi(mejor_individuo, x_min, x_max, t_p, n_p)
    Solve = odeint(Diff_Equ, y_initial, dias, args=(sigma, gamma, beta, f) )
    S,E,I,R,D = [Solve[:,i] for i in range(5)]

    
    plt.plot(dias, D, label="Deceased")
    plt.plot(dias, data , label = 'Acumulados-Normal Pichincha(D. Robalino)')
    plt.title('DECEASED \n sigma: {:.2f} gamma: {:.2f} beta: {:.2f} f: {:.2f}'.format(sigma, gamma, beta, f))
    plt.legend()
    plt.show()
    
    file_name = "D_plots"

    for key, value in parameters.items():
        file_name += "_{}-{}".format(key,value)

    file_name += ".jpg"

    plt.savefig(os.path.join(path_to_save,file_name))
    plt.close()