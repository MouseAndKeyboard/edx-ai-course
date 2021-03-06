"""
Skeleton code for Project 1 of Columbia University's AI EdX course (8-puzzle).
Python 3
"""

import queue as Q

import time

import resource

import sys

import math

#### SKELETON CODE ####

## The Class that Represents the Puzzle

class PuzzleState(object):

    """docstring for PuzzleState"""

    def __init__(self, config, n, parent=None, action="Initial", cost=0):

        if n*n != len(config) or n < 2:

            raise Exception("the length of config is not correct!")

        self.n = n

        self.cost = cost

        self.parent = parent

        self.action = action

        self.dimension = n

        self.config = config

        self.children = []

        for i, item in enumerate(self.config):

            if item == 0:

                self.blank_row = i // self.n

                self.blank_col = i % self.n

                break

    def __lt__(self, value):
        thisval = 0
        otherval = 0
        if self.action == "Up":
            thisval = 0
        elif self.action == "Down":
            thisval = 1
        elif self.action == "Left":
            thisval = 2
        elif self.action == "Right":
            thisval = 3

        if value.action == "Up":
            otherval = 0
        elif value.action == "Down":
            otherval = 1
        elif value.action == "Left":
            otherval = 2
        elif value.action == "Right":
            otherval = 3

        return thisval < otherval

    def __eq__(self, value):
        return self.config == value.config

    def display(self):

        for i in range(self.n):

            line = []

            offset = i * self.n

            for j in range(self.n):

                line.append(self.config[offset + j])

            print(line)

    def move_left(self):

        if self.blank_col == 0:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index - 1

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):

        if self.blank_col == self.n - 1:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index + 1

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):

        if self.blank_row == 0:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index - self.n

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):

        if self.blank_row == self.n - 1:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index + self.n

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)

    def expand(self):

        """expand the node"""

        # add child nodes in order of UDLR

        if len(self.children) == 0:

            up_child = self.move_up()

            if up_child is not None:

                self.children.append(up_child)

            down_child = self.move_down()

            if down_child is not None:

                self.children.append(down_child)

            left_child = self.move_left()

            if left_child is not None:

                self.children.append(left_child)

            right_child = self.move_right()

            if right_child is not None:

                self.children.append(right_child)

        return self.children

# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters

def writeOutput(node, nodes_expanded):
    path = []
    path.append(node)
    while node.parent is not None:
        path.append(node.parent)
        node = node.parent

    path = path[:-1]

    output_string = f"""path_to_goal: {[x.action for x in reversed(path)]}\ncost_of_path: {len(path)}\nnodes_expanded: {nodes_expanded}\nsearch_depth: {0}\nmax_search_depth: {0}"""

    with open('output.txt', mode='w+') as output_file:
        output_file.write(output_string)

   
def bfs_search(initial_state):
    """BFS search"""

    discovered = [initial_state]
    frontier = Q.Queue()
    frontier.put(initial_state)
    nodes_expanded = 0
    while not frontier.empty():
        v = frontier.get()

        if test_goal(v):
            return (v, nodes_expanded)
      
        nodes_expanded += 1
        for edge in v.expand():
            if edge not in discovered:
                valid_children = True
                discovered.append(edge)
                frontier.put(edge)




def dfs_search(initial_state: PuzzleState):
    """DFS search"""

    frontier = []
    discovered = []
    nodes_expanded = 0
    
    frontier.append(initial_state)
    while len(frontier) > 0:
        v = frontier.pop()

        if test_goal(v):
            return (v, nodes_expanded)
            
        if v not in discovered:
            discovered.append(v)
            nodes_expanded += 1
            for child in v.expand():
                frontier.append(child)



def A_star_search(initial_state):
    """A * search"""

    discovered = []
    frontier = Q.PriorityQueue()

    frontier.put((calculate_total_cost(initial_state), initial_state))

    discovered = []
    nodes_expanded = 0

    while not frontier.empty():
        (cost, v) = frontier.get()
        
        if test_goal(v):
            return (v, nodes_expanded)
        if v not in discovered:
            discovered.append(v)
            nodes_expanded += 1
            for child in v.expand():
                frontier.put((calculate_total_cost(child), child))

    

def calculate_total_cost(state):

    """calculate the total estimated cost of a state"""

    total_cost = 0
    n = state.n
    for current, target in zip(state.config, range(n*n)):
        total_cost += calculate_manhattan_dist(current, target, n)

    return state.cost + total_cost

    

def calculate_manhattan_dist(index_current, index_target, n):
    """calculate the manhattan distance of a tile"""
    
    current_col = index_current % n
    current_row = index_current // n

    target_col = index_target % n
    target_row = index_target // n

    manhattan = abs(current_col - target_col) + abs(current_row - target_row)
    return manhattan


def test_goal(puzzle_state: PuzzleState):
    """test the state is the goal state or not"""
    if puzzle_state.config == tuple(sorted(puzzle_state.config)):
        return True
    else:
        return False 

# Main Function that reads in Input and Runs corresponding Algorithm

def main():

    sm = sys.argv[1].lower()

    begin_state = sys.argv[2].split(",")

    begin_state = tuple(map(int, begin_state))

    size = int(math.sqrt(len(begin_state)))

    hard_state = PuzzleState(begin_state, size)
    result = None
    if sm == "bfs":

        result, nodes_expanded = bfs_search(hard_state)

    elif sm == "dfs":

        result, nodes_expanded = dfs_search(hard_state)

    elif sm == "ast":
        result, nodes_expanded = A_star_search(hard_state)

    else:

        print("Enter valid command arguments !")
        quit()
    
    writeOutput(result, nodes_expanded)

if __name__ == '__main__':

    main()