with open('result/result_ga.txt','r') as f:
    data = f.read()
    
data = data.split('/kaggle/input/tulkh-data/')
for d in data:
    if len(d) < 3:
        continue
    sub_data = d.split('\n')
    name_file = sub_data[0]
    object_value = sub_data[-2]
    object_value = object_value.replace('total time:', 'Objective: ')
    time_run = sub_data[1]
    with open(f'result/result_ga/{name_file}','w') as f:
        f.write(object_value)
        f.write(f'\nRunning time : {time_run}\nSolution:\n')
        for line in sub_data[2:-2]:
            f.write(f"0 {' '.join(line.split(' ')[1:]).replace('[','').replace(']','').replace(',','')} 0\n")