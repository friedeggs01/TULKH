import time

def two_opt(route, cost_matrix):
    best_route = route
    best_cost = calculate_cost(route, cost_matrix)
    improved = True
    
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1: continue
                new_route = route[:i] + route[i:j][::-1] + route[j:]
                new_cost = calculate_cost(new_route, cost_matrix)
                if new_cost < best_cost:
                    best_route = new_route
                    best_cost = new_cost
                    improved = True
        route = best_route
    
    return best_route, best_cost

def calculate_cost(route, cost_matrix):
    return sum(cost_matrix[route[i]][route[i+1]] for i in range(len(route) - 1))

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
        optimized_path, optimized_cost = two_opt(path, c)
        total_cost = optimized_cost + sum(d[task - 1] for task in tasks[u])
        argTasks[u] = optimized_path
        
        if max_cost < total_cost:
            max_cost = total_cost
    
    if max_cost < best_cost:
        best_cost = max_cost
        for u in range(1, K + 1):
            argAll[u] = argTasks[u]

def greedyAssignTask(u, tasks):
    if u == N + 1:
        greedyRouteWay(tasks)
        return
    
    min_load_agent = None
    min_load = float('inf')
    for k in range(1, K + 1):
        current_load = sum(d[task - 1] for task in tasks[k])
        if current_load < min_load:
            min_load = current_load
            min_load_agent = k
    
    tasks[min_load_agent].append(u)
    greedyAssignTask(u + 1, tasks)
    tasks[min_load_agent].pop()

if __name__ == "__main__":
    start_time = time.time()
    
    N, K = map(int, input().split())
    
    d = [int(item) for item in input().split()]
    c = [[] for _ in range(N + 5)]
    for j in range(N + 1):
        c[j] = [int(item) for item in input().split()]
    
    best_cost = float('inf')
    argAll = [[] for _ in range(K + 5)]
    tasks = [[] for _ in range(K + 1)]
    
    greedyAssignTask(1, tasks)
    
    end_time = time.time()
    running_time = end_time - start_time
    
    print(f"Objective value: {best_cost}")
    print(f"Running time: {running_time:.6f}")
    print(f"Number customers: {N}")
    print(f"Number vehicles: {K}")
    print("Solution:")
    for u in range(1, K + 1):
        print(" ".join(map(str, argAll[u])))
