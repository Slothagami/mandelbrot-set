import numpy  as np 
import pygame as pg 
import sys
from pygame.locals import *
from render3D import renderPoint, cube, c
from math import isnan, pi
from color import gray

def gray(z): 
    value = (z/2 - zrange[0]) / zspan * 255 + 40
    col = np.round(np.array([value, value, value])).astype(int)
    col = np.minimum(col, 255)
    return col

#region Seutp
startPop      = complex(0, .5)#complex(-.4, 0)#-.4
noiseRemoval  = 0#10#45
layerDetail   = 100#200
scale         = 3
prec          = 300
viewAngles    = {"-birdseye": [pi/2,0,0], "": [-pi/6,0,0], "-profile": [0,0,0]}
viewAngleName = ""
viewAngle     = viewAngles[viewAngleName]

zprec = prec
rprec = prec

zrange = [-6,6]#[-2, 2]
rrange = [-6,6]#[-2, 4.15]

zspan  = zrange[1] - zrange[0]
rspan  = rrange[1] - rrange[0]
done   = False

rendername = f"Logmap-{prec}-sp-[{startPop}]-nr{noiseRemoval}{viewAngleName}"
#endregion
#region Pygame Seutp
pg.init()
pg.display.set_caption(rendername)

width, height = 1024, 650
center = np.array([width, height]) / 2
window = pg.display.set_mode((width, height))

window.fill(c.grey)
#endregion

r = complex(rrange[0], zrange[0])
while True:
    # render the map
    if not done:
        for _ in range(rprec):
            pop = startPop
            rowColor = gray(r.imag)

            for _ in range(noiseRemoval):
                pop = r * pop * (1 - pop)

            for _ in range(layerDetail):
                pop = r * pop * (1 - pop)
                if isnan(pop.real): continue

                try:        
                    # point = (r.real, -abs(pop), r.imag)
                    point = (r.real, -pop.real, r.imag)
                    
                    renderPoint(point, viewAngle, window, center, scale, rowColor)
                except OverflowError: pass

            r += rspan / rprec
        r = complex(rrange[0], r.imag)
        r += complex(0, zspan / zprec)

        pg.display.update()
        if r.imag >= zrange[1]: done = True

    for e in pg.event.get():
        if e.type == QUIT:
            pg.quit()
            sys.exit()

        if e.type == KEYDOWN:
            if e.key == K_a:
                pg.image.save(window, f"renders/3D-Render/{rendername}.jpg")

