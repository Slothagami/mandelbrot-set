from pygame.locals import QUIT, KEYDOWN, K_SPACE
from renderer      import Color, HyperspaceRenderer
from math          import isnan, isinf, pi
from color         import hsv_to_rgb
from time          import time
import pygame as pg 
import sys, os

os.chdir(os.path.dirname(__file__))

def mandlebrot(pop, r): return pop*pop + r 
def logmap(pop, r): return r * pop * (1 - pop)

def isnum(n):
    return not (isnan(n) or isinf(n))

def map_column(r, map):
    pop = params.get("starting_population")
    if abs(pop) > 2: return
    for _ in range(params.get("noise_removal_steps")): pop = map(pop, r)

    for _ in range(params.get("layer_max_bifrications")):
        pop = map(pop, r)

        if not ( isnum(pop.real) or isnum(pop.imag) ): return

        point = (r.real, -pop.real, r.imag, -pop.imag)

        # Set Color
        try:
            col = hsv_to_rgb(pop.imag - r_imag_range[0], .5, .5)
        except OverflowError: return
        # col = hsv_to_rgb(iteration/layerDetail, .5, .5)

        render.rotation = viewAngle
        render.pixel(point, col, params.get("scale"))

def render_map(map):
    global done, r
    if done: return

    for _ in range(prec):
        map_column(r, map)
        r += r_imag_span / prec

    r = complex(r_real_range[0], r.imag)
    r += complex(0, r_real_span / prec)

    pg.display.update()
    if r.imag >= r_imag_range[1]: done = True

params = {
    "map":                      mandlebrot,
    "view_angle":               "overhead",
    "render_density":           300,
    "noise_removal_steps":      100,
    "layer_max_bifrications":   150,
    "starting_population":      0,
    "scale":                    3,
}

view_angles = {
    "birdseye": [pi/2 , 0, 0, 0], 
    "overhead": [-pi/6, 0, 0, 0], 
    "profile":  [0    , 0, 0, 0]
}

prec       = params.get("render_density")
viewAngle  = view_angles.get(params.get("view_angle"))
rendername = f"{params.get('map').__name__}-{params.get('view_angle')}"

r_imag_range = (-2, 2  )
r_real_range = (-2, 4.2)

r_real_span = r_imag_range[1] - r_imag_range[0]
r_imag_span = r_real_range[1] - r_real_range[0]
done        = False


# Pygame Stuff
pg.init()
pg.display.set_caption(rendername)

screen_size = 1024, 650
window = pg.display.set_mode(screen_size)
render = HyperspaceRenderer(screen_size, window, 4)

window.fill(Color.grey)

r = complex(r_real_range[0], r_imag_range[0])
while True:
    render_map(params.get("map"))

    for e in pg.event.get():
        if e.type == QUIT:
            pg.quit()
            sys.exit()

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                pg.image.save(window, f"renders/{rendername}-{round(time())}.jpg")
