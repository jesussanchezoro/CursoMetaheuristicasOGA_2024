
def create_solution(instance):
    sol = dict()
    sol['i'] = instance
    sol['s'] = set()
    sol['of'] = 0
    return sol


def add(sol, u, d=None):
    sol['s'].add(u)
    if d:
        sol['of'] += d
    else:
        for s in sol['s']:
            if s != u:
                sol['of'] += sol['i']['d'][s][u]
    ## NOT EFFICIENT
    ###############################
    # evaluate_solution(sol)
    ###############################


def interchange(sol, u, v):
    # O(n)
    sol['s'].remove(u)
    for s in sol['s']:
        sol['of'] -= sol['i']['d'][s][u]
        sol['of'] += sol['i']['d'][s][v]
    sol['s'].add(v)
    ###############################
    ## NOT EFFICIENT
    ###############################
    ## O(n^2)
    # sol['s'].remove(u)
    # sol['s'].add(v)
    # evaluate_solution(sol)
    ###############################


def dist_to_sol(sol, u):
    d = 0
    for s in sol['s']:
        d += sol['i']['d'][s][u]
    return d


def evaluate_solution(sol):
    sol['of'] = 0
    for s1 in sol['s']:
        for s2 in sol['s']:
            if s1 < s2:
                sol['of'] += sol['i']['d'][s1][s2]


def find_critical(sol):
    min_dist = 0x3f3f3f3f
    critical = -1
    for u in sol['s']:
        d = dist_to_sol(sol, u)
        if d < min_dist:
            min_dist = d
            critical = u
    return critical


def is_better(sol1, sol2):
    return sol1['of'] > sol2['of']


def print_sol(sol):
    print("SELECTED: "+str(sol['s']))
    print("OF: "+str(sol['of']))