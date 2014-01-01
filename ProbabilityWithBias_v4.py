# -*- coding: utf-8 -*-

# imports
from numpy import arange, ones, random
import matplotlib.pyplot as plt


theta = u'\u03b8'

# %%%%%%%%%%%%%%%%%%%%%
# % Matlab code for plotting probability of head/tail outcomes
# % as a function of bias b.
# clear all;
# % set random number seeds.
s=999 # rand(’seed’,s); randn(’seed’,s);
# Make vector of possible bias values
inc = 0.001 # set resolution of distributions.
bmin = inc
bmax = 1.0 - inc
#b = arange(bmin, bmax, inc) #b = bmin:inc:bmax; # range of bias values p(head).
b = arange(bmin, 1.0, inc) #b = bmin:inc:bmax; # range of bias values p(head).
a = 1-b # range of p(tails) values.
# make prior either uniform or binomial.
# set switch for uniform prior.
uprior=1 # ??? Will never be executed
if uprior :# Make uniform prior
    ht=1.0/(bmax-bmin)
    prior = ones(len(b))*ht
else: # Make prior=binomial
    C = 1.0 # nchoosek(4,2); # not really needed here.
    p = C * b**2 * a**2
    prior = p/max(p)
#plot prior
# figure(1);set(gca,’FontSize’,20)
#fig1 = plt.figure(1,(6,6))
#plt.plot(b,prior) #,’k-’,’Linewidth’,2) # set(gca,’Linewidth’,2);
#plt.xlabel(u'Coin bias, ' + theta) # xlabel(’Coin bias, \theta’); ylabel(’Prior, p(\theta)’);
#plt.ylabel(u'Prior, ' + theta)
#plt.show()
#==============================================================================

# set(gca,’YLim’,[0 1.1],’FontName’,’Ariel’); grid on;
ni=10
if uprior==0 :
    ni=3 # ??? Will never be executed
# end # make graphs for figure 4.3.
print ni
NN = 2**ni # max number of coin flips in loop below is NN.

flips = random.random(NN); # get NN random numbers between zero and one.
x0 = [int(x+0.6) for x in flips] # x0 = flips<0.6; %get number of heads for a coin with bias 0.6.
# % Cheat a bit as want to show distribution for specific outcomes.
x0[0]=1 # x0(1)=1; x0(2)=0; x0(3)=1; x0(4)=1; fprintf(’\n’);
x0[1]=0
x0[2]=1
x0[3]=1

fig2 = plt.figure(1,(10,18))

# % find likelihood and posterior for different numbers N of coin flips.
for i in range(0, ni): # step up number of coin flips in powers of 2. (Python range needs +1 added to get n values)
    N=2**i # get number of coin flips.
    x = x0[0:N] # x = x0(1:N); % get data for first N coin flips
    k = sum(x) # get number of heads.
    #C = nchoosek(N,k) # binomial coefficient, not needed here.
    C = 1 # set binomial coefficient to one.
    nh = k # nh = number of heads.
    nt = N-k # nt = number of tails.
    #  likelihood function = probability of nh heads and nt tails.
    lik = C* b**nh * a**nt
    lik = lik/max(lik) # scale likelihood to have max value of one
    #  plot likelihood function.
    fig3 = plt.subplot(ni/2,2,i+1) # figure(2) #set(gca,’FontSize’,20);
    plt.plot(b,lik) #,’k-’,’Linewidth’,2); set(gca,’Linewidth’,2);
    plt.xlabel(u'Coin bias ' + theta, fontsize=9)
    plt.ylabel(u'Likelihood, p(' + theta + u'|x)', fontsize=9)
    plt.ylim((0,1.1)) # set(gca,’YLim’,[0 1.1],’FontName’,’Ariel’); grid on
    plt.grid()
    plt.text(0.05, 1.0, 'Coin flips = ' + str(N))
    p=lik*prior # find posterior = likelihood * prior
    maxp = max(p) # find max value of p
    ind = p.argmax() # ind = find(maxp==p) # find index of max value of p
    p = p/maxp # make max value of p be one.
    best = b[ind] # find estimated bias,
    # same as (number of heads)/(number of coin flips)
    # plot posterior
    #fig4 = plt.subplot(ni,2,i*2) # set(gca,’FontSize’,20)
    #plt.plot(b,p[0],'k-',linewidth=2)
    # set(gca,’YLim’,[0 1.1],’FontName’,’Ariel’);
    #plt.xlabel(u'Coin bias, ' + theta, fontsize=9)
    #plt.ylabel(u'Posterior, p(' + theta + u'|x)', fontsize=9) # set(gca,’Linewidth’,2);
    #ss = "Heads = %d/%d" % (k,N)
    #print ss
    #plt.text(0.1,0.9, ss) #’FontSize’,20) # grid on;
    # print value of bias associated with max value of p
    #=============================================================================
    print "N = %d Number of heads = %d. Estimated bias = %.3f\n" % (N, k ,best)
plt.show()
