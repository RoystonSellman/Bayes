#-------------------------------------------------------------------------------
# Name:        entropy
# Purpose:
# Version 1.01
#
# Author:      JdP
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import collections
import math
import string

# HX = HX + Px * math.log(1.0/Px, 2)
# is equivalent to
# HX = HX - Px * math.log(Px, 2)
# The latter, more efficient form is used.


def EntropyFromProbabilityDistribution(distribution):

    """Calculate the entropy of the passed list of probabilities.

    distribution is an iterable list of probabilities.
    All values should be positive.
    The sum of the probabilities should be equal to 1.0 to 3 decimal places
    This function returns the entropy (HX) as a number of bits to 3 sig figs.

    The error return is -1"""

    if not type(distribution) is list:
        HX = -1

    # Check the sum of probabilies is 1.0
    elif (round(sum(distribution),3) != 1.0):
        HX = -1

    # Check for negative probabilities
    elif (min(distribution) < 0.0):
        HX = -1

    else:
        HX = 0

        for i in range(0, len(distribution)):
            Px = distribution[i]

            if (Px > 0):
                HX = HX - Px * math.log(Px, 2)

    return (HX)


def EntropyFromFrequencyDistribution(distribution):

    """Calculate the entropy of the passed list of frequencies.

    distribution is an iterable list of frequencies.
    This function returns the entropy (HX) as a number of bits to 3 sig figs.

    The error return is -1"""

    if not type(distribution) is list:
        HX = -1

    elif len(distribution) < 1:
        HX = -1

    elif (min(distribution) < 0.0):
        HX = -1

    else:
        total_frequency = sum(distribution)

        HX = 0

        for i in range(0, len(distribution)):
            Px = float(distribution[i]) / total_frequency

            if (Px > 0.0):
                HX = HX - Px * math.log(Px, 2)

    return (HX)


def EntropyFromSampleDistribution(distribution):

    """Calculate the entropy of the passed list of sample outcomes.

    distribution is an iterable list of outcomes/values/items/states/etc.
    e.g     [1,2,5,2,2,1,4,4,2,2,2,2]
            ["A","B","C","B","B","A","D","D","B","B","B","B"]
            ["H","T","H","T",,"H","H","H","H","H"]
    This function returns the entropy (HX) as a number of bits to 3 sig figs.

    The error return is -1"""

    if not type(distribution) is list:
        HX = -1

    elif len(distribution) < 1:
        HX = -1

    else:
        sample_size = len (distribution)

        HX = 0

        for frequency in collections.Counter(sorted(distribution)).values():
            Px = float(frequency)/sample_size

            if (Px > 0.0):
                HX = HX - Px * math.log(Px, 2)

    return (HX)

def EntropyHXFromFrequencyDistribution(distribution, rows):

    """returns HX = entropy of the row totals

    distribution is an iterable list of frequencies and rows is the
    number of rows in the data.  If the list comprises N values, then
    N = rows x columns.
    The error return is both set to -1"""


    HX = -1

    rows = max(rows, 1)
    columns = int(len(distribution) / rows)

    # check that rows is a factor of the size of the distribution - ensures
    # we have a proper AxB matrix with integer numbers of rows and columns
    if (columns * rows == len(distribution)):

        listx = []

        for row in range(0, rows):
            listx.append(0)
            for col in range(0, columns):
                listx[row] = listx[row] + distribution[row * columns + col]

        HX = EntropyFromFrequencyDistribution(listx)

    return (HX)

def EntropyHYFromFrequencyDistribution(distribution, rows):

    """returns HY = entropy of the column totals

    distribution is an iterable list of frequencies and rows is the
    number of rows in the data.  If the list comprises N values, then
    N = rows x columns.
    The error return is both set to -1"""

    HY = -1

    rows = max(rows, 1)
    columns = int(len(distribution) / rows)

    # check that rows is a factor of the size of the distribution - ensures
    # we have a proper AxB matrix with integer numbers of rows and columns
    if (columns * rows == len(distribution)):

        listy = []

        for col in range(0, columns):
            listy.append(0)
            for row in range(0, rows):
                listy[col] = listy[col] + distribution[row * columns + col]

            HY = EntropyFromFrequencyDistribution(listy)

    return (HY)

