from particles import Particle
from bus_schedule import BusSchedule
from game_of_life import GameOfLife
from PIL import Image, ImageOps
import numpy as np
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from signal import pause
import time
import random

NUM_PARTICLES = 8
MIDTONE_COLOR = "#fcf876"
HIGHLIGHT_COLOR = "#8bcdcd"

sense = SenseHat()
sense.set_rotation(180)
bus = BusSchedule()
gol = GameOfLife()

sense.clear()
sense.set_pixel(0,0,0,0,255)

def load_colors():
    with open("colormaps.txt") as f:
        colors = f.read().splitlines()

    return colors


def create_particles(num_particles):
    particle_list = []
    for _ in range(num_particles):
        particle_list.append(Particle())
        
    return particle_list


def draw_particle_image(particle_list):
    
    for particle in particle_list:
        particle.engine()
    
    frame = [particle.blurred_matrix for particle in particle_list]
    frame = np.asarray(frame)
    frame = np.sum(frame, axis = 0)
    frame = frame/np.max(frame)
    
    im = Image.fromarray(frame*256).convert("L")
    im = im.resize((8,8), resample=Image.NEAREST)
    im = ImageOps.colorize(im, black="black", mid=MIDTONE_COLOR, white=HIGHLIGHT_COLOR)
    colorlist = list(im.getdata())
    showlist = [list(rgb) for rgb in colorlist]

    return showlist


def draw_gol_image():
    gol.play_game()
    frame = gol.blurred_matrix
    frame = frame / np.max(frame)

    im = Image.fromarray(frame * 256).convert("L")
    im = im.resize((8, 8), resample=Image.NEAREST)
    im = ImageOps.colorize(im, black="black", mid=MIDTONE_COLOR, white=HIGHLIGHT_COLOR)
    colorlist = list(im.getdata())
    showlist = [list(rgb) for rgb in colorlist]

    return showlist


def particle_action(event):
    global HIGHLIGHT_COLOR
    global MIDTONE_COLOR
    if event.action != ACTION_RELEASED:
        colormap = random.choice(colors)
        HIGHLIGHT_COLOR = colormap.split(", ")[0]
        MIDTONE_COLOR = colormap.split(", ")[1]
        
        sense.clear()
        i = 0
        go_rgb = True    
        particle_list = create_particles(NUM_PARTICLES)

        while go_rgb:
            i += 1
            #time.sleep(0.3)
            frame = draw_particle_image(particle_list)
            sense.set_pixels(frame)
            has_pushed = sense.stick.get_events()
            if i > 10:
                if len(has_pushed) > 0:
                       go_rgb = False


def gol_action(event):
    global HIGHLIGHT_COLOR
    global MIDTONE_COLOR
    if event.action != ACTION_RELEASED:
        colormap = random.choice(colors)
        HIGHLIGHT_COLOR = colormap.split(", ")[0]
        MIDTONE_COLOR = colormap.split(", ")[1]

        sense.clear()
        i = 0
        go_rgb = True
        while go_rgb:
            i += 1
            #time.sleep(0.3)
            frame = draw_gol_image()
            sense.set_pixels(frame)
            has_pushed = sense.stick.get_events()
            if i > 10:
                if len(has_pushed) > 0:
                       go_rgb = False


def bus_action(event):
    if event.action != ACTION_RELEASED:
        naechster = bus.next_bus()
        sense.show_message(naechster)


colors = load_colors()
sense.stick.direction_up = particle_action
sense.stick.direction_down = bus_action
sense.stick.direction_middle = sense.clear
sense.stick.direction_right = gol_action

pause()
