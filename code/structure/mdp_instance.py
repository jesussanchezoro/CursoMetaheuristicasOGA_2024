
def read_instance(path):
    with open(path, "r") as f:
        n, p = map(int, f.readline().strip().split())
        instance = dict()
        instance['name'] = path.split('/')[-1]
        instance['n'] = n
        instance['p'] = p
        instance['d'] = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                u, v, d = f.readline().strip().split()
                u = int(u)
                v = int(v)
                d = float(d)
                instance['d'][u][v] = d
                instance['d'][v][u] = d
        return instance
