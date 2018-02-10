# practice-01.py
# Artificial Intelligence, ETSII, Univ. Seville

# Práctice 1: Introduction to Python
# ==================================

# In this practice, we will see some basic exercises in python programming 


# -----------
# EXERCISE 1
# -----------
#
# Define a function squares(l), such that receiving a sequence l of numbers,
# returns the list of squares of those numbers, in the same order.  


# For  example:
# 
# >>> squares([4,1,5.2,3,8])
# [16, 1, 27.040000000000003, 9, 64]

# Write two versions: one using an explicit loop, and another using list
# comprehensions  
# ---------------------------------------------------------------------------






# -----------
# EXERCISE 2
# -----------

# Define a function vocals_consonants(s), such that receives a string s (only
# with capital letters), and prints if their letters are vocals or consonants,
# as shown in the following example. 

# Example:
# >>> vocals_consonants("INTELLIGENCE")
# I is vocal
# N is consonant
# T is consonant
# E is vocal
# L is consonant
# L is consonant
# I is vocal
# G is consonant
# E is vocal
# N is consonant
# C is consonant
# E is vocal
# ---------------------------------------------------------------------------





# -----------
# EXERCISE 3
# -----------

# Using the technique of defining sequences by comprehension, define the
# following functions:

# a) Given a list of natural numbers, return the sum of the squares of the 
# even numbers from the list.

# Example:
# >>> sum_squares([9,4,2,6,8,1])
# 220




# b) Given a list of numbers l=[a(1),..., a(n)], calculate the sum, from i=1
# to n, of the products i*a(i).

# Example:

# >>> sum_formula([2,4,6,8,10])
# 110



# =============

# c) Given two numeric lists of the same length, representing to n-dimensional
# vectors, calculate the euclidean distance between them.

# Example:

# >>> eucl_distance([3,1,2],[1,2,1])
# 2.449489742783178





# d) Given a list and function of one argument, return the list of the results
# of applying the function to each element of the list.

# Example:

# >>> my_map(abs,[-2,-3,-4,-1])
# [2, 3, 4, 1]




# e) Given a pair of lists (of the same length) and a function of two
# arguments, return the list of results of applying the function to
# each pair of elements that occur at the same position in the respective
# input lists  

# Example:

# >>> my_map2((lambda x,y: x+y) ,[1,2,3,4],[5,2,7,9])
# [6, 4, 10, 13]




# f) 



# >>> Give a numeric list and a natural number n, count the number of elements
# that are multiples of n and different from zero.

# Example:

# >>> mul_not_zero([4,0,6,7,0,9,18],3) 
# 3





# f) Given two lists of the same length, count the number of positions 
# in which the elements of both lists, at that positions, are equal 

# Example:

# >>> count_matches([4,2,6,8,9,3],[3,2,1,8,9,6])
# 3






# g) Given two lists of the same length, return a dictionary that has
# as keys the positions where the corresponding elements of both lists 
# are equal, and as a value of those keys, the matching element. 

# Examples:

# >>> dic_match_positions([4,2,6,8,9,3],[3,2,1,8,9,6])
# {1: 2, 3: 8, 4: 9}
# >>> dic_match_positions([2,8,1,2,1,3],[1,8,1,2,1,6])
# {1: 8, 2: 1, 3: 2, 4: 1}






# -----------
# EXERCISE 4
# -----------

# A number is perfect if it is the sum of all its divisors (except
# itself). Define a function filter_perfect(n, m, p) that outputs (print) 
# all perfect numbers between n and m that meet the condition p. Also, output
# the divisors of each perfect number printed. 


# Example:

# >>> filter_perfect(3,500, lambda x: True)
# 6 is perfect and its divisors are [1, 2, 3]
# 28 is perfect and its divisors are [1, 2, 4, 7, 14]
# 496 is perfect and its divisors are [1, 2, 4, 8, 16, 31, 62, 124, 248]

# >>> filter_perfect(3,500, lambda x: (x%7==0))
# 28 is perfect and its divisors are [1, 2, 4, 7, 14]

# ------------------------------------------------------------------------

def filter_perfect(n, m, p):
    for i in range(n, m + 1):
        group = []
        for j in range(i - 1):
            if i % (j + 1) == 0:
                group.append(j + 1)
        if sum(group) == i:
            if p(i):
                print("{0} is perfect and its divisors are {1}".format(i, group))


