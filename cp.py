
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
from ortools.sat.python import cp_model

def solve_cp_model(N, K, t):
    model = cp_model.CpModel()

    # Define variables
    x = [[[model.NewBoolVar(f'x[{i},{j},{k}]') for k in range(K)] for j in range(N+1)] for i in range(N+1)]
    p_ik = [[model.NewIntVar(0, 10000000, f'p_{i}{k}') for k in range(K)] for i in range(N+1)]
    max_sub_x = model.NewIntVar(0, 10000000, 'max_sub_x')


    # Khởi tạo kích thước ma trận
    num_points = N  # Số điểm tối đa dựa trên danh sách chu trình (0 đến 10)
    num_vehicles = K  # Số phương tiện


    if False:#debug
        # Tạo ma trận 3 chiều với tất cả các giá trị ban đầu là 0
        x = [[[0 for _ in range(num_vehicles)] for _ in range(num_points  + 1)] for _ in range(num_points + 1)]

        # Danh sách các chu trình của các phương tiện
        cycles = [
            [0, 1, 9, 0],
            [0, 2, 7, 8, 0],
            [0, 3, 4, 0],
            [0, 5, 10, 0],
            [0, 6, 0]
        ]

        # Điền giá trị vào ma trận x
        for k, cycle in enumerate(cycles):
            for i in range(len(cycle) - 1):
                from_point = cycle[i]
                to_point = cycle[i + 1]
                x[from_point][to_point][k] = 1
        p_ik = [[0 for k in range(K)] for i in range(N+1)]
        for k, cycle in enumerate(cycles):
            for id, i in enumerate(cycle):
                p_ik[i][k] = id + 1
        print(p_ik)

    def total_in(x, N, K, j):
        total = 0
        for i in range(N+1):
            for k in range(K):
                total += x[i][j][k]
        return total

    def total_out_from_0(x, N, k):
        total = 0
        for j in range(1, N+1):
            total += x[0][j][k]
        return total
    def total_out_to_0(x, N, k):
        total = 0
        for i in range(1, N+1):
            total += x[i][0][k]
        return total
    

    
    def total_in_ik(x, N, i, k):
        total = 0
        for j in range(N+1):
            total += x[i][j][k]
        return total
    def total_out_ik(x, N, i, k):
        total = 0
        for j in range(N+1):
            total += x[j][i][k]
        return total
    
    def total_time_of_k(x, N, k, t):
        total = 0
        for i in range(N + 1):
            for j in range(N + 1):
                total += x[i][j][k] * t[i][j]
        return total
    
    for i in range(N+1):
        for k in range(K):
            # if not x[i][i][k] == 0:
            #     print('if not x[i][i][k] == 0:')
            #     exit(0)
            model.Add(x[i][i][k] == 0)
    # Define constraints
    for j in range(1, N + 1):
            # if not total_in(x, N, K, j) == 1:
            #     print('total_in(x, N, K, j) == 1')
            #     exit(0)
            model.Add(total_in(x, N, K, j) == 1)

    for k in range(K):    
        # if not total_out_from_0(x, N, k) == 1:
        #     print('total_out_from_0(x, N, k) == 1')
        #     exit(0)
        model.Add(total_out_from_0(x, N, k) == 1) 

    for k in range(K):    
        # if not total_out_to_0(x, N, k) == 1:
        #     print('total_out_to_0(x, N, k) == 1')
        #     exit(0)
        model.Add(total_out_to_0(x, N, k) == 1) 

    for i in range(1,N+1):
        for k in range(K):
            # if not total_out_ik(x, N, i, k) - total_in_ik(x, N, i, k) == 0:
            #     print('total_out_ik(x, N, i, k) - total_in_ik(x, N, i, k) == 0')
            #     exit(0)            
            model.Add(total_out_ik(x, N, i, k) - total_in_ik(x, N, i, k) == 0) 


    for j in range(1, N+1):
        for k in range(K):
            for i in range(1,N+1):
                # if not 10000000*(x[i][j][k] - 1) + p_ik[i][k] + 1 <= p_ik[j][k]:
                #     print('10000000*(x[i][j][k] - 1) + p_ik[i][k] + 1 <= p_ik[j][k]:')
                #     print(i,j,k)
                #     print(x[i][j][k], p_ik[i][k], p_ik[j][k])
                #     exit(0)
                model.Add(10000000*(x[i][j][k] - 1) + p_ik[i][k] + 1 <= p_ik[j][k]) 


    for k in range(K):
        model.Add(max_sub_x >= total_time_of_k(x, N, k, t))

    # Minimize max_sub_x_constraint
    model.Minimize(max_sub_x)

    # Create solver and solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        solution = [[[solver.Value(x[i][j][k]) for k in range(K)] for j in range(N+ 1)] for i in range(N+1)]
        print([[solver.Value(p_ik[i][k]) for k in range(K)] for i in range(N+1)])
        return solver.Value(max_sub_x), solution
    else:
        print("No optimal solution found.")
        return None





for file in ['data_5_2.txt']:#os.listdir('data'):, 'data_10_5.txt', 'data_20_10.txt', 'data_50_25.txt'
    st = time.time()
    inp = os.path.join('data',file)
    with open('log_output.txt', 'a+') as f:
        f.write(f"{inp}\n")
    with open('output.txt','a') as f:
        f.write(f"{inp}\n")
    start_time = time.time()

    N, K, d, t = readData(inp)
    # print(t)
    t = creat_cost(N, d, t)
    # st = time.time()
    # max_route_distance, plan_output = cp(t, K)
    # tt_time = time.time() - st
    # with open(file,'w') as f:
    #     f.write(f'Objective: {max_route_distance}\nRunning time : {tt_time}\nSolution : \n{plan_output}')


    # # Example usage:
    # N = 3  # Example number of nodes
    # K = 2  # Example number of types
    max_sub_x, solution = solve_cp_model(N, K, t)
    def find_cycles(x, N, K):
        cycles = []
        for k in range(K):
            my_stack = []
            cycle = [0]
            for i in range(1, N+1):
                if x[0][i][k]:
                    my_stack.append(i)
                    cycle.append(i)
                    # print(i, cycle)
            while len(my_stack):
                v = my_stack.pop()
                for i in range(N+1):
                    if x[v][i][k]:
                        cycle.append(i)
                        # print(i, cycle)
                        if i:
                            my_stack.append(i)
                        break
            cycles.append(cycle)
        return cycles
    et = time.time()
    os.makedirs(f'result/result_cp/',exist_ok=True)
    with open(f'result/result_cp/{file}','w') as f:
        f.write(f'Objective: {max_sub_x}\n')
        f.write(f'Time run: {et-st}\n')
        print("===================================")
        print(f'Objective: {max_sub_x}')
        print(f'Time run: {et-st}')
        cycles = find_cycles(solution, N, K)
        for cycle in cycles:
            cycle = [str(i) for i in cycle]
            print(" ".join(cycle))
            f.write(f'{" ".join(cycle)}\n')