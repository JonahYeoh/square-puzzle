    def manhattan_dis(self,state,goal): #second heuristc function to test state outside best search function
        distance=0
        for i in range(len(state)):
            for j in range(len(state)):
                index_i , index_j=i ,j
                for x in range(len(goal)):
                    for y in range(len(goal)):
                        index_x, index_y = x, y
                        if state[i][j] == goal[x][y]:
                           distance += abs(index_i - index_x) + abs(index_j - index_y)
        return distance