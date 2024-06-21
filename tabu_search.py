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
                if len(neighbors) > 5000: break 
            if len(neighbors) > 5000: break 
        if len(neighbors)> 5000: break 
    
    for old_emp in assignments.keys():
        for i in range(len(assignments[old_emp])):
            for j in range(i+1, len(assignments[old_emp])):
                new_assignments = {emp: assignments[emp].copy() for emp in assignments.keys()}
                new_assignments[old_emp] = new_assignments[old_emp][:i] + list(reversed(new_assignments[old_emp][i:j+1])) + new_assignments[old_emp][j+1:]
                neighbors.append(new_assignments)
                if len(neighbors) > 5000:
                    break
                if len(neighbors) > 5000:
                    break
            if len(neighbors) > 5000: break 
        if len(neighbors)> 5000: break 
    random.shuffle(neighbors) 
    
    return neighbors

def tabu_search(customers, repair_times, travel_times, num_employees):
    # Initialize the initial assignments randomly
    assignments = {i: [] for i in range(num_employees)}
    for customer in customers:
        emp = random.randint(0, num_employees - 1)
        assignments[emp].append(customer)

    current_time = calculate_total_time(assignments, repair_times, travel_times)
    best_assignments = assignments.copy()
    best_time = current_time

    # Define Tabu Search parameters
    tabu_list = []
    max_iter = 500
    tabu_size = 20

    # Perform Tabu Search iterations
    for _ in range(max_iter):
        neighbors = generate_neighbors(assignments, num_employees)
        best_emp = None
        best_time_diff = float('inf')

        for neighbor in neighbors:
            new_time = calculate_total_time(neighbor, repair_times, travel_times)
            time_diff = new_time - current_time
            if neighbor not in tabu_list and time_diff  < best_time_diff :
                best_emp = neighbor
                best_time_diff = time_diff

        
        assignments = best_emp
        current_time += best_time_diff

        if current_time < best_time:
            best_assignments = assignments.copy()
            best_time = current_time

        tabu_list.append(assignments)
        if len(tabu_list) > tabu_size:
            tabu_list = tabu_list[1:]

    return best_assignments, current_time

if __name__=="__main__": 
    
    #inp = ['data_50_10.txt','data_50_20.txt','data_50_25.txt',
    #       'data_5_3.txt','data_10_2.txt','data_10_3.txt','data_10_5.txt',
    #       'data_20_3.txt','data_20_5.txt','data_20_7.txt','data_20_10.txt','data_100_10.txt',
    #     'data_100_50.txt','data_200_20.txt']
    #inp.extend(['data_100_50.txt','data_200_20.txt','data_200_50.txt','data_500_20.txt','data_1000_50.txt'])
    #inp = ['data_200_50.txt','data_500_20.txt','data_500_50.txt',
    #       'data_700_50.txt','data_700_70.txt','data_1000_50.txt','data_1000_100.txt']
    inp = ['data_10_2.txt']
   
    for s in inp: 
        path_inp = './data/'+s 
        path_out = './result/result_tabu_search/'+s
        fi = open(path_inp,'r') 
        output = open(path_out,'w')
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
        assignments, best_time = tabu_search(customers, repair_times, travel_times, num_employees)
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
        

