"""
right click on PreonSolver1
Export Particles
Preset = HoudiniFX (geo)
Start frame = end frame
Untick everything except velocity and position
Browse where you want your file
set in the following code : file = "YOURFILE.geo"
"""

import pandas as pd
import numpy as np

#User data
file = "000017.geo" #your geo file

xmin = -0.094 #volume of interest
xmax = 0
ymin = -0.08
ymax = 0
zmin = -0.2
zmax = 0

wheel_center = np.array([0.1, 0.3, 0.02]) #position of wheel center
wheel_axis = np.array([0, 1, 0])

#Parsing
with open(file, "r") as f1:
    lines = f1.readlines()
with open("clean" + file, "w") as f2:
    for line in lines:
        if line.split(" ")[0].replace('.','',1).replace('-','',1).isnumeric():
            f2.write(line.replace('(','',1).replace(')','',1))

file = "clean" + file
df = pd.read_csv(file, delimiter=' ')
df.columns = ['x', 'y', 'z', 'o', 'u', 'v', 'w']

#Code
interest = df.loc[(df['x'] >= xmin) & (df['x'] <= xmax) & (df['y'] >= ymin) & (df['y'] <= ymax) & (df['z'] >= zmin) & (df['z'] <= zmax)]
XYZ = np.array([interest["x"].mean(), interest["y"].mean(), interest["z"].mean()])
UVW = np.array([interest["u"].mean(), interest["v"].mean(), interest["w"].mean()])

#Project
other_axis = np.array([1, 1, 1]) - wheel_axis
tangentvector = np.cross(wheel_center*other_axis - XYZ*other_axis, wheel_axis) #Produit vectoriel pour avoir le vecteur directeur de la tangente au pignon
tangentvector = tangentvector / np.linalg.norm(tangentvector)
radialvector = wheel_center*other_axis - XYZ*other_axis
radialvector = radialvector / np.linalg.norm(radialvector)

Vtangentielle = np.dot(UVW, tangentvector)
Vradiale = np.dot(UVW, radialvector)
Vorthoradiale = np.dot(UVW, wheel_axis)

print("Vtangentielle = ", str(Vtangentielle) + " m/s")
print("Vradiale = ", str(Vradiale) + " m/s")
print("Vorthoradiale = ", str(Vorthoradiale) + " m/s")




