from math import *
from numpy import *
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt
import Giotto

# create Giotto instance
robot = Giotto.Giotto(1,1)
robot.mode = "efficiency"

# start MQTT client
talk = mqtt.Client('itsLiam')
talk.connect('67.253.32.232')

# start matplotlib plot
fig, ax = plt.subplots()
ax.axhline(y=0, color='grey')
ax.axvline(x=0, color='grey')
plt.ylim(-1,2)
plt.xlim(-1,2)

# function to check the output of Giotto and graph its results
def checkGiotto(A,B,a1,a2):
    a1 = a1 * pi / 180
    a2 = a2 * pi / 180

    x1 = A*cos(a1) 
    x2 = x1 + B*cos(a1+a2)
    y1 = A*sin(a1) 
    y2 = y1 + B*sin(a1+a2)

    # alter the below lines to control graph output
    ax.plot([x1,0], [y1,0], linestyle="--",color='grey')
    ax.plot([x1,x2], [y1,y2], linestyle="-")
    ax.scatter(x2,y2,s=20)
    #fig.savefig('my_plot.png')
    #time.sleep(0.08)
    #plt.cla()
    #ax.axhline(y=0, color='grey')
    #ax.axvline(x=0, color='grey')
    #plt.ylim(-1,2)
    #plt.xlim(-1,2)

    return x2, y2

# number of points to graph
fidelity = 30

# loop to get points on a circle
for i in range(fidelity):
    # circle:
    x = .5*cos(i*2*pi/fidelity) + 1
    y = .5*sin(i*2*pi/fidelity)
    
    try:
        angs = robot.solve(x,y)
        msg = "("+str(angs[0])+","+str(angs[1])+")"
        print("Published: ", msg)
        talk.publish('ME035',msg)
        cx, cy = checkGiotto(1,1,angs[0],angs[1])
        if abs(x - cx) > 0.05 or abs(y - cy) > 0.05:
            print("Target: ", x, y)
            print("Angles: ", angs[0],angs[1])
            print("Result: ",cx, cy)
    except Exception as e:
        print(e)

# SECRET CODE:
# THIS LOOP MAY OR MAY NOT PROVIDE COORDINATES TO 
# DRAW A VERY ROUGH SKETCH OF CHRIS ROGERS
# IT HAS NOT BEEN TESTED AND WILL LIKELY BE A VERY BAD SKETCH
points="78.3 115.96 68.54 102.19 69.86 93.02 75.33 83.82 76.58 70.67 71.1 84.21 67.26 94.2 55.05 100.95 45.54 96.93 37.4 88.56 32.09 76.89 35 76.03 41.53 76.56 46.9 81.81 54.25 83.09 62.33 83.8 66.65 78.49 69.12 75.03 63.37 76.2 56.28 77.62 49.61 77.56 42.94 76.9 46.62 81 58.97 80.41 69.12 75.03 51.46 75.06 59.24 72.42 59.61 67.51 57.94 70.03 51.05 70.61 48.22 68.69 48.65 65.05 50.75 60.39 51.14 54.97 49.42 50.33 46.1 49 42.43 46.28 33.82 45.62 28.61 49.42 35.73 52.39 46.57 52.39 42.43 46.28 38.78 45.45 36.31 49.21 38.58 52.71 40.87 49.28 38.78 45.45 33.19 44.89 32.47 41.74 35.82 35.45 35.25 25.02 40.74 22.76 54.72 24.19 66.72 22.64 72.18 25.82 74.19 29.55 73.67 32 73.23 39.94 73.96 44.89 70.6 47.05 65.21 45.2 62.33 47.91 57.01 50.76 56.36 52.12 59.61 54.54 64.44 54.22 66.81 50.53 65.07 45.94 62.33 51.38 65.62 54.25 71.46 47.57 74.89 54.46 76.22 53.85 77.51 64.23 81.75 59.99 79.12 57.38 84.11 56.34 80.69 53.95 84.11 52.83 87.98 51.52 80.69 49.92 87.24 46.01 81.94 44.78 88.13 41.09 82.88 39.86 86.57 33.16 80.2 33.16 82.26 26.45 76.87 28.91 81.01 22.29 76.06 22.63 76.61 15.37 72.18 16.94 72.18 12.85 69.89 13.48 66.04 7.92 56.36 6.87 47.81 .57 37.9 4.87 29.3 5.96 23 12.43 15.25 17.46 11.04 30.58 6.95 39.81 9.15 46.21 6.95 54.6 11.25 63.1 11.46 71.39 18.16 73.76 23.45 94.24 19.28 95.95 13.81 107.03 .24 114.38"
points = points.split()
print(len(points))

for i in range(113):

    x = (int(float(points[2*i])) + 130) / 175
    y = (134 - int(float(points[2*i+1])) - 67) / 175
    
    try:
        angs = robot.solve(x,y)
        msg = "("+str(angs[0])+","+str(angs[1])+")"
        print("Published: ", msg)
        talk.publish('ME035',msg)
        cx, cy = checkGiotto(1,1,angs[0],angs[1])
        if abs(x - cx) > 0.05 or abs(y - cy) > 0.05:
            print("Target: ", x, y)
            print("Angles: ", angs[0],angs[1])
            print("Result: ",cx, cy)
    except Exception as e:
        print(e)

fig.savefig('my_plot.png')
