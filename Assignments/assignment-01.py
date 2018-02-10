# ==========================================================
# Artificial Intelligence.  ETSII (University of Seville).
# Course 2017-18
# Deliverable 01
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




# -----------------------------------------------------------------------------
# EXERCISE 1)

# Suppose we have a text file containing an ASCII representation of different
# digits written by hand. The digits.txt file provided is an example of this
# type of file, with 300 digit images written by hand.  We'll assume that each
# digit is represented by a 28x28 pixel image, where each pixel is represented
# by a character ("#" for a black pixel where the stroke has passed, " " for
# blank pixels)

# Define a function:

# print_least_used_pixels(file,n)

# to print on screen a 28x28 image, in which the pixels where the stroke has
# passed less than n times (taking into account all the images of the file)
# are marked with a "*". That is to say, in the image that has to be printed,
# we will write a "*" only on those pixel positions for which there are
# fewer than n images in the file, whose stroke passes through that pixel.


# For example:

# >>> print_least_used_pixels("digits.txt",5)
# ****************************
# ****************************
# **********    **************
# *********            *******
# *******               ******
# ******                   ***
# ****                     ***
# ****                     ***
# ****                     ***
# ****                     ***
# ****                     ***
# ****                     ***
# ****                     ***
# ****                     ***
# ****                     ***
# *****                    ***
# ****                     ***
# *****                    ***
# *****                    ***
# *****                    ***
# *****                    ***
# *****                   ****
# *****                  *****
# ******                ******
# *******               ******
# ********            ********
# ************      **********
# ****************************

# >>> print_least_used_pixels("digits.txt",150)
# ****************************
# ****************************
# ****************************
# ****************************
# ****************************
# ****************************
# ************      **********
# ***********        *********
# **********         *********
# **********   **    *********
# ********** *****   *********
# ****************  **********
# ***************   **********
# *************     **********
# ***********       **********
# ************      **********
# ************       *********
# *************     **********
# **************    **********
# **************    **********
# *************     **********
# ************      **********
# ************     ***********
# *************   ************
# ****************************
# ****************************
# ****************************
# ****************************
import array


def print_least_used_pixels(file, n):
    f = open(file, 'r')
    my_2_dim = [[0 for i in range(28)] for j in range(28)]

    while True:
        for row in range(28):
            line = f.readline()
            if not line.__len__() == 29:
                break
            for column in range(28):
                character = line[column]
                if not character == " ":
                    my_2_dim[row][column] += 1
        if not line.__len__() == 29:
            break

    for line in my_2_dim:
        for character in line:
            print(" ", end="") if character >= n else print("*", end="")
        print()

    f.close()


# -----------------------------------------------------------------------------
# EJERCICIO 2)

# Suppose our department has bought a new computer that we're going to use as
# a server for practices. For that reason, we need to register the students as
# users of that server. To this end, we have to automatically generate a
# username for each student, based on his/her name and surnames (they are
# spanish students, so they have two surnames).


# Define a function auto_usernames(file) such that receiving as input the name
# of a file containing the data of each user, it prints out a listing of them in
# alphabetical order of surnames, along with the automatically generated
# username.


# For example, applying the function auto_usernames to the file nombres.txt
# provided, the following lines has to be printed:

# >>> imprime_usuarios("nombres.txt")
#
# DNI      Surnames                       Name            User
# -------- ------------------------------ --------------- --------
# 67834547 Abad Garcia                    Maria Jose      mjabagar
# 87452221 Fernandez Lopera               Maria           mferlop1
# 76865412 Fernandez Lopez                Mario           mferlop
# 36638712 Gomariz Gonzaga                Amador          agomgon1
# 12987534 Gomez Gonzalez                 Alicia          agomgon
# 21783647 Gonzalez Echevarri             Antonia Maria   amgonech
# 87654321 Luna Espejo                    Emilio          elunesp
# 78988851 Mencheta Ruiz                  Javier Liborio  jlmenrui2
# 88734412 Mencheta Ruiz                  Jose Luis       jlmenrui1
# 22426553 Menendez Ruiz                  Juan            jmenrui
# 23823472 Mensaque Ruibarros             Juan Luis       jlmenrui
# 63555789 Muela Garcia                   Lidia           lmuegar
# 73535787 Navas Suarez                   Rocio           rnavsua
# 73163633 Perez Posada                   Manuel Jose     mjperpos
# 73263638 Poza Ramirez                   Isabel          ipozram
# 73276362 Rodicio Martinez               Antonio Manuel  amrodmar1
# 12326523 Rodriguez Marquez              Antonio Manuel  amrodmar
# 34551211 Sanchez Sanchez                Fermin Jose     fjsansan
# 78363677 Sanchez Santaella              Enrique Manuel  emsansan
# 21334456 Torres Chacon                  Eduardo         etorcha


# The input file has a sequence of lines of the form:
# ID:Name1:Name2:Surname1:Surname2
# or (for students who do not have a compound name):
# ID:Name::Surname1:Surname2

# As shown in the above example, each student's user name is generated by the
# following rule: initial of the first name, initial of the middle name (if
# any), the first three letters of the first surname and the first three
# letters of the second surname, all in lowercase. If under this rule there
# are several students with the same username, they have to be distinguished
# by successive numerical indexes that are added at the end.


# Note that if a line in the file does not have the above format, you should
# ignore it


# HINTS:
# - The methods "split" and "lower" of the string class may be useful.
# - When reading each line of the input file, the last character will be "\n"
#   (newline). If we have a string s, then s[:-1] is the same string but
#   without the last character.
# - To sort the lines in alphabetical order, it may be useful the "sort"
#   method of the list class, with an appropriate "key=..." parameter.
# - The lines in the example above has been printed using the following
#   formatting string:  "{0:>8} {1:<30} {2:<15} {3}"


# ----------------------------------------------------------------------------------

def auto_usernames(file):
    f = open(file, 'r')
    lst_name = []

    for line in f.readlines():
        row = line.split(":")
        if row.__len__() == 5 and (row[0]!= ""and row[1]!= ""  and row[3]!= "" and row[4]!= "" ):
            row[4] = row[4].strip()
            user = (row[1][:1] + row[2][:1] + row[3][:3] + row[4][:3]).lower()
            counter = 0
            search = user
            while any(arr[5] == search for arr in lst_name):
                counter += 1
                search = user + "{}".format(counter)

            row.insert(5, user) if counter == 0 else row.insert(5, user + "{}".format(counter))
            lst_name.append(row)

    print("DNI      Surnames                       Name            User")
    print("-------- ------------------------------ --------------- --------")

    for data in sorted(lst_name, key=lambda x: (x[3], x[4], x[1])):
        print("{0:>8} {1:<30} {2:<15} {3}".format(data[0], data[3] + " " + data[4], data[1] + " " + data[2],
                                                  data[5]))

    f.close()
# ===================================

# End of file
