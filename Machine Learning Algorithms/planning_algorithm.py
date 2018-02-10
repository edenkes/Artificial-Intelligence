# =====================================
# PARTE I. STATE SPACES REPRESENTATION
# =====================================

# According to unit 6, when we talk about "implementing the representation",
# we mean:

# * Represent states and actions using suitable data structures
# * Define: initial_state, is_final_state(_), actions(_) and apply(_,_).

# The following class Problem represent this general pattern. Concrete
# problems should be defined as subclasses of Problem, implementing the
# concrete versions of actions, apply and eventually __init__,
# is_final_state.
import re
from functools import reduce


class Problem(object):
    """Abstract class for state space problem. Concrete problems have to be
    defined as subclasses of Problem, implementing the concrete versions of
    actions(_), apply and eventually __init__, is_final_state. Instances of
    that subclass would be the input for the search procedures."""

    def __init__(self, initial_state, final_state=None):
        """ The constructor specifies the initial state and eventually the
        final state (if unique). Subclasses could in principle add more
        arguments"""

        self.initial_state = initial_state
        self.final_state = final_state

    def actions(self, state):
        """It returns the list of actions applicable to a give state"""
        pass

    def apply(self, state, action):
        """ Returns the resultimg state after applying action to state. We
        assume the action applicable to state"""
        pass

    def is_final_state(self, state):
        """Returns True when state is final. By default, checks equality with
        the final state (if it has been introduced by the constructor). When
        there is not only one final state, then this function has to be
        defined in the corresponding subclass."""

        return state == self.final_state


# The following is an example of how we implement the representation of a
# concrete problem (the water jugs problem), as a subclass of Problem. See a
# description of this problem in unit 6 slides.

class Jugs(Problem):
    """Jugs problem:
    We represent a state as a tuple (x,y), the respective contents (in number
    of liters) of the 4-liter and 3-liter jugs."""

    def __init__(self):
        super().__init__((0, 0))

    def actions(self, state):
        jug4 = state[0]
        jug3 = state[1]
        accs = list()
        if jug4 > 0:
            accs.append("Empty 4-liter jug")
            if jug3 < 3:
                accs.append("Transfer from 4-liter jug to 3-liter jug")
        if jug4 < 4:
            accs.append("Fill 4-liter jug")
            if jug3 > 0:
                accs.append("Transfer from 3-liter jug to 4-liter jug")
        if jug3 > 0:
            accs.append("Empty 3-liter jug")
        if jug3 < 3:
            accs.append("Fill 3-liter jug")
        return accs

    def apply(self, state, action):
        jug4 = state[0]
        jug3 = state[1]
        if action == "Fill 4-liter jug":
            return (4, jug3)
        elif action == "Fill 3-liter jug":
            return (jug4, 3)
        elif action == "Empty 4-liter jug":
            return (0, jug3)
        elif action == "Empty 3-liter jug":
            return jug4, 0
        elif action == "Transfer from 4-liter jug to 3-liter jug":
            return (jug4 - 3 + jug3, 3) if jug3 + jug4 >= 3 else (0, jug3 + jug4)
        else:  # "Transfer from 3-liter jug to 4-liter jug"
            return (jug3 + jug4, 0) if jug3 + jug4 <= 4 else (4, jug3 - 4 + jug4)

    def is_final_state(self, state):
        return state[0] == 2


# Examples:

# In [1]: pj=Jugs()
#
# In [2]: pj.initial_state
# Out[2]: (0, 0)
#
# In [3]: pj.actions(pj.initial_state)
# Out[3]: ['Fill 4-liter jug', 'Fill 3-liter jug']
#
# In [4]: pj.is_final_state(pj.initial_state)
# Out[4]: False




# ----------
# Exercise 1
# ----------

# ---------------------------------------------------------------------------
# Define the clasee Eight_Puzzle, implementing the represention of the
# 8-puzzle problem. For hat, complete the following code, susbtituting the
# question marks.
# ----------------------------------------------------------------------------


class Eight_Puzzle(Problem):
    #     """8-puzzle problem. States are tuples of length 9, permutations of the
    #     numbers from 0 to 8 (0 is the empty space). The represent the blocks
    #     positions, reading the rows from top to bottom and each row from left to
    #     right. For example, the final  state is the tuple (1, 2, 3, 8, 0, 4, 7, 6,
    #     5). The four actions of the problem are represented by the strings "Up",
    #     "Down", "Left" and "Right", meaning a "movement" of the empty space in that
    #     direction."""


    def __init__(self, initial_board):
        super().__init__(initial_state=initial_board, final_state=(1, 2, 3, 8, 0, 4, 7, 6, 5))

    def actions(self, state):
        pos_blank = state.index(0)
        # print(pos_blank)
        acts = list()
        if pos_blank not in [0, 1, 2]:
            acts.append("Move the space up")
        if pos_blank not in [2, 5, 8]:
            acts.append("Move the space to the right")
        if pos_blank not in [6, 7, 8]:
            acts.append("Move the space down")
        if pos_blank not in [0, 3, 6]:
            acts.append("Move the space to the left")
        return acts

    def apply(self, state, action):
        pos_blank = state.index(0)
        resl = list(state)
        new_pos = []
        if action == "Move the space up":
            new_pos = pos_blank - 3
        elif action == "Move the space down":
            new_pos = pos_blank + 3
        elif action == "Move the space to the right":
            new_pos = pos_blank + 1
        elif action == "Move the space to the left":
            new_pos = pos_blank - 1
        else:
            pass

        resl[pos_blank], resl[new_pos] = resl[new_pos], resl[pos_blank]

        return tuple(resl)


# Examples that can be executed once the class have been defined:


# In [1]: p8p_1 = Eight_Puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5))
#
# In [2]: p8p_1.initial_state
# Out[2]: (2, 8, 3, 1, 6, 4, 7, 0, 5)
#
# In [3]: p8p_1.final_state
# Out[3]: (1, 2, 3, 8, 0, 4, 7, 6, 5)
#
# In [4]: p8p_1.actions(p8p_1.initial_state)
# Out[4]: ['Up', 'Left', 'Right']
#
# In [5]: p8p_1.apply(p8p_1.initial_state,"Up")


