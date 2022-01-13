def solution(g):
    if len(g) < 2 or len(g[0]) < 2:
        return 0
    mat = Mat(g)
    mat.solve((0,0))
    return mat.legal_result_count

class Mat:
    def __init__(self, mat):
        self.mat = mat
        self.length = len(self.mat)+1
        self.width = len(self.mat[0]) + 1
        self.original_mat = [[None] * self.width for i in range(self.length)]
        self.legal_result_count = 0

        self.__next_point_cache = {}
        self.__mat_to_next_cache = {}
        self.__prev_mat_cache = {}
    def getOriginalMat(self, x0,x1,y0,y1):
        return tuple(self.original_mat[x0][y0:y1] + self.original_mat[x1-1][y0:y1])
    def isLegalVal(self, point):
        x,y = point
        point_list = ((x,y), (x-1, y), (x, y-1), (x-1, y-1))
        mat_list = [(point,self.getPrevMatrix(point)) for point in point_list]
        return all([x0 == None or self.isLegal(self.mat[x][y], self.getOriginalMat(x0,x1,y0,y1)) for (x,y),(x0,x1,y0,y1) in mat_list])
    def getPrevMatrix(self, point):
        if self.__prev_mat_cache.get(point) is not None:
            return self.__prev_mat_cache.get(point) 
        x, y = point
        if self.length-1 > x >= 0 and  self.width-1 > y >= 0:
            result = (x,x+2,y,y+2)
        else:
            result = (None, None, None, None)
        self.__prev_mat_cache[point] = result
        return result

    def isLegal(self, val, original_mat_tuple):
        if self.__mat_to_next_cache.get((val,original_mat_tuple)) is None:
            count_true = sum([x==True for x in original_mat_tuple])
            count_none = sum([x==None for x in original_mat_tuple])
            if val:
                self.__mat_to_next_cache[(val,original_mat_tuple)] = count_true == 1 or (count_true == 0 and count_none > 0)
            else: # False
                self.__mat_to_next_cache[(val,original_mat_tuple)] = not (count_true == 1 and count_none == 0)

        return self.__mat_to_next_cache.get((val,original_mat_tuple))
    def solve(self,point = (0,0)):
        x,y = point
        
        for fill_val in [True, False]:
            self.original_mat[x][y] = fill_val
            if self.isLegalVal(point):
                next_point = self.next_cell(point)
                if next_point == None:
                    self.legal_result_count += 1
                else:
                    self.solve(next_point)
        self.original_mat[x][y] = None

    def next_cell(self,point):
        x,y = point
        if point in self.__next_point_cache:
            return self.__next_point_cache.get(point)
        if y >= self.width - 1:
            if x >= self.length - 1:
                next_point = None
            else:
                next_point = (x+1,0)
        else:
            next_point = (x,y+1)
        self.__next_point_cache[point] = next_point
        return next_point

def transpose(matrix):
    return [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]
def printMat(mat):
    print("\n".join([str(row) for row in mat]))

import time
class Timer:
    def __init__(self):
        self.start = time.time()
    def restart(self):
        print(time.time() - self.start)
        self.start = time.time()

if __name__ == "__main__":

    g1 = [[True, False, True], [False, True, False], [True, False, True]]
    g2 = [[True, True, False, True, False, True, False, True, True, False], [True, True, False, False, False, False, True, True, True, False], [True, True, False, False, False, False, False, False, False, True], [False, True, False, False, False, False, True, True, False, False]]
    g3 = [[True, False, True, False, False, True, True, True], [True, False, True, False, False, False, True, False], [True, True, True, False, False, False, True, False], [True, False, True, False, False, False, True, False], [True, False, True, False, False, True, True, True]]
    g4 = [[True]*50]*9
    timer = Timer()
    print(solution(transpose(g1)))
    timer.restart()
    print(solution(transpose(g2)))
    timer.restart()
    print(solution(transpose(g3)))
    timer.restart()
