from collections import defaultdict, Counter

BASE_ELEMENT = (
            (True, True),
            (True, False),
            (False, True),
            (False, False)
        )
ALL_STATE = tuple(
            [(i,j) for i in BASE_ELEMENT for j in BASE_ELEMENT]
        )  

def transpose(matrix):
    return zip(*matrix)



class State:
    def __init__(self):
        self.next_state = {
            mat_val:self.map_next_state(mat_val) for mat_val in ALL_STATE
        }

        self.prev_state = {
            True:[mat_val for mat_val,val in self.next_state.items() if val],
            False:[mat_val for mat_val,val in self.next_state.items() if not val],
        }

    def map_next_state(self, mat_val):
        return (sum(mat_val[0]) + sum(mat_val[1])) == 1
    def next(self, mat_val):
        return self.next_state[mat_val]
    def prev(self, val):
        return self.prev_state[val]
    def getPrevRowState(self, row):
        next_states = [(x,) for x in BASE_ELEMENT]
        for val in row:
            init_states = next_states
            next_states = []

            for state in init_states:
                overlap_state = state[-1]
                next_row_states = [state+(append_state,) for append_state in BASE_ELEMENT if self.next((overlap_state, append_state)) == val]
                next_states.extend(next_row_states)

        return [transpose(x) for x in next_states]

class Matrix:
    def __init__(self, mat):
        self.mat = [tuple(row) for row in mat] if len(mat) >= len(mat[0]) else transpose(mat)

        self.state = State()
        self.row_prev_state = {row:self.state.getPrevRowState(row) for row in set(self.mat)}
    def getMatPrevStateCount(self):
        self.next_row = None
        self.init_row = Counter([row[-1] for row in self.row_prev_state[self.mat[0]]])

        for row in self.mat[1:]:
            self.next_row = defaultdict(int)
            for pre_state in self.row_prev_state[row]:
                self.next_row[pre_state[1]] = (pre_state[0] in self.init_row) * self.init_row[pre_state[0]] + self.next_row[pre_state[1]]
            self.init_row = self.next_row
        return sum(self.init_row.values())

def solution(g):
    mat = Matrix(g)
    result = mat.getMatPrevStateCount()
    return result

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