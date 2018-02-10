# ==========================================================
# Artificial Intelligence.  ETSII (University of Seville).
# Course 2017-18
# Deliverable 03
# ===========================================================


# Define, using Python, the functions asked in each exercise, using the blank
# space below the statement.

# IMPORTANT: DO NOT CHANGE THE NAMES EITHER TO THIS FILE OR TO THE FUNCTIONS
# ASKED IN EACH EXERCISE (in that case, the exercise will not be evaluated)


# THIS ASSIGNMENT WORTHS 5% OF THE TOTAL GRADE


# *****************************************************************************
# ACADEMIC INTEGRITY AND CHEATING: the assignments are individual, and thus
# they have to be carried out independently by each student. SHARING CODE IS
# STRICTLY FORBIDDEN. It as also forbidden to use any third-party code,
# available on web or on any source, without the approval of the teacher.

# Any plagiarism detected will result in a FINAL GRADE OF ZERO IN THE COURSE,
# for ALL the students involved, and it may lead to other disciplinary
# measures. Furthermore, the grades obtained until that moment will not be
# kept for future calls.
# *****************************************************************************

#

# This assignment consists in implementing in Python the LIKELIHOOD WEIGHTING
# algorithm, modifying an implementation of the rejection sampling
# algorithm. We give the implementation of rejection sampling, and we ask to
# modify that implementation to obtain an implementation of likelihood
# weighting. To understand this assignment, you should understand first both
# algorithms, as described in the section "Approximate inference on bayesian
# networks" of unit 7 (slides 97 to 110).

# Both algorithms are approximate probabilistic inference algorithms. They
# receive as input a bayesian network, a query variable X and a list of
# evidences e, and apply sampling techniques to compute an approximate value
# of the probability P(X|e).

# In rejection sampling, from the samples ganerated, only those compatible
# with the evidences are used, and the rest are rejected. This is usually a
# problem, since the number of useful samples may be very low, and then the
# approximation computed can be not very precise. Likelihood weighting tries
# to solve that issue, by only generating samples compatible with the
# evidences, and weighting them according to the probability of the evidence
# values that have been fixed.


import random

# ------------------------------------------------------------------

# =============================================================
# A data structure for representing bayesian networks in Python
# =============================================================

# First, we need a data structure in Python to store a bayesian network. The
# following is our representation of the "Alarm" network we have been using in
# class:

net_alarm = [{"robbery": [True, False],
              "earthquake": [True, False],
              "alarm": [True, False],
              "johncalls": [True, False],
              "marycalls": [True, False]},

             {"robbery": [],
              "earthquake": [],
              "alarm": ["robbery", "earthquake"],
              "johncalls": ["alarm"],
              "marycalls": ["alarm"]},

             {"robbery": {(): [0.001, 0.999]},
              "earthquake": {(): [0.002, 0.998]},
              "alarm": {(True, True): [0.95, 0.05],
                        (True, False): [0.94, 0.06],
                        (False, True): [0.29, 0.71],
                        (False, False): [0.001, 0.999]},
              "johncalls": {(True,): [0.9, 0.1],
                            (False,): [0.05, 0.95]},
              "marycalls": {(True,): [0.7, 0.3],
                            (False,): [0.01, 0.99]}}]

# In general, a bayesian network is represented by a three element list,
# representing:

# 1. The first element of that list stores the random variables, with its
# names and possible values. Represented by a dictionary whose keys are the
# variable names and whose associated value is a list with the possible values
# that the variable may take.

# 2. The second element of the list is for describing the "arrows" in the
#    network. They are represented by a dictionary associating each variable
#    with the list of parents of that variable.

# 3. The third element of the list stores the probability tables. Again, is a
# dictionary, now associating each variable with its probability table. A
# probability table associated to a variable X is also represented by a
# dictionary that associates to each combination of values of the parents of
# X, a probability distribution for the different values of X.

#    For example, the probability table for "alarm" is a dictionary, and one
#    of its correspondences is:
#    (True,False):[0.94,0.06]
#    This means that
#    P(alarm=True|Robbery=True,Earthquake=False)=0.94, and
#    P(alarm=False|Robbery=True,Earthquake=False)=0.06.
#
#    Note that the implicit ordering of the values of a variable and of the
#    parents of a variable is the one defined in the corresponding
#    dictionaries in the first two components of the structure.

