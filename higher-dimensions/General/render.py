#region Seutp
from renderMap import Render
from functions import *

import pygame as pg 
from pygame.locals import *
from color import c
import numpy as np
from math import pi

import sys
import os

os.chdir(os.path.dirname(__file__))
pg.init()

width, height = 1024, 650
center = np.array([width, height]) / 2
window = pg.display.set_mode((width, height))

window.fill(c.grey)
#endregion

animate = False
frames  = 30
frame   = 1 # change to resume from partway

settings = {
    "function":      mandlebrot_4th, 
    "startVal":      0, 
    "noiseRemoval":  300, 
    "scale":         5.2, 
    "precision":     200, 
    # "viewAngle":     "birdseye", 
    "folder":        "renders" # "renders/frames"
}


render = Render(window, center, settings, "" if not animate else "1.png")

while True:
    try:
        next(render)
    except StopIteration:
        if animate:
            frame += 1
            if frame > frames: break
            settings["viewAngle"] = [pi/6, 0, (pi*2)/frames * frame, 0]

            window.fill(c.grey)
            render = Render(window, center, settings, f"{frame}.png")
        else: break

    for e in pg.event.get():
        if e.type == QUIT:
            pg.quit()
            sys.exit()