def filter_perfect_pro(n, m, p):
    for x in range(n, m + 1):
        divisor = [y for y in range(1, int(x / 2 + 1)) if x % y == 0]
        if sum(divisor) == x and p(x):
            print("{0} is perfect and its divisors are {1}".format(x, divisor))


# -----------
# EXERCISE 5
# -----------
#

# Suppose we receive a dictionary whose keys are strings of length one and the
# associated values are integers between 0 and 50.  Define a function
# horizontal_histogram(d) function, which receiving a dictionary of that type,
# prints the corresponding horizontal bar histogram, as illustrated in the
# following example:


# >>> d1={"a":5,"b":10,"c":12,"d":11,"e":15,"f":20,
#         "g":15,"h":9,"i":7,"j":2}
# >>> horizontal_histogram(d1)
# a: *****
# b: **********
# c: ************
# d: ***********
# e: ***************
# f: ********************
# g: ***************
# h: *********
# i: *******
# j: **
#
# Note: print the bars, from top to bottom, in the order determined by the
# function "sorted" on the keys.

# ---------------------------------------------------------------------------





# -----------
# EXERCISE 6
# -----------

# With the same input as the previous exercise, define a function
# vertical_histogram(d) that prints the same histogram but with the bars
# in vertical.

# Example:

# >>> d2={"a":5,"b":7,"c":9,"d":12,"e":15,"f":20,
#         "g":15,"h":9,"i":7,"j":2}
# >>> vertical_histogram(d2)
#           *         
#           *         
#           *         
#           *         
#           *         
#         * * *       
#         * * *       
#         * * *       
#       * * * *       
#       * * * *       
#       * * * *       
#     * * * * * *     
#     * * * * * *     
#   * * * * * * * *   
#   * * * * * * * *   
# * * * * * * * * *   
# * * * * * * * * *   
# * * * * * * * * *   
# * * * * * * * * * * 
# * * * * * * * * * * 
# a b c d e f g h i j

# Note: print the bars, from left to right, in the order determined by the
# function "sorted" on the keys.
# ---------------------------------------------------------------------------






# -----------
# EXERCISE 7
# -----------
#
#  
# (a) Define a function compression(l) such that it returns the list resulting
# of compressing the list l received as an entry, in the following sense:
# - If x appears n (n > 1) times consecutively in l, replace those n
# occurrences with the tuple (n, x) 
# - If x is different from its neighbours, then we leave it the same. 

# Example:

#  >>> compression([1, 1, 1, 2, 1, 3, 2, 4, 4, 6, 8, 8, 8])
#  [[3, 1], 2, 1, 3, 2, [2, 4], 6, [3, 8]]
#  >>> compression(["a", "a", "a", "b", "a", "c", "b", "d", "d", "f", "h", "h", "h"])
#  [[3, 'a'], 'b', 'a', 'c', 'b', [2, 'd'], 'f', [3, 'h']]

#  (b) Define the function decompression(l) that returns the list l
#  decompressed, assuming that it has been compressed using the method in the
#  previous section.

#  >>> decompression([[3, 1], 2, 1, 3, 2, [2, 4], 6, [3, 8]])
#  [1, 1, 1, 2, 1, 3, 2, 4, 4, 6, 8, 8, 8]
# ************************************************************************

def compression(l):
    last_num = []
    counter = 1
    ans = []
    for x in l:
        if x == last_num:
            counter += 1
        else:
            if last_num != []:
                ans.append(([counter, last_num] if counter > 1 else last_num))
            last_num = x
            counter = 1
    ans.append(([counter, last_num] if counter > 1 else last_num))
    return ans


def decompression(lst):
    ans = []
    for x in lst:
        if isinstance(x, list):
            for times in range(x[0]):
                ans.append(x[1])
        else:
            ans.append(x)
    return ans


# -----------
# EXERCISE 8
# -----------
#

# The depth of a nested list is the maximum number of nesting in the
# list. Define a function depth(l) that calculates the depth of a given
# list. 


# Examples:

# >>> depth(3)
# 0
# >>> depth([7,5,9,5,6])
# 1
# >>> depth([1,[1,[1,[1,1],1],[1,1]],1])
# 4