# The following are two networks examples we have seen in unit 7:


net_infarction = [{"sport": [True, False],
                   "healthy_nutrition": [True, False],
                   "hypertense": [True, False],
                   "smoker": [True, False],
                   "infarction": [True, False]},

                  {"sport": [],
                   "healthy_nutrition": [],
                   "hypertense": ["sport", "healthy_nutrition"],
                   "smoker": [],
                   "infarction": ["hypertense", "smoker"]},

                  {"sport": {(): [0.1, 0.9]},
                   "healthy_nutrition": {(): [0.4, 0.6]},
                   "hypertense": {(True, True): [0.01, 0.99],
                                  (True, False): [0.25, 0.75],
                                  (False, True): [0.2, 0.8],
                                  (False, False): [0.7, 0.3]},
                   "smoker": {(): [0.4, 0.6]},
                   "infarction": {(True, True): [0.8, 0.2],
                                  (True, False): [0.7, 0.3],
                                  (False, True): [0.6, 0.4],
                                  (False, False): [0.3, 0.7]}}]

net_sprinkler = [{"wet grass": [True, False],
                  "rain": [True, False],
                  "overcast": [True, False],
                  "sprinkler": [True, False]},

                 {"overcast": [],
                  "sprinkler": ["overcast"],
                  "rain": ["overcast"],
                  "wet grass": ["sprinkler", "rain"]},

                 {"overcast": {(): [0.5, 0.5]},
                  "sprinkler": {(True,): [0.1, 0.9],
                                (False,): [0.5, 0.5]},
                  "rain": {(True,): [0.8, 0.2],
                           (False,): [0.2, 0.8]},
                  "wet grass": {(True, True): [0.99, 0.01],
                                (True, False): [0.9, 0.1],
                                (False, True): [0.9, 0.1],
                                (False, False): [0.0, 1.0]}}]


# ============================
# Rejection sampling in Python
# ============================


# The following is a Python implementation of the rejection sampling
# algorithm. Comments below explain each function.


# The following function obtains a list of the variables of the network,
# ordered in a way compatible with the network. That is, the list is ordered
# such that any variable goes after all its parents:

def compatible_ordering(net):
    parents = net[1]
    ordered = []
    to_be_ordered = list(parents.keys())
    while to_be_ordered:
        for i in range(len(to_be_ordered) - 1, -1, -1):
            if set(parents[to_be_ordered[i]]).issubset(ordered):
                ordered.append(to_be_ordered[i])
                to_be_ordered.pop(i)
    return (ordered)

# print(compatible_ordering(net_alarm))
# >>> compatible_ordering(net_alarm)
# ['robbery', 'earthquake', 'alarm', 'marycalls', 'johncalls']
# print(compatible_ordering(net_infarction))
# >>> compatible_ordering(net_infarction)
# ['smoker', 'healthy_nutrition', 'sport', 'hypertense', 'infarction']
# print(compatible_ordering(net_sprinkler))
# >>> compatible_ordering(net_sprinkler)
# ['overcast', 'rain', 'sprinkler', 'wet grass']

# --------

# The following function randomly returns a value chosen from a given list of
# values, following a given probability distribution.

def sample_distr(values, distr):
    r = random.random()
    acum = 0
    for (v, p) in zip(values, distr):
        acum += p
        if acum > r:
            return (v)


# For example, suppose we have three values "v1", "v2" and "v3" for a random
# variable, "v2" with probability 0.8 and the rest with probability 0.1. Then
# we show here several samples obtained with the function:
# arr = [sample_distr(["v1","v2","v3"],[0.1,0.8,0.1]) for _ in range(50)]
# print(sum(i == "v1" for i in arr)/50, sum(i == "v2" for i in arr)/50, sum(i == "v3" for i in arr)/50, arr)
# >>> sample_distr(["v1","v2","v3"],[0.1,0.8,0.1])
# 'v2'
# >>> sample_distr(["v1","v2","v3"],[0.1,0.8,0.1])
# 'v2'
# >>> sample_distr(["v1","v2","v3"],[0.1,0.8,0.1])
# 'v3'
# >>> sample_distr(["v1","v2","v3"],[0.1,0.8,0.1])
# 'v2'
# >>> sample_distr(["v1","v2","v3"],[0.1,0.8,0.1])
# 'v2'
# ...


