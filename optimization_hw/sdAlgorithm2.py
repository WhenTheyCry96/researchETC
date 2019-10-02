# -*- coding: utf-8 -*-
import math
import numpy as np
from random import random
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Derivative function
def df(x):
    return -1*math.cos(1/x)/(x**2)

def funct(x):
    return math.sin(1/x)

def plotLine(xArr, yArr, xLabel, yLabel, title, *args):
    argsList = []
    for arg in args:
        argsList.append(arg)
    
    _fig, ax = plt.subplots()
    ax.set_xlabel(xLabel, fontsize=20)
    ax.set_ylabel(yLabel, fontsize=20)
    ax.plot(xArr, yArr)
    plt.title(title, fontsize=24)
    plt.grid()
    plt.show()
    
ratelist = [1e-5,1e-4,1e-3,1e-2,1e-1,1.5e-1, 1.7e-1,2e-1] # Learning rate
iterlist22 = []

for rate in ratelist: 
    next_x = random() # We start the search at x=6
    gamma = rate  # Step size multiplier
    precision = 0.000001  # Desired precision of result
    max_iters = 1000000  # Maximum number of iterations

    xlist = [next_x]
    iters = 0    
    for _i in range(max_iters):
        current_x = next_x
        next_x = current_x - gamma * df(current_x)
        step = next_x - current_x
        #print("current : ", current_x, ", next : ", next_x)
        if funct(current_x) > funct(next_x):
            gamma = gamma * 0.5
        iters = iters + 1
        xlist.append(next_x)
        if abs(step) <= precision:
            break
    iterlist = np.linspace(0, iters+1, iters+1)
    print("Iter %d Minimum at %f, function(x) : %f" %(iters, next_x, funct(next_x)))
    plotLine(iterlist,xlist, "Step", "X", " ")
    iterlist22.append(iters)