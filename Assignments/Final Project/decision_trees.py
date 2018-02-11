# ==========================================================
# Artificial Intelligence. Third course.
# Grado en IngenierÃ­a InformÃ¡tica
# 2017-2018
# Universidad de Sevilla
# Final Project
# Professor: JosÃ© Luis Ruiz Reina
# ===========================================================

# --------------------------------------------------------------------------
# First member of the group (or the only author):
#
# SURNAMES: Keshet
# NAME: Eden
#
# Second member (if it is a group):
#
# SURNAMES: Damti
# NAME: Oshri
# ----------------------------------------------------------------------------



# *****************************************************************************
# ACADEMIC INTEGRITY AND CHEATING: this project have to be carried out
# independently by each student or group. SHARING CODE IS STRICTLY
# FORBIDDEN. It as also forbidden to use any third-party code, available on
# web or on any source, without the approval of the teacher.

# Any plagiarism detected will result in a FINAL GRADE OF ZERO IN THE COURSE,
# for ALL the students involved, and it may lead to other disciplinary
# measures. Furthermore, the grades obtained until that moment will not be
# kept for future calls.
# *****************************************************************************

# IMPORTANT: DO NOT CHANGE THE NAMES EITHER TO THIS FILE OR TO THE FUNCTIONS
# ASKED (in that case, it will not be evaluated)


# THIS FINAL PROJECT WORTHS 20% OF THE TOTAL GRADE




# ---------------------------------------------------------------------------
# SECTION 0: Data sets
# ---------------------------------------------------------------------------

# In this section, you do not have to do anything, buth it is important to
# read it in order to understand the structure of the data sets provided.

#
# Files play_tennis.py, contac_lenses.py, votes.py and credit.py (that can be
# downloaded from the web page of this final project) contain the data sets
# we are going to use in this final project, and our implementations will be
# tested on them.

# Each of these files contain the corresponding definition for the following
# variables:


# * attributes: is a list of pairs (Attribute,Values) for each attribute (or
#   feature) of the data set. Attribute is the name of the attribute and
#   Values is the list of its possible values.

# * class_name: name of the classification attribute.

# * classes: possible values (or classes) of the classification attribute.

# * train: training set, a list of examples. Each example is a list of values,
#   where a value in a given position is the value of the attribute of the
#   same position in the attributes list described above. The value in the
#   last position is the class of the example.

# In addition, votes.py and credit.py contain the following additional
# variables:

# * valid: validation set, is a list of examples with the same format than the
#   trainig set. This set of examples will be used to adjust or generalize the
#   model learned in the trainig phase. In our case, it will be used to prune
#   the learned decision tree.


# * test: test set, a list of examples with the same format than the training
#   set. These examples will be used to evaluate the final accuracy of a
#   learned classifier.

# Let us import these for files:
import math
import random

from collections import defaultdict

import play_tennis
import contact_lenses
import titanic
import votes
import credit


# ---------------------------------------------------------------------------
# SECTION 1: Learning decision trees
# ---------------------------------------------------------------------------

# Decision tree representation:
# =============================

# NOTE: In the following description we could be using the same term
# "attribute" to refer to two different things: variables attributes of an
# object of a python class, and attributes of data sets. We hope that it will
# be clear from the context to what we are referring in each case, but to
# avoid confussion, we also use the term "field" for variable attributes
# of an python class.


# We will represent decision trees using the following data structure, in
# a recursive way


class NodeDT():
    def __init__(self, attribute=-1, distr=None, branches=None, clas=None):
        self.distr = distr;
        self.attribute = attribute;
        self.branches = branches;
        self.clas = clas;

        # An object of this class NodeDT will represent a decision tree node, by means


# of its four fields (distr, atrribute, branches, class), as we describe in
# the following. We will have two types of nodes, both represented by objects
# of the class NodeDT: LEAF nodes, those with a class value, and INNER nodes,
# corresponding to a given attribute and having as many successors subtrees as
# posible values of the attribute. Depending on the type of the node, some of
# the attributes of the object will have None value. That is:


# * In a leaf node, the "class" field contains the classification value
#   returned by the node. The "branches" and "attribute" fields have None
#   value.

# * In a inner node, the "class" field is None, the "attribute" field is an
#   index to the corresponding attribute in the list of attributes of the data
#   set, and "branches" is a dictionary representing its successors
#   subtrees. In particular, the keys of that dictionary are the different
#   values of the attribute (the label of the branch) and the value assigned
#   to that key is an object of the class NodeDT recusively representing the
#   subtree corresponding to that value.


# IMPORTANT NOTE: In the "attribute" field we will not store the name of the
# attribute, but an INDEX to the position of that attribute in list of
# attributes of the data set.


# In both types of nodes, the "distr" field will store the distribution,
# according to the different class values, of the examples in the training set
# corresponding to that node.


# With an example, it will better understood.


# EXAMPLE
# -------

# Let us describe how to represent the "Play Tennis" decision tree shown in
# slide 8 of unit 3.

# Let us assume the variable pt_tree contains such tree (in this case, the
# tree has been built using the learning algorithm asked later).

# >>> pt_tree=learn_tree(play_tennis.train,play_tennis.attributes)

# That tree is an object of the class NodeDT, or more precisely the root node
# of the tree:


# >>> pt_tree
# <__main__.NodeDT at 0x7f1b8d74b550>

# It is an inner node (the root in this case), whose attribute is
# "Outlook". In the attributes variable of play_tennis.py, "Outlook" is the
# first attribute, so the corresponding index is 0, and that is what we
# store in the "attribute" field:


# >>> pt_tree.attribute
# 0

# In the "distr" field, we store the class distribution of the examples
# corresponding to that node (in this case all the examples, since its the
# root node):

# >>> pt_tree.distr
# defaultdict(int, {'no': 5, 'yes': 9})

# Note that the distribution is stored using "defaultdict", a datatype similar
# to "dict", but with a default value that it is assumed to correspond to any
# "key" not present in the dictionary. In this particular case, initializing
# with "defaultdict(int)", we obtain a default dictionary in which every key
# not explicitly in it, will have associated default value of 0. For more
# details on default dictionaries, see the python manual reference, module
# "collections".

# In the "branches" field, we store a dictionary, with a key for every value
# of the "Outlook" attribute. The value associated to each key is itself a
# NodeDT object, recursively representing  the corresponding subtree.

# >>> pt_tree.branches

# {'Sunny': <__main__.NodeDT object at 0x7fa508e0e198>,
#  'Overcast': <__main__.NodeDT object at 0x7fa508e0ecf8>,
#  'Rainy': <__main__.NodeDT object at 0x7fa508e1eac8>}



# For example, the subtree of the branch "Outlook=Sunny", starts with an inner
# node corresponding to the index attribute 2 ("Humidity"):

# >>> pt_tree.branches["Sunny"].attribute
# 2

# With "Outlook=Sunny", we have 3 negative and 2 positive examples:

# >>> pt_tree.branches["Sunny"].distr
# defaultdict(int, {'no': 3, 'yes': 2})

# And the branches are:

# >>> pt_tree.branches["Sunny"].branches
# {'High': <__main__.NodeDT at 0x7f8c84687710>,
#  'Normal': <__main__.NodeDT at 0x7f8c846877f0>}

# The node corresponding to "Outlook=Sunny" and "Humidity=Normal" is a leaf of
# the tree, classifying as "yes":

# >>> pt_tree.branches["Sunny"].branches["Normal"].clas
# 'yes'

# And with "Outlook=Sunny" and "Humidity=Normal", we have 2 positive and 0
# negative examples:

# >>> pt_tree.branches["Sunny"].branches["Normal"].distr
# defaultdict(int, {'yes': 2}) #

# The node corresponding to "Outlook Sunny" and "Humidity=High" is also a leaf
# of the tree, classifying as negative, and whose distribution is 3 negative
# and 0 positive examples:

# >>> pt_tree.branches["Sunny"].branches["High"].clas
# 'no'
# >>> pt_tree.branches["Sunny"].branches["High"].distr
# defaultdict(int, {'no': 3})

# The following are the rest of the nodes:

# >>> pt_tree.branches["Overcast"].clas
# 'yes'
# >>> pt_tree.branches["Overcast"].distr
# defaultdict(int, {'yes': 4})


# >>> pt_tree.branches["Rainy"].attribute
# 3
# >>> pt_tree.branches["Rainy"].branches
# {'Strong': <__main__.NodeDT at 0x7f8c84687630>,
# 'Weak': <__main__.NodeDT at 0x7f8c84687668>}
# >>> pt_tree.branches["Rainy"].distr
# defaultdict(int, {'no': 2, 'yes': 3})