# --------

# Prior sampling of a bayesian network consists in obtaining a random atomic
# event (a particular combination of values for each variable of the network),
# following the joint probability distribution of the network.

# The following function implements PRIOR SAMPLING, as described is slides
# 100-102 of unit 7:


def prior_sampling(net):
    values = net[0]
    parents = net[1]
    tables = net[2]
    ordered_variables = compatible_ordering(net)
    sample = dict()
    for var in ordered_variables:
        parents_var = parents[var]
        parents_values = tuple(sample[vp] for vp in parents_var)
        sample[var] = sample_distr(values[var], tables[var][parents_values])
    return (sample)


# Examples:
# print(prior_sampling(net_infarction))
# >>> prior_sampling(net_alarm)
# {'marycalls': False, 'alarm': False, 'johncalls': False, 'earthquake': False, 'robbery': False}
# >>> prior_sampling(net_alarm)
# {'marycalls': False, 'alarm': False, 'johncalls': False, 'earthquake': False, 'robbery': False}
# >>> prior_sampling(net_alarm)
# {'marycalls': True, 'alarm': False, 'johncalls': False, 'earthquake': False, 'robbery': False}
# >>> prior_sampling(net_infarction)
# {'smoker': True, 'infarction': True, 'sport': False, 'healthy_nutrition': False, 'hypertense': True}
# >>> prior_sampling(net_infarction)
# {'smoker': False, 'infarction': True, 'sport': True, 'healthy_nutrition': False, 'hypertense': True}
# >>> prior_sampling(net_sprinkler)
# {'wet grass': True, 'overcast': False, 'sprinkler': True, 'rain': True}
# >>> prior_sampling(net_sprinkler)
# {'wet grass': True, 'overcast': True, 'sprinkler': False, 'rain': True}





# ----------

# The following function normalizes a probability distribution (given as a
# dictionary):


def normalize(d):
    total = sum(d.values())
    return {var: d[var] / total for var in d}


# Examples:

# >>> normalize({"v1":0.21,"v2":0.11,"v3":0.37})
# {'v1': 0.30434782608695654, 'v2': 0.15942028985507248, 'v3': 0.5362318840579711}
# >>> normalize({True:0.012,False:0.008})
# {False: 0.4, True: 0.6}


# -------


# The following function implements the REJECTION SAMPLING algorithm for
# approximate inference in bayesian networks, as explained in slides 104-105
# of unit 7. The evidences are given as a dictionary that associates an
# observed value to each evidence variable.

def rejection_sampling(net, var, evidences, N):
    acum = {val: 0 for val in net[0][var]}
    for _ in range(N):
        sample = prior_sampling(net)
        if all(sample[x] == evidences[x] for x in evidences):
            acum[sample[var]] += 1
    return normalize(acum)


# Examples:

# >>> rejection_sampling(net_alarm,"robbery",{"johncalls":True,"marycalls":True},100000)
# {False: 0.7446808510638298, True: 0.2553191489361702}

#
# Note: the exact probability is <False:0.71583,True:0.28417>

# >>> rejection_sampling(net_infarction,"smoker",{"infarction":True,"sport":False},100000)
# {False: 0.519272852919722, True: 0.480727147080278}


# Note: the exact probability is <False:0.52,True:0.48>
#






# ==============================
# Likelihood weighting in Python
# ==============================

# In the following exercises you are asked to implement the likelihood
# weighting algorithm


# ----------
# Exercise 1
# ----------

# Before implementing likelihood weighting, let us see the main deficiency of
# rejection sampling: too many samples are discarded.

# To see this in practice, implement a modification of the function
# rejection_sampling (call it rejection_samping_bis) that prints also the
# number of samples rejected.

# For example:
# >>> rejection_sampling_bis(net_alarm,"robbery",{"johncalls":True,"marycalls":True},1000)
# Rejected 998 samples out of a total of 1000
# {False: 1.0, True: 0.0}
# >>> rejection_sampling_bis(net_alarm,"robbery",{"johncalls":True,"marycalls":True},10000)
# Rejected 9990 samples out of a total of 10000
# {False: 0.4, True: 0.6}
# >>> rejection_sampling_bis(net_alarm,"robbery",{"johncalls":True,"marycalls":True},100000)
# Rejected 99795 samples out of a total of 100000
# {False: 0.7170731707317073, True: 0.28292682926829266}
# >>> rejection_sampling_bis(net_alarm,"robbery",{"johncalls":True,"marycalls":True},1000000)
# Rejected 997937 samples out of a total of 1000000
# {False: 0.7106156083373728, True: 0.28938439166262725}



