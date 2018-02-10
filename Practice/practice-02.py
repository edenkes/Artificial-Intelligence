# practice-02.py
# Artificial Intelligence, ETSII, Univ. Seville

# Práctice 2: Implementing k-means
# ================================

import math, random

# This practice has two parts:
# - In the first part we are going to implement in Python the k.means algorithm
# for clustering
# - In the second part we will test the implementation with a particular data
# set: the so-called "iris", a database in that each instance reflects a series
# of measures on the flower of the Iris plant, along with a classification on
# the type of flower (iris.dat file)


# ***********************************
# Part I: Implementing K-means
# ***********************************


# The k-means algorithm is a clustering algorithm that allows to classify in
# groups or clusters a series of examples (vectors) that constitute the input
# dataset. In addition to this dataset, it receives as input the number k of
# clusters that are intended to be made.

# Basically, it start by choosing K centers and assigning each element to the
# class represented by the nearest center. Once assigned a cluster to each
# example, the arithmetic mean of the examples of each cluster is taken as the
# new cluster center. This process of cluster assignment and center
# recalculation is repeated until some termination cndition is met
# (stabilization of the centers, for example).


# This the psudocode that we have seen in unit 3:


# -------------------------------------------------------------------
# 1. Initialize c_i (i=1,...,k) (randomly or with some heuristic
#    criterion)
# 2. REPEAT (until c_i do not vary):
#    2.1 FOR j=1,...,N, DO:
#        Calculate the cluster corresponding to x_j, by selecting,
#        among all c_i, the center c_h such that the
#        distance(x_j,c_h) is minimum
#    2.2 FOR i=1,...,k. DO:
#        Update c_i assigning to it the arithmetic mean of the
#        examples assigned to i-th cluster
# 3. Return c_1,...,c_n
# -------------------------------------------------------------------



# The following exercises have the final goal of implementing in Python the
# k-means algorithm. The distance function will be received as input.


# To test the implementation as long as we are defining the auxiliary
# functions, use the following (very simple, 1-dimensional) data set in which
# we list the weights of a population. It is expected that this data are taken
# from two groups (men and women), but in principle we do not know to which
# group belongs each weight. In this simple case, the distance between two
# data is the absolute value of its difference.


weights_population = [[51.0], [43.0], [62.0], [64.0], [45.0], [42.0], [46.0], [45.0], [45.0], [62.0], [47.0],
                      [52.0], [64.0], [51.0], [65.0], [48.0], [49.0], [46.0], [64.0], [51.0], [52.0], [62.0],
                      [49.0], [48.0], [62.0], [43.0], [40.0], [48.0], [64.0], [51.0], [63.0], [43.0], [65.0],
                      [66.0], [65.0], [46.0], [39.0], [62.0], [64.0], [52.0], [63.0], [64.0], [48.0], [64.0],
                      [48.0], [51.0], [48.0], [64.0], [42.0], [48.0], [41.0]]


def distance_abs(x, y):
    return abs(x[0] - y[0])


# ---------------------------------------------------------------
# Exercise 1

# The cluster we assign to each example, in each iteration of the algorithm
# can be stored in a list (we will call it "classification list") whose
# elements are two-element lists: the example and the number of cluster
# assigned.

# Define a function "initial_clusters_empty(dataset)", receiving as input a
# data set and it returns a classification list, in which the cluster of every
# example is not defined (that is, with value None).

# Example:

# >>> initial_clusters_empty(weights_population)
# [[[51.0], None], [[43.0], None], [[62.0], None], [[64.0], None],
#  [[45.0], None], [[42.0], None], [[46.0], None], [[45.0], None],
#  [[45.0], None], [[62.0], None], [[47.0], None], [[52.0], None],
#  .......]

# ---------------------------------------------------------------

def initial_clusters_empty(dataset):
    ans = []
    for x in dataset:
        ans.append([x, None])
    return ans









# ---------------------------------------------------------------
# Exercise 2
# The centres computed by the algorithm will be stored in a list of k
# elements (we will call it "centres list")

# To define the initial centres, we are going to obtain randomly k different
# examples from the input data set. Define a function
# "initial_centres(dataset,num_clusters)" that receives as input the data set
# and the number of clusters, returns an initial list of centres.

# For example (the result may be different):
# >>> initial_centres(weights_population,2)
# [[65.0], [48.0]]
# ---------------------------------------------------------------

# HINTS: use the function random.sample

