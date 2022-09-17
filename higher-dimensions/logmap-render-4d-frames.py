import numpy  as np 
import pygame as pg 
import sys
from pygame.locals import *
import renderND
from renderND import renderPoint, c
from math import isnan, pi
from color import gray, hsv_to_rgb

def gray(z): 
    value = (z/2 - zrange[0]) / zspan * 255 + 40
    col = np.round(np.array([value, value, value])).astype(int)
    col = np.minimum(col, 255)
    return col

#region Seutp
startPop      = .5#-2.5#.5#complex(-.4, 0)#-.4
noiseRemoval  = 0#45
layerDetail   = 150#200
scale         = 4.5
prec          = 300#100
framecount    = 200#120

# [X, Z, Y, W]
viewAngles    = {"-birdseye": [pi/2,0,0,0], "": [-pi/6,0,0,0], "-profile": [0,0,0,0]}
viewAngleName = ""
viewAngle     = viewAngles[viewAngleName]

zprec = prec
rprec = prec

zrange = [-2,2]#[-2, 2]
rrange = [-2,4.2]#[-2, 4.15]

zspan  = zrange[1] - zrange[0]
rspan  = rrange[1] - rrange[0]
done   = False
frame  = 0

drawLayer = 0

rendername = f"Logmap-{prec}-sp-[{startPop}]-nr{noiseRemoval}{viewAngleName}-4d-[{viewAngle[-1]}]"
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
            if abs(pop) > 2: continue


            for _ in range(noiseRemoval):
                pop = r * pop * (1 - pop)

            for iteration in range(layerDetail):
                pop = r * pop * (1 - pop)
                if isnan(pop.real): continue

                if iteration == drawLayer or iteration == drawLayer - 1:
                    point = (r.real, -pop.real, r.imag, -pop.imag)
                    # col = hsv_to_rgb(iteration/layerDetail, .5, .5)
                    # col = c.white
                    
                    renderPoint(point, viewAngle, window, center, scale, rowColor, 4)
                    # renderPoint(point, viewAngle, window, center, scale, col, 4)
                    if iteration == drawLayer: break

            r += rspan / rprec
        r = complex(rrange[0], r.imag)
        r += complex(0, zspan / zprec)

        pg.display.update()
        if r.imag >= zrange[1]:
            frame += 1
            drawLayer += 1
            # startPop = 5 / framecount * frame - 2.5
            # an = pi/(framecount/2) * frame
            # viewAngle[0] = an
            # viewAngle[1] = an
            # viewAngle[2] = an
            # viewAngle[3] = an
            r = complex(rrange[0], zrange[0])

            pg.image.save(window, f"renders/4D-Render/frames/{rendername}-FRAME-{frame}.jpg")
            
            window.fill(c.grey)
            pg.display.update()


            if frame >= framecount: done = True


    for e in pg.event.get():
        if e.type == QUIT:
            pg.quit()
            sys.exit()
