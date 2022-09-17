import numpy  as np 
import pygame as pg 
from math import sin, cos, isnan
import sys

def cube(dimensions):
    c = []
    for i in range(2 ** dimensions):
        binary = bin(i)[2:]
        binary = binary.rjust(dimensions, "0")
        binary = [int(x) for x in binary]

        vertex = [(x - .5) * 2 for x in binary]
        c.append(vertex)
    return np.array(c)

def transformMatrix(wid, hei):
    transform = np.zeros((wid, hei))
    for i, row in enumerate(transform):
        row[i] = 1

    return transform

# Generate transform matrices
# make the biggest one, and slice it for the smaller ones

class c:
    white  = (255, 255, 255)
    dwhite = (150, 150, 150)
    grey   = (32, 32, 32)
    orange = (255, 100, 0)

# Functions 
def renderPoint(point, rotation, surf, center, scale, color, dimensions=3):
    projection = project(point, rotation, scale, dimensions) * scale
    if isnan(point[1]): return
    # pg.draw.circle(surf, c.white, projection + center, 3)
    surf.set_at(np.round(projection + center).astype(int), color)

# Utility
def rotateX(a, point, dims=3):
    rotMatrix = transformMatrix(dims, dims)

    if dims > 2:
        rotMatrix[1, 1] =  cos(a)
        rotMatrix[2, 1] =  sin(a)
        rotMatrix[1, 2] = -sin(a)
        rotMatrix[2, 2] =  cos(a)

    return np.dot(rotMatrix, point)

def rotateN(a, point, axis, dims=3):
    rotMatrix = transformMatrix(dims, dims)

    rotMatrix[   0,    0] =  cos(a)
    rotMatrix[axis,    0] =  sin(a)
    rotMatrix[   0, axis] = -sin(a)
    rotMatrix[axis, axis] =  cos(a)

    return np.dot(rotMatrix, point)

def rotate(rot, point, dims=3):
    point = rotateX(rot[0], point, dims)

    for dim in range(1, dims):
        point = rotateN(rot[dim], point, dim, dims)

    return point

def project(point, rotation, scale, dims=3):
    transform = transformMatrix(dims-1, dims)

    # rotate in highest dimension
    point = rotate(rotation, point, dims)

    # project down to 2d
    for dim in reversed(range(2, dims)):
        dist   = 4
        dscale = 1 / (dist - point[-1])
        point  = np.dot(transform[:dim, :dim+1] * dscale, point)

    return point * scale**dims
