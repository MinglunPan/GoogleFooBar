MAX_INT = 999999

class Maze:
    def __init__(self, route_map, entry_node, exit_node):
        self.route_map = route_map
        self.entry_node, self.exit_node = entry_node, exit_node
        self.width, self.length = len(self.route_map), len(self.route_map[0])

        self._entry_bfs_layer_dict = None
        self._exit_bfs_layer_dict = None

    @property
    def entry_bfs_layer_dict(self):
        if not self._entry_bfs_layer_dict: self.solve()
        return self._entry_bfs_layer_dict
    @property
    def exit_bfs_layer_dict(self):
        if not self._exit_bfs_layer_dict: self.solve()
        return self._exit_bfs_layer_dict


    def updateMap(self, func = lambda x:None if x == 1 else x):
        '''Change some representattions of the element in map
        '''
        for i in range(self.width): self.route_map[i] = map(func, self.route_map[i])

    def buildBFS(self):
        '''Generate bfs from the entry node and from the exit node.
        '''
        self._entry_bfs_layer_dict = BFS(self.route_map, self.entry_node, {})
        self._exit_bfs_layer_dict = BFS(self.route_map, self.exit_node, {})  

    def breakWalltoSolve(self):
        '''Break the wall to find the solution. At first, find a shortest path to the exit node, 
        and then find a shortest path to the entry node. Then, connect these two paths by breaking the wall.
        '''
        min_dist = MAX_INT
        for node in self.entry_bfs_layer_dict.keys():
            next_nodes_list = getNext(self.route_map, node, 2)
            for next_node in next_nodes_list:
                if next_node in self.exit_bfs_layer_dict:
                    min_dist = min(min_dist, self.entry_bfs_layer_dict.get(node) + self.exit_bfs_layer_dict.get(next_node))
        return min_dist + 1

def BFS(route_map, start_node, walked_nodes_dict):
    '''BFS for route_map starting from start_node and skipping nodes in walked_nodes_dict
    '''
    # init
    queue = [(start_node,1), ]  # ((point_x, point_y), point_layer)
    walked_nodes_dict[start_node] = 1
    # bfs
    while len(queue) != 0:
        current_node, layer = queue.pop(0)
        for next_node in getNext(route_map, current_node):
            if next_node not in walked_nodes_dict:
                walked_nodes_dict[next_node] = layer + 1
                queue.append((next_node,layer+1))
    return walked_nodes_dict

def solution(map):
    maze = Maze(map, (0,0), (len(map)-1, len(map[0])-1) )
    maze.updateMap()
    maze.buildBFS()
    final_result = maze.breakWalltoSolve()
    return final_result

def getNext(map, curr_node, step = 1):
    '''Get next possible nodes with the specified length of step from current location.
    '''
    x,y = curr_node
    next_nodes_list = []
    for x_move in range(step+1):
        y_move = step - x_move
        next_nodes_list += [
            (x+x_move,y+y_move), 
            (x+x_move,y-y_move), 
            (x-x_move,y+y_move), 
            (x-x_move,y-y_move)]
    next_nodes_list = [(x,y) for x,y in set(next_nodes_list) 
            if 0 <= x < len(map) and 0 <= y < len(map[0]) and map[x][y]==0
            ]
    return next_nodes_list

if __name__ == "__main__":
    map1 = [
        [0, 0, 0, 0, 0, 0], 
        [1, 1, 1, 1, 1, 0], 
        [0, 0, 0, 0, 0, 0], 
        [1, 1, 1, 1, 1, 1], 
        [0, 0, 1, 0, 0, 0], 
        [1, 0, 0, 0, 1, 0]]
    map2 = [
        [0, 0, 0, 0, 0, 0], 
        [1, 1, 1, 1, 1, 0], 
        [0, 0, 0, 0, 0, 0], 
        [0, 1, 1, 1, 1, 1], 
        [0, 0, 1, 0, 0, 0], 
        [1, 0, 0, 0, 1, 0]]
    map3 = [
        [0, 0, 0, 0, 0, 0], 
        [1, 1, 1, 1, 1, 0], 
        [0, 0, 0, 0, 0, 0], 
        [0, 1, 1, 1, 1, 1], 
        [0, 0, 0, 0, 0, 0], 
        [1, 0, 0, 0, 1, 0]]
    map4 = [
        [0, 0, 0, 0, 0], 
        [1, 1, 1, 1, 0], 
        [0, 0, 0, 0, 0], 
        [0, 1, 1, 1, 1], 
        [0, 0, 0, 0, 0], 
        [1, 0, 0, 1, 0]]
    map5 = [
        [0, 1, 1, 0], 
        [0, 0, 0, 1], 
        [1, 1, 0, 0], 
        [1, 1, 1, 0]
    ]
    map6 = [[0, 0, 0, 0, 0, 0], 
            [1, 1, 1, 1, 1, 0], 
            [0, 0, 0, 0, 0, 0], 
            [0, 1, 1, 1, 1, 1], 
            [0, 1, 1, 1, 1, 1], 
            [0, 0, 0, 0, 0, 0]]
    print(solution(map1))
    
    print(solution(map2))
    
    print(solution(map3))
    
    print(solution(map4))
    
    print(solution(map5))
    
    print(solution(map6))


    map_test = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0],
        [0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0],
        [0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0],
        [0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
        [0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        ]
    maze = Maze(map_test, (0,0), (len(map_test)-1,len(map_test[0])-1))
    maze.updateMap()
    # print(maze.minSolution)
    # print(maze.breakWalltoImprove())
    print(solution(map_test))

    map_test = [
        [0,1],
        [1,0]
        ]
    print(solution(map_test))