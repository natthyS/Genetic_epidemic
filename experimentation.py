from genetic.main import main_loop
import pandas as pd
from utils.plot_utils import plot_adaptacion, plot_dead, plot_model
import numpy as np
import random
import utils.utils as utils
import argparse
import os
import logging
from genetic.genetic import f_decodi
log_format = '(line %(lineno)d %(filename)s) | [%(levelname)s]: %(message)s'
logging.basicConfig(format= log_format, level=logging.INFO)

# Numero de pruebas por experiments
N_TEST = 2
GRAFI = 5

#Parametros para ajustar los cromosomas
precision = 2       # precision for decoding one parameter
n_p = 4             # número de parametros a ajustar
t_p = utils.get_len_parameters(precision)  # tamaño del parámetro(bits/Tamaño)

#Parametros del modelo teorico
I0 = 1                              # numero inicial de infectados

#Parametros del modelo teorico
Np_AG = 3228233                     # Población estimada de Quito
# vector inicial para resolver ecuaciones diferenciales
y_initial = [Np_AG, 0, I0, 0, 0] 


def execute_experiment(data_name, excel_experiments, sheet, output_dir, base_name):
    # Load the data from .csv
    df = pd.read_csv("stuff/data/data_norm_2020.csv")
    data = df[data_name]
    data = np.clip(data,0, float('inf'))
    data = np.cumsum(data)

    # Load the excel experiment sheet
    experiments = pd.read_excel(excel_experiments,
                        sheet_name = sheet)



    for index, row in experiments.iterrows():
        logging.info(" Executing Experiment: {}".format(row.N_experiment))

        # Plot the best adaptation per generation
        parametros = {
        'inds' :  row.N_indv,
        'steps' : row.N_pasos,
        'pr' :    row.p_repro,
        'pm' :    row.p_muta,
        'nsurv' : row.n_surv,
        'i0' :    row.I0,
        'xmode' : row.cross_mode,
        'mutamode' : row.muta_mode,
        'select_mode' : row.select_mode,
        'y_initial': y_initial,
        'n_p' : n_p, 
        't_p' : t_p
        }

        mejor_adaptacions = []
        jaccarI_list = []
        jaccarP_list = []
        sorsP_list = []

        mej_adapta_bt_execution = -1
        execution_list = []

        for i in range(N_TEST):

            #Execute the main loop algorithm
            mejor_individuo, meta_results = main_loop(data, parametros)

            if max(meta_results['l_mej_adap']) > mej_adapta_bt_execution:
                mejor_ind_bt_execution = mejor_individuo

            experiment = pd.DataFrame({
                "iteration" : [(i+1) * GRAFI for i in range(len(meta_results['l_mej_adap']))],
                "best_adapta" : meta_results['l_mej_adap'],
                "JaccarI" : meta_results['l_jaccard_ind'],
                "JaccarP" : meta_results['l_jaccard_pop'],
                "SoresP" : meta_results['l_sorensen_pop']
            })
            experiment['execution'] = i
            experiment.to_csv(os.path.join(output_dir, "experiment_{}_execution_{}_iterations.csv".format(row.N_experiment, i)), index = False) 

            execution_list.append(experiment)

            mejor_adaptacions.append(max(meta_results['l_mej_adap']))
            jaccarI_list.append(meta_results['l_jaccard_ind'][-1])
            jaccarP_list.append(meta_results['l_jaccard_pop'][-1])
            sorsP_list.append(meta_results['l_sorensen_pop'][-1])                                    ,                                    

            logging.info('Mejor adaptación : {}'.format(max(meta_results['l_mej_adap'])))


        sigma, gamma, beta, f = f_decodi(mejor_ind_bt_execution, 0, 1, t_p, n_p)
        mean_mej_adapta = np.mean(mejor_adaptacions)
        mean_jaccarI = np.mean(jaccarI_list)
        mean_jaccarP = np.mean(jaccarP_list)
        mean_sorsP = np.mean(sorsP_list)

        # saving in the same excel

        experiments.at[index,'best_adapta'] = mean_mej_adapta
        experiments.at[index,'JaccI'] = mean_jaccarI
        experiments.at[index,'JaccP'] = mean_jaccarP
        experiments.at[index,'SorsP'] = mean_sorsP
        experiments.at[index,'sigma'] = sigma
        experiments.at[index,'gamma'] = gamma
        experiments.at[index,'beta'] = beta
        experiments.at[index,'f'] = f
        # experiments.at[index,'indv'] = str(mejor_ind_bt_execution)

        experiment_best_executions = pd.DataFrame({
            "execution" : [i for i in range(len(mejor_adaptacions))],
            "best_adapta" : mejor_adaptacions,
            "JaccarI" : jaccarI_list,
            "JaccarP" : jaccarP_list,
            "SoresP" : sorsP_list        })

        experiment_best_executions.to_csv(os.path.join(output_dir, "experiment_{}_best_executions.csv".format(row.N_experiment)), index = False)

        experiment_several_iteration_per_execution = pd.concat(execution_list)
        experiment_several_iteration_per_execution.to_csv(os.path.join(output_dir, "experiment_{}_total_iterations.csv".format(row.N_experiment)), index = False) 

    experiments.to_csv(os.path.join(output_dir, "{}_results.csv".format(base_name)), index = False)
    
    # save_meta_results(meta_results)                 

if __name__ == '__main__':

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Execute a set of experiments')
    parser.add_argument('--dataname', required=False,
                        default="Pichincha",
                        metavar="Province Name",
                        help='Province name to be tested')
    parser.add_argument('--excel', required=True,
                        metavar="/path/to/experiment_sheet.xlsx",
                        help="Path to experiment sheet to be tested")
    parser.add_argument('--sheet', required=True,
                        metavar="Name of the sheet to be tested",
                        help="Name of the sheet to be tested")
    args = parser.parse_args()

    #
    base_name_excel = os.path.basename(os.path.normpath(args.excel))
    base_name_excel = base_name_excel.split(".")[0]
    output_dir = os.path.join("stuff/experiments/",base_name_excel + "_results_sheet_" + args.sheet)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    execute_experiment(args.dataname, args.excel, args.sheet, output_dir, base_name_excel)

    