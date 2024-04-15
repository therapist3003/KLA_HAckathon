import math
import numpy as np
from sympy import symbols, Eq, solve

import matplotlib.pyplot as plt

x, y = symbols('x y')

def get_circle_eqn(radius, centre=(0,0)):
    global x, y
    h, k = centre
    equation = Eq((x-h)**2 + (y-k)**2, radius**2)
    return equation

def get_line_eqn(point1, point2):
    global x, y
    x1, y1 = point1
    x2, y2 = point2

    if x2-x1 != 0:
        slope = (y2-y1)/(x2-x1)
    else:
        slope = float('inf')

    if slope != float('inf'):
        equation = Eq(y-y1, slope*(x-x1))
    else:
        equation = Eq(x, x1)

    return equation

def is_point_on_line(point, line_end1, line_end2):
    if line_end1[0] <= point[0] and point[0] <= line_end2[0] and line_end1[1] <= point[1] and point[1] <= line_end2[1]:
        return True
    else:
        return False

test_case_no = input('Enter testcase number: ')

file = open('Testcase' + test_case_no+'.txt', 'r')
lines = file.readlines()

wafer_dia = float(lines[0].split(':')[1])
radius = wafer_dia/2

die_dim = lines[1].split(':')[1]
die_width = float(die_dim.split('x')[0])
die_height = float(die_dim.split('x')[1])

die_shift_temp = (lines[2].split(':')[1])

die_shift_vector = (float(die_shift_temp.split(',')[0][1:]), float(die_shift_temp.split(',')[1][:-2]))
#print(die_shift_vector)

ref_die_temp = (lines[3].split(':')[1])
ref_die = (float(ref_die_temp.split(',')[0][1:]), float(ref_die_temp.split(',')[1][:-1]))
# print(ref_die)

circle_eqn = get_circle_eqn(radius)

# Finds euclidean distance between two 2d coordinates
def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

# Checks whether an input coordinate is inside the wafer 
def pointInCircle(point, rad = radius):
    if distance((0,0), point) < rad:
        return True
    return False

# Checks whether the die (partial/complete) is inside the wafer
# IDEA: Even if one corner of the die is inside the wafer, then the die is inside the wafer 
# New IDEA: If atleast one line segment intersects the circle, then die is inside wafer
def isDieInCircle(die_centre):
    global x, y
    # if not pointInCircle(die_centre):
    #     print('Point whose center not inside wafer: ', die_centre)
    die_top_left = (die_centre[0]-(die_width/2), die_centre[1]+(die_height/2))
    die_top_right = (die_centre[0]+(die_width/2), die_centre[1]+(die_height/2))
    die_bottom_left = (die_centre[0]-(die_width/2), die_centre[1]-(die_height/2))
    die_bottom_right = (die_centre[0]+(die_width/2), die_centre[1]-(die_height/2))

    line_segments = [[die_top_left, die_top_right], [die_top_right, die_bottom_right], [die_bottom_right, die_bottom_left], [die_bottom_left, die_top_left]]

    if pointInCircle(die_top_left) or pointInCircle(die_top_right) or pointInCircle(die_bottom_left) or pointInCircle(die_bottom_right):
        return True
    
    # If no corner point is inside the wafer, then check if any line segment intersects the wafer
    real_solutions = []
    for line_segment in line_segments:
        line_eqn = get_line_eqn(line_segment[0], line_segment[1])

        intersect_points = solve((line_eqn, circle_eqn), x, y)

        for point in intersect_points:
            if point[0].is_real and point[1].is_real:
                real_solutions.append(point)
        
    points_inside_wafer = []

    for point in real_solutions:
        for line_segment in line_segments:
            if is_point_on_line(point, line_segment[0], line_segment[1]):
                points_inside_wafer.append(point)

    if len(points_inside_wafer):
        return True
    return False
    
# Given the centre coordinate of the die w.r.t the wafer, it returns the lower left coordinate (w.r.t wafer) of the die
def lowerLeftCorner(die_centre):
    return (float(die_centre[0])-(die_width/2), float(die_centre[1])-(die_height/2))

# Dictionary to hold final result
# Keys: Die indices, Values: LLC values

res = {}
res[(0,0)] = lowerLeftCorner(ref_die)

# Denotes the first die that is to be scanned for the ith quadrant after (0,0)
beginning_indices = [(0,1), (0,1), (0,-1), (0,-1)]

# Repeating for 4 quadrants
for i in range(4):
    row_index, col_index = beginning_indices[i]

    #row loop
    while True:
        #col loop
        while True:
                # Finding current die coordinate
                curr_die = [ref_die[0] + row_index*die_width, ref_die[1] + col_index*die_height]
                
                if isDieInCircle(curr_die):
                    res[(row_index,col_index)] = lowerLeftCorner(curr_die)
                    
                    # For 1,2 quadrants, traverse in positive y-axis
                    if i==0 or i==1:    
                        col_index += 1

                    # For 3,4 quadrants, traverse in negative y-axis
                    else:
                        col_index -= 1
                else:
                    break
        
        # For 1,4 quadrants, traverse in positive x-axis
        if i==0 or i==3:
            row_index += 1
        # For 2,3 quadrants, traverse in negative x-axis
        else:
            row_index -=1

        # Irrespective of quadrant, once a vertical traversal goes out of the wafer, we return to the next vertical column, so resetting column index to 0
        col_index = 0

        # If the very first die in a vertical traversal is outside the wafer, it means all dies in the current quadrant have been scanned
        curr_die = [ref_die[0] + row_index*die_width, ref_die[1] + col_index*die_height]
        if not isDieInCircle(curr_die):
            break

file_path = 'out'+test_case_no+'.txt'

with open(file_path, 'w') as file:
    for key, value in res.items():
        file.write(f'{str(key)}: {str(value)}\n')

# Trying manual plotting
fig,ax = plt.subplots()
circle = plt.Circle((0,0), radius=wafer_dia/2, color='r', fill=False)
ax.add_artist(circle)
ax.set_aspect('equal')
ax.set_xlim(-wafer_dia/2 - 10, wafer_dia/2 + 10)
ax.set_ylim(-wafer_dia/2 - 10, wafer_dia/2 + 10)

for key, val in res.items():
    #ax.text(val[0]+die_width/2, val[1]+die_height/2, str(key), fontsize=6, ha='center', va='center')
    die_rad = 0.2
    die_index_str = ' '.join(map(str, key))
    #ax.text(val[0]+die_width/2, val[1]+die_height/2, die_index_str, fontsize=6, ha='center', va='center', bbox=dict(boxstyle='circle', fc='white', ec='black', pad=0.3))

    die_rect_coord = [val[0], val[1]]

    rect = plt.Rectangle(die_rect_coord, die_width, die_height, fill=False, edgecolor='black', linewidth=1)
    ax.add_patch(rect)

plt.show()
