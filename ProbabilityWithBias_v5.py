# -*- coding: utf-8 -*-
# imports
from numpy import random, linspace
import matplotlib.pyplot as plt

# Constants
theta = u'\u03b8'

"""

    Matlab code for plotting probability of head/tail
    outcomes as a function of bias b.

"""

# Make vector of possible bias values
bmin = 0.001
bmax = 0.999
b = linspace(bmin, bmax, 1000) # range of bias values p(head).
a = 1-b # range of p(tails) values.

# Make prior=binomial
C = 1.0 # Not really needed here.
p = C * b**2 * a**2
prior = p/max(p)

ni = 10
NN = 2**ni # max number of coin flips in loop below is numFlips.

flips = random.random(NN); # get numFlips random numbers between zero and one.
x0 = [int(x+0.6) for x in flips] # get number of heads for a coin with bias 0.6.
# % Cheat a bit as want to show distribution for specific outcomes.
x0[0]=1 
x0[1]=0
x0[2]=1
x0[3]=1

fig1 = plt.figure(1,(10,16))

# find likelihood and posterior for different numbers N of coin flips.
for i in range(0, ni): # step up number of coin flips in powers of 2.
    N=2**i # get number of coin flips.
    x = x0[0:N] # get data for first numCoinFlips flips

    C = 1 # Set binomial coefficient to one in this simple case.
    k = sum(x) # get number of heads.
    nh = k
    nt = N-k # nt = number of tails.
    #  likelihood function = probability of nh heads and nt tails.
    lik = C* b**nh * a**nt
    lik = lik/max(lik) # scale likelihood to have max value of one
    p=lik*prior 
    maxp = max(p) # find max value of p
    ind = p.argmax() # find index of max value of p
    p = p/maxp # make max value of p be one.
    best = b[ind] # find estimated bias, same as (number of heads)/(number of coin flips)
    #  plot likelihood function.
    fig2 = plt.subplot(ni/2,2,i+1) 
    plt.plot(b,lik) 
    plt.xlabel(u'Coin bias ' + theta, fontsize=9)
    plt.ylabel(u'Likelihood, p(' + theta + u'|x)', fontsize=9)
    plt.ylim((0,1.1)) 
    plt.grid()
    plt.text(0.05, 1.0, 'Coin flips = ' + str(N))
    plt.text(0.05, 0.9, 'Num heads = ' + str(nh))
    plt.text(0.05, 0.8, 'Bias = ' + '%(num)1.3f' % {"num" : best})
plt.show()