# ----------
# Exercise 2
# ----------


# Define a class Arithmetic, sibclass of the class Problem, implementing the
# representation of the arithmetic problem described in Exercise of the
# Problem set of unit 6.

# The problem is: starting from 0, apply arithmetic operations to obtain a
# given goal numbre T. The only allowed arithmetic operations are: take the
# current number, and sum/substract/multiply/divide by n or m, where n and m
# are two given numbers. An additional restriction is that we can not use
# each of these numbers (n or m), more than a given number of times (r).

# For example, if we have T=67,n=2,m=7 and r=3, then a solution is:
# ((((((0+3)+3)*3)/7)+7)*7)

# Or if we have T=653, n=7, m=5 and r=4, then a possible solution
# is: ((((((((0+7)*5)*5)*5)/7)+7)*5)-7) and another (shorter) solution is
# ((((((0+5)*5)*5)+7)*5)-7)

# Examples:

# In [1]: pa1=Arithmetic(67,3,7,3)
#
# In [2]: pa1.actions(pa1.initial_state)
# Out[2]: [('+', 3),('-', 3),('*', 3), ('/', 3),
#         ('+', 7),('-', 7),('*', 7), ('/', 7)]

# ========== Solution:
class Arithmetic(Problem):
    def __init__(self, Tot, n, m, r):
        super().__init__(initial_state=(0, r, r))
        self.n = n
        self.m = m
        self.Tot = Tot
        self._dict_op = {"+": lambda x, y: x + y,
                         "-": lambda x, y: x - y,
                         "*": lambda x, y: x * y,
                         "/": lambda x, y: x / y, }

    def actions(self, state):
        acts = []
        ns = state[1]
        ms = state[2]
        if ns != 0:
            acts.extend([(op, self.n) for op in ["+", "-", "*", "/"]])
        if ms != 0:
            acts.extend([(op, self.m) for op in ["+", "-", "*", "/"]])
        return acts

    def apply(self, state, action):
        new_c = self._dict_op[action[0]](state[0], action[1])
        new_ns = state[1]
        new_ms = state[2]
        if action[1] == self.n:
            new_ns -= 1
        else:
            new_ms -= 1
        return new_c, new_ns, new_ms

    def is_final_state(self, state):
        return state[0] == self.Tot


# =======================


# =============================
# PART II. DEPTH-FIRST SEARCH
# =============================


# ----------
# Exercise 3
# ----------

# Implement a function depth_first_search(problem), that takes as input an
# object of the class Problem and apply a depth-first search algorithm to
# obtain a solution of the problem. Succesors of a state should be explored in
# the same order as given by the method "actions" of the Problem object.

# Examples:

# In [1]: depth_first_search(pj)
# Out[1]:
# ['Fill 4-liter jug',
# 'Transfer from 4-liter jug to 3-liter jug',
# 'Empty 4-liter jug',
# 'Transfer from 3-liter jug to 4-liter jug',
# 'Fill 3-liter jug',
# 'Transfer from 3-liter jug to 4-liter jug',
# 'Empty 4-liter jug',
# 'Transfer from 3-liter jug to 4-liter jug']

# In [2]: depth_first_search(pa1)
# Out[2]: [('+', 3), ('+', 3), ('*', 3), ('/', 7), ('+', 7), ('*', 7)]

# In [3]: depth_first_search(p8p_1)
# ERROR (maximum recursion depth exceeded)

# =========== Solution:
def depth_first_search(problem):
    i_s = problem.initial_state
    # Return DFS - REC({}, {*INITIAL - STATE *}, *INITIAL - STATE *)
    return DFS_rec(problem, [], [i_s], i_s, 0)


def DFS_rec(problem, seq, visited, current, high):
    # print("DFS_rec", len(visited), current, problem.is_final_state(current))

    # If IS-FINAL-STATE(CURRENT) then return SEQ
    if problem.is_final_state(current):
        return seq
    if high > 100:
        return False
    # For each ACT in ACTIONS(CURRENT)
    for act in problem.actions(current):
        # Let S’=APPLY(ACT,CURRENT)
        sec = problem.apply(current, act)
        # If S’ is not in VISITED
        if sec not in visited:
            visited.append(sec)
            # Let RES equal to DFS-REC(SEQACT,VISITED U {S’},S’)
            res = DFS_rec(problem, seq + [act], visited, sec, high + 1)
            # If RES is not FAIL, return RES and halt
            if res:
                return res
    # Return FAIL
    return False


# ==============

# ----------
# Exercise 4
# ----------

# Define a function check_solution(problem,sequence) such that given a state
# space problem (an object of the class Problem) and a sequence of actions,
# check if that sequence is solution of the problem.

# Example:

# In [1]: seqj=depth_first_search(pj)
#
# In [2]: check_solution(pj,seqj)
# Out[2]: True
#
# In [3]: check_solution(pj,reversed(seqj))
# Out[3]: False
#
# In [4]: check_solution(pj,seqj[:-1])
# Out[4]: False

# ======= Solution:
def check_solution(problem, sequence):
    currnt = problem.initial_state
    # print("check_solution", currnt, sequence)
    for unit in sequence:
        currnt = problem.apply(currnt, unit)
    return problem.is_final_state(currnt)


# ==================


# =====================
# PART III. HEURISTICS
# =====================


# ----------
# Exercise 5
# ----------

# Define the two heuristics for the 8-puzzle problem that have been given in
# unit 6. That is:

# h1_eight_puzzle(state): number of tiles in wrong positions in state
# h2_eight_puzzle(state): sum of the (Manhattan) distances form the curent position of
#                         each tile in state to its correct position.

# Examples:

# In [1]: h1_eight_puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5))
# Out[1]: 4
#
# In [2]: h2_eight_puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5))
# Out[2]: 5
#
# In [3]: h1_eight_puzzle((5,2,3,0,4,8,7,6,1))
# Out[3]: 4
#
# In [4]: h2_eight_puzzle((5,2,3,0,4,8,7,6,1))
# Out[4]: 11


# ========== Solution:
def h1_eight_puzzle(state):
    final_state = (1, 2, 3, 8, 0, 4, 7, 6, 5)
    return sum(final_i == state_i for final_i, state_i in zip(final_state, state))


