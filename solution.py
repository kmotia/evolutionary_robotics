import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c
import math
#-----------------------------------------------------------------------------------------


class SOLUTION:
    def __init__(self, nextAvailableID, overallBot):
        self.myID = nextAvailableID
        self.overallBot = int(overallBot)
        self.swarmNumber = math.floor(self.overallBot / c.botsPerSwarm)
        self.botNumber = self.overallBot % c.botsPerSwarm
        self.initialPos = c.botPositions[self.botNumber]                    # give solution.py the bot number


        self.weights = np.random.rand(c.numSensorNeurons,c.numMotorNeurons)
        self.weights = self.weights * 2 - 1
        
        # Load weights from disk if continuing evolution 
        if c.continueEvolution == True: 
            with open(f'weights/weights_{self.overallBot}_{self.myID}.txt', 'r') as f:
                self.weights = np.loadtxt(f)




    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-10,5,.5] , size=[1,1,1])
        pyrosim.End()

    def Generate_Body(self, xi, yi, zi=1):
        if c.swarmType == 'case1' or 'case2':
            pyrosim.Start_URDF(f"bodies/body_{self.botNumber}.urdf")            # differentiate files by 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
        elif c.swarmType == 'case3':
            pyrosim.Start_URDF(f"bodies/body_{self.overallBot}_{self.myID}.urdf")   # differentiate files by their evolution traits ie overallBot and myID since we evolve body for case3

        # Root link
        pyrosim.Send_Cube(name="Torso", pos=[xi, yi, zi], size=[1,1,1])

        # Upper joints (from root link)
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[xi, yi+0.5,zi], jointAxis="1 0 1")
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[xi, yi-0.5,zi], jointAxis="1 0 1")
        pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute", position=[xi-0.5, yi, zi], jointAxis="0 1 1")
        pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute", position=[xi+0.5, yi, zi], jointAxis="0 1 1")

        # LowerLeg joints
        pyrosim.Send_Joint(name="FrontLeg_FrontLowerLeg", parent="FrontLeg", child="FrontLowerLeg", type="revolute", position=[0,1,0], jointAxis="1 0 1")
        pyrosim.Send_Joint(name="BackLeg_BackLowerLeg", parent="BackLeg", child="BackLowerLeg", type="revolute", position=[0,-1,0], jointAxis="1 0 1")
        pyrosim.Send_Joint(name="LeftLeg_LeftLowerLeg", parent="LeftLeg", child="LeftLowerLeg", type="revolute", position=[-1,0,0], jointAxis="0 1 1")
        pyrosim.Send_Joint(name="RightLeg_RightLowerLeg", parent="RightLeg", child="RightLowerLeg", type="revolute", position=[1,0,0], jointAxis="0 1 1")

        # Upper legs
        pyrosim.Send_Cube(name="FrontLeg", pos=[0,0.5,0], size=[0.2,1,0.2])
        pyrosim.Send_Cube(name="BackLeg", pos=[0,-0.5,0], size=[0.2,1,0.2])
        pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5,0,0], size=[1,0.2,0.2])
        pyrosim.Send_Cube(name="RightLeg", pos=[0.5,0,0], size=[1,0.2,0.2])

        # LowerLeg legs
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0,0,-0.5], size=[0.2,0.2,1])
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0,0,-0.5], size=[0.2,0.2,1])
        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0,0,-0.5], size=[0.2,0.2,1])
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0,0,-0.5], size=[0.2,0.2,1])

        pyrosim.End()
        #exit() # uncommenting this allows you to see effects of code on body.urdf

    def Generate_Brain(self): 
        pyrosim.Start_NeuralNetwork("brains/brain_" + str(self.overallBot) + "_" + str(self.myID) + ".nndf")

        # Note: Do not add neuron for Torso. Root links have the same index as SDF links, so their touchValues will be conflated. 

        # Sensor neurons (only lower legs)
        pyrosim.Send_Sensor_Neuron(name=0, linkName="FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="RightLowerLeg")

        # Upper motor neurons
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name=5, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=6, jointName="Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name=7, jointName="Torso_RightLeg")

        # Lower motor neurons
        pyrosim.Send_Motor_Neuron(name=8, jointName="FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron(name=9, jointName="BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron(name=10, jointName="LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name=11, jointName="RightLeg_RightLowerLeg")

        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn+c.numSensorNeurons , weight = self.weights[currentRow][currentColumn] )

        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0,c.numSensorNeurons - 1) 
        randomColumn = random.randint(0,c.numMotorNeurons - 1)
        self.weights[randomRow, randomColumn] = random.random() * 2 - 1


    def Save_Weights(self):
        file_path = f'weights/weights_{self.overallBot}_{self.myID}.txt'
        with open(file_path, 'w') as f: 
            np.savetxt(f,self.weights)
                      

    def Start_Simulation(self, directOrGUI):
        self.Generate_Body(*self.initialPos)   # (0,0,1)
        self.Generate_Brain()
        self.Create_World()
        os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID) + " " + str(self.overallBot) + " &")

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("fitness" + str(self.overallBot) + "_" + str(self.myID) + ".txt"):
            time.sleep(0.01)

        f = open("fitness" + str(self.overallBot) + "_" + str(self.myID) + ".txt","r")
        time.sleep(0.1)
        lines = f.read()
        time.sleep(0.1)
        self.fitness = float(lines)
        f.close()

        os.system("rm fitness" + str(self.overallBot) + "_" + str(self.myID) + ".txt")
        while os.path.exists("rm fitness" + str(self.overallBot) + "_" + str(self.myID) + ".txt"):
            os.system("rm fitness" + str(self.overallBot) + "_" + str(self.myID) + ".txt")
