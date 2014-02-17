# -*- coding: utf-8 -*-

##################################################################################
# File: BayesRuleMatlabRegression.m
# Demonstration code forBayes' Rule: A Tutorial Introduction to Bayesian Analysis
# JV Stone, 2012.
# Copyright: 2012, JV Stone,  Sheffield University, Sheffield, England.
# The Python code below is version 0.1. This code can be downloaded from http://jim-stone.staff.shef.ac.uk/BayesBook/Matlab.
##################################################################################
# imports
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from numpy import arange, linspace, random, ones, linalg, zeros, amin, amax, exp
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.regression.linear_model as sm

s=6 # set random number seed.
                                        #   In MatLabversion: rand('seed',s);    randn('seed',s);

# Make noisy data with slope m and intercept c.
# Define 10 salary values for horizontal axis.
s = arange(1,12)                        #   In MatLabversion: s = 1:1:11
#s = s.reshape(11,1)                    #   In MatLabversion: s=s';

# Set true values of slope m and intercept c.
m = 0.5
c = 3
# Set standard deviation of each measured height.
sds = 2*arange(1,12)/10.0               #   In MatLabversion: sds = 2*[1:11]’/10; %rand(size(s))*2;
sds = sds * arange(1,12)/10.0           #   In MatLabversion: sds = sds .* [1:11]'/10;

# Use sds to make vector of noise.
eta = random.randn(len(s)) * sds        #   In MatLabversion: eta = randn(size(s)).*sds;
# Pretend some data points are extreme.
eta[7]=-1
eta[8]=-3
eta[10]=-3

# Find observed values of x (with noise added).
x = m*s + c + eta

# Weighted Least Squares regression. We could find the solution using the smallest value in the Farray below also.
# Find weightings w (discount) for each data point.
vars0 = sds ** 2
w=1/vars0                               #   In MatLabversion: w=1./vars0
#w=ones(size(w)) # un-comment this line to get solution based on uniform noise terms.
ss = sm.add_constant(s)                 #   In MatLabversion: ss=[ones(size(s)) s] # prepend column of ones so that solution includes intercept term.
model = sm.WLS(ss, x, weights=w)        #   In MatLabversion: [params,stdx,mse,S] =lscov(ss,x,w)
results = model.fit()
mest2, cest2 = results.params[0]
cest2 = cest2 + c # +c to compensate for apparent incorrect intercept returned from WLS
########
xest2 = mest2 * s + cest2               #   In MatLabversion: xest2 = mest2.*s + cest2;
c0 = cest2;
m0 = mest2;

# Plot fitted line xest (=xhat in text) and data points.
fig1 = plt.figure() # ; clf;
plt.plot(s,x, 'k*', s, xest2, 'k')
plt.xlabel('Salary, ' + r'$s$' + ' (groats)'); # use trick to get italic font
plt.ylabel('Height, ' + r'$x$' + ' (feet)');
plt.xlim((0,12))
plt.ylim((0,9))
# Plot sd  from each data point
for i in range(0,11):
    x1 = x[i]-sds[i]
    x2=x[i]+sds[i]
    s1 = i+1
    s2 = i+1
    ss = (s1, s2)
    xx = (x1, x2)
    # hold on;
    plt.plot(ss,xx,'k', linewidth=2)
plt.show()



# Code for 2d plot
m = mest2
mmin = mest2-1 # 0.5
mmax = mest2+1

c = cest2
cmin = cest2-1 #0.4
cmax = cest2+1
minc = (mmax-mmin)/100
cinc = (cmax-cmin)/100

Fs = []
#  In MatLabversion: ms = mmin:minc:mmax;
ms = linspace(mmin, mmax, 100) # minc not used as linspace takes number of values to be generated
nm = len(ms)
#  In MatLabversion: cs = cmin:cinc:cmax);
cs = linspace(cmin, cmax, 100) # cinc not used as linspace takes number of values to be generated
nc = len(cs)

Farray = zeros((nm,nc))
for m1 in arange(0,nm):                 #  In MatLabversion: 1:nm
    for c1 in arange(0, nc):            #  In MatLabversion: 1:nc
        mval=ms[m1]
        cval=cs[c1]
        y1 = mval*s + cval
        F1 = ((x-y1)/sds) ** 2
        Farray[m1,c1]=sum(F1)
        Fs = (Fs, F1)

fig2 = plt.figure()
Z1 = Farray.T
zmin = amin(Z1)                         #  In MatLabversion: min(Z1(:));
zmax = amax(Z1)                         #  In MatLabversion: max(Z1(:));
zrange = zmax - zmin # cannot use variable name 'range' in python
v = arange(zmin, zmax, zrange / 10)     #  In MatLabversion: min:range/10:zmax;
# Adjust spacing of contour lines.
v = arange(0, 9 ,0.5)
v=exp(v)
v=v*zrange/max(v);
X, Y = np.meshgrid(ms,cs)               #  In MatLabversion: [X Y]=meshgrid(ms,cs);
plt.xlabel('Slope, ' + r'$m$') # use trick to get italic font
plt.ylabel('Intercept, ' + r'$c$');
plt.contour(X, Y, Z1, v)
plt.show()

fig3 = plt.figure()
ax = fig3.add_subplot(111, projection='3d')
ax.set_xlim(-0.5, 1.5)
ax.set_ylim(2,4)
ax.set_zlim(min(v), max(v))
ax.autoscale(enable=True, axis='z')
ax.set_xlabel(r'$m$') # use trick to get italic font
ax.set_ylabel(r'$c$')
ax.set_zlabel(r'$F$')
surf = ax.plot_surface(X, Y, Z1, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=True)
plt.show()