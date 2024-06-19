#PYTHON 
import heapq

def greedyTSP(start, tasks):
    visited = [False] * len(c)
    path = [start]
    visited[start] = True
    current_cost = 0

    current_node = start
    while len(path) < len(tasks) + 1:
        min_cost = float('inf')
        next_node = None
        for task in tasks:
            if not visited[task] and c[current_node][task] < min_cost:
                min_cost = c[current_node][task]
                next_node = task
        if next_node is not None:
            path.append(next_node)
            visited[next_node] = True
            current_cost += min_cost
            current_node = next_node
        else:
            break
    path.append(0)
    current_cost += c[current_node][0]
    return path, current_cost

def greedyRouteWay(tasks):
    global best_cost, argAll
    max_cost = 0
    argTasks = [[] for _ in range(K + 5)]
    
    for u in range(1, K + 1):
        path, cost = greedyTSP(0, tasks[u])
        total_cost = cost + sum(d[task - 1] for task in tasks[u])
        argTasks[u] = path
        
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
    N, K = map(int, input().split())
    
    d = [int(item) for item in input().split()]
    c = [[] for _ in range(N + 5)]
    for j in range(N + 1):
        c[j] = [int(item) for item in input().split()]
    
    best_cost = float('inf')
    argAll = [[] for _ in range(K + 5)]
    tasks = [[] for _ in range(K + 1)]
    
    greedyAssignTask(1, tasks)
    
    print(K)
    for u in range(1, K + 1):
        print(len(argAll[u]))
        for x in argAll[u]:
            print(x, end=' ')
        print()
