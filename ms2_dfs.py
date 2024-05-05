class Die:
    def __init__(self, index, coord):
        self.index = index
        self.coordinate = coord

import math
import numpy as np

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

# Finds euclidean distance between two 2d coordinates
def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

# Checks whether an input coordinate is inside the wafer 
def pointInCircle(point, rad = radius):
    if distance((0,0), point) < rad:
        return True
    return False

def getMidPoint(point1, point2):
    return ((point1[0] + point2[0])/2, (point1[1] + point2[1])/2)
            
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
    
# Given the centre coordinate of the die w.r.t the wafer, it returns the lower left coordinate (w.r.t wafer) of the die
def lowerLeftCorner(die_centre):
    return (float(die_centre[0])-(die_width/2), float(die_centre[1])-(die_height/2))

# Dictionary to hold final result
# Keys: Die indices, Values: LLC values

res = {}
res[(0,0)] = lowerLeftCorner(ref_die)

ref_die_obj = Die((0,0), lowerLeftCorner(ref_die))
visited = []

# DFS
stack = []
visited.append((0,0))
stack.append(ref_die_obj)

while stack:
    curr_die = stack.pop()
    up = Die((curr_die.index[0], curr_die.index[1]+1), (curr_die.coordinate[0], curr_die.coordinate[1]+die_height))
    down = Die((curr_die.index[0], curr_die.index[1]-1), (curr_die.coordinate[0], curr_die.coordinate[1]-die_height))
    right = Die((curr_die.index[0]+1, curr_die.index[1]), (curr_die.coordinate[0]+die_width, curr_die.coordinate[1]))
    left = Die((curr_die.index[0]-1, curr_die.index[1]), (curr_die.coordinate[0]-die_width, curr_die.coordinate[1]))

    neighbors = [up, down, right, left]

    for neighbor in neighbors:
        if isDieInCircle(neighbor.coordinate) and neighbor.index not in visited:
            visited.append(neighbor.index)
            res[neighbor.index] = neighbor.coordinate
            stack.append(neighbor)

file_path = 'out'+test_case_no+'.txt'
file = open(file_path, 'w')

for key, value in res.items():
    file.write(f'{str(key)}: {str(value)}\n')
