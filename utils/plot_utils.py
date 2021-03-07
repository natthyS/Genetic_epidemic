from os.path import join
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
        file_name += "_{}:{}".format(key,value)

    file_name += ".jpg"

    plt.savefig(os.path.join(path_to_save,file_name))
    plt.close()