import random
import time
import structure.mdp_solution as mdp_s
import copy


def alg_constructive(instance, constructive, iters, alpha=None):
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


def grasp_pr(instance, constructive, local_search, iters, alpha):
    best_sol = None
    start = time.time()
    elite_set = []
    elite_set_sols = set()
    for i in range(iters):
        s = constructive(instance, alpha)
        local_search(s)
        if not best_sol or mdp_s.is_better(s, best_sol):
            best_sol = copy.deepcopy(s)
        if s['s'] not in elite_set_sols:
            elite_set.append(s)
            elite_set_sols.add(frozenset(s['s']))
    for i in range(len(elite_set)):
        for j in range(i+1, len(elite_set)):
            # path_sol = random_pr(elite_set[i], elite_set[j])
            path_sol = greedy_pr(elite_set[i], elite_set[j])
            if path_sol:
                local_search(path_sol)
                if mdp_s.is_better(path_sol, best_sol):
                    best_sol = copy.deepcopy(path_sol)
    seconds = time.time() - start
    return best_sol, seconds


def random_pr(initiating, guiding):
    path_sol = copy.deepcopy(initiating)
    to_insert = list(guiding['s'] - initiating['s'])
    to_remove = list(initiating['s'] - guiding['s'])
    random.shuffle(to_insert)
    random.shuffle(to_remove)
    best_sol = None
    for i in range(len(to_insert)):
        mdp_s.interchange(path_sol, to_remove[i], to_insert[i])
        if not best_sol or mdp_s.is_better(path_sol, best_sol):
            best_sol = copy.deepcopy(path_sol)
    return best_sol


def greedy_pr(initiating, guiding):
    path_sol = copy.deepcopy(initiating)
    to_insert = list(guiding['s'] - initiating['s'])
    to_remove = list(initiating['s'] - guiding['s'])
    best_sol = None
    more_changes = True
    while more_changes:
        best_in_path = None
        i_sel = -1
        j_sel = -1
        for i in range(len(to_insert)):
            for j in range(len(to_remove)):
                mdp_s.interchange(path_sol, to_remove[j], to_insert[i])
                if not best_in_path or mdp_s.is_better(path_sol, best_in_path):
                    best_in_path = copy.deepcopy(path_sol)
                    i_sel = i
                    j_sel = j
                mdp_s.interchange(path_sol, to_insert[i], to_remove[j])
        del to_remove[j_sel]
        del to_insert[i_sel]
        if best_in_path['s'] == guiding['s']:
            more_changes = False
        else:
            path_sol = copy.deepcopy(best_in_path)
            if not best_sol or mdp_s.is_better(best_in_path, best_sol):
                best_sol = copy.deepcopy(best_in_path)
    return best_sol



def greedy_randomized_pr(initiating, guiding, alpha):
    path_sol = copy.deepcopy(initiating)
    to_insert = list(guiding['s'] - initiating['s'])
    to_remove = list(initiating['s'] - guiding['s'])
    best_sol = None
    more_changes = True
    while more_changes:
        cl = []
        g_min = 0x3f3f3f3f
        g_max = 0
        for i in range(len(to_insert)):
            for j in range(len(to_remove)):
                mdp_s.interchange(path_sol, to_remove[j], to_insert[i])
                g_min = min(g_min, path_sol['of'])
                g_max = max(g_max, path_sol['of'])
                cl.append((path_sol['of'], i, j))
                mdp_s.interchange(path_sol, to_insert[i], to_remove[j])
        threshold = g_max - alpha * (g_max - g_min)
        sel_idx = random.randint(0, len(cl)-1)
        while cl[sel_idx][0] < threshold:
            sel_idx = (sel_idx + 1) % len(cl)
        u = to_remove[cl[sel_idx][2]]
        v = to_insert[cl[sel_idx][1]]
        mdp_s.interchange(path_sol, u, v)
        del to_remove[cl[sel_idx][2]]
        del to_insert[cl[sel_idx][1]]
        if path_sol['s'] == guiding['s']:
            more_changes = False
        else:
            if not best_sol or mdp_s.is_better(path_sol, best_sol):
                best_sol = copy.deepcopy(path_sol)
    return best_sol


def vns(instance, k_step, k_max, iters, constructive, local_search):
    best_sol = constructive(instance)
    local_search(best_sol)
    start_time = time.time()
    for _ in range(iters):
        k = k_step
        while k <= k_max:
            shake_sol = shake(k, best_sol)
            local_search(shake_sol)
            best_sol, k = neighborhood_change(shake_sol, best_sol, k, k_step)
    seconds = time.time() - start_time
    return best_sol, seconds


def neighborhood_change(shake_sol, best_sol, k, k_step):
    if mdp_s.is_better(shake_sol, best_sol):
        return shake_sol, k_step
    else:
        return best_sol, k+k_step


def shake(k, sol):
    n = sol['i']['n']
    shake_sol = copy.deepcopy(sol)
    selected = list(sol['s'])
    unselected = [v for v in range(n) if v not in sol['s']]
    sel_idx = random.sample(range(len(selected)), k)
    unsel_idx = random.sample(range(len(unselected)), k)
    for i in range(k):
        mdp_s.interchange(shake_sol, selected[sel_idx[i]], unselected[unsel_idx[i]])
    return shake_sol





