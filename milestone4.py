'''NOTE: Make sure that in DieCoordinates at line 9 of input file has no space after the comma within the tuple'''

import math
import numpy as np
import matplotlib.pyplot as plt

class Die:
    def __init__(self, index, lowerLeftCoord):
        self.index = index
        self.llc = lowerLeftCoord
test_case_no = input('Enter testcase number: ')

# Takes two floating point coords and returns whether they are close or not
def is_close_coord(coord1, coord2):
    if round(coord1[0], 4) == round(coord2[0], 4) and round(coord1[1], 4) == round(coord2[1], 4):
        return True
    return False

file = open('Testcase' + test_case_no+'.txt', 'r')
lines = file.readlines()

wafer_dia = float(lines[0].split(':')[1])
radius = wafer_dia/2

die_dim = lines[1].split(':')[1].strip()
die_width = float(die_dim.split(',')[0][1:])
die_height = float(die_dim.split(',')[1][:-1])

die_shift_temp = lines[2].split(':')[1].strip()

die_shift_vector = (float(die_shift_temp.split(',')[0][1:]), float(die_shift_temp.split(',')[1][:-1]))

ref_die_temp = lines[3].split(':')[1].strip()
ref_die = (float(ref_die_temp.split(',')[0][1:]), float(ref_die_temp.split(',')[1][:-1]))

die_street_temp = lines[4].split(':')[1].strip()
die_st_width = float(die_street_temp.split(',')[0][1:])
die_st_height = float(die_street_temp.split(',')[1][:-1])

ret_street_temp = lines[5].split(':')[1].strip()
ret_st_width = float(ret_street_temp.split(',')[0][1:])
ret_st_height = float(ret_street_temp.split(',')[1][:-1])

reticle_temp = lines[6].split(':')[1].strip()
reticle_rows = int(reticle_temp.split('x')[0])
reticle_cols = int(reticle_temp.split('x')[1])

inner_rad = float(lines[7].split(':')[1])
die_location_coords_str = lines[8].split(':')[1].split()
die_location_coords = []

for str_tuple in die_location_coords_str:
    die_location_coords.append((float(str_tuple.split(',')[0][1:]), float(str_tuple.split(',')[1][:-1])))
    print(die_location_coords[-1])

# Finds euclidean distance between two 2d coordinates
def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

# Checks whether an input coordinate is inside the wafer 
def pointInCircle(point, rad = radius):
    if distance((0,0), point) < rad:
        return True
    return False

def getMidPoint(point1, point2):
    return (round((point1[0] + point2[0])/2, 4), round((point1[1] + point2[1])/2, 4))
            
# Checks whether the die (partial/complete) is inside the wafer
# IDEA: Even if one corner of the die is inside the wafer or one midpoint, then the die is inside the wafer 
def isDieInCircle(die_llc):
    # if not pointInCircle(die_centre):
    #     print('Point whose center not inside wafer: ', die_centre)
    die_top_left = (die_llc[0], die_llc[1]+die_height)
    die_top_right = (die_llc[0] + die_width, die_llc[1]+die_height)
    die_bottom_right = (die_llc[0]+die_width, die_llc[1])

    die_top_mid = getMidPoint(die_top_left, die_top_right)
    die_right_mid = getMidPoint(die_top_right, die_bottom_right)
    die_bottom_mid = getMidPoint(die_llc, die_bottom_right)
    die_left_mid = getMidPoint(die_top_left, die_llc)

    if pointInCircle(die_top_left) or pointInCircle(die_top_right) or pointInCircle(die_llc) or pointInCircle(die_bottom_right) or pointInCircle(die_top_mid) or pointInCircle(die_right_mid) or pointInCircle(die_bottom_mid) or pointInCircle(die_left_mid):
        return True
