from ortools.constraint_solver import pywrapcp

def minimize_max_value():
    # Khởi tạo Solver
    solver = pywrapcp.Solver('minimize_max_value')
    
    # Định nghĩa các biến x1, x2, x3
    x1 = solver.IntVar(0, 100, 'x1')
    x2 = solver.IntVar(0, 100, 'x2')
    x3 = solver.IntVar(0, 100, 'x3')
    
    # Định nghĩa biến max_value
    max_value = solver.IntVar(0, 100, 'max_value')
    
    # Ràng buộc max_value phải bằng một trong x1, x2 hoặc x3
    solver.Add(max_value == solver.Max(x1, x2, x3))
    
    # Hàm mục tiêu: Tối thiểu hóa max_value
    objective = solver.Minimize(max_value, 1)
    
    # Tạo một phương thức tìm kiếm và tìm lời giải
    db = solver.Phase([x1, x2, x3, max_value],
                      solver.CHOOSE_FIRST_UNBOUND,  # Chọn biến chưa gán giá trị đầu tiên
                      solver.ASSIGN_MIN_VALUE)      # Gán giá trị nhỏ nhất đầu tiên
    
    solver.NewSearch(db)
    
    while solver.NextSolution():
        # In ra giá trị của các biến
        print(f'Solution found: max_value = {max_value.Value()}')
        print(f'  x1 = {x1.Value()}, x2 = {x2.Value()}, x3 = {x3.Value()}')
    
    solver.EndSearch()

minimize_max_value()