def h2_eight_puzzle(state):
    final_state = (1, 2, 3, 8, 0, 4, 7, 6, 5)
    vertical = sum(abs(int(final_state.index(i) / 3) - int(state.index(i) / 3)) for i in range(1, 9))
    horzintel = sum(abs(int(final_state.index(i) % 3) - int(state.index(i) % 3)) for i in range(1, 9))
    return horzintel + vertical


# ============================






# ----------
# Exercise 6
# ----------

# Define an heuristic for the Arithmetic problem



# ======== Solution:
def heuristic_arithmetic(state):
    return abs(state[0] - 67)


# =================



# ============================================
# PART IV. DEPTH-FIRST-SEARCH WITH HEURISTICS
# ============================================

# ----------
# Exercise 7
# ----------

# Define a function depth_first_search_h(problem,h) implementing depth-first
# search in the state space described by problem, in which succesors of a
# state are explored in the order given by a given heuristic h.


# ======= Solution:
def depth_first_search_h(problem, h):
    i_s = problem.initial_state
    # Return DFS - REC({}, {*INITIAL - STATE *}, *INITIAL - STATE *)
    return depth_first_search_h_rec(problem, [], [i_s], i_s, h, 0)


def depth_first_search_h_rec(problem, seq, visited, current, h, high):
    # print(current)
    # If IS-FINAL-STATE(CURRENT) then return SEQ
    if problem.is_final_state(current):
        return seq
    if high > 100:
        return False
    # For each ACT in HEURISTIC-SORT(ACTIONS(CURRENT))
    # Where HEURISTIC-SORT is a function that sorts (in ascending order)
    for act in sorted(problem.actions(current), key=lambda act: h(problem.apply(current, act))):
        # Let S’=APPLY(ACT,CURRENT)
        sec = problem.apply(current, act)
        # If S’ is not in VISITED
        if sec not in visited:
            visited.append(sec)
            # Let RES equal to DFS-REC(SEQACT,VISITED U {S’},S’)
            res = depth_first_search_h_rec(problem, seq + [act], visited, sec, h, high + 1)
            # If RES is not FAIL, return RES and halt
            if res:
                return res
    # Return FAIL
    return False


# =======================



# ----------
# Exercise 8
# ----------

# Experiment the results we obtain when searching using depth-first search
# (with and without heuristiucs), in the state spaces we have defined, and
# with the heuristcs we have implemented. In particular:

# - Several instances of the arithmetic problem
# - 8-puzzle with the following initial states:

#           E1              E2              E3              E4
#
#     +---+---+---+   +---+---+---+   +---+---+---+   +---+---+---+
#     | 2 | 8 | 3 |   | 4 | 8 | 1 |   | 2 | 1 | 6 |   | 5 | 2 | 3 |
#     +---+---+---+   +---+---+---+   +---+---+---+   +---+---+---+
#     | 1 | 6 | 4 |   | 3 | H | 2 |   | 4 | H | 8 |   | H | 4 | 8 |
#     +---+---+---+   +---+---+---+   +---+---+---+   +---+---+---+
#     | 7 | H | 5 |   | 7 | 6 | 5 |   | 7 | 5 | 3 |   | 7 | 6 | 1 |
#     +---+---+---+   +---+---+---+   +---+---+---+   +---+---+---+

# epp1=Eight_Puzzle((2,8,3,1,6,4,7,0,5))
# epp2=Eight_Puzzle((4,8,1,3,0,2,7,6,5))
# epp3=Eight_Puzzle((2,1,6,4,0,8,7,5,3))
# epp4=Eight_Puzzle((5,2,3,0,4,8,7,6,1))


# Compare the time taken to find a solution and the length of that solution.


# ========= Solution:
epp1 = Eight_Puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5))


# print(depth_first_search_h(epp1, h2_eight_puzzle))
# print(depth_first_search(epp1))






# ======================



# ===========
# Exercise 9
# ===========

# The following heuristics h3_eight_puzzle is a refinement of h2_eight_puzzle
# and is obtained summing to h2 a component quantifying how close to the final
# state is a given state, when we read the board clockwise.



def h3_eight_puzzle(state):
    suc_eight_puzzle = {0: 1, 1: 2, 2: 5, 3: 0, 4: 4, 5: 8, 6: 3, 7: 6, 8: 7}

    def sequential_aux(state, i):

        val = state[i]
        if val == 0:
            return 0
        elif i == 4:
            return 1
        else:
            i_sig = suc_eight_puzzle[i]
            val_sig = (val + 1 if val < 8 else 1)
            return 0 if val_sig == state[i_sig] else 2

    def sequential(state):
        res = 0
        for i in range(8):
            res += sequential_aux(state, i)
        return res

    return h2_eight_puzzle(state) + 3 * sequential(state)


# Try h3 with the four initial 8-puzzles above.


# ============ Solution:







# =====================
class RiverBank(Problem):
    def __init__(self, M, C, P):
        initial_state = (M, 0, C, 0, 0)
        final_state = (0, M, 0, C, 1)
        # print(initial_state, final_state)
        super().__init__(initial_state=initial_state, final_state=final_state)
        self.M = M
        self.C = C
        self.P = P
        self.map_state = {'missionaries_left': 0, 'missionaries_right': 1, 'cannibals_left': 2, 'cannibals_right': 3,
                          'boat': 4}

    def actions(self, state):
        acts = list()
        capacity = self.P
        missionaries_left = state[self.map_state['missionaries_left']]
        missionaries_right = state[self.map_state['missionaries_right']]
        # missionaries_right = sum(state[i] == 1 for i in range(self.M))
        cannibals_left = state[self.map_state['cannibals_left']]
        cannibals_right = state[self.map_state['cannibals_right']]
        # print(capacity, missionaries_left, missionaries_right, cannibals_left, cannibals_right)

        if state[self.map_state['boat']]:
            for m in range(min(missionaries_right, capacity) + 1):
                for c in range(min(cannibals_right, capacity - m) + 1):
                    if (missionaries_right - m == 0 or (missionaries_right - m) >= (cannibals_right - c)):
                        # and ((missionaries_left + m) == 0 or missionaries_left + m >= cannibals_left + c):
                        acts.append("Move {} missionaries and {} the cannibals to the left bank".format(m, c))
        else:
            for m in range(min(missionaries_left, capacity) + 1):
                for c in range(min(cannibals_left, capacity - m) + 1):
                    # print(m, c, (missionaries_left - m) == 0 or (missionaries_left - m) >= (cannibals_left - c))
                    if ((missionaries_left - m) == 0 or (missionaries_left - m) >= (cannibals_left - c)):
                        # and (missionaries_right + m == 0 or missionaries_right + m >= cannibals_right + c):
                        acts.append("Move {} missionaries and {} the cannibals to the right bank".format(m, c))
        # print(acts, reversed(acts))
        return list(reversed(acts))

    def apply(self, state, action):
        resl = list(state)
        # print(state, action)
        if 'right' in action:
            # print('right', state, action)
            switch = re.findall('\d+', action)
            m = int(switch[0])
            c = int(switch[1])
            resl = (state[self.map_state['missionaries_left']] - m, state[self.map_state['missionaries_right']] + m,
                    state[self.map_state['cannibals_left']] - c, state[self.map_state['cannibals_right']] + c, 1)
            # print(resl)
        else:
            # print('left', state, action)
            switch = re.findall('\d+', action)
            m = int(switch[0])
            c = int(switch[1])
            resl = (state[self.map_state['missionaries_left']] + m, state[self.map_state['missionaries_right']] - m,
                    state[self.map_state['cannibals_left']] + c, state[self.map_state['cannibals_right']] - c, 0)
        return resl


def heuristic_river_bank(state):
    return state[0] + state[2]


# =====================
class LinearBoard(Problem):
    def __init__(self):
        initial_state = (1, 1, 1, 2, 2, 2, 0)
        super().__init__(initial_state=initial_state)

    def actions(self, state):
        acts = list()
        pos_empty = state.index(0)
        if pos_empty < 6:
            acts.append("Move the empty adjacent 1 step right")
        if pos_empty < 5:
            acts.append("Move the empty adjacent 2 step right")
        if pos_empty < 4:
            acts.append("Move the empty adjacent 3 step right")
        if pos_empty > 0:
            acts.append("Move the empty adjacent 1 step left")
        if pos_empty > 1:
            acts.append("Move the empty adjacent 2 step left")
        if pos_empty > 2:
            acts.append("Move the empty adjacent 3 step left")
        return list(acts)

    def apply(self, state, action):
        resl = list(state)
        pos_empty = state.index(0)
        # print(state, action)
        if 'right' in action:
            # print('right', state, action)
            switch = re.findall('\d+', action)
            step = int(switch[0])
            resl[pos_empty], resl[pos_empty + step] = resl[pos_empty + step], resl[pos_empty]
            # print(resl)
        else:
            # print('left', state, action)
            switch = re.findall('\d+', action)
            step = int(switch[0])
            resl[pos_empty], resl[pos_empty - step] = resl[pos_empty - step], resl[pos_empty]

        return tuple(resl)

    def is_final_state(self, state):
        index_black = []
        index_white = []

        for i, j in enumerate(state):
            if j == 1:
                index_black.append(i)
            elif j == 2:
                index_white.append(i)
        return all(i < min(index_black) for i in index_white)


def heuristic_linear_board(state):
    index_black = []
    index_white = []

    for i, j in enumerate(state):
        if j == 1:
            index_black.append(i)
        elif j == 2:
            index_white.append(i)
    # print(sum(1 if i > min(index_black) else 0 for i in index_white))
    return sum(1 if i > min(index_black) else 0 for i in index_white)


class JugsPro(Problem):
    "Jugs Pro problem:"

    def __init__(self, jugs, goal):
        self.length = len(jugs)
        super().__init__(tuple(0 for _ in range(len(jugs))))
        self.jugs = jugs
        self.goal = goal

    def actions(self, state):
        accs = list()
        for i in range(self.length):
            if state[i] > 0:
                accs.append("Empty {}-liter jug-{}".format(self.jugs[i], i))
                for j in range(self.length):
                    if i != j and state[j] < self.jugs[j]:
                        accs.append(
                            "Transfer from {}-liter jug-{} to {}-liter jug-{}".format(self.jugs[i], i, self.jugs[j], j))
            if state[i] < self.jugs[i]:
                accs.append("Fill {}-liter jug-{}".format(self.jugs[i], i))
        return accs

    def apply(self, state, action):
        resl = list(state)
        if "Fill" in action:
            act = re.findall('\d+', action)
            amount = int(act[0])
            index = int(act[1])
            resl[index] = amount
        if "Empty" in action:
            act = re.findall('\d+', action)
            index = int(act[1])
            resl[index] = 0
        if "Transfer" in action:
            act = re.findall('\d+', action)
            amount1 = int(act[0])
            index1 = int(act[1])
            amount2 = int(act[2])
            index2 = int(act[3])
            amount_state1 = resl[index1]
            amount_state2 = resl[index2]
            resl[index2] = min(amount_state1 + amount_state2, amount2)
            resl[index1] = max(0, amount_state1 + amount_state2 - amount2)

        return tuple(resl)

    def is_final_state(self, state):
        return any(state[i] == self.goal for i in range(self.length))

    def heuristic(self, state):
        return reduce((lambda x, y: x * y), [abs(self.goal - state[i]) for i in range(self.length)])
        # return min(abs(self.goal - state[i]) for i in range(self.length))