# IDEA: If no corners inside & one midpt inside => die intersects inner circle
#       Else 1 or 2 or 3 corners inside => die intersects inner circle
#       Else => die DOES NOT intersect inner circle
def isDieIntersectsInnerCircle(die_llc):
    # bottom left, bottom right, top right, top left
    corners = [die_llc, (die_llc[0]+die_width, die_llc[1]), (die_llc[0]+die_width, die_llc[1]+die_height), (die_llc[0], die_llc[1]+die_height)]
    # bottom mid, right mid, top mid, left mid
    midpoints = [getMidPoint(corners[0], corners[1]), getMidPoint(corners[1], corners[2]), getMidPoint(corners[2], corners[3]), getMidPoint(corners[3], corners[0])]

    in_corner_count = 0
    for corner in corners:
        if pointInCircle(corner, inner_rad):
            in_corner_count += 1

    in_midpoint_count = 0
    for midpoint in midpoints:
        if pointInCircle(midpoint, inner_rad):
            in_midpoint_count += 1

    if in_corner_count == 0 and in_midpoint_count == 1:
        return True
    elif in_corner_count == 1 or in_corner_count == 2 or in_corner_count == 3:
        return True
    else:
        return False

def isReticleInCircle(reticle_llc):
    res = False

    for i in range(reticle_cols): # x should be incremented reticle_col times
        for j in range(reticle_rows): # y should be incremented reticle_row times
            if isDieInCircle((reticle_llc[0] + i*(die_width+die_st_width), reticle_llc[1] + j*(die_height+die_st_height))):
                res = True
                break
        if res:
            break
    return res

# Given the centre coordinate of the die w.r.t the wafer, it returns the lower left coordinate (w.r.t wafer) of the die
def lowerLeftCorner(die_centre):
    return (round(float(die_centre[0])-(die_width/2),4), round(float(die_centre[1])-(die_height/2),4))

# Dictionary to hold final result
# Keys: Die indices, Values: LLC values

res = {}

# DFS
visited = []
stack = []
ref_die_llc = lowerLeftCorner(ref_die)

# Initially indexing dies from the die shift vector. Die at die shift vector is (0,0)
die_at_die_shift = Die((0,0), die_shift_vector)
stack.append(die_at_die_shift)

# Modelling: Each lower left corner die in the reticle is made as the representative of the reticle
while stack:
    curr_die = stack.pop()

    if curr_die.index in visited: # Already visisted reticle case
        continue
    visited.append(curr_die.index)

    # Checking for all dies in the current reticle
    if isDieInCircle(curr_die.llc) or isReticleInCircle(curr_die.llc):
        if curr_die.index not in res:
            for i in range(reticle_cols):
                for j in range(reticle_rows):
                    # Extracting die llc for each die within a reticle
                    die_llc = (curr_die.llc[0] + i*(die_width + die_st_width), curr_die.llc[1] + j*(die_height + die_st_height))

                    # Checking whether reference die is reached, to store reference die index with die at die_shift_vector as (0,0)
                    if is_close_coord(die_llc, ref_die_llc):
                        index_shift = (curr_die.index[0]+i, curr_die.index[1]+j)

                    # Try changing this to isDieInInnerCircle
                    if isDieInCircle(die_llc) and isDieIntersectsInnerCircle(die_llc):
                        die_ref_coords = []
                        for location in die_location_coords:
                            inside_die_coord = (die_llc[0] + location[0], die_llc[1] + location[1])
                            if pointInCircle(inside_die_coord, inner_rad):
                                die_ref_coords.append(inside_die_coord)

                        res[(curr_die.index[0]+i, curr_die.index[1]+j)] = die_ref_coords
                    
            up = Die((curr_die.index[0], curr_die.index[1]+reticle_rows), (curr_die.llc[0], curr_die.llc[1] + reticle_rows*(die_height+die_st_height) + ret_st_height))
            down = Die((curr_die.index[0], curr_die.index[1]-reticle_rows), (curr_die.llc[0], curr_die.llc[1] - reticle_rows*(die_height+die_st_height) - ret_st_height))
            right = Die((curr_die.index[0]+reticle_cols, curr_die.index[1]), (curr_die.llc[0] + reticle_cols*(die_width+die_st_width) + ret_st_width, curr_die.llc[1]))
            left = Die((curr_die.index[0]-reticle_cols, curr_die.index[1]), (curr_die.llc[0] - reticle_cols*(die_width+die_st_width) - ret_st_width, curr_die.llc[1]))

            stack.append(up)
            stack.append(down)
            stack.append(right)
            stack.append(left)

shifted_res = {}
# Shifting the grid
for index in res:
    shifted_res[(index[0]-index_shift[0], index[1]-index_shift[1])] = res[index]

file_path = 'out'+test_case_no+'.txt'
file = open(file_path, 'w')

for index, coords_list in shifted_res.items():
    for coord in coords_list:
        file.write(f'{str(index)}: {str(coord)}\n')