# =========== Solution:
def rejection_sampling_bis(net, var, evidences, N):
    acum = {val: 0 for val in net[0][var]}
    rejected = 0
    for _ in range(N):
        sample = prior_sampling(net)
        if all(sample[x] == evidences[x] for x in evidences):
            acum[sample[var]] += 1
        else:
            rejected += 1
    print("Rejected {} samples out of a total of {}".format(rejected, N))
    return normalize(acum)



# ===================================

# ----------
# Exercise 2
# ----------

# Modify the function prior_sampling to implement a function

# weighted_sample(net,evidences)

# such that receiving a bayesian network and a dictionary with evidences,
# returns a sample consistent with the evidences, with its the corresponding
# weight.

# This function is described in slide 109 of unit 7.

# Examples:

# >>> weighted_sample(net_alarm,{"johncalls":True,"marycalls":True})
# ({'marycalls': True, 'alarm': False, 'johncalls': True, 'earthquake': False, 'robbery': False}, 0.0005)

# >>> weighted_sample(net_infarction,{"infarction":True,"sport":False})
# ({'smoker': True, 'infarction': True, 'sport': False, 'healthy_nutrition': False, 'hypertense': True}, 0.72)

# =========== Solution:
def weighted_sample(net,evidences):
    w = 1.0
    values = net[0]
    parents = net[1]
    tables = net[2]
    ordered_variables = compatible_ordering(net)
    sample = dict()
    for var in ordered_variables:
        parents_var = parents[var]
        parents_values = tuple(sample[vp] for vp in parents_var)
        # If the variable Xi has value xi in e, then
        if var in evidences:
            # w = w * p(Xi = xi | parents(Xi))
            w = w * tables[var][parents_values][values[var].index(evidences[var])]
            sample[var] = evidences[var]
        else:
            # Else, let xi be a value of Xi returned sampling from P(Xi | padres(Xi))
            sample[var] = sample_distr(values[var], tables[var][parents_values])
    # Return [(x1, ... , xn); w]
    return (sample, w)
# ===================================

# ----------
# Exercise 3
# ----------

# Modify the function rejection_sampling, to implement a function

# likelihood_weighting(net,var,evidences,N)

# such that receiving a bayesian network, a query variable, a dictionary of
# evidences and a number N of samples to generate, apply the LIKELIHOOD
# WEIGHTING algorithm for approximate inference in bayesian networks, as
# explained in slides 106-110 of unit 7.

# This function is described in slide 108 of unit 7.

# Examples:

# >>> likelihood_weighting(net_alarm,"robbery",{"johncalls":True,"marycalls":True},1000)
# {False: 0.7912524850894644, True: 0.20874751491053556}
# >>> likelihood_weighting(net_alarm,"robbery",{"johncalls":True,"marycalls":True},100000)
# {False: 0.7342125355091325, True: 0.2657874644908675}




# =========== Solution:
def likelihood_weighting(net,var,evidences,N):
    # Let W[X] be a vector with one component for each possible value of the query variable X,
    # initially with zeros
    acum = {val: 0 for val in net[0][var]}
    for _ in range(N):
        # Let [(y1; ...; yn); w] be a weighted sample returned by WEIGHTED-SAMPLE(NET,e)
        sample = weighted_sample(net, evidences)
        # Make W[x] equal to W[x] + w, where x is the value taken by the query variable X in y
        acum[sample[0][var]] += sample[1]
    #  Return NORMALIZE(W[X])
    return normalize(acum)
# ===================================



# ----------
# Exercise 4
# ----------

# Make a comparison between rejection sampling and likelihood weighting,
# computing a probability a the network below, that models different problems
# of car starting.

# You can try to compute the following probability with respect that network:

# P("Fuel System OK"| "Battery Age":"old",
#                     "Alternator OK":True,
#                     "Air Filter OK":False,
#                     "Car Starts":False})

