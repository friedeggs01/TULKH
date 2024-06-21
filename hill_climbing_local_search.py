import random
from time import time 

def calculate_total_time(assignments, repair_times, travel_times):
    max_time = 0
    for emp_assignments in assignments.values():
        total_time = 0
        for i in range(len(emp_assignments)):
            if i < len(emp_assignments)-1:
                total_time += travel_times[emp_assignments[i]][emp_assignments[i+1]] 
            total_time += repair_times[emp_assignments[i]]
        if len(emp_assignments)>0: 
            total_time += travel_times[0][emp_assignments[0]] 
            total_time += travel_times[emp_assignments[-1]][0] 
        max_time = max(max_time, total_time)
    return max_time

def generate_neighbors(assignments,num_employees):
    neighbors = []
    random.shuffle(assignments)
    for old_emp in assignments.keys():
        for old_cust in assignments[old_emp]: 
            for new_emp in range(num_employees):
                #if old_emp != new_emp:
                new_assignments ={emp :assignments[emp].copy() for emp in assignments.keys()} 
                new_assignments[old_emp].remove(old_cust)
                new_assignments[new_emp].append(old_cust)
                neighbors.append(new_assignments)
    return neighbors

def local_search(customers, repair_times, travel_times, num_employees):
    # Initialize the initial assignments randomly
    assignments = {i: [] for i in range(num_employees)}
    for customer in customers:
        emp = random.randint(0, num_employees - 1)
        assignments[emp].append(customer)

    best_time = calculate_total_time(assignments, repair_times, travel_times)

    # Perform local search iterations
    num_iterations = 10000
    for _ in range(num_iterations):
        neighbors = generate_neighbors(assignments,num_employees)
        best_emp = None
        best_time_diff = float('inf')

        for neighbor in neighbors:
            new_time = calculate_total_time(neighbor, repair_times, travel_times)
            time_diff = new_time - best_time
            if time_diff < best_time_diff:
                best_emp = neighbor
                best_time_diff = time_diff

        if best_time_diff < 0:
            assignments = best_emp
            best_time += best_time_diff
        else:
            break

    return assignments, best_time

if __name__=="__main__": 

    fi = open('./data/data_10_2.txt','r') 
    output = open('./result/result_hill_climbing_local_search/data_10_2.txt','w')
    num_customers, num_employees = fi.readline().split(' ') 
    #num_customers, num_employees = input().split(' ')
    num_customers, num_employees = int(num_customers), int(num_employees) 
    customers = [i+1 for i in range(num_customers)]
    d = fi.readline().split(' ') 
    #d = input().split(' ') 
    repair_times = { i+1: int(d[i]) for i in range(num_customers)}
    
    travel_times = [[] for i in range(num_customers+1)]
    for i in range(num_customers+1): 
        tmp = fi.readline().split(' ')
        #tmp = input().split(' ')
        travel_times[i] = [int(tmp[i]) for i in range(num_customers+1)]
    #print(repair_times)
    #print(travel_times)
    starttime = time() 
    assignments, best_time = local_search(customers, repair_times, travel_times, num_employees)
    endtime = time() 
    output.write("Objective value: "+str(best_time)+'\n')
    print("Running time "+str(endtime-starttime))
    output.write("Running time "+str(endtime-starttime)+'\n') 
    print("Minimum Total Time:", best_time)
    output.write("Solution"+'\n')
    print(num_employees)
    for emp in assignments.keys(): 
        print(len(assignments[emp]))
        print(0,end=' ') 
        output.write(str(0)+' ') 
        for task in assignments[emp]: 
            print(task,end=' ') 
            output.write(str(task)+' ')
        print(0)
        output.write(str(0)+'\n')
    output.close()
    print("Best Assignments:", assignments)
    