# >>> pt_tree.branches["Rainy"].branches["Strong"].clas
# 'no'
# >>> pt_tree.branches["Rainy"].branches["Strong"].distr
# defaultdict(int, {'no': 2})

# >>> pt_tree.branches["Rainy"].branches["Weak"].clas
# 'yes'
# >>> pt_tree.branches["Rainy"].branches["Weak"].distr
# defaultdict(int, {'yes': 3})


# FUNCTIONS ASKED
# ===============

# Using the above data structure, implement the following four functions:


# 1. A function "learn_tree(examples,attributes)", such that receiving a set
# of examples and a list of attributes (with names and values, as in in data
# set files) apply the id3 algorithm described in class, to obtain a decision
# tree.

def entropy(distributions):
    # sum_{i=1,n} -(xi/N)log(xi/N)
    N = sum(dist for dist in distributions)
    return -sum(dist / N * math.log(dist / N, 2) if dist != 0 else 0 for dist in distributions)


def gini(distributions):
    # 1- sum_{i=1,n} (xi/N)**2
    N = sum(distribution for distribution in distributions)
    return 1 - sum((distribution / N) ** 2 if distribution != 0 else 0 for distribution in distributions)


def learn_tree(examples, attributes, impurity_func=entropy, max_freq_split=1.0, min_prop_examples=0.0):
    return learn_tree_rec(examples, attributes, impurity_func, max_freq_split, min_prop_examples, len(examples))


def learn_tree_rec(examples, attributes, impurity_func, max_freq_split, min_prop_examples, number_examples):
    classes = set(example[-1] for example in examples)
    distribution = defaultdict(int)
    for class_name in classes:
        distribution[class_name] = sum(example[-1] == class_name for example in examples)

    # Base Cases
    # - If all the Examples are from the same class.
    for class_name in classes:
        if all(example[-1] == class_name for example in examples):
            # Return a leaf node labeled
            return NodeDT(-1, distribution, None, class_name)

    # - If Attributes is empty
    if all(not attribute for attribute in attributes):
        # Return a node labeled with the most frequent class in Examples
        return NodeDT(-1, distribution, None, frequent_class(examples, classes))

    # - If in a given node the proportion of the most frequent class is greater or equal than
    #   max_freq_split, then we make that node a leaf, predicting that majority class.
    if (max(sum(example[-1] == class_name for example in examples) for class_name in classes) / len(
            examples) >= max_freq_split):
        # Return a node labeled with the most frequent class in Examples
        return NodeDT(-1, distribution, None, frequent_class(examples, classes))

    # - If the proportion of examples in a node is less or equal than min_prop_examples,
    #   then we make that node a leaf, predicting the most frequent class.
    if len(examples) / number_examples <= min_prop_examples:
        # Return a node labeled with the most frequent class in Examples
        return NodeDT(-1, distribution, None, frequent_class(examples, classes))

    # - Otherwise:
    # Let best_attribute be the BEST attribute of Attributes, as for the classifying Examples
    best_attribute = get_best_attribute(examples, attributes, classes, impurity_func)
    changed_attributes = copy.deepcopy(attributes)
    changed_attributes[best_attribute] = ()
    branches = {}

    for value in attributes[best_attribute][1]:
        example_subset = [example for example in examples if value == example[best_attribute]]
        # - If Examples(v) is empty:
        if not example_subset:
            distr_subset = defaultdict(int)
            for class_name in classes:
                distr_subset[class_name] = sum(example[-1] == class_name for example in example_subset)
            # Then put a leaf labeled with the most frequent class in Examples
            branches[value] = NodeDT(-1, distr_subset, None, frequent_class(examples, classes))
        else:
            # Extend the outgoing edge with the subtree ID3(Examples(v), Class, Attributes-{A}).
            branches[value] = learn_tree_rec(example_subset, changed_attributes, impurity_func, max_freq_split,
                                             min_prop_examples, number_examples)
    # Return Tree
    return NodeDT(best_attribute, distribution, branches)


# Return a node labeled with the most frequent class in Example
def frequent_class(examples, classes):
    (value, index) = max((val, ind) for ind, val in enumerate((sum(example[-1] == class_name for example in examples)
                                                               for class_name in classes)))
    return list(classes)[index]


def get_best_attribute(examples, attributes, classes, impurity_func):
    gain = [0 for _ in range(len(attributes))]
    org_dist = [sum(example[-1] == class_name for example in examples) for class_name in classes]
    for (i, attribute) in enumerate(attributes):
        if attribute:
            atr_dist = [[sum(example[-1] == class_name if example[i] == j else False for example in examples)
                         for class_name in classes] for j in attribute[1]]
            # Gain(A,E)=impurity(E)-sum_{j=1,m}(N_vj/N)*impurity(E_vj)
            gain[i] = impurity_func(org_dist) - sum(
                sum(E_vj) / sum(org_dist) * impurity_func(E_vj) for E_vj in atr_dist)
    return gain.index(max(gain))


# This function has additional input parameters, explained below in detail.

# 2. A function "print_DT(tree,attributes,class_name)" such that receiving a
# decision tree, the list of attributes of the problem (as in the data set
# files) and the name of the class attribute, prints the tree as shown in the
# examples below.
def print_DT(tree, attributes, class_name):
    if tree:
        print("Root node (", end="")
        first = 0
        for (i, j) in zip(tree.distr.keys(), tree.distr.values()):
            print("  {}: {}".format(i, j), end="") if first else print("{}: {}".format(i, j), end="")
            first = 1
        print(")")
        print_DT_rec(tree, attributes, class_name, 1)


def print_DT_rec(tree, attributes, class_name, num_space):
    print(" " * num_space, end="")
    if tree.branches:
        first_atr = 0
        for attribute in attributes[tree.attribute][1]:
            print("{} = {}. (".format(attributes[tree.attribute][0], attribute), end="") if not first_atr else print(
                " " * (num_space - 1), "{} = {}. (".format(attributes[tree.attribute][0], attribute), end="")
            first_atr = 1
            first = 0
            if not tree.branches[attribute].distr:
                pass
            elif 0 in tree.branches[attribute].distr.values():
                print("No examples", end="")
            else:
                for (i, j) in zip(tree.branches[attribute].distr.keys(),
                                  tree.branches[attribute].distr.values()):
                    print("  {}: {}".format(i, j), end="") if first else print("{}: {}".format(i, j), end="")
                    first = 1
            print(")")
            print_DT_rec(tree.branches[attribute], attributes, class_name, num_space + 5)
    elif tree.clas:
        print("{}: {}.".format(class_name, tree.clas))
    else:
        print("error")


# 3. A function "classify_DT(example,tree)" such that receiving an example
# (without its class) and a decision tree, returns the class that the tree
# assigns to the example.
def classify_DT(example, tree):
    if tree.branches and example[tree.attribute] in tree.branches:
        return classify_DT(example, tree.branches[example[tree.attribute]])
    return tree.clas


# 4. A function "accuracy_DT(tree,examples)", such that receiving and list of
# examples (with their class) and a decision tree, returns the proportion of
# examples correctly classified by the tree.
def accuracy_DT(tree, examples):
    if examples and tree:
        return sum(classify_DT(example[:-1], tree) == example[-1] for example in examples) / len(examples)
# -------------

# Let us explain in more detail a number of additional input parameters of  the
# function learn_tree. The complete specification of the function is:

# learn_tree(training_set,
#            attributes,
#            impurity_func=entropy,
#            max_freq_split=1.0,
#            min_prop_examples=0)

# where:

# - training_set is a list of examples, as provided in the data files.

# - attributes is list of the attributes of the data, and its possible values,
#   as provided in the data files.

# - impurity_func: this is a parameter indicating the function that we will
#   use to mesure the "impurity" of a distribution of examples in
#   classes. This generalizes the criteria used in the slides.
#   The impurity function may be either entropy or gini (the default value is
#   entropy):

#     * The entropy of a distribution is defined as in the slides of unit 3,
#       but generalized to possibly more than two classes: if we have n
#       different classes, the entropy of a distribution [x1,...,xn] is
#                     sum_{i=1,n} -(xi/N)log(xi/N),
#       where N is x1+...+xn and log is base 2 logarithm.

#     * Analogously, the gini impurity of a distribution is defined in the
#       following way:
#                      1- sum_{i=1,n} (xi/N)**2

#   Both entropy and gini measure the lack of homogeneity of a distribution
#   and can be used as a criteria to decide which is the best attribute to
#   split at a given node of a decision tree, in the following way. If we have
#   a set of examples E at a Node, and a candidate attribute A with values
#   v1,...,vm, then we define the Gain of A in E as:

#      Gain(A,E)=impurity(E)-sum_{j=1,m}(N_vj/N)*impurity(E_vj)

