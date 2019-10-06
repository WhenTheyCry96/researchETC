# -*- coding: utf-8 -*-
import math
import numpy as np
from random import random
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

deltaX = 1e-10
deltaY = 1e-10

# Derivative function

# Beale function
def funct(x, y):
    return math.pow(1.5-x+x*y, 2) + math.pow(2.25-x+x*y**2, 2) + math.pow(2.625-x+x*y**3,2)

'''
# Booth function
def funct(x, y):
    return (x+2*y-7)**2 + (2*x+y-5)**2
'''
'''
# Bukin function N.6
def funct(x, y):
    return 100*math.sqrt(abs(y-0.01*x**2))+0.01*abs(x+10)
'''
def dfx(x, y):
    result = funct(x+deltaX, y) - funct(x, y)
    result = result / deltaX
    return result
    
def dfy(x, y):
    result = funct(x, y+deltaY) - funct(x, y)
    result = result / deltaY
    return result

def plotLine(xArr, yArr, xLabel, yLabel, title, *args):
    argsList = []
    for arg in args:
        argsList.append(arg)
    
    _fig, ax = plt.subplots()
    ax.set_xlabel(xLabel, fontsize=20)
    ax.set_ylabel(yLabel, fontsize=20)
    ax.plot(xArr, yArr, marker='o')
    plt.title(title, fontsize=24)
    plt.grid()
    plt.show()
iterlist22 = []

rate = 1e-2
next_x = random() # We start the search at x=6

cur_x = random() #*1e2 # The algorithm starts at x=3
cur_y = -1*random() #*1e2
precision = 0.000001 #This tells us when to stop the algorithm
previous_step_size = 1 #
max_iters = 1e6 # maximum number of iterations
iters = 0 #iteration counter
#dfx = lambda x,y : 4 * x**3 - 9 * x**2
#dfy = lambda x,y : 0
xlist = [cur_x]
ylist = [cur_y]
flist = [funct(cur_x, cur_y)]

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
    flist.append(funct(cur_x, cur_y))
print(iters)   
print("The local minimum occurs at (", cur_x, ", ", cur_y, ")", "The optimized value is ", funct(cur_x, cur_y))

plotLine(xlist, ylist, "X", "Y", "Steepest Descent Method")