def EntropyValuesFromFrequencyDistribution(distribution, rows):

    """returns a six DICTIONARY with keys HX, HY, HXY, HXgY, HYgX, IXY
    HXY = joint entropy
    HX = entropy of the row totals
    HY = entropy of the column totals
    HX|Y = conditional entropy of X given Y
    HY|X = conditional entropy of Y given X
    IXY = mutual information

    distribution is an iterable list of frequencies and rows is the
    number of rows in the data.  If the list comprises N values, then
    N = rows x columns.
    The error return is both set to -1"""


    HXgY = -1
    HYgX = -1
    IXY = -1

    HXY = EntropyFromFrequencyDistribution(distribution)

    HX = EntropyHXFromFrequencyDistribution(distribution, rows)
    if (HX != -1):
        HYgX = HXY - HX

    HY = EntropyHYFromFrequencyDistribution(distribution, rows)
    if (HY != -1):
        HXgY = HXY - HY

    if (HX !=-1) and (HY != -1) and (HXY !=-1):
        IXY = HX + HY - HXY

    HXY = RoundSF(HXY, 3)
    HX = RoundSF(HX, 3)
    HY = RoundSF(HY, 3)
    HXgY = RoundSF(HXgY, 3)
    HYgX = RoundSF(HYgX, 3)
    IXY = RoundSF(IXY, 3)

    rc = {'HXY': HXY, 'HX': HX, 'HY': HY, 'HX|Y': HXgY, 'HY|X': HYgX, 'IXY': IXY}
    return (rc)

def RoundSF(num, sigfigs):

    """Round to specified number of sigfigs."""

    if num == 0:
        return (0)

    rc = round(num, -int(math.floor(math.log(abs(num), 10)) - (sigfigs - 1)))

    return (rc)


def CheckResult (result, target, sigfigs=3):

    rc = RoundSF(result, sigfigs)

    if rc == target:
        print ("OK", rc)
    else:
        print ("FAIL->", rc, " target->", target)


# Test data for the above two functions
# The more test data, the more testing gets done.

# Entropy of  fair 8 sided die is 3 bits
# Two added 0.0 values ended to check that they are skipped over
distribution = [0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.125,0.0,0.0]
HX = EntropyFromProbabilityDistribution(distribution)
CheckResult(HX, 3.0)

# Entropy of  fair 6 sided die is 3 bits
distribution = [0.16667,0.16667,0.16667,0.16667,0.16667,0.16667]
HX = EntropyFromProbabilityDistribution(distribution)
CheckResult(HX, 2.58)

# Entropy (4.33, P81)
distribution = [0.125,0.375,0.375,0.125]
HX = EntropyFromProbabilityDistribution(distribution)
CheckResult(HX, 1.81)

# Entropy (4.36, P82)
distribution = [0.227,0.273,0.273,0.227]
HX = EntropyFromProbabilityDistribution(distribution)
CheckResult(HX, 1.99)

# Entropy PDF Eq 4.37 P82 based on table 4.1
distribution = [2.0/128,15.0/128,12.0/128,10.0/128,21.0/128,4.0/128,4.0/128,
            21.0/128,10.0/128,12.0/128,15.0/128,2.0/128]
HX = EntropyFromProbabilityDistribution(distribution)
CheckResult(HX, 3.30)

# Entropy P85
distribution = [0.276,0.724]
HX = EntropyFromProbabilityDistribution(distribution)
CheckResult(HX, 0.85)

# Entropy P79
distribution = [0.322,0.678]
HX = EntropyFromProbabilityDistribution(distribution)
CheckResult(HX, 0.907)

# Entropy Table 4.2 Eq 4.6 P82
distribution = [0.651,0.072,0.028,0.249]
HX = EntropyFromProbabilityDistribution(distribution)
CheckResult(HX, 1.32)

distribution = [1,2,5,2,2,1,4,4,2,2,2,2]
HX = EntropyFromSampleDistribution(distribution)
CheckResult(HX, 1.61)

distribution = ["A","B","C","B","B","A","D","D","B","B","B","B"]
HX = EntropyFromSampleDistribution(distribution)
CheckResult(HX, 1.61)

