import numpy
import pyrosim.pyrosim as pyrosim
import pybullet as p
import os
import random
import time
import constants as c





# Create a new file which starts up the virtual environment and generates some stuff in it. there should be one of the first things 
class OBSTACLE_WORLD:
    def __init__(self):        
        self.planeId = p.loadURDF("plane.urdf")
        p.loadSDF("obstacleWorld.sdf")


    def Create_World(self):

        pyrosim.Start_SDF("obstacleWorld.sdf")
        for x in range(-5, -15,-2):
                for y in range(-4, 10, 2):
                    pyrosim.Send_Cube(name="Box", pos=[x,y,.5] , size=[1/3,1/3,1/3]) 
        pyrosim.End()