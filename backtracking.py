import numpy as np
def read(filename):
    with open(filename, 'r') as f:
        N, K = map(int, f.readline().split())
        d = [0] + list(map(float, f.readline().split()))
        t = np.zeros((N + 1, N + 1))
        for i in range(N + 1):
            t[i] = list(map(float, f.readline().split()))

    return N, K, d, t

def creat_cost(N, d, t):
    cost_matrix = np.zeros((N + 1, N + 1))
    for i in range(N + 1):
        for j in range(N + 1):
            if i != j:
                cost_matrix[i][j] = d[j] + t[i][j]

    return cost_matrix

class Back_Tracking:
    def __init__(self):
        self.N, self.K = map(int, input().split())
        self.d = [0] + list(map(int, input().split()))
        self.t = np.zeros((self.N + 1, self.N + 1))
        for i in range(self.N + 1):
            self.t[i] = list(map(float, input().split()))

        self.cost_matrix = creat_cost(self.N, self.d, self.t)
        self.visited = np.zeros(self.N + 1)
        self.x = np.zeros(1000, dtype = int)
        self.y = np.zeros(100, dtype = int)

        self.f_best = 1e9
        self.f_current = 0
        self.numSegments = 0

    def solution(self):
        max_cost = 0
        for k in range(1, self.K + 1):
            temp_cost = 0
            start_employee = self.y[k]
            if start_employee == 0:
                continue
            temp_cost = temp_cost + self.cost_matrix[0][start_employee]
            next_employee = self.x[start_employee]
            while next_employee != 0:
                temp_cost = temp_cost + self.cost_matrix[start_employee][next_employee]
                start_employee = next_employee
                next_employee = self.x[start_employee]
            temp_cost = temp_cost + self.cost_matrix[start_employee][0]
            if temp_cost > max_cost:
                max_cost = temp_cost
        if max_cost < self.f_best:
            self.f_best = max_cost
            self.x_best = self.x.copy()
            self.y_best = self.y.copy()
            

    def checkX(self, v, i, k):
        if v == 0:
            return True
        if self.visited[v] == 1:
             return False
        return True

    def checkY(self, i, k):
        if self.visited[i] == 1:
            return False
        if i == 0:
            if k == self.K:
                return False
        return True
            
        

    def TryX( self, i, k):
        for v in range(0, self.N + 1):
            if self.checkX(v, i, k):
                self.x[i] = v
                self.visited[v] = 1
                self.numSegments = self.numSegments + 1
                if v == 0:
                    if k == self.K:
                        if self.numSegments == self.N + self.K:
                            self.solution()
                    else:
                        self.TryX(self.y[k+1], k + 1)
                else:
                    self.TryX(v, k)

                self.visited[v] = 0
                self.numSegments = self.numSegments - 1

    def TryY(self, k):
            for i in range(self.y[k-1], self.N + 1):
                
                if self.checkY(i, k):
                    self.y[k] = i
                    self.visited[i] = 1
                    self.numSegments = self.numSegments + 1
                    if k == self.K:
                        first = 1
                        while self.y[first] == 0:
                            first = first + 1
                        self.TryX(self.y[first], first)
                    else:
                        self.TryY(k + 1)
                    
                    self.visited[i] = 0
                    self.numSegments = self.numSegments - 1      
import time
def back_tracking():
    indi = Back_Tracking()
    start = time.time()
    indi.TryY(1)
    print(indi.K)
    for k in range(1, indi.K + 1):
        if indi.y_best[k] == 0:
            print("0")
        else:
            cnt = 3
            temp = indi.y_best[k]
            next_employee = indi.x_best[temp]
            while next_employee != 0:
                cnt += 1
                temp = next_employee
                next_employee = indi.x_best[temp]
            print(cnt)
            print("0 ", end='')
            temp = indi.y_best[k]
            print(str(temp) + " ", end='')
            next_employee = indi.x_best[temp]
            while next_employee != 0:
                print(str(next_employee) + " ", end='')
                temp = next_employee
                next_employee = indi.x_best[temp]
            print("0")
      
def main():
    back_tracking()

if __name__ == "__main__":
    main()