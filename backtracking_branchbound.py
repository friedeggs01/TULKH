
#task_k la danh sach cac cong viec phan cong cho nguoi thu k 


best_cost=1e9
min_cost=0 
min_Edge=1e9 

# tim duong di toi uu 
def TSP(u: int,numVisited: int,current_cost: int,tasks): 
    global min_cost,argX
    if current_cost+ min_Edge*(len(tasks)-numVisited+1) > min_cost: # kiem tra dieu kien nhanh can 
        return 
    if numVisited == len(tasks): # neu da tham het cac dinh 
        current_cost+=c[u][0] 
        if current_cost<min_cost: 
            min_cost=current_cost
            x[numVisited+1]=0 
            argX=x.copy() 
        return 
    
    for i in range(len(tasks)): 
        if visited[tasks[i]] == False: 
            visited[tasks[i]]=True 
            current_cost+= c[u][tasks[i]]
            x[numVisited+1]=tasks[i] 
            TSP(tasks[i],numVisited+1,current_cost,tasks) 
            current_cost-= c[u][tasks[i]]
            visited[tasks[i]]=False 
            
# tim duong di cho K nguoi 
def RouteWay(tasks):
    global best_cost,min_cost,argAll
    argTasks=[[] for i in range(K+5)] 
    max_cost=0 
    for u in range(1,K+1):
        min_cost=1e9
        TSP(0,0,0,tasks[u]) 
        tmp_cost=min_cost 
        for v in tasks[u]: 
            tmp_cost+=d[v-1] 
        argTasks[u]=argX.copy() 
        if max_cost<tmp_cost: max_cost=tmp_cost
    if max_cost<best_cost : 
        best_cost=max_cost
        for u in range(K+1): 
            while len(argTasks[u])>len(tasks[u])+2: 
                argTasks[u].pop() 
        for u in range(K+1): 
            argAll[u]=argTasks[u].copy() 

# phan cong cong viec cho K nguoi     
def assignTask(u: int,tasks):
    
    if u==N+1: # neu da phan cong het ca N viec 
        RouteWay(tasks)
        return 
    for k in range(1,K+1): 
        tasks[k].append(u) 
        assignTask(u+1,tasks) 
        tasks[k].pop() 

if __name__=="__main__": 
    N,K = map(int,input().split())
 
    d = [int(item) for item in input().split()] 
    c = [[] for i in range(N+5)] 
    for j in range(N+1): 
        c[j] = [int(item) for item in input().split()]
    for u in range(N+1): 
        for v in range(N+1): 
            min_Edge=min(min_Edge,c[u][v])
    x=[0]*(N+5) 
    argX=[0]*(N+5) 
    argAll=[[] for i in range(K+5)]
    tasks =[[] for i in range(K+1)] 
    visited = [False]*(N+5)
    argTasks = [[] for i in range(K+1)] 
    assignTask(1,tasks) 
    print(K)   
    for u in range(1,K+1): 
        print(len(argAll[u])) 
        for x in argAll[u]: 
            print(x,end=' ')
        print()