# Hint: to know if a data is a list, it may be useful to the built-in function
# isinstance. Specifically,"isinstance(x, list)" checks if x is a list.

# -------------------------------------------------------------------------

def depth(lst):
    return max(1 + depth(x) for x in lst) if isinstance(lst, list) else 0


# -----------
# EXERCISE 9
# -----------
#
# Define the function deep_member(x, l), which checks if x is in a nested list
# (in some depth) 


# Examples:

# >>> deep_member(1,[2,[3,[4,[1]]]])
# True
# >>> deep_member("a",[["c",["d","e",["f","a"],"g"],"h"],["i",["j","k"],"l"],"b",["x","y"]])
# True
# >>> deep_member("a",["c",["d","e",["f","m"],"g"],"h",["i",["j","k"],"l"],"b",["x","y"]])
# False
#
# Hint: it can be useful the built-in function any (see the reference manual).

# -----------------------------------------------------------------------

def deep_member(value, lst):
    return ori(deep_member(value, x) for x in lst) if isinstance(lst, list) else lst == value


def ori(lst):
    for x in lst:
        if x:
            return x
    return False


# ------------
# EXERCISE 10
# ------------
#
# Define a function my_grep(string, file) similar to the unix grep command
# (without patterns). In other words, it outputs the file lines in which
# string occurs (along with the line number).

# For example, if we look for the string "function" in a file similar to this
# one, the first few lines of the output could be similar to this one:


# >>> my_grep("function","practice-01.py")

# Line 13: # Define a function squares(l), such that receiving a sequence l of numbers,
#                      ^^^^^^^^
# Line 35: # Define a function vocals_consonants(s), such that receives a string s (only
#                      ^^^^^^^^
# Line 64: # following functions:
#                       ^^^^^^^^
# Line 100: # d) Given a list and function of one argument, return the list of the results
#                                  ^^^^^^^^
# Line 101: # of applying the function to each element of the list.
#                              ^^^^^^^^
# Line 111: # e) Given a pair of lists (of the same length) and a function of two
#                                                                  ^^^^^^^^
# Line 112: # arguments, return the list of results of applying the function to
#                                                                    ^^^^^^^^
# Line 174: # itself). Define a function filter_perfect(n, m, p) that outputs (print) 
#                                ^^^^^^^^
# .....
# .....
# .....


def my_grep(string, file):
    num_line = 0
    for lin in open(file):
        num_line += 1
        if lin.__contains__(string):
            print("Line {0}: {1}".format(num_line, lin))


# ------------
# EXERCISE 11
# ------------



# Suppose we want to simulate the trajectory of a projectile that is
# being fired at a given point, and at a given initial height. The shot was
# fired forward, at a given initial speed and angle. 

# Initially the projectile will go upward but due to the gravity,  at one
# given moment it will begin to descend until it lands. To simplify, we will
# assume that there is no friction or wind resistance. 

# Design a Projectile class to represent the state of the projectile in
# a given moment of time. To do this, we need at least the following data
# attributes: 
# - distance travelled (horizontal)
# - height
# - horizontal speed
# - vertical speed

# In addition, include the following three methods:
# - update(t): updates the projectile position and velocity after t seconds 
# - get_posx(): returns the horizontal distance travelled 
# - get_posy(): returns the vertical distance travelled 

# Once the Projectile class is defined, use it to define a function 
# landing(height, speed, angle, interval)
# which will output the succesive positions of a single projectile that has
# been fired at a speed, with an angle (in degrees)  and with a given initial
# height. Projectile position will be displayed in every time interval, until
# it lands. In addition, the maximum altitude reached will be
# displayed, and how many intervals of time has needed to land.   

# Indications:

# - If the projectile has an initial velocity v and is launched at an angle
#   theta, the horizontal and vertical components of the initial velocity are
#   v*cos(theta) and v*sen(theta), respectively.
# - We can assume that the horizontal component of the speed, in the absence
#   of friction and wind,  remains constant. 
# - The vertical component of the speed changes as follows, after an interval
#   t: if vy0 is the vertical velocity at the beginning of the 
#   interval, then at the end of the interval it has a velocity vy1=vy0-9.8*t,
#   due to the gravity. 
# - In that case, if the projectile is at a height of h0,
#   after a time interval t will be found at a height h1=h0 + vm*t, where vm 
#   is the average between the previous vy0 and vy1. 
# - It will be necessary to import the math library

