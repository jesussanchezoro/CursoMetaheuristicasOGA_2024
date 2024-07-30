import algorithms.constructives as mdp_const
import time
import structure.mdp_solution as mdp_s
import copy

def alg_constructive(instance, constructive, iters, alpha = None):
    best_sol = None
    start = time.time()
    for i in range(iters):
        if alpha:
            s = constructive(instance, alpha)
        else:
            s = constructive(instance)
        if not best_sol or mdp_s.is_better(s, best_sol):
            best_sol = copy.deepcopy(s)
    seconds = time.time() - start
    return best_sol, seconds


def grasp(instance, constructive, local_search, iters, alpha):
    best_sol = None
    start = time.time()
    for i in range(iters):
        s = constructive(instance, alpha)
        local_search(s)
        if not best_sol or mdp_s.is_better(s, best_sol):
            best_sol = copy.deepcopy(s)
    seconds = time.time() - start
    return best_sol, seconds