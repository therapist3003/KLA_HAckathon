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
    if distance((0,0), point) <= rad:
        return True
    return False

# Checks whether the die (partial/complete) is inside the wafer
# IDEA: Even if one corner of the die is inside the wafer, then the die is inside the wafer 
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

# Wafer Plotting

