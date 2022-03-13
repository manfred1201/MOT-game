import math
from random import randint, choice
import time



def brownian_motion(C1, C2):
    c1_spd = math.sqrt((C1.dx ** 2) + (C1.dy ** 2))
    diff_x = -(C1.x - C2.x)
    diff_y = -(C1.y - C2.y)
    vel_x = 0
    vel_y = 0
    if diff_x > 0:
        if diff_y > 0:
            angle = math.degrees(math.atan(diff_y / diff_x))
            vel_x = -c1_spd * math.cos(math.radians(angle))
            vel_y = -c1_spd * math.sin(math.radians(angle))
        elif diff_y < 0:
            angle = math.degrees(math.atan(diff_y / diff_x))
            vel_x = -c1_spd * math.cos(math.radians(angle))
            vel_y = -c1_spd * math.sin(math.radians(angle))
    elif diff_x < 0:
        if diff_y > 0:
            angle = 180 + math.degrees(math.atan(diff_y / diff_x))
            vel_x = -c1_spd * math.cos(math.radians(angle))
            vel_y = -c1_spd * math.sin(math.radians(angle))
        elif diff_y < 0:
            angle = -180 + math.degrees(math.atan(diff_y / diff_x))
            vel_x = -c1_spd * math.cos(math.radians(angle))
            vel_y = -c1_spd * math.sin(math.radians(angle))
    elif diff_x == 0:
        if diff_y > 0:
            angle = -90
        else:
            angle = 90
        vel_x = c1_spd * math.cos(math.radians(angle))
        vel_y = c1_spd * math.sin(math.radians(angle))
    elif diff_y == 0:
        if diff_x < 0:
            angle = 0
        else:
            angle = 180
        vel_x = c1_spd * math.cos(math.radians(angle))
        vel_y = c1_spd * math.sin(math.radians(angle))
    C1.dx = vel_x
    C1.dy = vel_y

def set_color(img, color):
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            img.set_at((x, y), color)  # Set the color of the pixel.