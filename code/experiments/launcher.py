import random

import algorithms.constructives as mdp_const
import algorithms.improvements as mdp_imp
import structure.mdp_solution as mdp_s
import structure.mdp_instance as mdp_i
import algorithms.metaheuristics as mdp_mh
import os

if __name__ == '__main__':
    path = "../instances/"
    results_path = "output.csv"

    # constructive = mdp_const.construct_greedy
    # constructive = mdp_const.construct_grasp_naive
    # constructive = mdp_const.construct_grasp_efficient
    constructive = mdp_const.construct_grasp_rg

    # local_search = mdp_imp.ls_1x1
    local_search = mdp_imp.advanced_ls_1x1

    alpha = -1
    iters = 100

    with open(results_path, 'w') as f:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".txt"):
                    random.seed(13)
                    instance = mdp_i.read_instance(os.path.join(root, file))
                    print(instance['name'], end=" ")
                    # best, seconds = mdp_mh.alg_constructive(instance, constructive, iters)
                    # best, seconds = mdp_mh.alg_constructive(instance, constructive, iters, alpha)
                    best, seconds = mdp_mh.grasp(instance, constructive, local_search, iters, alpha)
                    print("\t{:.2f}".format(best['of']) + "\t{:.2f}".format(seconds))
                    f.write(instance['name'] + "\t{:.2f}".format(best['of']) + "\t{:.2f}".format(seconds) + "\n")