# =====================
def tests():
    p8p_1 = Eight_Puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5))
    if p8p_1.initial_state != (2, 8, 3, 1, 6, 4, 7, 0, 5):
        print("faild 1", p8p_1.initial_state)
    if p8p_1.final_state != (1, 2, 3, 8, 0, 4, 7, 6, 5):
        print("faild 2", p8p_1.final_state)
    if p8p_1.actions(p8p_1.initial_state) != ['Move the space up', 'Move the space to the right',
                                              'Move the space to the left']:
        print("faild 2a", p8p_1.actions(p8p_1.initial_state))
    if p8p_1.apply(p8p_1.initial_state, "Move the space up") != (2, 8, 3, 1, 0, 4, 7, 6, 5):
        print("faild 3", p8p_1.apply(p8p_1.initial_state, "Move the space up"))
    if p8p_1.is_final_state(p8p_1.initial_state) != False:
        print(p8p_1.is_final_state(p8p_1.initial_state))
    if p8p_1.is_final_state(p8p_1.final_state) != True:
        print(p8p_1.is_final_state(p8p_1.initial_state))

    p8p_2 = Eight_Puzzle((1, 2, 3, 8, 4, 0, 7, 6, 5))
    if depth_first_search(p8p_2) != \
            ['Move the space up', 'Move the space to the left', 'Move the space down', 'Move the space to the right',
             'Move the space up', 'Move the space to the left', 'Move the space down', 'Move the space to the right',
             'Move the space up', 'Move the space to the left', 'Move the space down']:
        print(depth_first_search(p8p_2))

    pa1 = Arithmetic(67, 3, 7, 3)
    if pa1.actions(pa1.initial_state) != [('+', 3), ('-', 3), ('*', 3), ('/', 3), ('+', 7), ('-', 7), ('*', 7),
                                          ('/', 7)]:
        print("faild 4", pa1.actions(pa1.initial_state))
    if depth_first_search(pa1) != [('+', 3), ('+', 3), ('*', 3), ('/', 7), ('+', 7), ('*', 7)]:
        print(depth_first_search(pa1))
    if depth_first_search_h(pa1, heuristic_arithmetic) != [('+', 7), ('*', 7), ('-', 3), ('/', 3), ('+', 7), ('*', 3)]:
        print(depth_first_search_h(pa1, heuristic_arithmetic))

    pj = Jugs()
    if pj.initial_state != (0, 0):
        print("faild 5", pj.initial_state)
    if pj.actions(pj.initial_state) != ['Fill 4-liter jug', 'Fill 3-liter jug']:
        print("faild 6", pj.actions(pj.initial_state))
    if pj.is_final_state(pj.initial_state) != False:
        print("faild 7", pj.is_final_state(pj.initial_state))
    if depth_first_search(pj) != ['Fill 4-liter jug', 'Transfer from 4-liter jug to 3-liter jug', 'Empty 4-liter jug',
                                  'Transfer from 3-liter jug to 4-liter jug', 'Fill 3-liter jug',
                                  'Transfer from 3-liter jug to 4-liter jug', 'Empty 4-liter jug',
                                  'Transfer from 3-liter jug to 4-liter jug']:
        print(depth_first_search(pj))
    seqj = depth_first_search(pj)
    if check_solution(pj, seqj) != True:
        print(check_solution(pj, seqj))
    seqj = ['Fill 4-liter jug', 'Transfer from 4-liter jug to 3-liter jug', 'Empty 4-liter jug',
            'Transfer from 3-liter jug to 4-liter jug', 'Fill 3-liter jug',
            'Transfer from 3-liter jug to 4-liter jug', 'Empty 4-liter jug']
    if check_solution(pj, seqj) != False:
        print(check_solution(pj, seqj))
    if check_solution(pj, reversed(seqj)) != False:
        print(check_solution(pj, reversed(seqj)))
    if check_solution(pj, seqj[:-1]) != False:
        print(check_solution(pj, seqj[:-1]))

    if h1_eight_puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5)) != 4:
        print(h1_eight_puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5)))
    if h2_eight_puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5)) != 5:
        print(h2_eight_puzzle((2, 8, 3, 1, 6, 4, 7, 0, 5)))
    if h1_eight_puzzle((5, 2, 3, 0, 4, 8, 7, 6, 1)) != 4:
        print(h1_eight_puzzle((5, 2, 3, 0, 4, 8, 7, 6, 1)))
    if h2_eight_puzzle((5, 2, 3, 0, 4, 8, 7, 6, 1)) != 11:
        print(h2_eight_puzzle((5, 2, 3, 0, 4, 8, 7, 6, 1)))
    if depth_first_search_h(p8p_2, h2_eight_puzzle) != ['Move the space to the left']:
        print(depth_first_search_h(p8p_2, h2_eight_puzzle))
    if depth_first_search(p8p_2) != ['Move the space up', 'Move the space to the left', 'Move the space down',
                                     'Move the space to the right', 'Move the space up', 'Move the space to the left',
                                     'Move the space down', 'Move the space to the right', 'Move the space up',
                                     'Move the space to the left', 'Move the space down']:
        print(depth_first_search(p8p_2))
    epp4 = Eight_Puzzle((5, 2, 3, 0, 4, 8, 7, 6, 1))
    # if depth_first_search_h(epp4, h3_eight_puzzle) != ['Move the space to the right', 'Move the space to the right', 'Move the space down', 'Move the space to the left', 'Move the space to the left', 'Move the space up', 'Move the space up', 'Move the space to the right', 'Move the space to the right', 'Move the space down', 'Move the space to the left', 'Move the space down', 'Move the space to the right', 'Move the space up', 'Move the space to the left', 'Move the space down', 'Move the space to the left', 'Move the space up', 'Move the space to the right', 'Move the space to the right', 'Move the space up', 'Move the space to the left', 'Move the space to the left', 'Move the space down', 'Move the space down', 'Move the space to the right', 'Move the space up', 'Move the space to the right', 'Move the space down', 'Move the space to the left', 'Move the space up', 'Move the space to the right', 'Move the space up', 'Move the space to the left', 'Move the space down', 'Move the space down', 'Move the space to the right', 'Move the space up', 'Move the space up', 'Move the space to the left', 'Move the space down', 'Move the space down', 'Move the space to the left', 'Move the space up', 'Move the space up', 'Move the space to the right', 'Move the space down', 'Move the space to the right', 'Move the space up', 'Move the space to the left', 'Move the space down', 'Move the space to the right', 'Move the space up', 'Move the space to the left', 'Move the space to the left', 'Move the space down', 'Move the space down', 'Move the space to the right', 'Move the space to the right', 'Move the space up', 'Move the space to the left', 'Move the space down', 'Move the space to the right', 'Move the space up', 'Move the space to the left', 'Move the space down', 'Move the space to the right', 'Move the space up', 'Move the space up', 'Move the space to the left', 'Move the space down', 'Move the space down', 'Move the space to the left', 'Move the space up', 'Move the space up', 'Move the space to the right', 'Move the space down', 'Move the space down', 'Move the space to the left', 'Move the space up', 'Move the space up', 'Move the space to the right', 'Move the space down', 'Move the space to the right', 'Move the space down', 'Move the space to the left', 'Move the space up', 'Move the space up', 'Move the space to the right', 'Move the space down', 'Move the space to the left', 'Move the space down', 'Move the space to the left', 'Move the space up', 'Move the space up', 'Move the space to the right', 'Move the space down']:
    #     print(depth_first_search_h(epp4, h3_eight_puzzle))
    # if depth_first_search_h(epp4, h2_eight_puzzle) != ['Move the space up', 'Move the space to the right', 'Move the space to the right', 'Move the space down', 'Move the space down', 'Move the space to the left', 'Move the space up', 'Move the space to the right', 'Move the space up', 'Move the space to the left', 'Move the space down', 'Move the space to the right', 'Move the space up', 'Move the space to the left', 'Move the space to the left', 'Move the space down', 'Move the space to the right', 'Move the space down', 'Move the space to the right', 'Move the space up', 'Move the space to the left', 'Move the space up', 'Move the space to the right', 'Move the space down', 'Move the space down', 'Move the space to the left', 'Move the space up', 'Move the space up', 'Move the space to the left', 'Move the space down', 'Move the space to the right', 'Move the space up', 'Move the space to the right', 'Move the space down', 'Move the space to the left', 'Move the space up', 'Move the space to the right', 'Move the space down', 'Move the space to the left', 'Move the space down', 'Move the space to the right', 'Move the space up', 'Move the space up', 'Move the space to the left', 'Move the space down', 'Move the space to the right', 'Move the space down', 'Move the space to the left', 'Move the space up', 'Move the space up', 'Move the space to the right', 'Move the space down', 'Move the space down', 'Move the space to the left', 'Move the space up', 'Move the space to the right', 'Move the space up', 'Move the space to the left', 'Move the space down', 'Move the space down', 'Move the space to the right', 'Move the space up', 'Move the space up', 'Move the space to the left', 'Move the space down', 'Move the space to the right', 'Move the space up', 'Move the space to the left', 'Move the space down', 'Move the space to the right', 'Move the space down', 'Move the space to the left', 'Move the space up', 'Move the space up', 'Move the space to the right', 'Move the space down', 'Move the space to the left', 'Move the space up', 'Move the space to the right', 'Move the space down', 'Move the space down', 'Move the space to the left', 'Move the space to the left', 'Move the space up', 'Move the space up', 'Move the space to the right', 'Move the space down', 'Move the space to the left', 'Move the space down', 'Move the space to the right', 'Move the space to the right', 'Move the space up', 'Move the space up', 'Move the space to the left', 'Move the space to the left', 'Move the space down', 'Move the space to the right', 'Move the space up', 'Move the space to the right', 'Move the space down', 'Move the space to the left']:
    #     print(depth_first_search_h(epp4, h2_eight_puzzle))

    #     River_Bank
    riverB = RiverBank(1, 1, 2)
    if riverB.actions(riverB.initial_state) != ['Move 1 missionaries and 1 the cannibals to the right bank',
                                                'Move 1 missionaries and 0 the cannibals to the right bank',
                                                'Move 0 missionaries and 1 the cannibals to the right bank',
                                                'Move 0 missionaries and 0 the cannibals to the right bank']:
        print(riverB.actions(riverB.initial_state))
    if riverB.apply(riverB.initial_state, 'Move 0 missionaries and 0 the cannibals to the right bank') != (
            1, 0, 1, 0, 1):
        print(riverB.apply(riverB.initial_state, 'Move 0 missionaries and 0 the cannibals to the right bank'))
    if riverB.apply(riverB.initial_state, 'Move 1 missionaries and 1 the cannibals to the right bank') != (
            0, 1, 0, 1, 1):
        print(riverB.apply(riverB.initial_state, 'Move 1 missionaries and 1 the cannibals to the right bank'))

    riverB = RiverBank(3, 4, 2)
    if riverB.actions(riverB.initial_state) != ['Move 0 missionaries and 2 the cannibals to the right bank',
                                                'Move 0 missionaries and 1 the cannibals to the right bank']:
        print(riverB.actions(riverB.initial_state))
    if depth_first_search(riverB) != ['Move 0 missionaries and 2 the cannibals to the right bank',
                                      'Move 0 missionaries and 1 the cannibals to the left bank',
                                      'Move 1 missionaries and 1 the cannibals to the right bank',
                                      'Move 1 missionaries and 0 the cannibals to the left bank',
                                      'Move 1 missionaries and 1 the cannibals to the right bank',
                                      'Move 1 missionaries and 0 the cannibals to the left bank',
                                      'Move 2 missionaries and 0 the cannibals to the right bank',
                                      'Move 0 missionaries and 2 the cannibals to the left bank',
                                      'Move 1 missionaries and 1 the cannibals to the right bank',
                                      'Move 1 missionaries and 0 the cannibals to the left bank',
                                      'Move 1 missionaries and 1 the cannibals to the right bank',
                                      'Move 0 missionaries and 1 the cannibals to the left bank',
                                      'Move 0 missionaries and 2 the cannibals to the right bank']:
        print(depth_first_search(riverB))
    if check_solution(riverB, depth_first_search(riverB)) != True:
        print(check_solution(riverB, depth_first_search(riverB)))

    riverB = RiverBank(30, 23, 5)
    if (depth_first_search_h(riverB, heuristic_river_bank)) != \
            ['Move 5 missionaries and 0 the cannibals to the right bank',
             'Move 0 missionaries and 0 the cannibals to the left bank',
             'Move 3 missionaries and 2 the cannibals to the right bank',
             'Move 0 missionaries and 0 the cannibals to the left bank',
             'Move 3 missionaries and 2 the cannibals to the right bank',
             'Move 0 missionaries and 0 the cannibals to the left bank',
             'Move 2 missionaries and 3 the cannibals to the right bank',
             'Move 0 missionaries and 0 the cannibals to the left bank',
             'Move 3 missionaries and 2 the cannibals to the right bank',
             'Move 0 missionaries and 0 the cannibals to the left bank',
             'Move 2 missionaries and 3 the cannibals to the right bank',
             'Move 0 missionaries and 0 the cannibals to the left bank',
             'Move 3 missionaries and 2 the cannibals to the right bank',
             'Move 0 missionaries and 0 the cannibals to the left bank',
             'Move 2 missionaries and 3 the cannibals to the right bank',
             'Move 0 missionaries and 0 the cannibals to the left bank',
             'Move 3 missionaries and 2 the cannibals to the right bank',
             'Move 0 missionaries and 0 the cannibals to the left bank',
             'Move 4 missionaries and 1 the cannibals to the right bank',
             'Move 0 missionaries and 0 the cannibals to the left bank',
             'Move 0 missionaries and 3 the cannibals to the right bank']:
        print((depth_first_search_h(riverB, heuristic_river_bank)))
    if len(depth_first_search_h(riverB, heuristic_river_bank)) != 21:
        print(len(depth_first_search_h(riverB, heuristic_river_bank)))

    linear = LinearBoard()
    if linear.actions(linear.initial_state) != \
            ['Move the empty adjacent 1 step left', 'Move the empty adjacent 2 step left',
             'Move the empty adjacent 3 step left']:
        print(linear.actions(linear.initial_state))
    if linear.apply((1, 1, 1, 0, 2, 2, 2), 'Move the empty adjacent 1 step right') != (1, 1, 1, 2, 0, 2, 2):
        print(linear.apply((1, 1, 1, 0, 2, 2, 2), 'Move the empty adjacent 1 step right'))
    if not linear.is_final_state((0, 2, 2, 2, 1, 1, 1)):
        print(linear.is_final_state((0, 2, 2, 2, 1, 1, 1)))
    if linear.is_final_state((0, 2, 2, 1, 2, 1, 1)):
        print(linear.is_final_state((0, 2, 2, 1, 2, 1, 1)))
    if linear.is_final_state((1, 1, 1, 0, 2, 2, 2)):
        print(linear.is_final_state((1, 1, 1, 0, 2, 2, 2)))
    if depth_first_search(linear) != \
            ['Move the empty adjacent 1 step left', 'Move the empty adjacent 1 step left',
             'Move the empty adjacent 1 step left', 'Move the empty adjacent 1 step left',
             'Move the empty adjacent 2 step right', 'Move the empty adjacent 1 step right',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 3 step left',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 1 step right',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 2 step left',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 1 step right',
             'Move the empty adjacent 3 step left', 'Move the empty adjacent 1 step left',
             'Move the empty adjacent 1 step left', 'Move the empty adjacent 2 step right',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 1 step right',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 3 step left',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 1 step right',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 2 step left',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 3 step left',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 1 step right',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 1 step right',
             'Move the empty adjacent 2 step left', 'Move the empty adjacent 1 step right',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 3 step left',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 1 step right',
             'Move the empty adjacent 2 step left', 'Move the empty adjacent 1 step left',
             'Move the empty adjacent 1 step left', 'Move the empty adjacent 1 step left',
             'Move the empty adjacent 2 step right', 'Move the empty adjacent 1 step right',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 1 step right',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 2 step left',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 2 step left',
             'Move the empty adjacent 3 step right', 'Move the empty adjacent 1 step left',
             'Move the empty adjacent 1 step left', 'Move the empty adjacent 1 step left',
             'Move the empty adjacent 1 step left', 'Move the empty adjacent 3 step right',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 2 step left',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 1 step right',
             'Move the empty adjacent 2 step left', 'Move the empty adjacent 1 step left',
             'Move the empty adjacent 3 step right', 'Move the empty adjacent 1 step left',
             'Move the empty adjacent 2 step left', 'Move the empty adjacent 1 step left',
             'Move the empty adjacent 1 step left', 'Move the empty adjacent 3 step right',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 1 step right',
             'Move the empty adjacent 2 step left', 'Move the empty adjacent 1 step right',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 3 step left',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 1 step right',
             'Move the empty adjacent 2 step left', 'Move the empty adjacent 1 step left',
             'Move the empty adjacent 3 step right']:
        print(depth_first_search(linear))
    if len(depth_first_search(linear)) != 79:
        print(len(depth_first_search(linear)))
    if depth_first_search_h(linear, heuristic_linear_board) != \
            ['Move the empty adjacent 1 step left', 'Move the empty adjacent 1 step left',
             'Move the empty adjacent 1 step left', 'Move the empty adjacent 1 step left',
             'Move the empty adjacent 2 step right', 'Move the empty adjacent 1 step right',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 3 step left',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 1 step right',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 2 step left',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 1 step right',
             'Move the empty adjacent 3 step left', 'Move the empty adjacent 1 step left',
             'Move the empty adjacent 1 step left', 'Move the empty adjacent 2 step right',
             'Move the empty adjacent 3 step left', 'Move the empty adjacent 1 step right',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 1 step right',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 1 step right',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 3 step left',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 1 step right',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 2 step left',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 3 step left',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 2 step left',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 1 step right',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 1 step right',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 2 step left',
             'Move the empty adjacent 1 step right', 'Move the empty adjacent 1 step right',
             'Move the empty adjacent 3 step left', 'Move the empty adjacent 1 step right',
             'Move the empty adjacent 2 step left']:
        print(depth_first_search_h(linear, heuristic_linear_board))
    if len(depth_first_search_h(linear, heuristic_linear_board)) != 45:
        print(len(depth_first_search_h(linear, heuristic_linear_board)))

    jugs = JugsPro([4, 3, 2], 2)
    if jugs.initial_state != (0, 0, 0):
        print(jugs.initial_state)
    if jugs.actions((1, 3, 2)) != \
            ['Empty 4-liter jug-0', 'Fill 4-liter jug-0', 'Empty 3-liter jug-1',
             'Transfer from 3-liter jug-1 to 4-liter jug-0', 'Empty 2-liter jug-2',
             'Transfer from 2-liter jug-2 to 4-liter jug-0']:
        print(jugs.actions((1, 3, 2)))
    if jugs.apply((1, 1, 1), "Transfer from 3-liter jug-1 to 4-liter jug-0") != (2, 0, 1):
        print(jugs.apply((1, 1, 1), "Transfer from 3-liter jug-1 to 4-liter jug-0"))

    if jugs.is_final_state((0, 0, 0)) != False:
        print(jugs.is_final_state((0, 0, 0)))
    if jugs.is_final_state((2, 0, 0)) != True:
        print(jugs.is_final_state((2, 0, 0)))
    if jugs.is_final_state((0, 0, 2)) != True:
        print(jugs.is_final_state((0, 0, 2)))
    if jugs.is_final_state((0, 2, 2)) != True:
        print(jugs.is_final_state((0, 2, 2)))

    jugs = JugsPro([14, 23, 17, 33, 72, 11, 115], 10)
    if jugs.heuristic(jugs.initial_state) != 10000000:
        print(jugs.heuristic(jugs.initial_state))
    if depth_first_search_h(jugs, jugs.heuristic) != \
            ['Fill 11-liter jug-5', 'Fill 14-liter jug-0', 'Fill 17-liter jug-2',
             'Transfer from 14-liter jug-0 to 23-liter jug-1', 'Fill 14-liter jug-0',
             'Transfer from 17-liter jug-2 to 23-liter jug-1', 'Empty 23-liter jug-1',
             'Transfer from 14-liter jug-0 to 23-liter jug-1', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 33-liter jug-3', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 72-liter jug-4', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 115-liter jug-6', 'Fill 14-liter jug-0', 'Empty 23-liter jug-1',
             'Transfer from 17-liter jug-2 to 23-liter jug-1', 'Fill 17-liter jug-2', 'Empty 14-liter jug-0',
             'Transfer from 17-liter jug-2 to 14-liter jug-0', 'Transfer from 23-liter jug-1 to 17-liter jug-2',
             'Transfer from 14-liter jug-0 to 23-liter jug-1', 'Fill 14-liter jug-0', 'Empty 33-liter jug-3',
             'Transfer from 17-liter jug-2 to 33-liter jug-3', 'Fill 17-liter jug-2',
             'Transfer from 17-liter jug-2 to 23-liter jug-1', 'Empty 23-liter jug-1',
             'Transfer from 14-liter jug-0 to 23-liter jug-1', 'Fill 14-liter jug-0', 'Empty 72-liter jug-4',
             'Transfer from 17-liter jug-2 to 72-liter jug-4', 'Fill 17-liter jug-2',
             'Transfer from 17-liter jug-2 to 23-liter jug-1', 'Empty 23-liter jug-1',
             'Transfer from 14-liter jug-0 to 23-liter jug-1', 'Fill 14-liter jug-0', 'Empty 115-liter jug-6',
             'Transfer from 17-liter jug-2 to 115-liter jug-6', 'Fill 17-liter jug-2',
             'Transfer from 17-liter jug-2 to 23-liter jug-1', 'Empty 23-liter jug-1',
             'Transfer from 14-liter jug-0 to 23-liter jug-1', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 23-liter jug-1', 'Empty 23-liter jug-1',
             'Transfer from 14-liter jug-0 to 23-liter jug-1', 'Fill 14-liter jug-0',
             'Transfer from 23-liter jug-1 to 17-liter jug-2', 'Transfer from 14-liter jug-0 to 17-liter jug-2']:
        print(depth_first_search_h(jugs, jugs.heuristic))
    if len(depth_first_search_h(jugs, jugs.heuristic)) != 50:
        print(len(depth_first_search_h(jugs, jugs.heuristic)))
    if depth_first_search(jugs) != \
            ['Fill 14-liter jug-0', 'Transfer from 14-liter jug-0 to 23-liter jug-1', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 23-liter jug-1', 'Empty 14-liter jug-0', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 17-liter jug-2', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 17-liter jug-2', 'Empty 14-liter jug-0', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 33-liter jug-3', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 33-liter jug-3', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 33-liter jug-3', 'Empty 14-liter jug-0', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 72-liter jug-4', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 72-liter jug-4', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 72-liter jug-4', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 72-liter jug-4', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 72-liter jug-4', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 72-liter jug-4', 'Empty 14-liter jug-0', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 11-liter jug-5', 'Empty 14-liter jug-0', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 115-liter jug-6', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 115-liter jug-6', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 115-liter jug-6', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 115-liter jug-6', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 115-liter jug-6', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 115-liter jug-6', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 115-liter jug-6', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 115-liter jug-6', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 115-liter jug-6', 'Empty 14-liter jug-0', 'Fill 14-liter jug-0',
             'Empty 23-liter jug-1', 'Empty 14-liter jug-0', 'Empty 17-liter jug-2', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 23-liter jug-1', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 23-liter jug-1', 'Empty 14-liter jug-0', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 17-liter jug-2', 'Fill 14-liter jug-0', 'Empty 23-liter jug-1',
             'Empty 14-liter jug-0', 'Empty 33-liter jug-3', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 23-liter jug-1', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 23-liter jug-1', 'Empty 14-liter jug-0', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 17-liter jug-2', 'Empty 14-liter jug-0', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 33-liter jug-3', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 33-liter jug-3', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 33-liter jug-3', 'Empty 23-liter jug-1',
             'Transfer from 14-liter jug-0 to 23-liter jug-1', 'Fill 14-liter jug-0', 'Empty 17-liter jug-2',
             'Empty 14-liter jug-0', 'Transfer from 23-liter jug-1 to 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 17-liter jug-2', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 23-liter jug-1', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 23-liter jug-1', 'Empty 14-liter jug-0', 'Fill 14-liter jug-0',
             'Transfer from 14-liter jug-0 to 17-liter jug-2', 'Empty 23-liter jug-1',
             'Transfer from 14-liter jug-0 to 23-liter jug-1', 'Fill 14-liter jug-0',
             'Transfer from 72-liter jug-4 to 23-liter jug-1', 'Empty 23-liter jug-1',
             'Transfer from 33-liter jug-3 to 23-liter jug-1']:
        print(depth_first_search(jugs))
    if len(depth_first_search(jugs)) != 101:
        print(len(depth_first_search(jugs)))


# =====================
def main():
    print("practice-04")

    tests()


# =====================
if __name__ == '__main__':
    main()
