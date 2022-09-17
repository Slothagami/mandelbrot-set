import numpy  as np 
import sys
import pygame as pg
from renderND import renderPoint, c
from math import isnan, isinf, pi
import os 
from color import gray, hsv_to_rgb

os.chdir(os.path.dirname(__file__))

def isnum(n):
    return not (isnan(n) or isinf(n))

#region Seutp
zrange = [-2,2]#[-2, 2]
rrange = [-2,4.2]#[-2, 4.15]

zspan  = zrange[1] - zrange[0]
rspan  = rrange[1] - rrange[0]
done   = False
#endregion

def Render(window, center, settings, fileName=""):
    settings.setdefault("scale", 1)
    settings.setdefault("viewAngle", "")
    settings.setdefault("layerDetail", 150)

    function     = settings["function"]
    startVal     = settings["startVal"]
    noiseRemoval = settings["noiseRemoval"]
    layerDetail  = settings["layerDetail"]
    scale        = settings["scale"]
    prec         = settings["precision"]
    folder       = settings["folder"]
    viewAngle    = settings["viewAngle"]

    if viewAngle == "": viewAngle = [-pi/6,0,0,0]
    if viewAngle == "birdseye": viewAngle = [pi/2,0,0,0]
    if viewAngle == "profile": viewAngle = [0,0,0,0]

    startPop = startVal
    done = False
    r = complex(rrange[0], zrange[0])
    
    while not done:
        for _ in range(prec):
            pop = startPop
            if abs(pop) > 2: continue

            for _ in range(noiseRemoval):
                pop = function(pop, r)

            for iteration in range(layerDetail):
                pop = function(pop, r)

                if not ( isnum(pop.real) or isnum(pop.imag) ): continue

                point = (r.real, -pop.real, r.imag, -pop.imag)
                try:
                    col = hsv_to_rgb(pop.imag - zrange[0], .6, .5)
                except OverflowError: continue

                renderPoint(point, viewAngle, window, center, scale, col, 4)

            r += rspan / prec
        r = complex(rrange[0], r.imag)
        r += complex(0, zspan / prec)

        pg.display.update()
        yield 

        if r.imag >= zrange[1]: 
            done = True

            if fileName == "":
                fn = f"{folder}/{function.__name__}-n{noiseRemoval}-p{prec}-{settings['viewAngle']}.png"
            else:
                fn = f"{folder}/{fileName}"

            pg.image.save(window, fn)
