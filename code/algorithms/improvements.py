import random

import structure.mdp_solution as mdp_s

def ls_1x1(sol):
    improve = True
    while improve:
        improve = try_improve_ls1x1(sol)


def try_improve_ls1x1(sol):
    n = sol['i']['n']
    selected = list(sol['s'])
    random.shuffle(selected)
    unselected = [v for v in range(n) if v not in sol['s']]
    random.shuffle(unselected)
    for s in selected:
        for us in unselected:
            of_prev = sol['of']
            mdp_s.interchange(sol, s, us)
            if sol['of'] > of_prev:
                return True
            else:
                mdp_s.interchange(sol, us, s)
    return False


def advanced_ls_1x1(sol):
    improve = True
    while improve:
        improve = try_improve_advanced_ls1x1(sol)


def try_improve_advanced_ls1x1(sol):
    n = sol['i']['n']
    s = mdp_s.find_critical(sol)
    unselected = [v for v in range(n) if v not in sol['s']]
    random.shuffle(unselected)
    for us in unselected:
        of_prev = sol['of']
        mdp_s.interchange(sol, s, us)
        if sol['of'] > of_prev:
            return True
        else:
            mdp_s.interchange(sol, us, s)
    return False