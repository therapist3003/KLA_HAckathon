import math
import numpy as np
import matplotlib.pyplot as plt

class Die:
    def __init__(self, index, lowerLeftCoord):
        self.index = index
        self.llc = lowerLeftCoord

def plot_rect_from_corners(corner_points):
    x = [point[0] for point in corner_points]
    y = [point[1] for point in corner_points]

    rectangle = plt.Polygon(corner_points, closed=True, fill=None, edgecolor='r', linewidth=2)

    ax.add_patch(rectangle)

def rotate_and_translate_homogeneous(points, angle_degrees, translation):
    angle_radians = np.radians(angle_degrees)
    
    rotation_matrix = np.array([[np.cos(angle_radians), -np.sin(angle_radians), 0],
                                 [np.sin(angle_radians), np.cos(angle_radians), 0],
                                 [0, 0, 1]])
    
    translation_matrix = np.array([[1, 0, translation[0]],
                                    [0, 1, translation[1]],
                                    [0, 0, 1]])
    
    # Convert points to homogeneous coordinates
    points_homogeneous = np.hstack((np.array(points), np.ones((len(points), 1))))
    
    # Apply rotation
    rotated_points_homogeneous = np.dot(points_homogeneous, rotation_matrix.T)
    
    # Apply translation
    translated_points_homogeneous = np.dot(rotated_points_homogeneous, translation_matrix.T)
    
    transformed_points = [(round(point[0], 4), round(point[1],4)) for point in translated_points_homogeneous]

    return transformed_points

test_case_no = input('Enter testcase number: ')
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

exclusion_radius = radius - float(lines[7].split(':')[1])
gripper_dim = lines[8].split(':')[1].strip()
gripper_width = float(gripper_dim.split(',')[0][1:])
gripper_height = float(gripper_dim.split(',')[1][:-1])
gripper_angle_str = lines[9].split(':')[1]
gripper_angles = list(map(float, gripper_angle_str.split(',')))

wafer_test_coords = []

for i in range(12, len(lines)):
    coord = lines[i].strip()
    coord = coord.split(',')
    test_coord = (float(coord[0][1:]), float(coord[1][:-1]))

    wafer_test_coords.append(test_coord)

# Plotting wafer circles
fig,ax = plt.subplots()
circleOut = plt.Circle((0,0), radius=wafer_dia/2, color='g', fill=False)
ax.add_artist(circleOut)
circleIn = plt.Circle((0,0), radius=exclusion_radius, color='r', fill=False)
ax.add_artist(circleIn)
ax.set_aspect('equal')
ax.set_xlim(-wafer_dia/2 - 10, wafer_dia/2 + 10)
ax.set_ylim(-wafer_dia/2 - 10, wafer_dia/2 + 10)

# NOTE: Reference point is taken as the midpoint of the gripper line that coincides with circle boundary

# NOTE: For gripper at origin, reference point is mid of right edge
# Common gripper coords
#gripper_right_mid = (0,0)
gripper_top_right = (0, gripper_height/2)
gripper_top_left = (-gripper_width, gripper_height/2)
gripper_bottom_left = (-gripper_width, -gripper_height/2)
gripper_bottom_right = (0, -gripper_height/2)

common_gripper_points = [gripper_bottom_left,gripper_bottom_right, gripper_top_right,gripper_top_left]
plot_rect_from_corners(common_gripper_points)

# List of list - Each list contains four corners of a gripper
grippers = []
# Plotting gripper rectangles
for angle in gripper_angles:
    gripper = rotate_and_translate_homogeneous(common_gripper_points, angle, (radius*np.cos(math.radians(angle)), radius*np.sin(math.radians(angle))))
    grippers.append(gripper)
    plot_rect_from_corners(gripper)

# print(grippers)

def is_point_inside_rectangle(corner_points, point):
    min_x = min(corner_points, key=lambda p: p[0])[0]
    max_x = max(corner_points, key=lambda p: p[0])[0]
    min_y = min(corner_points, key=lambda p: p[1])[1]
    max_y = max(corner_points, key=lambda p: p[1])[1]
    
    # Check if the given point lies within the bounding box
    return min_x <= point[0] <= max_x and min_y <= point[1] <= max_y

# Finds euclidean distance between two 2d coordinates
def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

# Checks whether an input coordinate is inside the wafer 
def pointInCircle(point, rad = exclusion_radius, grippers=grippers):
    if distance((0,0), point) < rad:
        for gripper in grippers:
            if is_point_inside_rectangle(gripper, point):
                return False
        return True
    return False

def pointInDie(point, die_llc):
    if (die_llc[0] <= point[0] <= die_llc[0]+die_width) and (die_llc[1] <= point[1] <= die_llc[1]+die_height):
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

# Takes two floating point coords and returns whether they are close or not
def is_close_coord(coord1, coord2):
    if round(coord1[0], 4) == round(coord2[0], 4) and round(coord1[1], 4) == round(coord2[1], 4):
        return True
    return False

# Returns the corresponding die coordinate for a given wafer coordinate and the lower left corner of the die in wafer coordinate
def relative_die_coord(die_llc, wafer_coord):
    return (round(float(wafer_coord[0])-float(die_llc[0]),4), round(float(wafer_coord[1])-float(die_llc[1]),4))

# Plotting measurement locations
for measurement_loc in wafer_test_coords:
    plt.scatter(measurement_loc[0], measurement_loc[1], color='blue', s=1)

plt.savefig('grippers.png')

res = {}
# DFS
visited = []
stack = []
ref_die_llc = lowerLeftCorner(ref_die)

# Initially indexing dies from the die shift vector. Die at die shift vector is (0,0)
die_at_die_shift = Die((0,0), die_shift_vector)
stack.append(die_at_die_shift)

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

                    if isDieInCircle((curr_die.llc[0]+i*(die_width+die_st_width), curr_die.llc[1]+j*(die_height+die_st_height))):
                        res[(curr_die.index[0]+i, curr_die.index[1]+j)] = die_llc
                    
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

# print(shifted_res)

# Key: Die index, Value: List of wafer test coordinates in their die coordinates
final_res = {}
# To-do: For each inspection wafer coordinate, check which die index contains this wafer coordinate, then return the die index and die coordinate 
for wafer_test_coord in wafer_test_coords:
    for index, die_llc in shifted_res.items():
        if pointInDie(wafer_test_coord, die_llc):
            if index in final_res:
                final_res[index].append(relative_die_coord(die_llc, wafer_test_coord))
            else:
                final_res[index] = [relative_die_coord(die_llc, wafer_test_coord)]


file_path = 'out'+test_case_no+'.txt'
file = open(file_path, 'w')

for index, die_coords_list in final_res.items():
    for die_coord in die_coords_list:
        file.write(f'{str(index)}: {str(die_coord)}\n')