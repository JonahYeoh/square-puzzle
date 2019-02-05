import random
import math
from copy import deepcopy

GState = \
    [[1,2,3,4]
    ,[5,6,7,8]
    ,[9,10,11,12]
    ,[13,14,15,0]]

def index(item, seq):
    """Helper function that returns -1 for non-found index value of a seq"""
    if item in seq:
        return seq.index(item)
    else:
        return -1


class squarePuzzle:


    def __init__(self):
        self.heuristic = 0
        self.depth = 0
        self.parent = None
        self.matrix = []
        for i in range(4):
            self.matrix.append(GState[i][:])
#--------------------------------------------------------------




#------------------------------------------------------------
    def build_blank_direction(self): #brg3 l possible states l ynf3 a3mlha shuffle

        row, col = self.find_blank(0)
        free = []
        if row > 0:
            free.append((row - 1, col))
        if col > 0:
            free.append((row, col - 1))
        if row < 3:
            free.append((row + 1, col))
        if col < 3:
            free.append((row, col + 1))

        return free
 #------------------------------------------------------------


#---------------------------------------------------------- generate moves
    def get_possible_stste(self):
        free = self.build_blank_direction()
        zero = self.find_blank(0)

        def swap_with_blank(a, b):
            p = squarePuzzle()
            p.matrix = deepcopy(self.matrix)
            p.Pswap(a,b)
            p.depth = self.depth + 1
            p.parent = self
            return p


        return map(lambda pair: swap_with_blank(zero, pair), free)#####(1)
#-----------------------------------------------------------
    def _generate_solution_path(self, path): #generate path
        if self.parent == None:
            return path
        else:
            path.append(self)
            return self.parent._generate_solution_path(path)
 #---------------------------------------------------------------------

    def best_first_search(self, h): #best first search function
        """Performs A* search for goal state.
        h(puzzle) - heuristic function, returns an integer
        """

        def check_if_goal(squarePuzzle):
            return squarePuzzle.matrix == GState

        openll = [self]
        check_open=[]
        closedl = []
        move_count = 0
        while len(openll) > 0:
            x = openll.pop(0)
            
            move_count += 1
            if (check_if_goal(x)):
                if len(closedl) > 0:
                    return x._generate_solution_path([]), move_count
                else:
                    return [x]

            succ = x.get_possible_stste()
            idx_open = idx_closed = -1
            for move in succ:
                # have we already seen this node?
                idx_open = index(move, openll)
                idx_closed = index(move, closedl)
                hval = h(move)
                fval = hval + move.depth

                if idx_closed == -1 and idx_open == -1:
                    move.heuristic = hval
                    openll.append(move)
                    check_open.append(move)
                elif idx_open > -1:
                    copy = openll[idx_open]
                    if fval < copy.heuristic + copy.depth:
                        # copy move's values over existing
                        copy.heuristic = hval
                        copy.parent = move.parent
                        copy.depth = move.depth
                elif idx_closed > -1:
                    copy = closedl[idx_closed]
                    if fval < copy.heuristic + copy.depth:
                        move.heuristic = hval
                        closedl.remove(copy)
                        openll.append(move)
                        

            closedl.append(x)
            openll = sorted(openll, key=lambda p: p.heuristic + p.depth)

        # if finished state not found, return failure
        return []

#--------------------------------------------------------------------------

    def shuffle(self, step_count): # bt3ml shuffle
        for i in range(step_count):
            row, col = self.find_blank(0)
            free = self.build_blank_direction()
            target = random.choice(free)
            self.Pswap((row, col), target)
            row, col = target
#------------------------------------------------------------
    def find_blank(self, value):# arg3 l index Of blank
        for row in range(4):
            for col in range(4):
                if self.matrix[row][col] == value:
                    return row, col
#--------------------------------------------------------------------

    def get_val(self, row, col):# ptrg3 value bta3 index mo3yn
        return self.matrix[row][col]

#-------------------------------------------------------------------
    def Pswap(self,pos_a, pos_b): #bt3ml swap brdo
        temp = self.matrix[pos_a[0]][pos_a[1]]
        self.matrix[pos_a[0]][pos_a[1]] = self.matrix[pos_b[0]][pos_b[1]]
        self.matrix[pos_b[0]][pos_b[1]] = temp

#---------------------------------------------------------------------

    def misPlace(self,State): # first heuristic function to use outside best first search
        num = 1
        mis_place = 0
        for i in range(len(State)):
            for j in range(len(State)):
                if (State[i][j] != num):
                    mis_place +=1
                num +=1
        return mis_place

#-------------------------------------------------------------------------
    def check_if_goal(self,state,goal): # check if goal state or not to test outside best search function
        for x in range(len(state)):
            for y in range(len(state)):
                if state[x][y]!=goal[x][y]:
                    return false
        return true
#-------------------------------------------------------------------------
def manhattan_distance(squarePuzzle): #to used in best search function
    t = 0
    for row in range(4):
        for col in range(4):
            val = squarePuzzle.get_val(row, col) - 1
            target_col = val % 4
            target_row = val / 4

                # account for 0 as blank
            if target_row < 0:
                target_row = 3

            t += abs(target_row - row) + abs(target_col - col)

        return t
 #----------------------------------------------------------------

def mis_placed(squarePuzzle):#to use in best search function
    num = 1
    mis_p=0
    for row in range(4):
        for col in range(4):
            if (squarePuzzle.get_val(row, col) != num):
                mis_p+=1
            num+=1
        return mis_p
#-------------------------------------------------------------------
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
#-------------------------------------------------------------------------------------

p = squarePuzzle()
p.shuffle(5)
print p.matrix

#print(p._get_legal_moves())


path, count = p.best_first_search(manhattan_distance)
path.reverse()
for i in path:
    for row  in i.matrix:
        print row
    print "\n"
    #print i.matrix
print "Solved with Manhattan distance exploring", count, "states"
path, count = p.best_first_search(mis_placed)
print "Solved with Misplaced squares exploring", count, "states"
   # path, count = p.solve(h_manhattan_lsq)
    #print "Solved with Manhattan least squares exploring", count, "states"
    #path, count = p.solve(h_linear)
    #print "Solved with linear distance exploring", count, "states"
    #path, count = p.solve(h_linear_lsq)
    #print "Solved with linear least squares exploring", count, "states"
#    path, count = p.solve(heur_default)
#    print "Solved with BFS-equivalent in", count, "moves"




"""
s = squarePuzzle()
#print (s.matrix)
s.shuffle(100)
for i in s.matrix:
    print (i)
print ("")

path, count = s.solve(s.manhattan_dis)

for i in path:
    print i
"""
"""goal = \
    [[1,2,3,4]
    ,[5,6,7,8]
    ,[9,10,11,12]
    ,[13,14,15,0]]
"""



#print(s.manhattan_dis(s.matrix,GState))

#states=s.get_possible_stste(s,s.misPlace)
#for i in states:
#    print("\n")
#    for x in i:
#        print x

#for i in nstate:
 #   print (i)



#for x in nstate:
   # for row in x:
    #    print(row)

    #print ("\n")