# The exact probability (computed with the AISpace applet, www.aispace.org) is:
#       <False:0.13227,True:0.86773>


# Compare and comment the results obtained by both algorithms.
net_car_starting = [{"Alternator OK": [True, False],
                     "Charging System OK": [True, False],
                     "Battery Age": ["new", "old", "very_old"],
                     "Battery Voltage": ["strong", "weak", "dead"],
                     "Fuse OK": [True, False],
                     "Distributer OK": [True, False],
                     "Voltage at Plug": ["strong", "weak", "dead"],
                     "Starter Motor OK": [True, False],
                     "Starter System OK": [True, False],
                     "Headlights": ["bright", "dim", "off"],
                     "Spark Plugs": ["okay", "too wide", "fouled"],
                     "Car Cranks": [True, False],
                     "Spark Timing": ["good", "bad", "very_bad"],
                     "Fuel System OK": [True, False],
                     "Air Filter OK": [True, False],
                     "Air System OK": [True, False],
                     "Car Starts": [True, False],
                     "Spark Quality": ["good", "bad", "very_bad"],
                     "Spark Adequate": [True, False]},

                    {"Alternator OK": [],
                     "Charging System OK": ["Alternator OK"],
                     "Battery Age": [],
                     "Battery Voltage": ["Charging System OK", "Battery Age"],
                     "Fuse OK": [],
                     "Distributer OK": [],
                     "Voltage at Plug": ["Battery Voltage", "Fuse OK", "Distributer OK"],
                     "Starter Motor OK": [],
                     "Starter System OK": ["Battery Voltage", "Fuse OK", "Starter Motor OK"],
                     "Headlights": ["Voltage at Plug"],
                     "Spark Plugs": [],
                     "Car Cranks": ["Starter System OK"],
                     "Spark Timing": ["Distributer OK"],
                     "Fuel System OK": [],
                     "Air Filter OK": [],
                     "Air System OK": ["Air Filter OK"],
                     "Car Starts": ["Car Cranks", "Fuel System OK",
                                    "Air System OK", "Spark Adequate"],
                     "Spark Quality": ["Voltage at Plug", "Spark Plugs"],
                     "Spark Adequate": ["Spark Timing", "Spark Quality"]},

                    {"Alternator OK": {(): [0.9997, 0.0003]},
                     "Charging System OK": {(True,): [0.995, 0.005],
                                            (False,): [0.0, 1.0]},
                     "Battery Age": {(): [0.4, 0.4, 0.2]},
                     "Battery Voltage": {(True, "new"): [0.999, 0.0008, 0.0002],
                                         (True, "old"): [0.99, 0.008, 0.002],
                                         (True, "very_old"): [0.6, 0.3, 0.1],
                                         (False, "new"): [0.8, 0.15, 0.05],
                                         (False, "old"): [0.05, 0.3, 0.65],
                                         (False, "very_old"): [0.002, 0.1, 0.898]},
                     "Fuse OK": {(): [0.999, 0.001]},
                     "Distributer OK": {(): [0.99, 0.01]},
                     "Voltage at Plug": {("strong", True, True): [0.98, 0.015, 0.005],
                                         ("strong", True, False): [0.0, 0.0, 1.0],
                                         ("strong", False, True): [0.0, 0.0, 1.0],
                                         ("strong", False, False): [0.0, 0.0, 1.0],
                                         ("weak", True, True): [0.1, 0.8, 0.1],
                                         ("weak", True, False): [0.0, 0.0, 1.0],
                                         ("weak", False, True): [0.0, 0.0, 1.0],
                                         ("weak", False, False): [0.0, 0.0, 1.0],
                                         ("dead", True, True): [0.0, 0.0, 1.0],
                                         ("dead", True, False): [0.0, 0.0, 1.0],
                                         ("dead", False, True): [0.0, 0.0, 1.0],
                                         ("dead", False, False): [0.0, 0.0, 1.0]},
                     "Starter Motor OK": {(): [0.992, 0.008]},
                     "Starter System OK": {("strong", True, True): [0.998, 0.002],
                                           ("strong", True, False): [0.0, 1.0],
                                           ("strong", False, True): [0.0, 1.0],
                                           ("strong", False, False): [0.0, 1.0],
                                           ("weak", True, True): [0.72, 0.28],
                                           ("weak", True, False): [0.0, 1.0],
                                           ("weak", False, True): [0.0, 1.0],
                                           ("weak", False, False): [0.0, 1.0],
                                           ("dead", True, True): [0.0, 1.0],
                                           ("dead", True, False): [0.0, 1.0],
                                           ("dead", False, True): [0.0, 1.0],
                                           ("dead", False, False): [0.0, 1.0]},
                     "Headlights": {("strong",): [0.98, 0.015, 0.005],
                                    ("weak",): [0.05, 0.9, 0.05],
                                    ("dead",): [0.0, 0.0, 1.0]},
                     "Spark Plugs": {(): [0.99, 0.003, 0.007]},
                     "Car Cranks": {(True,): [0.98, 0.02],
                                    (False,): [0.0, 1.0]},
                     "Spark Timing": {(True,): [0.97, 0.02, 0.01],
                                      (False,): [0.2, 0.3, 0.5]},
                     "Fuel System OK": {(): [0.9, 0.1]},
                     "Air Filter OK": {(): [0.9, 0.1]},
                     "Air System OK": {(True,): [0.9, 0.1],
                                       (False,): [0.3, 0.7]},
                     "Car Starts": {(True, True, True, True): [1.0, 0.0],
                                    (True, True, True, False): [0.0, 1.0],
                                    (True, True, False, True): [0.0, 1.0],
                                    (True, True, False, False): [0.0, 1.0],
                                    (True, False, True, True): [0.0, 1.0],
                                    (True, False, True, False): [0.0, 1.0],
                                    (True, False, False, True): [0.0, 1.0],
                                    (True, False, False, False): [0.0, 1.0],
                                    (False, True, True, True): [0.0, 1.0],
                                    (False, True, True, False): [0.0, 1.0],
                                    (False, True, False, True): [0.0, 1.0],
                                    (False, True, False, False): [0.0, 1.0],
                                    (False, False, True, True): [0.0, 1.0],
                                    (False, False, True, False): [0.0, 1.0],
                                    (False, False, False, True): [0.0, 1.0],
                                    (False, False, False, False): [0.0, 1.0]},
                     "Spark Quality": {("strong", "okay"): [1.0, 0.0, 0.0],
                                       ("strong", "too wide"): [0.0, 1.0, 0.0],
                                       ("strong", "fouled"): [0.0, 0.0, 1.0],
                                       ("weak", "okay"): [0.0, 1.0, 0.0],
                                       ("weak", "too wide"): [0.0, 0.5, 0.5],
                                       ("weak", "fouled"): [0.0, 0.2, 0.8],
                                       ("dead", "okay"): [0.0, 0.0, 1.0],
                                       ("dead", "too wide"): [0.0, 0.0, 1.0],
                                       ("dead", "fouled"): [0.0, 0.0, 1.0]},
                     "Spark Adequate": {("good", "good"): [0.99, 0.01],
                                        ("good", "bad"): [0.5, 0.5],
                                        ("good", "very_bad"): [0.1, 0.9],
                                        ("bad", "good"): [0.5, 0.5],
                                        ("bad", "bad"): [0.05, 0.95],
                                        ("bad", "very_bad"): [0.01, 0.99],
                                        ("very_bad", "good"): [0.1, 0.9],
                                        ("very_bad", "bad"): [0.01, 0.99],
                                        ("very_bad", "very_bad"): [0.0, 1.0]}}]

# Solution:
print(rejection_sampling(net_car_starting,"Fuel System OK",{"Battery Age":"old","Alternator OK":True,
                                                 "Air Filter OK":False, "Car Starts":False},1000))
print(likelihood_weighting(net_car_starting,"Fuel System OK",{"Battery Age":"old","Alternator OK":True,
                                                 "Air Filter OK":False, "Car Starts":False},1000))

print(rejection_sampling(net_car_starting,"Fuel System OK",{"Battery Age":"old","Alternator OK":True,
                                                 "Air Filter OK":False, "Car Starts":False},100000))
print(likelihood_weighting(net_car_starting,"Fuel System OK",{"Battery Age":"old","Alternator OK":True,
                                                 "Air Filter OK":False, "Car Starts":False},100000))

# As we can see the accuracy of likelihood_weighting is higher


# End of file