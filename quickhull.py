#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 18:11:17 2021

quickhull algorithm 

@author: simone
"""

import numpy as np
import math
from pandas.core.common import flatten


def centroidpython(points):
    
    centroid_x = np.mean(points[:,0])
    centroid_y = np.mean(points[:,1])

    return centroid_x,centroid_y



def sort_clockwise(points):
    
    val = np.zeros(len(points))
    centroid_x, centroid_y = centroidpython(points)
    for i,pt in enumerate(points):
        val[i] = math.atan2((pt[1]-centroid_y),(pt[0]-centroid_x))
    
    idxs = sorted(range(len(val)), key=lambda k: val[k])
    
    return points[idxs,:]


def min_max_x(pts):
    
    '''
    pts contains the x,y coordinates of N points in a numpy matrix N x 2
    
    '''
    
    minX = pts[0][0]
    maxX = pts[0][0]
    
    minXPoint = pts[0]
    maxXPoint = pts[0]
    
    for pt in pts:
        if pt[0] < minX:
            minX = pt[0]
            minXPoint = pt
        if pt[0] > maxX:
            maxX = pt[0]
            maxXPoint = pt
    
    return minXPoint, maxXPoint


def PointSide(point, line):
        
	sp = line[0]
	ep = line[1]
    
	d = (point[0] - sp[0]) * (ep[1] - sp[1]) - (point[1] - sp[1])*(ep[0] - sp[0])
	if d > 0:
		return 1
	elif d == 0:
		return 0
	else:
		return -1

def PointsRightSide(points, line):
    
    '''
      points in the right side are returned as 1 and on the left side as -1. 
      If the point lies on the line is returned as 0
     
    '''
    ret = []
    for pt in points:
        if (PointSide(pt, line)) > 0:   
            ret.append(pt)
    return ret

def PointsLeftSide(points, line):
    
    ret = []
    for pt in points:
        if (PointSide(pt, line)) < 0:
            ret.append(pt)
    return ret


def distance_pt_line(pt,line):
    
    '''
    Compute distance from pt to line joining pt1 and pt2
    
    '''
    pt1 = line[0]
    pt2 = line[1]
    
    return 	abs((pt[1] - pt1[1]) * (pt2[0] - pt1[0]) - (pt2[1] - pt1[1]) * (pt[0] - pt1[0]))


def PointFarthest(points, line):
    if len(points) == 0:
        return None
    far = points[0]
    max_dist = distance_pt_line(far,line)
    for pt in points:
        if distance_pt_line(pt,line) > max_dist:
            far = pt
            max_dist = distance_pt_line(pt,line) 
    return far;
 

def GetNextPointRight(line, ptsRight):
    
    if len(ptsRight) == 0:
        return line
    
    farPointRight = PointFarthest(ptsRight, line)
    
    line1 = [line[0], farPointRight]
    line2 = [farPointRight, line[1]]
    
    restOfPoints1 = PointsRightSide(ptsRight, line1)
    restOfPoints2 = PointsRightSide(ptsRight, line2)
 
    r1 = GetNextPointRight(line1, restOfPoints1)
    r2 = GetNextPointRight(line2, restOfPoints2)

    return [r1,r2]
 
def GetNextPointLeft(line, ptsLeft):
    
    if len(ptsLeft) == 0:
        return line
    
    
    farPointLeft = PointFarthest(ptsLeft, line)
   
    
    line1 = [line[0], farPointLeft]
    line2 = [farPointLeft, line[1]]
    
    restOfPoints1 = PointsLeftSide(ptsLeft, line1)
    restOfPoints2 = PointsLeftSide(ptsLeft, line2)
    
    r1 = GetNextPointLeft(line1,restOfPoints1)
    r2 = GetNextPointLeft(line2,restOfPoints2)
 
    return [r1,r2]
    
    
def quick(pts):
    #determining points with min and max X coordinate
    minXPoint, maxXPoint = min_max_x(pts)
    #creating line between these points
    lineMinMaxX = [minXPoint, maxXPoint]
    
    ptsRight = PointsRightSide(pts, lineMinMaxX)
    ptsLeft = PointsLeftSide(pts, lineMinMaxX)
   
    resultRight = GetNextPointRight(lineMinMaxX, ptsRight)
    resultLeft = GetNextPointLeft(lineMinMaxX,  ptsLeft)
    
    result= [resultLeft,resultRight]
    res = list(flatten(result))
    res = np.array(res).reshape(-1,2)

    return np.unique(res,axis=0)
    
    