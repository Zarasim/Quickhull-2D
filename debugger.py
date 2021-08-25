#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 09:43:20 2021

Debugger for quickhull module


Test N batches containg an increasing number of points distributed according to 

uniform distribution from [0,1]x[0,1]
Normal distribution with mean mu and variance sigma 

@author: simone
"""

from quickhulls import * 
import numpy as np
from scipy.spatial import ConvexHull, convex_hull_plot_2d


import matplotlib.pyplot as plt
import time 


D = int(input('Insert from which distributiion the points are sampled from [0: uniform, 1: uniform polar, 2: normal]:  '))
B = int(input('Insert number of batches to insert: '))
T = int(input('Insert number of tests of each batch: '))
S = int(input('Insert scaling factor for increasing number of points in each batch: '))

# S = 100, B = 40, T = 10, d=1
print('Batches: ' + str(B) + ', Tests: ' + str(T) + ', Scaling factor: ' + str(S))    

# start test with 5 points 
npoints = 5

def  random_sample(npoints,d):
    
    if d==0:  # sample from uniform distribution in cartesian coordinates  
        points = np.random.rand(npoints,2)
    elif d==1: # sample from uniform distribution for radius and angle 
        r = np.random.rand(npoints)
        theta = 2*np.pi*np.random.rand(npoints)
        points = np.zeros([npoints,2])
        points[:,0] = r[:]*np.cos(theta[:])
        points[:,1] = r[:]*np.sin(theta[:])
    elif d==2: 
        points = np.random.randn(npoints,2)
    else:
        print('you have to insert the number 0,1 or 2')
        raise ValueError 
        
    return points 

time_vec = np.zeros([B,2])
counter = 0

for n in range(B):
    npoints += n*S
    print('Batch n°: ' + str(n) + ' with ' + str(npoints) + ' points')
    for t in range(T):
        
        # test the quickhull with npoints sampled from the distribution 
        points = random_sample(npoints,D) 
        pts = [list(points[i]) for i in range(len(points))]
        t0 = time.time()
        res = quick(pts)
        res = sort_clockwise(res)
        t1 = time.time() - t0
        print('time test quickhull n° ' + str(t) + ': ' + str(t1))
        
        t0 = time.time()
        res_scipy = ConvexHull(points)
        res_scipy = np.unique(points[res_scipy.simplices].reshape(-1,2),axis = 0)
        t2 = time.time() - t0
        print('time test scipy n° ' + str(t) + ': ' + str(t2))
         
        time_vec[counter,:] += [t1,t2]
        
        for i in range(len(res_scipy)):    
            try:
                res_scipy[i] not in res
            except:
                print('The point with coordinates ' + str(res_scipy[i]) + 'has not been detected')
        
            break
    
    time_vec[counter,:] /= T
    counter += 1
    
print('The test has passed successfully')

plt.plot(time_vec[:,0],c = 'red',label = 'Convex-hull Python')
plt.plot(time_vec[:,1],c = 'blue',label = 'Convex-hull Scipy')
plt.legend()

plt.xlabel('counter')
plt.ylabel('time [s]')
np.save('time_vec',time_vec)
