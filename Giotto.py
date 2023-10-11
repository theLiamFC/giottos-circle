from math import *
from numpy import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt

class Giotto:
    def __init__(self, arm1, arm2):
        self.arm1 =  arm1
        self.arm2 = arm2
        self.lastI = [1,1]
        self.mode = "efficiency"

    def __pythag(self,x1,y1,x2,y2):
        return sqrt((x1-x2)**2 + (y1-y2)**2)

    def __findIntersections(self,c1,c2,r1,r2):
        dist = self.__pythag(c1[0],c1[1],c2[0],c2[1])

        # circles don't intersect
        if dist > (r1 + r2):
            raise Exception("OutOfReach")
        # one circle is contained within the other
        elif dist < abs(r1 - r2):
            raise Exception("BadGeometry")
            return (-888, -888)
        # coincident and matching circles
        elif dist == 0 and r1 == r2:
            return (1, 0)
        else:
            a = (r1**2 - r2**2 + dist**2)/(2*dist)
            h = sqrt(r1**2 - a**2)

            x2 = c1[0] + a*(c2[0]-c1[0]) / dist   
            y2 = c1[1] + a*(c2[1]-c1[1]) / dist

            ix1 = x2 + h*(c2[1]-c1[1]) / dist     
            iy1 = y2 - h*(c2[0]-c1[0]) / dist 

            ix2 = x2 - h*(c2[1]-c1[1]) / dist
            iy2 = y2 + h*(c2[0]-c1[0]) / dist
        
            closeness1 = self.__pythag(self.lastI[0],self.lastI[1],ix1,iy1)
            closeness2 = self.__pythag(self.lastI[0],self.lastI[1],ix2,iy2)

            if self.mode == "high":
                if iy1 < iy2:
                    self.lastI = [ix2,iy2]
                    return (ix2, iy2)
                else:
                    self.lastI = [ix1,iy1]
                    return (ix1,iy1)
            elif self.mode == "low":
                if iy1 > iy2:
                    self.lastI = [ix2,iy2]
                    return (ix2, iy2)
                else:
                    self.lastI = [ix1,iy1]
                    return (ix1,iy1)
            elif self.mode == "right":
                if ix1 < ix2:
                    self.lastI = [ix2,iy2]
                    return (ix2, iy2)
                else:
                    self.lastI = [ix1,iy1]
                    return (ix1,iy1)
            elif self.mode == "left":
                if ix1 > ix2:
                    self.lastI = [ix2,iy2]
                    return (ix2, iy2)
                else:
                    self.lastI = [ix1,iy1]
                    return (ix1,iy1)
            else:
                if closeness1 > closeness2:
                    self.lastI = [ix2,iy2]
                    return (ix2, iy2)
                else:
                    self.lastI = [ix1,iy1]
                    return (ix1,iy1)

    def solve(self,x,y):
        [ix, iy] = self.__findIntersections([0,0],[x,y],self.arm1,self.arm2)
        angle1 = 180 / pi * acos(ix/self.arm1)
        if iy < 0:
            angle1 = 360 - angle1
        angle2 = 180 / pi * acos(x-ix/self.arm2)
        if y < iy:
            angle2 = 360 - (angle1 + angle2)
        else:
            angle2 = 360 - (angle1 - angle2)
        return (angle1,angle2)

