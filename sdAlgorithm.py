# -*- coding: utf-8 -*-
import math
import numpy as np
from random import random
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def funct(x,y):
    result = 4*np.power(x,2) + 5*x*y + 2*np.power(y,2)
    return result

def plot3d(XX, YY, ZZ):
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_title("F(x,y)")
    ax.plot_surface(XX, YY, ZZ, rstride=1, cstride=1, cmap='hot')
    plt.show()

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
    

cur_x = random()#*1e2 # The algorithm starts at x=3
cur_y = -1*random()#*1e2
df = lambda x,y: 4*np.power(x,2) + 5*x*y + 2*np.power(y,2) # main function
#dfx = lambda x,y: 8*x+5*y#Gradient of our function
#dfy = lambda x,y: 4*y+5*x
dfx = lambda x, y: 4 * x**3 - 9 * x**2
dfy = lambda x, y: 0    
ratelist = [1e-5,1e-4,1e-3,1e-2,1e-1,1.5e-1, 1.7e-1,2e-1] # Learning rate
iterlist = []

for rate in ratelist: 
    cur_x = random()#*1e2 # The algorithm starts at x=3
    cur_y = -1*random()#*1e2
    precision = 0.000001 #This tells us when to stop the algorithm
    previous_step_size = 1 #
    max_iters = 1e6 # maximum number of iterations
    iters = 0 #iteration counter
    df = lambda x,y: 4*np.power(x,2) + 5*x*y + 2*np.power(y,2) # main function
    dfx = lambda x,y: 8*x+5*y#Gradient of our function
    dfy = lambda x,y: 4*y+5*x
    #dfx = lambda x,y : 4 * x**3 - 9 * x**2
    #dfy = lambda x,y : 0
    xlist = [cur_x]
    ylist = [cur_y]
    flist = [df(cur_x, cur_y)]
    while previous_step_size > precision and iters < max_iters:
        prev_x = cur_x #Store current x value in prev_x
        prev_y = cur_y #Store current x value in prev_x
        cur_x = cur_x - rate * dfx(prev_x, prev_y) #Grad descent
        cur_y = cur_y - rate * dfy(prev_x, prev_y) #Grad descent
        previous_step_size = pow(abs(cur_x - prev_x),2)+pow(abs(cur_y - prev_y),2) #Change in x,y
        previous_step_size = math.sqrt(previous_step_size)
        iters = iters+1 #iteration count
        #print("Iteration",iters,"\nX value is",cur_x,"\nY value is",cur_y) #Print iterations
        xlist.append(cur_x)
        ylist.append(cur_y)
        flist.append(df(cur_x, cur_y))
    print(iters)
    iterlist.append(iters)    
    print("The local minimum occurs at (", cur_x, ", ", cur_y, ")")

    plotLine(np.linspace(0,len(xlist), len(xlist)),xlist, "Step", "X", " ")
    '''
    plotLine(xlist, ylist, "x", "y", "Steepest Descent Method")
    
    xmax = max(xlist)
    ymax = abs(min(ylist))
    xarr = np.linspace(-1*xmax, 0.2, iters+1)
    yarr = np.linspace(-1*ymax, 0.2, iters+1)
    #print(xarr)
    #print(yarr)
    X, Y = np.meshgrid(xarr, yarr)
    #X, Y = np.meshgrid(xlist, ylist)
    F = funct(X, Y)
    plot3d(X, Y, F)
    #print(np.shape(xlist))
    #print(np.shape(F))
    fig, ax = plt.subplots()
    CS = ax.contourf(X, Y, F, cmap='RdGy')
    ax.set_title('Simplest default with labels')
    ax.plot(xlist, ylist)
    #plt.colorbar()
    fig.colorbar(CS, ax=ax)
    plt.show()
    '''
plotLine(ratelist, iterlist, "Rate", "Iteration", " ")