#   where E_vj is the subset of examples in E with A=vj, N_vj is the size
#   of E_vj, N is the size of E, and impurity may be either entropy or gini.

#   When learning the tree, we will select the attribute with the greatest
#   gain (and we will use entropy or gini as impurity, depending on the
#   value of the input argument impurity_func).

# - max_freq_split is a number between 0 and 1.0 (default 1.0). If in a given
#   node the proportion of the most frequent class is greater or equal than
#   max_freq_split, then we make that node a leaf, predicting that majority
#   class.

# - min_prop_examples is a number between 0 and 1.0 (default 0). If the
#   proportion of examples in a node is less or equal than min_prop_examples,
#   then we make that node a leaf, predicting the most frequent class.

# The last two arguments (max_freq_split and min_prop_examples) provide a way
# of "early stopping" when learning the tree, to avoid overfitting by means of
# pre-pruning. In the next section, we will also implement post-pruning, an
# alternative way to avoid overfitting.

# Some examples:
# --------------

# Play tennis:

# >>> pt_tree=learn_tree(play_tennis.train,play_tennis.attributes)

# >>> print_DT(pt_tree,play_tennis.attributes,play_tennis.class_name)

# Root node (no: 5  yes: 9)
#  Outlook = Sunny. (no: 3  yes: 2)
#       Humidity = High. (no: 3)
#            Play Tennis: no.
#       Humidity = Normal. (yes: 2)
#            Play Tennis: yes.
#  Outlook = Overcast. (yes: 4)
#       Play Tennis: yes.
#  Outlook = Rainy. (yes: 3  no: 2)
#       Wind = Weak. (yes: 3)
#            Play Tennis: yes.
#       Wind = Strong. (no: 2)
#            Play Tennis: no.

# >>> classify_DT(["Sunny","Mild","High","Strong"],pt_tree)
# 'no'

# >>> accuracy_DT(pt_tree,play_tennis.train)
# 1.0

# ------------------

# Contact lenses:

# >>> cl_tree=learn_tree(contact_lenses.train,contact_lenses.attributes)
# >>> print_DT(cl_tree,contact_lenses.attributes,contact_lenses.class_name)

# Root node (None: 15  Soft: 5  Hard: 4)
# Tear rate = Reduced. (None: 12)
#      Lens: None.
# Tear rate = Normal. (Soft: 5  Hard: 4  None: 3)
#      Astigmatic = +. (Hard: 4  None: 2)
#           Prescription = Myope. (Hard: 3)
#                Lens: Hard.
#           Prescription = Hypermetrope. (Hard: 1  None: 2)
#                Age = Young. (Hard: 1)
#                     Lens: Hard.
#                Age = Pre-presbyopic. (None: 1)
#                     Lens: None.
#                Age = Presbyopic. (None: 1)
#                     Lens: None.
#      Astigmatic = -. (Soft: 5  None: 1)
#           Age = Young. (Soft: 2)
#                Lens: Soft.
#           Age = Pre-presbyopic. (Soft: 2)
#                Lens: Soft.
#           Age = Presbyopic. (None: 1  Soft: 1)
#                Prescription = Myope. (None: 1)
#                     Lens: None.
#                Prescription = Hypermetrope. (Soft: 1)
#                     Lens: Soft.

# >>> classify_DT(["Pre-presbyopic","Hypermetrope","-","Normal"],cl_tree)
# 'Soft'

# >>> accuracy_DT(cl_tree,contact_lenses.train)
# 1.0

# >>> cl_tree_2=learn_tree(contact_lenses.train,contact_lenses.attributes,
#                          impurity_func=gini,
#                          max_freq_split=0.75,
#                          min_prop_examples=0.15)

# >>> print_DT(cl_tree_2,contact_lenses.attributes,contact_lenses.class_name)

# Root node (None: 15  Soft: 5  Hard: 4)
#  Tear rate = Reduced. (None: 12)
#       Lens: None.
#  Tear rate = Normal. (Soft: 5  Hard: 4  None: 3)
#       Astigmatic = +. (Hard: 4  None: 2)
#            Prescription = Myope. (Hard: 3)
#                 Lens: Hard.
#            Prescription = Hypermetrope. (Hard: 1  None: 2)
#                 Lens: None.
#       Astigmatic = -. (Soft: 5  None: 1)
#            Lens: Soft.


# >>> classify_DT(["Pre-presbyopic","Hypermetrope","-","Normal"],cl_tree_2)
# 'Soft'

# >>> accuracy_DT(cl_tree_2,contact_lenses.train)
# 0.9166666666666666

# ----------------

# Congressional voting:

# >>> votes_tree=learn_tree(votes.train,votes.attributes)

# >>> print_DT(votes_tree,votes.attributes,votes.class_name)
# Root node (republican: 107  democrat: 172)
#  vote4 = y. (republican: 103  democrat: 6)
#       vote3 = y. (republican: 10  democrat: 4)
#            vote7 = y. (republican: 9)
#                 Party: republican.
#            vote7 = n. (democrat: 4  republican: 1)
#                 vote2 = y. (democrat: 3)
#                      Party: democrat.
#                 vote2 = n. (democrat: 1)
#                      Party: democrat.
#                 vote2 = ?. (republican: 1)
#                      Party: republican.
#            vote7 = ?. (No examples)
#                 Party: republican.
#       vote3 = n. (republican: 92  democrat: 1)
# ...
# ...
# ... (a big tree, we do not show it complete here)
# ...


# >>> accuracy_DT(votes_tree,votes.train)
# 1.0
# >>> accuracy_DT(votes_tree,votes.valid)
# 0.9420289855072463
# >>> accuracy_DT(votes_tree,votes.test)
# 0.9195402298850575


# >>> votes_tree_2=learn_tree(votes.train,votes.attributes,
#                             max_freq_split=0.95,
#                             impurity_func=gini,
#                             min_prop_examples=0.05)
# >>> print_DT(votes_tree_2,votes.attributes,votes.class_name)
# Root node (republican: 107  democrat: 172)
#  vote4 = y. (republican: 103  democrat: 6)
#       vote3 = y. (republican: 10  democrat: 4)
#            vote7 = y. (republican: 9)
#                 Party: republican.
#            vote7 = n. (democrat: 4  republican: 1)
#                 Party: democrat.
#            vote7 = ?. (No examples)
#                 Party: republican.
#       vote3 = n. (republican: 92  democrat: 1)
#            Party: republican.
#       vote3 = ?. (republican: 1  democrat: 1)
#            Party: republican.
#  vote4 = n. (democrat: 163  republican: 2)
#       Party: democrat.
#  vote4 = ?. (democrat: 3  republican: 2)
#       Party: democrat.


# >>> accuracy_DT(votes_tree_2,votes.train)
# 0.974910394265233
# >>> accuracy_DT(votes_tree_2,votes.valid)
# 0.9565217391304348
# >>> accuracy_DT(votes_tree_2,votes.test)
# 0.9195402298850575


# ------------

# Bank credit:

# >>> ct_tree=learn_tree(credit.train,credit.attributes)

# >>> print_DT(ct_tree,credit.attributes,credit.class_name)

# Root node (study: 116  not grant: 107  grant: 102)
# Income = low. (not grant: 73  study: 19  grant: 11)
#      Employment = official. (not grant: 9  study: 8  grant: 9)
#           Real estate = none. (not grant: 9)
#                Loan: not grant.
#           Real estate = one. (study: 6)
#                Loan: study.
#           Real estate = more. (study: 2  grant: 9)
#                Marital status = single. (grant: 4)
#                     Loan: grant.
#                Marital status = married. (grant: 1)
#                     Loan: grant.
# ....
# ....
# .... (very big tree, not shown complete).


# >>> accuracy_DT(ct_tree,credit.train)
# 1.0
# >>> accuracy_DT(ct_tree,credit.valid)
# 0.9197530864197531
# >>> accuracy_DT(ct_tree,credit.test)
# 0.8650306748466258

# >>> ct_tree_2=learn_tree(credit.train,credit.attributes,
#                          max_freq_split=0.75,
#                          min_prop_examples=0.1)

