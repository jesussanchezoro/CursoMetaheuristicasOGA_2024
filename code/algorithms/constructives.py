import structure.mdp_solution as mdp_s
import random
import math

# =======================================
# CONSTRUCTIVE 1: RANDOM CONSTRUCTIVE
# =======================================
def construct_random(instance):
    n = instance['n']
    p = instance['p']
    sol = mdp_s.create_solution(instance)
    sol['s'] = set(random.sample(range(n), p))
    mdp_s.evaluate_solution(sol)
    return sol


# =======================================
# CONSTRUCTIVE 2: GREEDY CONSTRUCTIVE (NAIVE)
# =======================================
def construct_greedy(instance):
    n = instance['n']
    p = instance['p']
    sol = mdp_s.create_solution(instance)
    s1, s2 = select_two_furthest(instance)
    mdp_s.add(sol, s1)
    mdp_s.add(sol, s2)
    cl = [v for v in range(n) if v not in sol['s']]
    while len(sol['s']) < p:
        next_idx, d = select_furthest(sol, cl)
        mdp_s.add(sol, cl[next_idx], d)
        del cl[next_idx]
    return sol


# =======================================
# CONSTRUCTIVE 3: GREEDY CONSTRUCTIVE (EFFICIENT)
# =======================================

def construct_greedy_efficient(instance):
    n = instance['n']
    p = instance['p']
    sol = mdp_s.create_solution(instance)
    s1, s2 = select_two_furthest(instance)
    mdp_s.add(sol, s1)
    mdp_s.add(sol, s2)
    cl = []
    next_idx = -1
    max_dist = 0
    for v in range(n):
        if v not in sol['s']:
            d = mdp_s.dist_to_sol(sol, v)
            cl.append([v, d])
            if d > max_dist:
                max_dist = d
                next_idx = v
    while len(sol['s']) < p:
        v, d = cl[next_idx]
        mdp_s.add(sol, v, d)
        del cl[next_idx]
        next_idx = -1
        max_dist = 0
        for c_idx in range(len(cl)):
            c = cl[c_idx]
            c[1] += sol['i']['d'][c[0]][v]
            if c[1] > max_dist:
                max_dist = c[1]
                next_idx = c_idx
    return sol


def select_two_furthest(instance):
    n = instance['n']
    max_dist = 0
    s1 = -1
    s2 = -1
    for u in range(n):
        for v in range(u+1, n):
            if instance['d'][u][v] > max_dist:
                max_dist = instance['d'][u][v]
                s1 = u
                s2 = v
    return s1, s2


def select_furthest(sol, cl):
    furthest = -1
    max_dist = 0
    for c_idx in range(len(cl)):
        d = mdp_s.dist_to_sol(sol, cl[c_idx])
        if d > max_dist:
            max_dist = d
            furthest = c_idx
    return furthest, max_dist






# =======================================
# CONSTRUCTIVE 4: GRASP CONSTRUCTIVE NAIVE
# =======================================
def construct_grasp_naive(instance, alpha):
    alpha = alpha if alpha >= 0 else random.uniform(0, 1)
    n = instance['n']
    p = instance['p']
    sol = mdp_s.create_solution(instance)
    first = random.randint(0, n-1)
    mdp_s.add(sol, first)
    cl, g_max, g_min = create_cl(sol)
    while len(sol['s']) < p:
        rcl = create_rcl(sol, cl, alpha, g_max, g_min)
        next_idx = rcl[random.randint(0, len(rcl)-1)]
        mdp_s.add(sol, cl[next_idx][1], cl[next_idx][0])
        del cl[next_idx]
        g_min, g_max = update_cl(sol, cl)
    return sol


def update_cl(sol, cl):
    g_min = 0x3f3f3f3f
    g_max = 0
    for c in cl:
        c[0] = mdp_s.dist_to_sol(sol, c[1])
        g_min = min(g_min, c[0])
        g_max = max(g_max, c[0])
    return g_min, g_max

def create_cl(sol):
    cl = []
    g_min = 0x3f3f3f3f
    g_max = 0
    n = sol['i']['n']
    for u in range(n):
        if u not in sol['s']:
            d = mdp_s.dist_to_sol(sol, u)
            g_min = min(g_min, d)
            g_max = max(g_max, d)
            cl.append([d, u])
    return cl, g_max, g_min


def create_rcl(sol, cl, alpha, g_max, g_min):
    threshold = g_max - alpha * (g_max - g_min)
    rcl = [c_idx for c_idx in range(len(cl)) if cl[c_idx][0] >= threshold]
    return rcl


# =======================================
# CONSTRUCTIVE 5: GRASP CONSTRUCTIVE EFFICIENT
# =======================================
def construct_grasp_efficient(instance, alpha):
    alpha = alpha if alpha >= 0 else random.uniform(0,1)
    n = instance['n']
    p = instance['p']
    sol = mdp_s.create_solution(instance)
    first = random.randint(0, n-1)
    mdp_s.add(sol, first)
    cl, g_max, g_min = create_cl(sol)
    while len(sol['s']) < p:
        threshold = g_max - alpha * (g_max - g_min)
        next_idx = random.randint(0, len(cl)-1)
        while cl[next_idx][0] < threshold:
            next_idx = (next_idx + 1) % len(cl)
        mdp_s.add(sol, cl[next_idx][1], cl[next_idx][0])
        del cl[next_idx]
        g_min, g_max = update_cl(sol, cl)
    return sol


# =======================================
# CONSTRUCTIVE 5: GRASP CONSTRUCTIVE EFFICIENT
# =======================================
def construct_grasp_rg(instance, alpha):
    alpha = alpha if alpha >= 0 else random.uniform(0,1)
    n = instance['n']
    p = instance['p']
    sol = mdp_s.create_solution(instance)
    first = random.randint(0, n-1)
    mdp_s.add(sol, first)
    cl = [v for v in range(n) if v != first]
    while len(sol['s']) < p:
        n_eval = int(math.ceil(alpha * len(cl)))
        next_idx = -1
        best_g = 0
        for _ in range(n_eval):
            c_idx = random.randint(0, len(cl)-1)
            d = mdp_s.dist_to_sol(sol, cl[c_idx])
            if d > best_g:
                next_idx = c_idx
                best_g = d
        mdp_s.add(sol, cl[next_idx], best_g)
        del cl[next_idx]
    return sol