def initial_centres(dataset,num_clusters):
    return random.sample(dataset, num_clusters)







# ---------------------------------------------------------------
# Exercise 3

# Define a function

# "nearest_centre(example,centres,distance)"

# that receives as input an example, a centres list and a distance function,
# and returns the number of cluster (that is, the position in the list) of the
# nearest center to the example.

# For example:

# >>> nearest_centre([41.0],[[39.0],[45.0]],distance_abs)
# 0
# >>> nearest_centre([64.0],[[39.0],[45.0]],distance_abs)
# 1
# -----------------------------------------------------------------
def nearest_centre(example,centres,distance):
    mid_dist = float("inf")
    for i, x in enumerate(centres):
        dist = distance(example, x)
        if dist < mid_dist:
            mid_dist = dist
            min_index = i
    return min_index

def nearest_centre2(example,centres,distance):
    return min(enumerate(centres), key=lambda x:distance(x[1],example))[0]











# ---------------------------------------------------------------
# Exercise 4


# Define the function

# "assign_cluster_example(classif,centres,distance)"

# such that it receives as input a classification list, a centres list and a
# distance function, and has the effect of updating the classification list in
# such a way that each example is assigned the centre nearest to the example


# For example:

# >>> clas=initial_clusters_empty(weights_population)
# >>> centr=[[65.0],[48.0]]
# >>> assign_cluster_example(clas,centr,distance_abs)
# >>> clas
# [[[51.0], 1], [[43.0], 1], [[62.0], 0], [[64.0], 0], [[45.0], 1],
#  [[42.0], 1], [[46.0], 1], [[45.0], 1], [[45.0], 1], [[62.0], 0],
#  [[47.0], 1], [[52.0], 1], [[64.0], 0], [[51.0], 1], [[65.0], 0],
#  ...]

# -----------------------------------------------------------------

def assign_cluster_example(classif,centres,distance):
    for x in classif:
        x[1] = nearest_centre(x[0], centres, distance)












# ---------------------------------------------------------------
# Exercise 5

#   Define a function "recompute_centres(classif,num_clusters)" such that
#   receiving a classification list and the number of clusters, it returns the
#   list with the new centres, computed as the centroids of the examples in
#   each cluster.

# For example (where "clas" has the value of the previous example):
# >>> recompute_centres(clas,2)
# [[63.63157894736842], [46.8125]]

def sum_vec(v1, v2):
    return [x1+x2 for x1, x2 in zip(v1, v2)]

def recompute_centres(classif,k):

    n = len(classif[0][0])
    new_centres = [[0]*n for _ in range(k)]
    num = [0]*k
    for d in classif:
        new_centres[d[1]] = sum_vec(new_centres[d[1]], d[0])
        num[d[1]] += 1
    return [[x/i for x in c] for c, i in zip(new_centres, num)]










# ------------------------------------------------------------------------------
# Exercise 6
# ------------------------------------------------------------------------------


# Using the function defined previously, define the function
# "k-means(k,dataset,distance)"
# implenting in Python the k-means algorithm (as presented in the pseudocode
# above)
# The algorithm has to return a tuple with two elements: the centres finally
# computed and the final classification list

# For example:

# >>> k_means(2,weights_population,distance_abs)
# [[[46.8125], [63.63157894736842]],

#  [[[51.0], 0], [[43.0], 0], [[62.0], 1], [[64.0], 1], [[45.0], 0],
#   [[42.0], 0], [[46.0], 0], [[45.0], 0], [[45.0], 0], [[62.0], 1],
#   [[47.0], 0], [[52.0], 0], [[64.0], 1], [[51.0], 0], [[65.0], 1],
#   ....]]

# -------------------------------------------------------------
def k_means(k,dataset,distance):
    print()
    centres = initial_centres(dataset, k)
    classif = initial_clusters_empty(dataset)
    while True:
        assign_cluster_example(classif, centres, distance)
        new_center = recompute_centres(classif, k)
        change = centres != nearest_centre()
        if change:
            centres = new_center
        else:
            return centres, classif









# ------------------------------------------------------------------------------
# Exercise 7
# ------------------------------------------------------------------------------

# In the previous implementation, the initial centres have been taken randomly
# from the examples in the dataset. Define an alternative version of k-means

# "k_medias_2(k,datos,distancia)"

# in which the initialization phase is done by randomly distributing the
# examples in k clusters (instead of randomly generate the initial centres)

# REMARK: you should try to initialize the clusters with about the same size.







