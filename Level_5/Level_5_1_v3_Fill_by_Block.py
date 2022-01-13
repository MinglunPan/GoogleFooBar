ALL_STATE_DICT = {
    1:[[True], [False]],
    2:[[True, True], [True, False], [False, True], [False, False]],
    3:[[True, True, True], [False, True, True], [True, False, True], [True, True, False], [False, False, True], [False, True, False], [True, False, False], [False, False, False]],
    4:[
        [True, True, True, True], 
        [False, True, True, True], [True, False, True, True], [True, True, False, True], [True, True, True, False], 
        [False, False, True, True], [False, True, False, True], [False, True, True, False], [True, False, False, True], [True, False, True, False], [True, True, False, False], 
        [False, False, False, True], [False, False, True, False], [False, True, False, False], [True, False, False, False], 
        [False, False, False, False],]

}
POTENTIAL_FILL_DICT = {
    True:{
        (0,1):[[True], ],
        (0,2):[[True, False], [False, True]],
        (0,3):[[True, False, False], [False, True, False], [False, False, True]],
        (0,4):[[True, False, False, False], [False, True, False, False], [False, False, True, False], [False, False, False, True]],
        (1,1):[[False]],
        (1,2):[[False, False]],
        (1,3):[[False, False, False]],
        (2,1):[],
        (2,2):[],
        (3,1):[],
    }}
POTENTIAL_FILL_DICT[False] = {
    (count_true, count_none):[x for x in ALL_STATE_DICT[count_none] if x not in values]
    for (count_true, count_none), values in POTENTIAL_FILL_DICT[True].items()}

def solution(g):
    if len(g) < 2 or len(g[0]) < 2:
        return 0
    mat = Mat(transpose(g))
    mat.solve((0,0))
    #print(mat._count_none)
    return mat.result_count

class Mat:
    def __init__(self, mat):
        self.mat = mat
        self.length = len(self.mat)+1
        self.width = len(self.mat[0]) + 1
        self.original_mat = [[None] * self.width for i in range(self.length)]
        self.result_count = 0

        self.__mat_count_cache = {}
        self._next_point_cache = {}
    def solve(self, point = (0,0)):
        # print(point)
        # Prerequisite: point is not None & count_none > 0
        next_point, count_none = point, 0
        fill_points_list, potential_solutions = self.getPotentialSolution(point)
        # print("ORIGINAL",point)
        # If having solution, then searching for the next fillable point
        
        if len(potential_solutions) > 0:
            # Pre-fill
            for fill_point in fill_points_list:
                self.original_mat[fill_point[0]][fill_point[1]] = True
            
            
            while count_none == 0: # Loop until we find a fillable point
                next_point = self.next_point(next_point)
                
                if next_point is None: # If reach the end, return and count
                    self.result_count += len(potential_solutions)
                    for fill_point in fill_points_list:
                        self.original_mat[fill_point[0]][fill_point[1]] = None
                    return
                mat_val = self.getOriginalMat(self.getOriginalMatIdx(next_point))
                count_none = len(self.getInfo(mat_val)[0])
                
        # # If having solution, then fill
        for solution in potential_solutions:
            # Fill
            for idx, fill_point in enumerate(fill_points_list):
                self.original_mat[fill_point[0]][fill_point[1]] = solution[idx]
            self.solve(next_point) # next_point is not None & count_none > 0
        # Rollback
        for fill_point in fill_points_list:
            self.original_mat[fill_point[0]][fill_point[1]] = None

    def getPotentialSolution(self, point):
        x,y = point
        next_val = self.mat[x][y]
        mat_idx = self.getOriginalMatIdx(point)
        mat_val = self.getOriginalMat(mat_idx)
        
        fill_points_list, count_true = self.getInfo(mat_val)
            # if len(fill_points_list) % 2 == 1:
            #    print "NEXT_STATE:", next_val, '\nPoint:', point, '\nMatVal:', mat_val, '\nOriginalMatrix:\n', strMat(self.original_mat), '\nMatrix:\n', strMat(self.mat)
        fill_points_list = [(mat_idx[idx_x], mat_idx[idx_y]) for idx_x,idx_y in fill_points_list]
        potential_fill_solutions = POTENTIAL_FILL_DICT.get(next_val).get((count_true, len(fill_points_list)))

        return fill_points_list, potential_fill_solutions
    def getOriginalMat(self, mat_idx):
        return tuple(self.original_mat[mat_idx[0]][mat_idx[2]:mat_idx[3]+1] + self.original_mat[mat_idx[1]][mat_idx[2]:mat_idx[3]+1])


    def getInfo(self, mat_val):
        if mat_val in self.__mat_count_cache:
            fill_points_list, count_true = self.__mat_count_cache.get(mat_val)
        else:
            fill_points_list, count_true = [], 0
            for idx, val in enumerate(mat_val):
                if val == True:
                    count_true += 1
                elif val is None:
                    fill_points_list.append((idx // 2,2 + idx % 2))
            self.__mat_count_cache[mat_val] = fill_points_list, count_true
        return fill_points_list, count_true
    
    def next_point(self,point):
        if point[1] < self.width - 2:
            return (point[0],point[1]+1)
        elif point[0] < self.length - 2:
            return (point[0]+1,0)
        else:
            return None
            
    def getOriginalMatIdx(self, point):
        return point[0], point[0]+1, point[1], point[1]+1

def transpose(matrix):
    return zip(*matrix)
def strMat(mat):
    return "\n".join([str(row) for row in mat])
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
    g4 = [[True]*30]*9
    timer = Timer()
    print(solution(g1))
    timer.restart()
    print(solution(g2))
    timer.restart()
    print(solution(g3))
    timer.restart()
    print(solution(g4))
    timer.restart()