# >>> print_DT(ct_tree_bis,credit.attributes,credit.class_name)
# Root node (study: 116  not grant: 107  grant: 102)
#  Income = low. (not grant: 73  study: 19  grant: 11)
#       Employment = official. (not grant: 9  study: 8  grant: 9)
#            Loan: not grant.
#       Employment = employed. (not grant: 17  study: 7)
#            Loan: not grant.
#       Employment = unemployed. (study: 2  grant: 1  not grant: 24)
#            Loan: not grant.
#       Employment = retired. (study: 2  grant: 1  not grant: 23)
#            Loan: not grant.
#  Income = medium. (grant: 37  not grant: 34  study: 36)
#       Real estate = none. (not grant: 23  grant: 1  study: 14)
#            Employment = official. (study: 6)
#                 Loan: study.
#            Employment = employed. (grant: 1  not grant: 1  study: 6)
#                 Loan: study.
#            Employment = unemployed. (study: 2  not grant: 13)
#                 Loan: not grant.
#            Employment = retired. (not grant: 9)
#                 Loan: not grant.
#       Real estate = one. (not grant: 11  study: 22  grant: 1)
#            Products = none. (study: 1  grant: 1  not grant: 7)
#                 Loan: not grant.
#            Products = one. (study: 14)
#                 Loan: study.
#            Products = more. (not grant: 4  study: 7)
#                 Loan: study.
#       Real estate = more. (grant: 35)
#            Loan: grant.
#  Income = high. (study: 61  grant: 54)
#       Employment = official. (grant: 26)
#            Loan: grant.
#       Employment = employed. (study: 3  grant: 25)
#            Loan: grant.
#       Employment = unemployed. (grant: 3  study: 29)
#            Loan: study.
#       Employment = retired. (study: 29)
#            Loan: study.


# >>> accuracy_DT(ct_tree_2,credit.train)
# 0.8584615384615385
#
# >>> accuracy_DT(ct_tree_2,credit.valid)
# 0.9012345679012346
#
# >>> accuracy_DT(ct_tree_2,credit.test)
# 0.8834355828220859




# ---------------------------------------------------------------------------
# SECTION 2: Reduced error pruning
# ---------------------------------------------------------------------------

# Overfitting is a phenomenon typically ocurring in supervised learning, when
# the learned model is so fitted to a particular training data, that it does
# not generalize well to predict on data that were not used for training.

# A way to avoid overfitting when learning decision trees is to prune the
# learned tree, trying to improve the accuracy on a set of examples different
# from the one used for training. This can be done in the training phase,
# applying some early stopping criteria (as shown in the previous section),
# but the most common way to do it is by post-pruning the learned tree.

# For that purpose, in the cases when we have enough data, we are going to
# split them in three different parts: training, validation and test sets. We
# will learn the tree using the training data, the validation examples will be
# used to prune the tree and finally we will measure its accuracy on the test
# set. Note that the examples on votes.py and credit.py are already splitted
# in these three parts.

# One of the basic pruning techniques is implemented by the "reduced error
# pruning" algorithm described in unit 3, slide 32. In this section we ask you
# to implement that algorithm in python. For that, the following auxiliary
# functions may be useful:

# * The function "inner_nodes_DT" receives a decision tree a returns a list
# with "paths" to all the inner nodes of the tree.

def inner_nodes_DT_rec(Tree_dt, current_path, acum_nodes):
    if Tree_dt.clas is not None:
        return acum_nodes
    else:
        acum_nodes.append(current_path)
        for val in Tree_dt.branches:
            acum_nodes = inner_nodes_DT_rec(Tree_dt.branches[val], current_path + [val], acum_nodes)
        return acum_nodes


def inner_nodes_DT(Tree_DT):
    return inner_nodes_DT_rec(Tree_DT, [], [])


# Examples:


# >>> inner_nodes_DT(pt_tree)
# [[], ['Sunny'], ['Rainy']]
# >>> inner_nodes_DT(cl_tree)
# [[], ['Normal'], ['Normal', '+'], ['Normal', '+', 'Hypermetrope'],
#  ['Normal', '-'], ['Normal', '-', 'Presbyopic']]

# Note that every path to an inner node can be characterized by the labels
# (values of attributes) of the branches leading to that node. The path
# corresponding to the root node is the empty list.


# * The function "prune_node_DT(tree,node)" receives a decision tree and a
# path to an inner node (in the form returned by the previous function), and
# returns a COPY of the tree in which that node has been pruned and replaced by
# a leaf with the majority class in that node (note that you must define the
# function "most_frequent_class")

import copy


def prune_node_DT(tree, node):
    if node == []:
        return NodeDT(distr=tree.distr, clas=most_frequent_class(tree.distr))
    else:
        val_node = node[0]
        pruned_tree = NodeDT(attribute=tree.attribute, distr=copy.copy(tree.distr))
        dict_subtrees = {}
        for val in tree.branches:
            if val_node == val:
                dict_subtrees[val] = prune_node_DT(tree.branches[val], node[1:])
            else:
                dict_subtrees[val] = copy.deepcopy(tree.branches[val])
        pruned_tree.branches = dict_subtrees
        return pruned_tree


def most_frequent_class(distr):
    return (max(distr, key=distr.get))


# Example:
# >>> print_DT(prune_node_DT(cl_tree,['Normal','+']),
#              contact_lenses.attributes,
#              contact_lenses.class_name)

# Root node (None: 15  Soft: 5  Hard: 4)
#  Tear rate = Reduced. (None: 12)
#       Lens: None.
#  Tear rate = Normal. (Soft: 5  Hard: 4  None: 3)
#       Astigmatic = +. (Hard: 4  None: 2)
#            Lens: Hard.
#       Astigmatic = -. (Soft: 5  None: 1)
#            Age = Young. (Soft: 2)
#                 Lens: Soft.
#            Age = Pre-presbyopic. (Soft: 2)
#                 Lens: Soft.
#            Age = Presbyopic. (None: 1  Soft: 1)
#                 Prescription = Myope. (None: 1)
#                      Lens: None.
#                 Prescription = Hypermetrope. (Soft: 1)
#                      Lens: Soft.


# FUNCTION ASKED
# ==============

# * A function "prune_tree(tree,examples)" such that receiving as input a
# decision tree and a set of examples, apply reduced error pruning as
# described in slide 32, unit 3.
def prune_tree(tree, examples):
    Continue = True
    while Continue:
        Measure_best = 0
        best_purne_tree = None

        # Measure = classification accuracy of the learned tree on Test
        Measure = calc_accuracy_DT(tree, examples)
        for node in inner_nodes_DT(tree):
            # Temporarily prune the subtree of Tree at node N, replacing it by a leaf labeled with the
            # majority class at that node
            temp_purne_tree = prune_node_DT(tree, node)

            # Compute the classification accuracy of the pruned tree, on the test set
            temp_ac = calc_accuracy_DT(temp_purne_tree, examples)
            if temp_ac > Measure_best:
                best_purne_tree = temp_purne_tree
                # Let Measure_best the node with best accuracy
                Measure_best = temp_ac

        # If its accuracy is better than Measure, then Tree = permanently prune Tree at node Measure_best
        # Otherwise, Continue=False ans stopping the while
        if Measure <= Measure_best:
            tree = best_purne_tree
        else:
            Continue = False
    return tree


# Measure = classification accuracy of the leraned tree on Test
def calc_accuracy_DT(tree, examples):
    return sum(1 if (classify_DT_ans(v, tree) == v[len(v) - 1]) else 0 for v in examples) / len(examples)


def classify_DT_ans(example, tree):
    if tree.branches and example[tree.attribute] in tree.branches:
        return classify_DT_ans(example, tree.branches[example[tree.attribute]])
    return tree.clas


# Examples:

# >>> votes_pruned=prune_tree(votes_tree,votes.valid)
# >>> print_DT(votes_pruned,votes.attributes,votes.class_name)
# Root node (republican: 107  democrat: 172)
#  vote4 = y. (republican: 103  democrat: 6)
#       Party: republican.
#  vote4 = n. (democrat: 163  republican: 2)
#       Party: democrat.
#  vote4 = ?. (democrat: 3  republican: 2)
#       Party: democrat.



# >>> ct_pruned=prune_tree(ct_tree,credit.valid)

# >>> print_DT(ct_pruned,credit.attributes,credit.class_name)