# Example:

# ------------
# EXERCISE 11
# ------------



# Suppose we want to simulate the trajectory of a projectile that is
# being fired at a given point, and at a given initial height. The shot was
# fired forward, at a given initial speed and angle. 

# Initially the projectile will go upward but due to the gravity,  at one
# given moment it will begin to descend until it lands. To simplify, we will
# assume that there is no friction or wind resistance. 

# Design a Projectile class to represent the state of the projectile in
# a given moment of time. To do this, we need at least the following data
# attributes: 
# - distance travelled (horizontal)
# - height
# - horizontal speed
# - vertical speed

# In addition, include the following three methods:
# - update(t): updates the projectile position and velocity after t seconds 
# - get_posx(): returns the horizontal distance travelled 
# - get_posy(): returns the vertical distance travelled 

# Once the Projectile class is defined, use it to define a function 
# landing(height, speed, angle, interval)
# which will output the succesive positions of a single projectile that has
# been fired at a speed, with an angle (in degrees)  and with a given initial
# height. Projectile position will be displayed in every time interval, until
# it lands. In addition, the maximum altitude reached will be
# displayed, and how many intervals of time has needed to land.   

# Indications:

# - If the projectile has an initial velocity v and is launched at an angle
#   theta, the horizontal and vertical components of the initial velocity are
#   v*cos(theta) and v*sen(theta), respectively.
# - We can assume that the horizontal component of the speed, in the absence
#   of friction and wind,  remains constant. 
# - The vertical component of the speed changes as follows, after an interval
#   t: if vy0 is the vertical velocity at the beginning of the 
#   interval, then at the end of the interval it has a velocity vy1=vy0-9.8*t,
#   due to the gravity. 
# - In that case, if the projectile is at a height of h0,
#   after a time interval t will be found at a height h1=h0 + vm*t, where vm 
#   is the average between the previous vy0 and vy1. 
# - It will be necessary to import the math library

# Example:


# >>> landing(30,45,20,0.01)
# Projectile at position (0.0,30.0)
# Projectile at position (0.4,30.2)
# Projectile at position (0.8,30.3)
# Projectile at position (1.3,30.5)
# Projectile at position (1.7,30.6)
# Projectile at position (2.1,30.8)
# Projectile at position (2.5,30.9)
# Projectile at position (3.0,31.1)
# Projectile at position (3.4,31.2)

# ... OUTPUT OMITTED ...

# Projectile at position (188.6,1.2)
# Projectile at position (189.0,0.9)
# Projectile at position (189.4,0.6)
# Projectile at position (189.9,0.3)
# Projectile at position (190.3,0.0)

# After 451 intervals of 0.01 seconds (4.51 seconds) the projectile has landed.
# It has traveled a distance of 190.7 meters
# It has reached a maximum height of 42.1 meters

# -------------------------------------------------------
from math import sin, cos, radians


class Projectile(object):
    def __init__(self, angle, speed, height):
        self.posx = 0
        self.posy = height
        theta = radians(angle)
        self.vx = speed * cos(theta)
        self.vy = speed * sin(theta)

    def update(self, time):
        self.posx += self.vx * time
        vy1 = self.vy - 9.8 * time
        vym = (self.vy + vy1) / 2
        self.posy += vym * time
        self.vy = vy1

    def __str__(self):
        return "({0:0.1f},{1:0.1f})".format(self.posx, self.posy)

    def get_posx(self):
        return self.posx

    def get_posy(self):
        return self.posy


def landing(height, speed, angle, interval):
    item = Projectile(angle, speed, height)
    n = 0
    maxh = -1
    while item.get_posy() >= 0:
        print("Projectile at position {0}".format(item))
        if item.get_posy() > maxh:
            maxh = item.get_posy()
        item.update(interval)
        n += 1

    print(
        "\nAfter {} intervals of {} seconds ({} seconds) the projectile has landed.".format(n, interval, n * interval),
        "\nIt has traveled a distance of {0:0.1f} meters".format(item.get_posx()),
        "\nIt has reached a maximum height of {0:0.1f} meters".format(maxh))

