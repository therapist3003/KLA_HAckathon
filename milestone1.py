import math
import numpy as np

file = open('Testcase4.txt', 'r')
lines = file.readlines()

wafer_dia = float(lines[0].split(':')[1])
radius = wafer_dia/2

num_points = int(lines[1].split(':')[1])
angle = float(lines[2].split(':')[1])

centre = (0,0)
slope = math.tan(math.radians(angle))
angle_radians = math.radians(angle)

#Using polar coordinates (rcos theta, rsin theta)
new_line_x_vals = np.linspace(-radius*math.cos(angle_radians), radius*math.cos(angle_radians), num_points)
new_line_y_vals = [slope*x_val for x_val in new_line_x_vals]

res = []
for i in range(num_points):
    res.append((new_line_x_vals[i], new_line_y_vals[i]))

with open('out4.txt', 'w') as out_file:
    for tup in res:
        out_file.write(str(tup) + '\n')