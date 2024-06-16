
import os
import time
from collections import deque
import queue
def readData(path2input='E:/src code 2/python 2/tulkh/TULKH/input.txt'):
    with open(path2input,'r') as f:
        data = f.read().split('\n')
        N, K = map(lambda x: int(x), data[0].split(' '))
        d = list(map(lambda x: int(x), data[1].split(' ')[:N]))
        t = [list(map(lambda x: int(x), i.split(' ')[:N+1])) for i in data[2:N+3]]
    return N, K, d, t
def creat_cost(N, d, t):
    for i in range(N + 1):
        for j in range(1, N + 1):
            if i != j:
                t[i][j] += d[j - 1] 

    return t
import numpy as np




N, K, d, t = None, None, None, None





def vertex2ij(v):
    return v // (N + 1), v % (N+1)
def ij2vertex(i, j):
    return i * (N + 1) + j 


             

from ortools.sat.python import cp_model

def cp():
    weights = np.array(t).reshape(-1)
    model = cp_model.CpModel()
    vars = []
    for i in range(N+1):
        for j in range(N+1):
            if i != j:
                var = model.new_int_var(0, 1, str(ij2vertex(i,j)))
                vars.append(var)
            else:
                var = model.new_int_var(0, 0, str(ij2vertex(i,j)))
                vars.append(var)
    def loss(vars, ws):
        tt_loss = 0
        for v, z in zip(vars, ws):
            tt_loss += v*z
        return -tt_loss
    model.maximize(loss(vars,weights))
    #thêm ràng buộc
    # trừ đỉnh 0, mọi đỉnh khác chỉ được đến/ đi bởi 1 đỉnh
    def total_edge_in(vars, i_of_vertext, j_of_orther_vertexts):
        total = 0
        for j in j_of_orther_vertexts:
            total += vars[ij2vertex(j, i_of_vertext)]
        return total
    def total_edge_out(vars, i_of_vertext, j_of_orther_vertexts):
        total = 0
        for j in j_of_orther_vertexts:
            total += vars[ij2vertex(i_of_vertext, j)]
        return total
    def total_edge(vars, i_of_orther_vertexts):
        total = 0
        for i in i_of_orther_vertexts:
            for j in i_of_orther_vertexts:
                total += vars[ij2vertex(i, j)]
        return total
    #số cạnh vào và ra các đỉnh khác 0 bằng 1.
    for i in range(1, N+1):
        model.add(total_edge_in(vars, i, range(N+1)) == 1)
        model.add(total_edge_out(vars, i, range(N+1)) == 1)
    # số cạnh vào và ra ở 0 bằng nhau
    model.add(total_edge_out(vars, 0, range(N+1)) - total_edge_in(vars, 0, range(N+1)) == 0)
    # tổng số chu trình nhỏ hơn bằng K
    model.add(total_edge_out(vars, 0, range(N+1)) <= K)
    # tất cả chu trình phải đi qua đỉnh 0
    model.add(total_edge(vars, range(N+1)) - total_edge_out(vars, 0, range(N+1)) == N)

    solver = cp_model.CpSolver()
    status = solver.solve(model)

    graph = [[] for _ in range(N+1)]
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"Maximum of objective function: {solver.objective_value}\n")
        for id, var in enumerate(vars):
            print(f"{vertex2ij(id)} = {solver.value(var)}")
            if solver.value(var) == 1:
                i,j = vertex2ij(id)
                graph[i].append(j)
    print(graph)
    paths = []
    stack = graph[0].copy()
    tmp = [0]
    while len(stack) > 0:
        v = stack.pop()
        tmp.append(v)
        if v == 0:
            paths.append(tmp)
            tmp = [0]
            continue
        
        for i in graph[v]:
            stack.append(i)
    print(paths)






    

for inp in ['data_5_2.txt', 'data_10_5.txt']:#os.listdir('data'):, 'data_10_5.txt', 'data_20_10.txt', 'data_50_25.txt'
    inp = os.path.join('data',inp)
    with open('log_output.txt', 'a+') as f:
        f.write(f"{inp}\n")
    with open('output.txt','a') as f:
        f.write(f"{inp}\n")
    start_time = time.time()

    N, K, d, t = readData(inp)

    t = creat_cost(N, d, t)

    cp()