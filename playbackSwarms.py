import os
import sys
import constants as c
from swarmSimulation import SWARM_SIMULATION
import pybullet as p
import pyrosim.pyrosim as pyrosim


# Generate world with obstacles ... you could put this in the inner loop, and shift the obstacles by some amount based on "bot" number.  Could do this for bots in diff pos or same pos. 
# pyrosim.Start_SDF("world.sdf")
# pyrosim.Send_Cube(name="Box", pos=[-10,5,.5] , size=[1,1,1])
# pyrosim.End()

overallBot = 0
for swarm in range(c.numberOfSwarms):
    for bot in range(c.botsPerSwarm):
        initialPos = c.botPositions[overallBot % c.botsPerSwarm]      # bot position --> used to determine which part of a grid of obstacles to generate. Also used to keep obstacles closest to bot from generating

        if c.swarmType == 'case1':
            swarmNumber = overallBot // c.botsPerSwarm**2
            botNumber = ( overallBot // c.botsPerSwarm ) % c.botsPerSwarm

        print('\n')
        print(f"{swarmNumber} and {botNumber} and {overallBot}")
        print('\n')

        swarmSim = SWARM_SIMULATION('GUI', swarmNumber, botNumber, overallBot)
        # swarmSim.Create_World(*initialPos)                                        Causes an error whenever it is called. Why?
        swarmSim.Run()
        swarmSim.Get_Fitness()
        swarmSim.Cleanup()
        overallBot += 1