# Root node (study: 116  not grant: 107  grant: 102)
# Income = low. (not grant: 73  study: 19  grant: 11)
#      Employment = official. (not grant: 9  study: 8  grant: 9)
#           Real estate = none. (not grant: 9)
#                Loan: not grant.
#           Real estate = one. (study: 6)
#                Loan: study.
#           Real estate = more. (study: 2  grant: 9)
#                Loan: grant.
#      Employment = employed. (not grant: 17  study: 7)
#           Products = none. (not grant: 8)
#                Loan: not grant.
#           Products = one. (not grant: 9)
#                Loan: not grant.
#           Products = more. (study: 7)
#                Loan: study.
#      Employment = unemployed. (study: 2  grant: 1  not grant: 24)
#           Loan: not grant.
#      Employment = retired. (study: 2  grant: 1  not grant: 23)
#           Loan: not grant.
# Income = medium. (grant: 37  not grant: 34  study: 36)
#      Real estate = none. (not grant: 23  grant: 1  study: 14)
#           Employment = official. (study: 6)
#                Loan: study.
#           Employment = employed. (grant: 1  not grant: 1  study: 6)
#                Loan: study.
#           Employment = unemployed. (study: 2  not grant: 13)
#                Loan: not grant.
#           Employment = retired. (not grant: 9)
#                Loan: not grant.
#      Real estate = one. (not grant: 11  study: 22  grant: 1)
#           Products = none. (study: 1  grant: 1  not grant: 7)
#                Loan: not grant.
#           Products = one. (study: 14)
#                Loan: study.
#           Products = more. (not grant: 4  study: 7)
#                Loan: study.
#      Real estate = more. (grant: 35)
#           Loan: grant.
# Income = high. (study: 61  grant: 54)
#      Employment = official. (grant: 26)
#           Loan: grant.
#      Employment = employed. (study: 3  grant: 25)
#           Loan: grant.
#      Employment = unemployed. (grant: 3  study: 29)
#           Loan: study.
#      Employment = retired. (study: 29)
#           Loan: study.




# ---------------------------------------------------------------------------
# SECTION 3: Classifiers
# ---------------------------------------------------------------------------

# In this project, a "classifier" will be a python class with methods for
# learning from examples and for predicting the class of new examples,
# together with other possible methods (like the evaluation of its
# performance). Specifically, a classifier will be a subclass of the following
# generic python class:


class Classifier:
    """
    Base class for classifiers
    """

    def __init__(self, class_name, classes, attributes):
        """
        Constructor.

        Input arguments (see play_tennis.py, for example)

        * class_name: name of the classification attribute
        * classes: list of the different classes
        * attributes: list of pairs of attributes and its values
        """

        self.class_name = class_name
        self.classes = classes
        self.attributes = attributes

    def fit(self, train, valid=None, impurity_func=entropy, max_freq_split=1.0, min_prop_examples=0.0):
        """
        Generic method for learning and tuning the classifier.
        This must be defined for each particular classifier, which may add
        extra input arguments.

        Input arguments:

        * train: examples of the training set
        * valid: examples of the validation set. Some basic classifiers
                 do not use validation sets, so in those cases this argument
                 will be omitted.
        """
        pass

    def predict(self, example):
        """
        Generic method to classify an example, once the classifier have been
        trained. It should be defined for each particular classifier.

        If this method is called without fitting (training) the model
        previously, it has to return an exception ClassifierNotTrained
        (included below).
        """
        pass

    def print_classifier(self):
        """
        Generic method to print the learned classifier. It should be defined
        for each particular classifier.

        If this method is called without fitting (training) the model
        previously, it has to return an exception ClassifierNotTrained
        (included below).
        """
        pass


