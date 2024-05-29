import time
import os

def greedyTSP(start, tasks, cost_matrix):
    visited = [False] * len(cost_matrix)
    path = [start]
    visited[start] = True
    current_cost = 0

    current_node = start
    while len(path) < len(tasks) + 1:
        min_cost = float('inf')
        next_node = None
        for task in tasks:
            if not visited[task] and cost_matrix[current_node][task] < min_cost:
                min_cost = cost_matrix[current_node][task]
                next_node = task
        if next_node is not None:
            path.append(next_node)
            visited[next_node] = True
            current_cost += min_cost
            current_node = next_node
        else:
            break
    path.append(start)
    current_cost += cost_matrix[current_node][start]
    return path, current_cost

def greedyRouteWay(tasks):
    global best_cost, argAll
    max_cost = 0
    argTasks = [[] for _ in range(K + 5)]
    
    for u in range(1, K + 1):
        path, cost = greedyTSP(0, tasks[u], c)
        total_cost = cost + sum(d[task - 1] for task in tasks[u])
        argTasks[u] = path
        
        if max_cost < total_cost:
            max_cost = total_cost
    
    if max_cost < best_cost:
        best_cost = max_cost
        for u in range(1, K + 1):
            argAll[u] = argTasks[u]

def greedyAssignTask(tasks):
    stack = [(1, tasks)]
    while stack:
        u, tasks = stack.pop()
        if u == N + 1:
            greedyRouteWay(tasks)
            continue

        min_load_agent = None
        min_load = float('inf')
        for k in range(1, K + 1):
            current_load = sum(d[task - 1] for task in tasks[k])
            if current_load < min_load:
                min_load = current_load
                min_load_agent = k
        
        tasks[min_load_agent].append(u)
        stack.append((u + 1, [task_list[:] for task_list in tasks]))
        tasks[min_load_agent].pop()

if __name__ == "__main__":
    start_time = time.time()
    
    # Use raw string to handle backslashes correctly
    file_path = r'D:\Tài Liệu\Tối ưu\abcd\TULKH\result\result_greedy\data_1000_100.txt'
    
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' not found.")
    else:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        N, K = map(int, lines[0].split())
        d = [int(item) for item in lines[1].split()]
        c = [[] for _ in range(N + 5)]
        for j in range(N + 1):
            c[j] = [int(item) for item in lines[j + 2].split()]
        
        best_cost = float('inf')
        argAll = [[] for _ in range(K + 5)]
        tasks = [[] for _ in range(K + 1)]
        
        greedyAssignTask(tasks)
        
        end_time = time.time()
        running_time = end_time - start_time
        
        with open(file_path, 'a') as file:
            file.write(f"\nObjective value: {best_cost}\n")
            file.write(f"Running time: {running_time:.6f}\n")
            file.write(f"Number customers: {N}\n")
            file.write(f"Number vehicles: {K}\n")
            file.write("Solution:\n")
            for u in range(1, K + 1):
                file.write(" ".join(map(str, argAll[u])) + "\n")