# **************************************************
# Part II: experimenting k-means on the iris dat set
# **************************************************

# The following list iris contains one of the most common data sets known and
# used as a test bed for machine learning. It is a list of 150 data vectors,
# each with four components measuring length and width of sepal and petal of the
# flower of the Iris plant. Each vector is assigned one of three possible
# classifications: setosa, versicolor or virginica (which is the fifth
# component).



iris = \
    [[5.1, 3.5, 1.4, 0.2, "Iris setosa"],
     [4.9, 3.0, 1.4, 0.2, "Iris setosa"],
     [4.7, 3.2, 1.3, 0.2, "Iris setosa"],
     [4.6, 3.1, 1.5, 0.2, "Iris setosa"],
     [5.0, 3.6, 1.4, 0.2, "Iris setosa"],
     [5.4, 3.9, 1.7, 0.4, "Iris setosa"],
     [4.6, 3.4, 1.4, 0.3, "Iris setosa"],
     [5.0, 3.4, 1.5, 0.2, "Iris setosa"],
     [4.4, 2.9, 1.4, 0.2, "Iris setosa"],
     [4.9, 3.1, 1.5, 0.1, "Iris setosa"],
     [5.4, 3.7, 1.5, 0.2, "Iris setosa"],
     [4.8, 3.4, 1.6, 0.2, "Iris setosa"],
     [4.8, 3.0, 1.4, 0.1, "Iris setosa"],
     [4.3, 3.0, 1.1, 0.1, "Iris setosa"],
     [5.8, 4.0, 1.2, 0.2, "Iris setosa"],
     [5.7, 4.4, 1.5, 0.4, "Iris setosa"],
     [5.4, 3.9, 1.3, 0.4, "Iris setosa"],
     [5.1, 3.5, 1.4, 0.3, "Iris setosa"],
     [5.7, 3.8, 1.7, 0.3, "Iris setosa"],
     [5.1, 3.8, 1.5, 0.3, "Iris setosa"],
     [5.4, 3.4, 1.7, 0.2, "Iris setosa"],
     [5.1, 3.7, 1.5, 0.4, "Iris setosa"],
     [4.6, 3.6, 1.0, 0.2, "Iris setosa"],
     [5.1, 3.3, 1.7, 0.5, "Iris setosa"],
     [4.8, 3.4, 1.9, 0.2, "Iris setosa"],
     [5.0, 3.0, 1.6, 0.2, "Iris setosa"],
     [5.0, 3.4, 1.6, 0.4, "Iris setosa"],
     [5.2, 3.5, 1.5, 0.2, "Iris setosa"],
     [5.2, 3.4, 1.4, 0.2, "Iris setosa"],
     [4.7, 3.2, 1.6, 0.2, "Iris setosa"],
     [4.8, 3.1, 1.6, 0.2, "Iris setosa"],
     [5.4, 3.4, 1.5, 0.4, "Iris setosa"],
     [5.2, 4.1, 1.5, 0.1, "Iris setosa"],
     [5.5, 4.2, 1.4, 0.2, "Iris setosa"],
     [4.9, 3.1, 1.5, 0.1, "Iris setosa"],
     [5.0, 3.2, 1.2, 0.2, "Iris setosa"],
     [5.5, 3.5, 1.3, 0.2, "Iris setosa"],
     [4.9, 3.1, 1.5, 0.1, "Iris setosa"],
     [4.4, 3.0, 1.3, 0.2, "Iris setosa"],
     [5.1, 3.4, 1.5, 0.2, "Iris setosa"],
     [5.0, 3.5, 1.3, 0.3, "Iris setosa"],
     [4.5, 2.3, 1.3, 0.3, "Iris setosa"],
     [4.4, 3.2, 1.3, 0.2, "Iris setosa"],
     [5.0, 3.5, 1.6, 0.6, "Iris setosa"],
     [5.1, 3.8, 1.9, 0.4, "Iris setosa"],
     [4.8, 3.0, 1.4, 0.3, "Iris setosa"],
     [5.1, 3.8, 1.6, 0.2, "Iris setosa"],
     [4.6, 3.2, 1.4, 0.2, "Iris setosa"],
     [5.3, 3.7, 1.5, 0.2, "Iris setosa"],
     [5.0, 3.3, 1.4, 0.2, "Iris setosa"],
     [7.0, 3.2, 4.7, 1.4, "Iris versicolor"],
     [6.4, 3.2, 4.5, 1.5, "Iris versicolor"],
     [6.9, 3.1, 4.9, 1.5, "Iris versicolor"],
     [5.5, 2.3, 4.0, 1.3, "Iris versicolor"],
     [6.5, 2.8, 4.6, 1.5, "Iris versicolor"],
     [5.7, 2.8, 4.5, 1.3, "Iris versicolor"],
     [6.3, 3.3, 4.7, 1.6, "Iris versicolor"],
     [4.9, 2.4, 3.3, 1.0, "Iris versicolor"],
     [6.6, 2.9, 4.6, 1.3, "Iris versicolor"],
     [5.2, 2.7, 3.9, 1.4, "Iris versicolor"],
     [5.0, 2.0, 3.5, 1.0, "Iris versicolor"],
     [5.9, 3.0, 4.2, 1.5, "Iris versicolor"],
     [6.0, 2.2, 4.0, 1.0, "Iris versicolor"],
     [6.1, 2.9, 4.7, 1.4, "Iris versicolor"],
     [5.6, 2.9, 3.6, 1.3, "Iris versicolor"],
     [6.7, 3.1, 4.4, 1.4, "Iris versicolor"],
     [5.6, 3.0, 4.5, 1.5, "Iris versicolor"],
     [5.8, 2.7, 4.1, 1.0, "Iris versicolor"],
     [6.2, 2.2, 4.5, 1.5, "Iris versicolor"],
     [5.6, 2.5, 3.9, 1.1, "Iris versicolor"],
     [5.9, 3.2, 4.8, 1.8, "Iris versicolor"],
     [6.1, 2.8, 4.0, 1.3, "Iris versicolor"],
     [6.3, 2.5, 4.9, 1.5, "Iris versicolor"],
     [6.1, 2.8, 4.7, 1.2, "Iris versicolor"],
     [6.4, 2.9, 4.3, 1.3, "Iris versicolor"],
     [6.6, 3.0, 4.4, 1.4, "Iris versicolor"],
     [6.8, 2.8, 4.8, 1.4, "Iris versicolor"],
     [6.7, 3.0, 5.0, 1.7, "Iris versicolor"],
     [6.0, 2.9, 4.5, 1.5, "Iris versicolor"],
     [5.7, 2.6, 3.5, 1.0, "Iris versicolor"],
     [5.5, 2.4, 3.8, 1.1, "Iris versicolor"],
     [5.5, 2.4, 3.7, 1.0, "Iris versicolor"],
     [5.8, 2.7, 3.9, 1.2, "Iris versicolor"],
     [6.0, 2.7, 5.1, 1.6, "Iris versicolor"],
     [5.4, 3.0, 4.5, 1.5, "Iris versicolor"],
     [6.0, 3.4, 4.5, 1.6, "Iris versicolor"],
     [6.7, 3.1, 4.7, 1.5, "Iris versicolor"],
     [6.3, 2.3, 4.4, 1.3, "Iris versicolor"],
     [5.6, 3.0, 4.1, 1.3, "Iris versicolor"],
     [5.5, 2.5, 4.0, 1.3, "Iris versicolor"],
     [5.5, 2.6, 4.4, 1.2, "Iris versicolor"],
     [6.1, 3.0, 4.6, 1.4, "Iris versicolor"],
     [5.8, 2.6, 4.0, 1.2, "Iris versicolor"],
     [5.0, 2.3, 3.3, 1.0, "Iris versicolor"],
     [5.6, 2.7, 4.2, 1.3, "Iris versicolor"],
     [5.7, 3.0, 4.2, 1.2, "Iris versicolor"],
     [5.7, 2.9, 4.2, 1.3, "Iris versicolor"],
     [6.2, 2.9, 4.3, 1.3, "Iris versicolor"],
     [5.1, 2.5, 3.0, 1.1, "Iris versicolor"],
     [5.7, 2.8, 4.1, 1.3, "Iris versicolor"],
     [6.3, 3.3, 6.0, 2.5, "Iris virginica"],
     [5.8, 2.7, 5.1, 1.9, "Iris virginica"],
     [7.1, 3.0, 5.9, 2.1, "Iris virginica"],
     [6.3, 2.9, 5.6, 1.8, "Iris virginica"],
     [6.5, 3.0, 5.8, 2.2, "Iris virginica"],
     [7.6, 3.0, 6.6, 2.1, "Iris virginica"],
     [4.9, 2.5, 4.5, 1.7, "Iris virginica"],
     [7.3, 2.9, 6.3, 1.8, "Iris virginica"],
     [6.7, 2.5, 5.8, 1.8, "Iris virginica"],
     [7.2, 3.6, 6.1, 2.5, "Iris virginica"],
     [6.5, 3.2, 5.1, 2.0, "Iris virginica"],
     [6.4, 2.7, 5.3, 1.9, "Iris virginica"],
     [6.8, 3.0, 5.5, 2.1, "Iris virginica"],
     [5.7, 2.5, 5.0, 2.0, "Iris virginica"],
     [5.8, 2.8, 5.1, 2.4, "Iris virginica"],
     [6.4, 3.2, 5.3, 2.3, "Iris virginica"],
     [6.5, 3.0, 5.5, 1.8, "Iris virginica"],
     [7.7, 3.8, 6.7, 2.2, "Iris virginica"],
     [7.7, 2.6, 6.9, 2.3, "Iris virginica"],
     [6.0, 2.2, 5.0, 1.5, "Iris virginica"],
     [6.9, 3.2, 5.7, 2.3, "Iris virginica"],
     [5.6, 2.8, 4.9, 2.0, "Iris virginica"],
     [7.7, 2.8, 6.7, 2.0, "Iris virginica"],
     [6.3, 2.7, 4.9, 1.8, "Iris virginica"],
     [6.7, 3.3, 5.7, 2.1, "Iris virginica"],
     [7.2, 3.2, 6.0, 1.8, "Iris virginica"],
     [6.2, 2.8, 4.8, 1.8, "Iris virginica"],
     [6.1, 3.0, 4.9, 1.8, "Iris virginica"],
     [6.4, 2.8, 5.6, 2.1, "Iris virginica"],
     [7.2, 3.0, 5.8, 1.6, "Iris virginica"],
     [7.4, 2.8, 6.1, 1.9, "Iris virginica"],
     [7.9, 3.8, 6.4, 2.0, "Iris virginica"],
     [6.4, 2.8, 5.6, 2.2, "Iris virginica"],
     [6.3, 2.8, 5.1, 1.5, "Iris virginica"],
     [6.1, 2.6, 5.6, 1.4, "Iris virginica"],
     [7.7, 3.0, 6.1, 2.3, "Iris virginica"],
     [6.3, 3.4, 5.6, 2.4, "Iris virginica"],
     [6.4, 3.1, 5.5, 1.8, "Iris virginica"],
     [6.0, 3.0, 4.8, 1.8, "Iris virginica"],
     [6.9, 3.1, 5.4, 2.1, "Iris virginica"],
     [6.7, 3.1, 5.6, 2.4, "Iris virginica"],
     [6.9, 3.1, 5.1, 2.3, "Iris virginica"],
     [5.8, 2.7, 5.1, 1.9, "Iris virginica"],
     [6.8, 3.2, 5.9, 2.3, "Iris virginica"],
     [6.7, 3.3, 5.7, 2.5, "Iris virginica"],
     [6.7, 3.0, 5.2, 2.3, "Iris virginica"],
     [6.3, 2.5, 5.0, 1.9, "Iris virginica"],
     [6.5, 3.0, 5.2, 2.0, "Iris virginica"],
     [6.2, 3.4, 5.4, 2.3, "Iris virginica"],
     [5.9, 3.0, 5.1, 1.8, "Iris virginica"]]


# ---------------------------------------------------------------
# Ejercicio 8



# The following function allows us to validate any classification of the
# following 150 numerical vectors of the iris list, comparing it with the
# original classification in the database.  For each of the three original
# classifications, count how many examples there are in each of the
# clusters assigned in the classification list received as input.


def validacion_iris(clasificacion):
    posibles_valores = ["Iris setosa", "Iris versicolor", "Iris virginica"]
    contadores = dict()
    for val in posibles_valores:
        for x in range(3):
            contadores[val, x] = 0
    for i in range(len(clasificacion)):
        contadores[iris[i][4], clasificacion[i][1]] += 1
    for val in posibles_valores:
        print(val + "\n" + "==============\n")
        for x in range(3):
            print("Cluster ", x, ": ", contadores[val, x])
        print("\n\n")


# It is requested:

# - Obtain, from the iris data set, the list of examples without the class
# - Apply the k-means algorithm to those examples, using the euclidean
#   distance
# - Validate the classification obtained, with respect to the original
#   classification.




if __name__ == '__main__':
    print(initial_clusters_empty(weights_population))

