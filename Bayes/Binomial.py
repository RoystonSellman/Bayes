# Set encoding, this needs to be first line in file, see http://www.python.org/dev/peps/pep-0263/
# -*- coding: utf-8 -*-
"""
File: BayesRulePythonBinomial_v1.py, by Royston Sellman (with tweeks by JV Stone).
Python code to accompany book: Bayes' Rule: A Tutorial Introduction Introduction by JV Stone, 2013.
    Overview: The code plots graphs like those in Figure 4.7, which show the probability of head outcomes as a function of coin bias b.
    For each value of coin bias b (the probability of a head), and for each of a different number of coin flips, 
    we generate a data set x. We then count the number of heads nh and tails nt in x. 
    We then compute the probability of x for each value of b in a range of putative bias values, which yields a likelihood function.
    We multiply each value in the likelihood function by a corresponding value in the prior distribution to obtain a posterior distribution.
    The prior can be either uniform or binomial, according to the set value of the boolean variable useuniformprior.
This code can be downloaded from http://jim-stone.staff.shef.ac.uk/BayesBook/Python.
The code below is compatible with Python version 2.7. 
Copyright: 2014, JV Stone, Psychology Department, Sheffield University, Sheffield, England.
Date: 12 January 2014.
"""
# Import required modules.
from numpy import random, linspace
import matplotlib.pyplot as plt

# set random number seed
random.seed(99)

# Constants
theta = u'\u03b8'  # define string for theta, used in graph labels below

# Make vector of possible coin bias values, bias = p(head).
bmin = 0.0      # smallest coin bias
bmax = 1.0
tiny = 1e-12
b = linspace(bmin, bmax, 1000) # list of bias values.
a = 1-b         # list of p(tails) values.

# choose prior, either uniform or binomial.
useuniformprior = 1
if useuniformprior: 
    prior=b**0
else:
    # Make prior=binomial
    C = 1.0 # Not really needed here.
    p = C * b**2 * a**2
    prior = p/max(p)

#Â Make data set x0, from which individual data set x will be extracted.
ni = 6 
NN = 2**ni # max number of coin flips in loop below is numFlips.
flips = random.random(NN); # get numFlips random numbers between zero and one.
x0 = [int(x+0.6) for x in flips] # get list of heads/tails for a coin with bias 0.6.
# Cheat a bit as want to show distribution for specific outcomes.
x0[0]=1
x0[1]=0
x0[2]=1
x0[3]=1

fig1 = plt.figure(1,(10,16)) # make container figure for sub-plots.
# find likelihood and posterior for different numbers N of coin flips.
for i in range(0, ni): # step up number of coin flips in powers of 2.
    N = 2**i            # get number of coin flips.
    x = x0[0:N]     # extract data from x0 for first numCoinFlips flips
    C = 1               # Set binomial coefficient to one in this simple case.
    k = sum(x)      # get number of heads.
    nh = k              # nh = number of heads.
    nt = N-k            # nt = number of tails.
    #  likelihood function = probability of nh heads and nt tails.
    lik = C* b**nh * a**nt
    if useuniformprior: 
        maxlik = lik[0] + tiny
    else:
        maxlik = max(lik) + tiny
    lik = lik/maxlik        # scale likelihood to have max value of one
    p = lik*prior           # find posterior distribution
    maxp = max(p)   # find max value of p
    p = p/maxp          # make max value of p be one.
    ind = p.argmax() # find index of max value of p
    best = b[ind]       # find estimated bias, same as (number of heads)/(number of coin flips)
    #  plot posterior distribution.
    fig2 = plt.subplot(ni/2,2,i+1) 
    plt.plot(b,p) 
    plt.xlabel(u'Coin bias ' + theta, fontsize=9)
    plt.ylabel(u'Posterior, p(' + theta + u'|x)', fontsize=9)
    plt.ylim((0,1.1)) 
    plt.grid()
    plt.text(0.05, 1.0, 'Num flips = ' + str(N))
    plt.text(0.05, 0.9, 'Num heads = ' + str(nh))
    plt.text(0.05, 0.8, 'Bias est = ' + '%(num)1.3f' % {"num" : best})
plt.show()

# End of program