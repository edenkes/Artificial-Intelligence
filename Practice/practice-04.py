# practice-04.py
# Inteligencia Artificial, tercer curso del Grado de IngenierÃ­a InformÃ¡tica -
# Grupo en InglÃ©s. Universidad de Sevilla.

# Practice 4: Planning
# ===========================================================================

# In this practice, we implement the representation of a number of problems as
# state spaces, and also we implement a depth-first search algorithm to solve
# problems represented in that way. We also explore how we can use heuristics
# to improve the performance of searching.

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
            return (jug4, 0)
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

        if action == "Move the space up":
            new_pos = pos_blank - 3
        elif action == "Move the space down":
            new_pos = pos_blank + 3
        elif action == "Move the space to the right":
            new_pos = pos_blank + 1
        elif action == "Move the space to the left":
            new_pos = pos_blank - 1
        else:  # "Transfer from 3-liter jug to 4-liter jug"
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
    return DFS_rec(problem, [], [i_s], i_s)


def DFS_rec(problem, seq, visited, current):
    if problem.is_final_state(current):
        return seq
    else:
        for act in problem.action(current):
            sec = problem.apply(current, act)
            if sec not in visited:
                visited.append(sec)
                res = DFS_rec(problem, seq + [act], visited, sec)
                if res:
                    return res
        else:
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













# ============================






# ----------
# Exercise 6
# ----------

# Define an heuristic for the Arithmetic problem



# ======== Solution:







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








# ======================



# ===========
# Exercise 9
# ===========

# The following heuristics h3_eight_puzzle is a refinement of h2_eight_puzzle
# and is obtained summing to h2 a component quantifying how close to the final
# state is a given state, when we read the board clockwise.



def h2_eight_puzzle(state):
    pass


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
