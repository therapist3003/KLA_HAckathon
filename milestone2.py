import math
import numpy as np

file = open('Testcase4.txt', 'r')
lines = file.readlines()

wafer_dia = float(lines[0].split(':')[1])
radius = wafer_dia/2

die_dim= lines[1].split(':')[1]
die_width = float(die_dim.split('x')[0])
die_height = float(die_dim.split('x')[1])

die_shift_temp = (lines[2].split(':')[1])
die_shift_vector = (float(die_shift_temp.split(',')[0][1:]), float(die_shift_temp.split(',')[1][:-2]))
# print(die_shift_vector)

ref_die_temp = (lines[3].split(':')[1])
ref_die = (float(ref_die_temp.split(',')[0][1:]), float(ref_die_temp.split(',')[1][:-1]))
# print(ref_die)

def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def pointInCircle(point, rad = radius):
    if distance((0,0), point) <= rad:
        return True
    return False

def isDieInCircle(die_centre):
    # if not pointInCircle(die_centre):
    #     print('Point whose center not inside wafer: ', die_centre)
    die_top_left = (die_centre[0]-(die_width/2), die_centre[1]+(die_height/2))
    die_top_right = (die_centre[0]+(die_width/2), die_centre[1]+(die_height/2))
    die_bottom_left = (die_centre[0]-(die_width/2), die_centre[1]-(die_height/2))
    die_bottom_right = (die_centre[0]+(die_width/2), die_centre[1]-(die_height/2))

    if pointInCircle(die_top_left) or pointInCircle(die_top_right) or pointInCircle(die_bottom_left) or pointInCircle(die_bottom_right):
        return True
    return False

def lowerLeftCorner(die_centre):
    return (float(die_centre[0])-(die_width/2), float(die_centre[1])-(die_height/2))

x_axis_ends = [(-radius,0), (radius,0)]
y_axis_ends = [(0,-radius), (0,radius)]

x_axis_ends = [tup + die_shift_vector for tup in x_axis_ends]
y_axis_ends = [tup + die_shift_vector for tup in y_axis_ends]


res = {}
res[(0,0)] = lowerLeftCorner(ref_die)

row_index, col_index = 0,0

# 1st quadrant
#row loop
while True:
    #col loop
    col_index = 0
    while True:
        if row_index == 0 and col_index==0:
            col_index += 1
            continue

        curr_die = [ref_die[0] + row_index*die_width, ref_die[1] + col_index*die_height]
        if isDieInCircle(curr_die):
            res[(row_index,col_index)] = lowerLeftCorner(curr_die)
            col_index += 1
        else:
            break
    row_index += 1
    col_index = 0
    curr_die = [ref_die[0] + row_index*die_width, ref_die[1] + col_index*die_height]
    if not isDieInCircle(curr_die):
        break

row_index, col_index = 0,0

#2nd quadrant
while True:
    #col loop
    col_index = 0
    while True:
        if row_index == 0 and col_index==0:
            col_index += 1
            continue

        curr_die = [ref_die[0] + row_index*die_width, ref_die[1] + col_index*die_height]
        if isDieInCircle(curr_die):
            res[(row_index,col_index)] = lowerLeftCorner(curr_die)
            col_index += 1
        else:
            break
    row_index -= 1
    col_index = 0
    curr_die = [ref_die[0] + row_index*die_width, ref_die[1] + col_index*die_height]
    if not isDieInCircle(curr_die):
        break

row_index, col_index = 0,0
#3rd quadrant
while True:
#col loop
    col_index = 0
    while True:
        if row_index == 0 and col_index==0:
            col_index -= 1
            continue

        curr_die = [ref_die[0] + row_index*die_width, ref_die[1] + col_index*die_height]
        if isDieInCircle(curr_die):
            res[(row_index,col_index)] = lowerLeftCorner(curr_die)
            col_index -= 1
        else:
            break
    row_index -= 1
    col_index = 0
    curr_die = [ref_die[0] + row_index*die_width, ref_die[1] + col_index*die_height]
    if not isDieInCircle(curr_die):
        break
    
row_index, col_index = 0,0
#4th quadrant
while True:
#col loop
    col_index = 0
    while True:
        if row_index == 0 and col_index==0:
            col_index -= 1
            continue

        curr_die = [ref_die[0] + row_index*die_width, ref_die[1] + col_index*die_height]
        if isDieInCircle(curr_die):
            res[(row_index,col_index)] = lowerLeftCorner(curr_die)
            col_index -= 1
        else:
            break
    row_index += 1
    col_index = 0
    curr_die = [ref_die[0] + row_index*die_width, ref_die[1] + col_index*die_height]
    if not isDieInCircle(curr_die):
        break

file_path = 'out4.txt'

with open(file_path, 'w') as file:
    for key, value in res.items():
        file.write(f'{str(key)}: {str(value)}\n')