# Exception returned when the predict or print_classifier methods are called
# without being trained previously.
class ClassifierNotTrained(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
        # # Error, it is not trained yet


# CLASSES TO IMPLEMENT:
# =====================

# * Implement a class Classifier_Tree as a subclass of the class
#   Classifier above, with the following methods:
#   - Train: the learn_tree algorithm implemented in Part I
#   - Classification: predict using the learned tree
#   - Print classifier: print the learned tree
#   In addition to the variable attributes of the parent class Classifier,
#   other attributes can be included if needed (for example, a variable
#   attribute to store the learned tree).
class ClassifierTree(Classifier):
    def __init__(self, class_name, classes, attributes):
        super().__init__(class_name, classes, attributes)
        self.learned_tree = None

    def fit(self, train, valid=None, impurity_func=entropy, max_freq_split=1.0, min_prop_examples=0.0):
        self.learned_tree = learn_tree(train, self.attributes, impurity_func, max_freq_split, min_prop_examples)

    def predict(self, example):
        if not self.learned_tree:
            raise ClassifierNotTrained("Error, it is not trained yet")
        # if type(self.learned_tree) is NodeDT:
        return classify_DT(example, self.learned_tree)

    def print_classifier(self):
        if not self.learned_tree:
            raise ClassifierNotTrained("Error, it is not trained yet")
        print_DT(self.learned_tree, self.attributes, self.class_name)


# * Implement a class ClassifierTreePrune, similar to the previous one, but
#   in which the tree finally used is obtained after applying reduced error
#   pruning on a learned tree.
class ClassifierTreePrune(Classifier):
    def __init__(self, class_name, classes, attributes):
        super().__init__(class_name, classes, attributes)
        self.learned_tree = None

    def fit(self, train, valid=None, impurity_func=entropy, max_freq_split=1.0, min_prop_examples=0.0):
        self.learned_tree = learn_tree(train, self.attributes, impurity_func, max_freq_split, min_prop_examples)
        if valid:
            self.learned_tree = prune_tree(self.learned_tree, valid)

    def predict(self, example):
        if not self.learned_tree:
            raise ClassifierNotTrained("Error, it is not trained yet")
        return classify_DT(example, self.learned_tree)

    def print_classifier(self):
        if not self.learned_tree:
            raise ClassifierNotTrained("Error, it is not trained yet")
        print_DT(self.learned_tree, self.attributes, self.class_name)


# FUNCTION ASKED
# ===============

# * Implement the function "accuracy(classifier,examples)" that computes the
# accuracy of a (trained) classifier on a set of examples whose class is
# known.
def accuracy(classifier, examples):
    if not classifier.learned_tree:
        raise ClassifierNotTrained("Error, it is not trained yet")
    return accuracy_DT(classifier.learned_tree, examples)


# EXPERIMENTATION ASKED
# =====================

# In the case of votes.py and credit.py, compare the accuracy of both
# classifiers (without pruning, with prepruning using several parameters, with
# post pruning, with both...)  on the training, validation and test sets,
# discussing the results obtained.

# Answer:
def Compare(ClassifierTree, ClassifierTreePrune, train, valid, test, name, epsilon=0.15, num_of_test=1,
            impurity_func_name="entropy", impurity_func=entropy, num_of_best=3):
    ClassifierTree.fit(train, impurity_func=impurity_func)
    ClassifierTreePrune.fit(train, valid, impurity_func=impurity_func)
    accuracy_list = []
    max_freq_split = 1.0
    min_prop_examples = 0

    while (num_of_test > 0):
        ClassifierTree.fit(train, max_freq_split=max_freq_split, min_prop_examples=min_prop_examples)
        ClassifierTreePrune.fit(train, valid, max_freq_split=max_freq_split, min_prop_examples=min_prop_examples)
        accuracy_list.append(
            [max_freq_split, min_prop_examples, accuracy(ClassifierTree, test), "without", impurity_func_name])
        accuracy_list.append(
            [max_freq_split, min_prop_examples, accuracy(ClassifierTreePrune, test), "with", impurity_func_name])

        max_freq_split -= epsilon
        min_prop_examples += epsilon
        ClassifierTree.fit(train, max_freq_split=max_freq_split)
        ClassifierTreePrune.fit(train, valid, max_freq_split=max_freq_split)
        accuracy_list.append(
            [max_freq_split, 0, accuracy(ClassifierTree, test), "without", impurity_func_name])
        accuracy_list.append(
            [max_freq_split, 0, accuracy(ClassifierTreePrune, test), "with", impurity_func_name])

        ClassifierTree.fit(train, min_prop_examples=min_prop_examples)
        ClassifierTreePrune.fit(train, valid, min_prop_examples=min_prop_examples)
        accuracy_list.append(
            [1, min_prop_examples, accuracy(ClassifierTree, test), "without", impurity_func_name])
        accuracy_list.append(
            [1, min_prop_examples, accuracy(ClassifierTreePrune, test), "with", impurity_func_name])

        num_of_test -= 1
    for v in accuracy_list:
        print("#the accuray %s %s purnig with fun = %s and max_freq_split = %f , min_prop_examples = %f is %f " % (
            name, v[3], v[4], v[0], v[1], v[2]))
    for i, v in zip(range(num_of_best), sorted(accuracy_list, reverse=True, key=lambda accur: accur[2])):
        print(
            "#the accuray %s %s purnig with fun = %s and max_freq_split = %f , min_prop_examples = %f is %f is Number %d" % (
                name, v[3], v[4], v[0], v[1], v[2], i + 1))


#
#
#
#
#

# classifier_votes = ClassifierTree(votes.class_name, votes.classes, votes.attributes)
# classifier_votes_prune = ClassifierTreePrune(votes.class_name, votes.classes, votes.attributes)

# classifier_credit = ClassifierTree(credit.class_name, credit.classes, credit.attributes)
# classifier_credit_prune = ClassifierTreePrune(credit.class_name, credit.classes, credit.attributes)

# Compare(classifier_votes, classifier_votes_prune, votes.train, votes.valid, votes.test, name="votes")


# check accury for votes on the test
# the accuray votes without purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.000000 is 0.919540
# the accuray votes with purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.000000 is 0.908046
# the accuray votes without purnig with fun = entropy and max_freq_split = 0.850000 , min_prop_examples = 0.000000 is 0.908046
# the accuray votes with purnig with fun = entropy and max_freq_split = 0.850000 , min_prop_examples = 0.000000 is 0.908046
# the accuray votes without purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.150000 is 0.908046
# the accuray votes with purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.150000 is 0.908046
# the accuray votes without purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.000000 is 0.919540 is Number 1
# the accuray votes with purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.000000 is 0.908046 is Number 2
# the accuray votes without purnig with fun = entropy and max_freq_split = 0.850000 , min_prop_examples = 0.000000 is 0.908046 is Number 3

# we can see the best perfome is for not puring and not a early stop and after that all the other is the same

# check accury for votes on the train
# the accuray votes without purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.000000 is 1.000000
# the accuray votes with purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.000000 is 0.964158
# the accuray votes without purnig with fun = entropy and max_freq_split = 0.850000 , min_prop_examples = 0.000000 is 0.971326
# the accuray votes with purnig with fun = entropy and max_freq_split = 0.850000 , min_prop_examples = 0.000000 is 0.964158
# the accuray votes without purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.150000 is 0.964158
# the accuray votes with purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.150000 is 0.964158
# the accuray votes without purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.000000 is 1.000000 is Number 1
# the accuray votes without purnig with fun = entropy and max_freq_split = 0.850000 , min_prop_examples = 0.000000 is 0.971326 is Number 2
# the accuray votes with purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.000000 is 0.964158 is Number 3

# we can see that the accury of the not puring one with no early stop is 1 as expected we can see that early stop give a better perfome on the tarin set then the puring.

# check accury for votes on the valid
# the accuray votes without purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.000000 is 0.942029
# the accuray votes with purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.000000 is 0.985507
# the accuray votes without purnig with fun = entropy and max_freq_split = 0.850000 , min_prop_examples = 0.000000 is 0.985507
# the accuray votes with purnig with fun = entropy and max_freq_split = 0.850000 , min_prop_examples = 0.000000 is 0.985507
# the accuray votes without purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.150000 is 0.985507
# the accuray votes with purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.150000 is 0.985507
# the accuray votes with purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.000000 is 0.985507 is Number 1
# the accuray votes without purnig with fun = entropy and max_freq_split = 0.850000 , min_prop_examples = 0.000000 is 0.985507 is Number 2
# the accuray votes with purnig with fun = entropy and max_freq_split = 0.850000 , min_prop_examples = 0.000000 is 0.985507 is Number 3

# we can see that the perfome of all are the same only the not puring with not early stop give lower perfome on the valid set

# check accury for credit on the test
# the accuray credit without purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.000000 is 0.883436
# the accuray credit with purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.000000 is 0.981595
# the accuray credit without purnig with fun = entropy and max_freq_split = 0.850000 , min_prop_examples = 0.000000 is 0.938650
# the accuray credit with purnig with fun = entropy and max_freq_split = 0.850000 , min_prop_examples = 0.000000 is 0.981595
# the accuray credit without purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.150000 is 0.773006
# the accuray credit with purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.150000 is 0.773006
# the accuray credit with purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.000000 is 0.981595 is Number 1
# the accuray credit with purnig with fun = entropy and max_freq_split = 0.850000 , min_prop_examples = 0.000000 is 0.981595 is Number 2
# the accuray credit without purnig with fun = entropy and max_freq_split = 0.850000 , min_prop_examples = 0.000000 is 0.938650 is Number 3

# we can see the accury of the puring in this case is much better then the other with and without early stop and then early stop give the second best
# perfome the perfome of no early stop and no puring is very low on the testing as expected because is to much close to the tarining set and the worst is early stop using max_freq_split = 1.000000 , min_prop_examples = 0.150000 .

# check accury for credit on the valid
# the accuray credit without purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.000000 is 0.938272
# the accuray credit with purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.000000 is 0.975309
# the accuray credit without purnig with fun = entropy and max_freq_split = 0.850000 , min_prop_examples = 0.000000 is 0.962963
# the accuray credit with purnig with fun = entropy and max_freq_split = 0.850000 , min_prop_examples = 0.000000 is 0.975309
# the accuray credit without purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.150000 is 0.790123
# the accuray credit with purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.150000 is 0.790123
# the accuray credit with purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.000000 is 0.975309 is Number 1
# the accuray credit with purnig with fun = entropy and max_freq_split = 0.850000 , min_prop_examples = 0.000000 is 0.975309 is Number 2
# the accuray credit without purnig with fun = entropy and max_freq_split = 0.850000 , min_prop_examples = 0.000000 is 0.962963 is Number 3

# we can see that the perfome of the puring is the best on the valid with and without early stop and then early stop and then early stop with max_freq_split = 0.850000 , min_prop_examples = 0.000000
# without early stop and puring not achieve a good perfome and the worst is with early stop using  max_freq_split = 1.000000 , min_prop_examples = 0.150000 again

# check accury for credit on the train
# the accuray credit without purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.000000 is 1.000000
# the accuray credit with purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.000000 is 0.926154
# the accuray credit without purnig with fun = entropy and max_freq_split = 0.850000 , min_prop_examples = 0.000000 is 0.956923
# the accuray credit with purnig with fun = entropy and max_freq_split = 0.850000 , min_prop_examples = 0.000000 is 0.926154
# the accuray credit without purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.150000 is 0.806154
# the accuray credit with purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.150000 is 0.806154
# the accuray credit without purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.000000 is 1.000000 is Number 1
# the accuray credit without purnig with fun = entropy and max_freq_split = 0.850000 , min_prop_examples = 0.000000 is 0.956923 is Number 2
# the accuray credit with purnig with fun = entropy and max_freq_split = 1.000000 , min_prop_examples = 0.000000 is 0.926154 is Number 3

# we can see as expected without puring and early stop is 1 and this why is perfome later on the test are not very good
# after that early stop perfome the best and the puring is third and again the worst is the early stop using max_freq_split = 1.000000 , min_prop_examples = 0.150000


# -----------

# Some examples:

# Play tennis:

# >>> classifier_pt=ClassifierTree(play_tennis.class_name,
#                                     play_tennis.classes,
#                                     play_tennis.attributes)
# >>> classifier_pt.predict(['Sunny','Mild', 'High','Strong'])
#                    # Error, it is not trained yet
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "/usr/tmp/python3-33217RM.py", line 761, in predict
# __main__.ClassifierNotTrained

# >>> classifier_pt.fit(play_tennis.train)

# >>> classifier_pt.print_classifier()
# Root node (no: 5  yes: 9)
#  Outlook = Sunny. (no: 3  yes: 2)
#       Humidity = High. (no: 3)
#            Play Tennis: no.
#       Humidity = Normal. (yes: 2)
#            Play Tennis: yes.
#  Outlook = Overcast. (yes: 4)
#       Play Tennis: yes.
#  Outlook = Rainy. (yes: 3  no: 2)
#       Wind = Weak. (yes: 3)
#            Play Tennis: yes.
#       Wind = Strong. (no: 2)
#            Play Tennis: no.

# >>> classifier_pt.predict(['Sunny','Mild', 'High','Strong'])
# 'no'

# >>> accuracy(classifier_pt,play_tennis.train)
# 1.0

# ----------

# Bank credit:

# >>> classifier_ct=ClassifierTree(credit.class_name,credit.classes,
#                                  credit.attributes)
# >>> classifier_ct.fit(credit.train)
# >>> classifier_ct.print_classifier()
# .... very big tree, not displayed ........
# >>> accuracy(classifier_ct,credit.train)
# 1.0
# >>> accuracy(classifier_ct,credit.valid)
# 0.9197530864197531
# >>> accuracy(classifier_ct,credit.test)
# 0.8650306748466258

# -----

# Bank credit with pre and post pruning:

# >>> classifier_ctp=ClassifierTreePrune(credit.class_name,
#                                        credit.classes,
#                                        credit.attributes)
# >>> classifier_ctp.fit(credit.train,credit.valid,
#                        max_freq_split=0.85,min_prop_examples=0.05)
# >>> classifier_ctp.print_classifier()
# Root node (study: 116  not grant: 107  grant: 102)
#  Income = low. (not grant: 73  study: 19  grant: 11)
#       Employment = official. (not grant: 9  study: 8  grant: 9)
#            Real estate = none. (not grant: 9)
#                 Loan: not grant.
#            Real estate = one. (study: 6)
#                 Loan: study.
#            Real estate = more. (study: 2  grant: 9)
#                 Loan: grant.
#       Employment = employed. (not grant: 17  study: 7)
#            Products = none. (not grant: 8)
#                 Loan: not grant.
#            Products = one. (not grant: 9)
#                 Loan: not grant.
#            Products = more. (study: 7)
#                 Loan: study.
#       Employment = unemployed. (study: 2  grant: 1  not grant: 24)
#            Loan: not grant.
#       Employment = retired. (study: 2  grant: 1  not grant: 23)
#            Loan: not grant.
#  Income = medium. (grant: 37  not grant: 34  study: 36)
#       Real estate = none. (not grant: 23  grant: 1  study: 14)
#            Employment = official. (study: 6)
#                 Loan: study.
#            Employment = employed. (grant: 1  not grant: 1  study: 6)
#                 Loan: study.
#            Employment = unemployed. (study: 2  not grant: 13)
#                 Loan: not grant.
#            Employment = retired. (not grant: 9)
#                 Loan: not grant.
#       Real estate = one. (not grant: 11  study: 22  grant: 1)
#            Products = none. (study: 1  grant: 1  not grant: 7)
#                 Loan: not grant.
#            Products = one. (study: 14)
#                 Loan: study.
#            Products = more. (not grant: 4  study: 7)
#                 Loan: study.
#       Real estate = more. (grant: 35)
#            Loan: grant.
#  Income = high. (study: 61  grant: 54)
#       Employment = official. (grant: 26)
#            Loan: grant.
#       Employment = employed. (study: 3  grant: 25)
#            Loan: grant.
#       Employment = unemployed. (grant: 3  study: 29)
#            Loan: study.
#       Employment = retired. (study: 29)
#            Loan: study.

# >>> accuracy(classifier_ctp,credit.train)
# 0.9261538461538461
# >>> accuracy(classifier_ctp,credit.valid)
# 0.9753086419753086
# >>> accuracy(classifier_ctp,credit.test)
# 0.9815950920245399


# ---------------------------------------------------------------------------
# SECTION 4: Explaining survival in the Titanic
# ---------------------------------------------------------------------------

# In this part, you will have to use some of previous classifiers for
# explaining the reasons for survival in the Titanic sinking, from the
# available data about the passengers (downloadable from links in the web
# page).


# For that, you should do the following steps:

# - Data preprocessing: we have "raw data", so they have to be prepared to be
#   input for our classifiers.
# - Learning and tuning the learned model, using the corresponding classifier
#   method.
# - Evaluating the learned classifier


# We now give some suggestions for the first step (preprocessing):

# In the data set provided there are a number of attributes that obviously
# have no influence on survival (for example, the name of the passenger). This
# makes necessary to select as attributes the features that are actually
# believed relevant. This is usually done using some statistical techniques,
# but in this assignment only we are going to ask you to manually choose(in a
# reasonable way, or by testing several alternatives) THREE ATTRIBUTES that
# are considered to be the ones that best determine survival or not.


# The "Age" attribute is numeric, and our implementation does not treat well
# attributes with numerical values. There are techniques for treating
# numerical attributes, which basically divide the possible values to be taken
# into intervals, in the best possible way. In our case, for the sake of
# simplification, we will do it directly with the following criteria:
# transform the AGE value into a binary value, in which we only annotate if
# the passenger is 13 YEARS OLD OR YOUNGER, or if the passenger is OLDER than
# 13.


# In the data, there are some values from some examples, which appear as NA
# (unknown). Two very simple techniques for treating missing or unknown
# values: replace NA by the most frequent value in examples of the
# same class, or by the arithmetic mean of that value in the class (this last
# option only makes sense with numeric attributes).

# To carry out training, pruning and performance measurement,you need to split
# the data into three parts: training, validation and testing. It is necessary
# to decide on the appropriate proportion of the data for each of these three
# parts. In addition, care has also to be taken to ensure that the partition
# is stratified: the proportion of examples according to the different values
# of the attributes must be in each part similar to the proportion in the
# whole set of examples.


# The final result of this last section should be:

# * A file titanic.py, with a format similar to the data files that has been
# provided (votes.py or credit.py, for example), in which we include the data
# resulted obtained after the preprocessing phase.

# * A decision tree (the one obtained with the best performance), explaining
# survival in the Titanic sinking. Include comments explaining all the steps
# and experimentations carried out until this final tree has been
# obtained. Include the printed tree and the coments also in the file
# titanic.py


# ------------------------------------
# Answer:
# ------------------------------------
# After processing the text file and transferring it to variables (attributes, train, valid, test),
#  we took All three subset from attributes, and possibilities seemed relevant to us
# We then calculated the accuracy of each classifier and hence we came to the conclusion that the best
#  accuracy for TEST is the variables with trying different pruning:
# We foung that the best 3 attributes are 'pclass', 'age' and 'sex\n'.
# About the decision tree that fit to those training set and pruning
# from the algorithm ID3, first it divide by gender for male and female its
# return the most frequent class, and for the one with no information
# its divide by sub-tree first by age and than by class-room.

# The decision tree:
# ------------------------------------
# Root node (survived: 235  not survived: 465)
#  sex = male. (survived: 82  not survived: 382)
#       age = Young. (survived: 13  not survived: 3)
#            pclass = 3rd. (survived: 5  not survived: 3)
#                 Titanic: survived.
#            pclass = 1st. (No examples)
#                 Titanic: survived.
#            pclass = 2nd. (survived: 8)
#                 Titanic: survived.
#       age = Old. (survived: 69  not survived: 379)
#            pclass = 3rd. (survived: 30  not survived: 234)
#                 Titanic: not survived.
#            pclass = 1st. (survived: 30  not survived: 60)
#                 Titanic: not survived.
#            pclass = 2nd. (survived: 9  not survived: 85)
#                 Titanic: not survived.
#  sex = female. (survived: 153  not survived: 83)
#       pclass = 3rd. (survived: 37  not survived: 70)
#            age = Young. (not survived: 5)
#                 Titanic: not survived.
#            age = Old. (survived: 37  not survived: 65)
#                 Titanic: not survived.
#       pclass = 1st. (survived: 64  not survived: 5)
#            age = Young. (not survived: 1)
#                 Titanic: not survived.
#            age = Old. (survived: 64  not survived: 4)
#                 Titanic: survived.
#       pclass = 2nd. (survived: 52  not survived: 8)
#            age = Young. (survived: 5)
#                 Titanic: survived.
#            age = Old. (survived: 47  not survived: 8)
#                 Titanic: survived.
# ------------------------------------


# The classifier titanic tree class:
# classifier_titanic = ClassifierTree(titanic.class_name,
#                                          titanic.classes,
#                                               titanic.attributes)
# classifier_titanic.fit(titanic.train, titanic.valid, max_freq_split=0.85, min_prop_examples=0.05)


# >>> accuracy(classifier_titanic, titanic.train)
#  0.8271428571428572
# >>> accuracy(classifier_titanic, titanic.valid)
# 0.8033333333333333
# >>> accuracy(classifier_titanic, titanic.test)
# 0.842948717948718
# ------------------------------------
# End of project
# ------------------------------------

def getRandomExamples(examples, numberOfTrain, numOfValid, first, second, third):
    random.shuffle(examples)
    train = get_3_col(examples[0:numberOfTrain], first, second, third)
    valid = get_3_col(examples[numberOfTrain:numOfValid], first, second, third)
    test = get_3_col(examples[numOfValid:-1], first, second, third)
    return (train, valid, test)


def get_3_col(train, first, second, third, last=True):
    if first > 10 or second > 10 or third > 10:
        print("error with num")
        return
    new_train = []
    if last:
        for row in train:
            new_train.append([row[first], row[second], row[third], row[-1]])
    else:
        new_train = [train[first], train[second], train[third]]
    return new_train


def read_file(file):
    f = open(file, 'r')

    attributes_from_text_line = f.readline().replace('"', '').replace('\n', "").split(',')
    attributes_from_text = []
    for i, attribute in enumerate(attributes_from_text_line):
        if i != 2:
            attributes_from_text.append(attribute)
    attributes_from_text.append(attributes_from_text_line[2])
    print(attributes_from_text)

    examples_from_text = []

    for line in f:
        line = line.replace('", ', '",').replace(", ", "").replace('\n', "").replace('""', "none") \
            .replace('" "', "None").replace("''", "None").replace('"', '')
        examples_from_text.append(line.split(','))

    examples = []
    for example in examples_from_text:
        add_example_i = []
        for index, example_i in enumerate(example):
            # If attribute == age
            if index == 4:
                if example_i == "NA":
                    add_example_i.append("Old")
                elif float(example_i) <= 13:
                    add_example_i.append("Young")
                else:
                    add_example_i.append("Old")
            # If attribute != survived
            elif index != 2:
                add_example_i.append(example_i)
        # If attribute == survived
        if example[2] == '0':
            add_example_i.append('not survived')
        else:
            add_example_i.append('survived')
        examples.append(add_example_i)
    for example in examples:
        if len(example) != 11:
            print(example)
    f.close()

    first = 9
    second = 1
    third = 3

    (train, valid, test) = getRandomExamples(examples, 700, 1000, first, second, third)
    attributes_from_text = get_3_col(attributes_from_text, first, second, third, False)

    clas_constents = {}
    for index, attribute in enumerate(attributes_from_text):
        clas_constents[attribute] = set(example[index] for example in train)

    attributes = []
    for clas_constent in clas_constents:
        if clas_constent != 'survived':
            attributes.append((clas_constent, list(clas_constents[clas_constent])))

    class_name = "Titanic"

    classes = ['survived', 'not survived']

    # -------------------------------------------------------------------
    # Do not change it!!! this part responsible for create new titanic.py
    # -------------------------------------------------------------------
    # f = open('titanic.py', 'w')
    # f.write("\n\n\nattributes = {}".format(attributes))
    # f.write("\n\n\nclass_name = \"{}\"".format(class_name))
    # f.write("\n\n\nclasses = {}".format(classes))
    # f.write("\n\n\ntrain = {}".format(train))
    # f.write("\n\n\nvalid = {}".format(valid))
    # f.write("\n\n\ntest = {}".format(test))
    # -------------------------------------------------------------------

    classifier_titanic = ClassifierTreePrune(class_name,
                                             classes,
                                             attributes)

    classifier_titanic = ClassifierTree(class_name,
                                        classes,
                                        attributes)
    classifier_titanic.fit(train)

    return classifier_titanic


def classifier_titanic():
    # read_file('titanic.txt')

    classifier_titanic = ClassifierTree(titanic.class_name,
                                        titanic.classes,
                                        titanic.attributes)
    classifier_titanic.fit(titanic.train, titanic.valid, max_freq_split=0.85, min_prop_examples=0.05)


    classifier_titanic.print_classifier()
    print(accuracy(classifier_titanic, titanic.train))
    print(accuracy(classifier_titanic, titanic.valid))
    print(accuracy(classifier_titanic, titanic.test))


def tests():
    pt_tree = learn_tree(play_tennis.train, play_tennis.attributes)
    if pt_tree.branches["Rainy"].branches["Strong"].clas != 'no':
        print(1, pt_tree.branches["Rainy"].branches["Strong"].clas)
    if pt_tree.branches["Rainy"].branches["Weak"].clas != 'yes':
        print(2, pt_tree.branches["Rainy"].branches["Weak"].clas)
    if classify_DT(["Sunny", "Mild", "High", "Strong"], pt_tree) != 'no':
        print(3, classify_DT(["Sunny", "Mild", "High", "Strong"], pt_tree))
    if classify_DT(["Rainy", "Mild", "High", "Weak"], pt_tree) != 'yes':
        print(4, classify_DT(["Rainy", "Mild", "High", "Weak"], pt_tree))
    if (accuracy_DT(pt_tree, play_tennis.train) != 1.0):
        print(5, accuracy_DT(pt_tree, play_tennis.train))
    cl_tree = learn_tree(contact_lenses.train, contact_lenses.attributes)
    if (classify_DT(["Pre-presbyopic", "Hypermetrope", "-", "Normal"], cl_tree) != 'Soft'):
        print(6, classify_DT(["Pre-presbyopic", "Hypermetrope", "-", "Normal"], cl_tree))
    if (accuracy_DT(cl_tree, contact_lenses.train) != 1.0):
        print(7, accuracy_DT(cl_tree, contact_lenses.train))
    cl_tree_2 = learn_tree(contact_lenses.train, contact_lenses.attributes,
                           impurity_func=gini,
                           max_freq_split=0.75,
                           min_prop_examples=0.15)
    if classify_DT(["Pre-presbyopic", "Hypermetrope", "-", "Normal"], cl_tree_2) != 'Soft':
        print(8, classify_DT(["Pre-presbyopic", "Hypermetrope", "-", "Normal"], cl_tree_2))
    if accuracy_DT(cl_tree_2, contact_lenses.train) != 0.9166666666666666:
        print(accuracy_DT(cl_tree_2, contact_lenses.train))

    votes_tree = learn_tree(votes.train, votes.attributes)

    if (accuracy_DT(votes_tree, votes.train) != 1.0):
        print(9, accuracy_DT(votes_tree, votes.train))
    if accuracy_DT(votes_tree, votes.valid) != 0.9420289855072463:
        accuracy_DT(10, votes_tree, votes.valid)
    if accuracy_DT(votes_tree, votes.test) != 0.9195402298850575:
        print(11, accuracy_DT(votes_tree, votes.test))
    votes_tree_2 = learn_tree(votes.train, votes.attributes,
                              max_freq_split=0.95,
                              impurity_func=gini,
                              min_prop_examples=0.05)
    if accuracy_DT(votes_tree_2, votes.train) != 0.974910394265233:
        print(12, accuracy_DT(votes_tree_2, votes.train))
    if accuracy_DT(votes_tree_2, votes.valid) != 0.9565217391304348:
        print(13, accuracy_DT(votes_tree_2, votes.valid))
    if accuracy_DT(votes_tree_2, votes.test) != 0.9195402298850575:
        print(14, accuracy_DT(votes_tree_2, votes.test))

    # Bank credit:
    ct_tree = learn_tree(credit.train, credit.attributes)
    if accuracy_DT(ct_tree, credit.train) != 1.0:
        print(14, accuracy_DT(ct_tree, credit.train))
    epsilon = 0.1
    if 0.9197530864197531 + epsilon <= accuracy_DT(ct_tree, credit.valid) and accuracy_DT(ct_tree,
                                                                                          credit.valid) <= 0.9197530864197531 - epsilon:
        print(15, accuracy_DT(ct_tree, credit.valid))
    if 0.8650306748466258 + epsilon <= accuracy_DT(ct_tree, credit.test) and accuracy_DT(ct_tree,
                                                                                         credit.test) <= 0.8650306748466258 - epsilon:
        print(16, accuracy_DT(ct_tree, credit.test))

    ct_tree_2 = learn_tree(credit.train, credit.attributes,
                           max_freq_split=0.75,
                           min_prop_examples=0.1)

    if accuracy_DT(ct_tree_2, credit.train) != 0.8584615384615385:
        print(17, accuracy_DT(ct_tree_2, credit.train))
    if accuracy_DT(ct_tree_2, credit.valid) <= 0.9012345679012346 - 3 * epsilon:
        print(18, accuracy_DT(ct_tree_2, credit.valid))
    if accuracy_DT(ct_tree_2, credit.test) <= 0.8834355828220859 - epsilon:
        print(19, accuracy_DT(ct_tree_2, credit.test))
    if inner_nodes_DT(pt_tree) != [[], ['Sunny'], ['Rainy']]:
        print(20, inner_nodes_DT(pt_tree))

    votes_pruned = prune_tree(votes_tree, votes.valid)
    # print_DT(votes_pruned, votes.attributes, votes.class_name)

    # Play tennis:
    classifier_pt = ClassifierTree(play_tennis.class_name,
                                   play_tennis.classes,
                                   play_tennis.attributes)
    classifier_pt.fit(play_tennis.train)

    if classifier_pt.predict(['Sunny', 'Mild', 'High', 'Strong']) != 'no':
        print(21, classifier_pt.predict(['Sunny', 'Mild', 'High', 'Strong']))
    if accuracy(classifier_pt, play_tennis.train) != 1.0:
        print(22, accuracy(classifier_pt, play_tennis.train))

    # Bank credit:

    # Bank credit with pre and post pruning:
    classifier_ctp = ClassifierTreePrune(credit.class_name,
                                         credit.classes,
                                         credit.attributes)
    classifier_ctp.fit(credit.train, credit.valid,
                       max_freq_split=0.85, min_prop_examples=0.05)
    if accuracy(classifier_ctp, credit.train) != 0.9261538461538461:
        print(23, accuracy(classifier_ctp, credit.train))
    if accuracy(classifier_ctp, credit.valid) != 0.9753086419753086:
        print(24, accuracy(classifier_ctp, credit.valid))
    if accuracy(classifier_ctp, credit.test) != 0.9815950920245399:
        print(25, accuracy(classifier_ctp, credit.test))

def main():
    print("project")
    print()

if __name__ == '__main__':
    main()