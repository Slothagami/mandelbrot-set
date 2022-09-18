from pygame.locals import QUIT, KEYDOWN, K_SPACE
from renderer      import Color, HyperspaceRenderer
from math          import isnan, isinf, pi
from color         import hsv_to_rgb
import numpy  as np 
import pygame as pg 
import sys
import os 

os.chdir(os.path.dirname(__file__))

def mandlebrot(pop, r): return pop*pop + r 
def logmap(pop, r): return r * pop * (1 - pop)

def isnum(n):
    return not (isnan(n) or isinf(n))

def map_column(r, map):
    pop = startPop
    if abs(pop) > 2: return

    for _ in range(noiseRemoval):
        pop = map(pop, r)

    for iteration in range(layerDetail):
        pop = map(pop, r)

        if not ( isnum(pop.real) or isnum(pop.imag) ): return

        point = (r.real, -pop.real, r.imag, -pop.imag)
        try:
            col = hsv_to_rgb(pop.imag - zrange[0], .5, .5)
        except OverflowError: return
        # col = hsv_to_rgb(iteration/layerDetail, .5, .5)

        render.rotation = viewAngle
        render.point(point, col, 1, scale)

def render_map():
    global done, r
    if not done:
        for _ in range(rprec):
            map_column(r, mandlebrot)
            r += rspan / rprec
        r = complex(rrange[0], r.imag)
        r += complex(0, zspan / zprec)

        pg.display.update()
        if r.imag >= zrange[1]: done = True

#region Seutp
startPop      = 0
noiseRemoval  = 100
layerDetail   = 150
scale         = 3
prec          = 300
viewAngles    = {"-birdseye": [pi/2,0,0,0], "": [-pi/6,0,0,0], "-profile": [0,0,0,0]}
viewAngle     = "-birdseye"
viewAngle     = viewAngles[viewAngle]

zprec = prec
rprec = prec

zrange = [-2,2]#[-2, 2]
rrange = [-2,4.2]#[-2, 4.15]

zspan  = zrange[1] - zrange[0]
rspan  = rrange[1] - rrange[0]
done   = False

rendername = f"Mandlebrot-{prec}-sp-[{startPop}]-nr{noiseRemoval}{viewAngle}-4d-[{viewAngle[-1]}]"
#endregion
#region Pygame Seutp
pg.init()
pg.display.set_caption(rendername)

screen_size = 1024, 650
window = pg.display.set_mode(screen_size)
render = HyperspaceRenderer(screen_size, window, 4)

window.fill(Color.grey)
#endregion

r = complex(rrange[0], zrange[0])
while True:
    render_map()

    for e in pg.event.get():
        if e.type == QUIT:
            pg.quit()
            sys.exit()

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                pg.image.save(window, f"renders/Mandlebrot/{rendername}.jpg")
