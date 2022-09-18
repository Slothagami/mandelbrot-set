import numpy  as np 
import pygame as pg 
import sys
from pygame.locals import QUIT, KEYDOWN, K_SPACE
from renderer import Color, HyperspaceRenderer
from math import isnan, isinf, pi
import os 
from color import hsv_to_rgb

os.chdir(os.path.dirname(__file__))

def isnum(n):
    return not (isnan(n) or isinf(n))

#region Seutp
startPop      = 0#.5#.5#complex(-.4, 0)#-.4
noiseRemoval  = 100#3000#100#45
layerDetail   = 150#200
scale         = 5.2
prec          = 500
viewAngles    = {"-birdseye": [pi/2,0,0,0], "": [-pi/6,0,0,0], "-profile": [0,0,0,0]}
viewAngleName = "-birdseye"
viewAngle     = viewAngles[viewAngleName]

zprec = prec
rprec = prec

zrange = [-2,2]#[-2, 2]
rrange = [-2,4.2]#[-2, 4.15]

zspan  = zrange[1] - zrange[0]
rspan  = rrange[1] - rrange[0]
done   = False

rendername = f"Mandlebrot-{prec}-sp-[{startPop}]-nr{noiseRemoval}{viewAngleName}-4d-[{viewAngle[-1]}]"
#endregion
#region Pygame Seutp
pg.init()
pg.display.set_caption(rendername)

width, height = 1024, 650
center = np.array([width, height]) / 2
window = pg.display.set_mode((width, height))
render = HyperspaceRenderer((width, height), window, 4)

window.fill(Color.grey)
#endregion

r = complex(rrange[0], zrange[0])
while True:
    # render the map
    if not done:
        for _ in range(rprec):
            pop = startPop
            if abs(pop) > 2: continue
            # rowColor = gray(r.imag)

            for _ in range(noiseRemoval):
                # pop = r * pop * (1 - pop)
                pop = pop * pop + r

            for iteration in range(layerDetail):
                # pop = r * pop * (1 - pop)
                pop = pop * pop + r

                if not ( isnum(pop.real) or isnum(pop.imag) ): continue

                point = (r.real, -pop.real, r.imag, -pop.imag)
                try:
                    col = hsv_to_rgb(pop.imag - zrange[0], .5, .5)
                except OverflowError: continue
                # col = hsv_to_rgb(iteration/layerDetail, .5, .5)
                # renderPoint(point, viewAngle, window, center, scale, rowColor, 4)
                render.rotation = viewAngle
                render.point(point, col, 1)

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
            if e.key == K_SPACE:
                pg.image.save(window, f"renders/Mandlebrot/{rendername}.jpg")