distribution = ["H","T","H","T","H","H","H","H","H"]
HX = EntropyFromSampleDistribution(distribution)
CheckResult(HX, 0.764)

# Entropy of two fair 6 sided dice
distribution = [2,3,3,4,4,4,5,5,5,5,6,6,6,6,6,7,7,7,7,7,7,
              8,8,8,8,8,9,9,9,9,10,10,10,11,11,12]
HX = EntropyFromSampleDistribution(distribution)
CheckResult(HX, 3.27)

# Entropy PDF Eq 4.37 P82 based on table 4.1 - try as a sample
distribution = [1,1,
            2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
            3,3,3,3,3,3,3,3,3,3,3,3,
            4,4,4,4,4,4,4,4,4,4,
            5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,
            6,6,6,6,
            7,7,7,7,
            8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,
            9,9,9,9,9,9,9,9,9,9,
            0,0,0,0,0,0,0,0,0,0,0,0,
            11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,
            12,12]
HX = EntropyFromSampleDistribution(distribution)
CheckResult(HX, 3.30)

distribution = [651,73,28,249]
HX = EntropyFromFrequencyDistribution(distribution)
CheckResult(HX, 1.32)

distribution = [724,277]
HX = EntropyFromFrequencyDistribution(distribution)
CheckResult(HX, 0.851)

distribution = [29,35,35,29]
HX = EntropyFromFrequencyDistribution(distribution)
CheckResult(HX, 1.99)

distribution = [16,48,48,16]
HX = EntropyFromFrequencyDistribution(distribution)
CheckResult(HX, 1.81)

# Table 4.1 on P73
distribution = [0, 2, 15, 12, 0, 10, 21, 4, 4, 21, 10, 0, 12, 15, 2, 0]
rc = EntropyValuesFromFrequencyDistribution(distribution, 4)
print(rc)

# Table 4.1 on P73
distribution = [0, 2, 15, 12, 0, 10, 21, 4, 4, 21, 10, 0, 12, 15, 2, 0]
HX = EntropyHXFromFrequencyDistribution(distribution, 4)
print('HX=', RoundSF(HX, 3))

# Table 4.1 on P73
distribution = [0, 2, 15, 12, 0, 10, 21, 4, 4, 21, 10, 0, 12, 15, 2, 0]
HY = EntropyHYFromFrequencyDistribution(distribution, 4)
print('HY=', RoundSF(HY, 3))

# Entropy PDF Eq 4.37 P82 based on table 4.1
distribution = [0, 2, 15, 12, 0, 10, 21, 4, 4, 21, 10, 0, 12, 15, 2, 0]
HXY = EntropyFromFrequencyDistribution(distribution)
CheckResult(HXY, 3.30)

print('HY|X=', RoundSF(HXY - HX, 3))
print('HX|Y=', RoundSF(HXY - HY, 3))
print('IXY=', RoundSF(HX + HY - HXY, 3))

# Table 4.2 on P85
distribution = [651,73,28,249]
rc = EntropyValuesFromFrequencyDistribution(distribution, 2)
print(rc)

# Table 4.2 on P85
distribution = [651,73,28,249]
HY = EntropyHYFromFrequencyDistribution(distribution, 2)
print('HY=', RoundSF(HY, 3))

# Table 4.2 on P85
distribution = [651,73,28,249]
HX = EntropyHXFromFrequencyDistribution(distribution, 2)
print('HX=', RoundSF(HX, 3))

# Table 4.2 on P85
distribution = [651,73,28,249]
HXY = EntropyFromFrequencyDistribution(distribution)
CheckResult(HXY, 1.32)

print('HY|X=', RoundSF(HXY - HX, 3))
print('HX|Y=', RoundSF(HXY - HY, 3))
print('IXY=', RoundSF(HX + HY - HXY, 3))

listx = []

with open("data_xx.txt") as f:
    for line in f:
        for word in str.split(line):
            listx.append(word)

HX = EntropyFromSampleDistribution(listx)
print(HX)

listy = []

with open("data_yy.txt") as f:
    for line in f:
        for word in str.split(line):
            listy.append(word)

HX = EntropyFromSampleDistribution(listy)
print(HX)
