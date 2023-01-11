import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c
import pickle
#import emptyWrapper as EMPTY_WRAPPER
#--------------------------------------------





class SOLUTION:
    def __init__(self, nextAvailableID, spaceOrC, emptyBotIndex, emptySwarmIndex, populationID):
        self.myID = nextAvailableID
        self.spaceOrC = spaceOrC
        self.emptyBotIndex = int(emptyBotIndex)
        self.emptySwarmIndex = int(emptySwarmIndex)
        self.populationID = populationID


        # now that we've incorporated spaceOrC here, we can finally make a conditional statement that executes if self.spaceOrC == '-c'
        
        # Generate a random matrix
        self.weights = np.random.rand(c.numSensorNeurons+1,c.numMotorNeurons)   
        #self.weights[0:9] = 1
        self.weights = self.weights * 2 - 1    
        for i in range(8):
            self.weights[9][i] = random.uniform(.5,1.5)


        # initialize matrixOfWeights
        emptyMatrixOfWeights = np.empty(shape=(c.numberOfSwarms,10,c.populationSize), dtype='object')

        self.matrixOfWeights = emptyMatrixOfWeights #[zeroList*c.numberOfSwarms*10]#np.zeros((c.numberOfSwarms,c.populationSize)) # numberOfSwarms x 5 matrix is initially what we have it set to.



    # if -c is used, open the pickledFile, and load all the matrices. Choose the appropriate matrix to continue evolving.
        if self.spaceOrC == 'continue':
            with open('weightsAndLegs.txt', 'rb') as pickledFile:
                #Load all matrices in the pickledFile
                
                loadedMatrixOfWeights = pickle.load(pickledFile)

                # set the self.weights to those of the appropriate robot to use the previous evolution end matrix as current starting matrix. After evolving it further, replace it in the pickledFile at the appropriate index.
                self.weights == loadedMatrixOfWeights[self.emptySwarmIndex][self.emptyBotIndex][int(self.myID)-(5*self.emptySwarmIndex)] # here, pass swarmIndex through in order to use the expression for appropriateRobot


    # if -c is not used, load any previous matrices, generate a new one, then add it to the previous matrices. This is a correct interpretation of what this code block does.
        else:
            # if pickledFile doesn't exist, initialize empty matrixOfWeights
                        
            # initialize matrixOfWeights
            emptyMatrixOfWeights = np.empty(shape=(c.numberOfSwarms,10,c.populationSize), dtype='object')
            #self.matrixOfWeights = emptyMatrixOfWeights



            # if pickledFile exists, open it and load matrixOfWeights
            if os.path.exists('weightsAndLegs.txt'):
                with open("weightsAndLegs.txt", "rb") as pickledFile:
                    # Load matrixOfWeights from pickledFile
                    matrixOfWeights = pickle.load(pickledFile)
                pickledFile.close()                             # Required to avoid EOFError: Ran out of input

            # If pickledFile doesn't exist, initialize matrixOfWeights 
            else:                
                emptyMatrixOfWeights = np.empty(shape=(c.numberOfSwarms,10,c.populationSize), dtype='object')

                matrixOfWeights = emptyMatrixOfWeights



            # Add a new matrix to matrixOfWeights
            weights = np.random.rand(c.numSensorNeurons+1,c.numMotorNeurons)   
        #self.weights[0:9] = 1
            weights = weights * 2 - 1    
            for i in range(8):
                weights[9][i] = random.uniform(.5,1.5)
            self.weights = weights   

            # add the new matrix to the correct position in the matrixOfWeights
            matrixOfWeights[self.emptySwarmIndex][self.emptyBotIndex][self.populationID] = self.weights


            # Overwrite pickledFile with new matrixOfWeights after we add a new random matrix. 
            with open("weightsAndLegs.txt", "wb") as pickledFile:       
                pickle.dump(matrixOfWeights, pickledFile) 
                pickledFile.close()                               # Required to avoid EOFError: Ran out of input




    def Evaluate(self,directOrGUI):
        pass


    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        #pyrosim.Send_Cube(name="Box", pos=[-3,3,0.5] , size=[1,1,1]) 
        pyrosim.End()

    def Generate_Body(self, xi,yi): 
        # tempfile1 = open('WeightsTemp.txt','a')
        # tempfile1.write(str(self.weights))
        # tempfile1.write('\n')
        # tempfile1.write('\n')
        # tempfile1.close  

        # tempfile2 = open('LegSizesTemp.txt','a')
        # tempfile2.write(str(self.weights[9]))
        # tempfile2.write('\n')
        # tempfile2.write('\n')
        # tempfile2.close   
        pyrosim.Start_URDF("bodyFiles/body"+str(xi)+str(yi)+str(self.myID)+".urdf") # LOOK here, we create the body with position and ID
        
        #Torso
        pyrosim.Send_Cube(name="Torso", pos=[0+xi,0+yi,max(self.weights[9])] , size=[1,1,1])
            
    # Upper Extremities
        #Back Leg
        pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [0+xi,-0.5+yi,max(self.weights[9])], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0,-(self.weights[9][0]/2),0] , size=[0.2,self.weights[9][0],0.2])

        #Front Leg
        pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [0+xi,0.5+yi,max(self.weights[9])], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0,(self.weights[9][1]/2),0] , size=[0.2,self.weights[9][1],0.2])

            #Left Leg
        pyrosim.Send_Joint( name = "Torso_LeftLeg" , parent= "Torso" , child = "LeftLeg" , type = "revolute", position = [-0.5+xi,0+yi,max(self.weights[9])], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[-(self.weights[9][2]/2),0,0] , size=[self.weights[9][2],0.2,0.2])        

            #Right Leg
        pyrosim.Send_Joint( name = "Torso_RightLeg" , parent= "Torso" , child = "RightLeg" , type = "revolute", position = [0.5+xi,0+yi,max(self.weights[9])], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[(self.weights[9][3]/2),0,0] , size=[self.weights[9][3],0.2,0.2])   

    # Lower Extremities
        #Back Lower Leg
        pyrosim.Send_Joint( name = "BackLeg_BackLowerLeg" , parent= "BackLeg", child = "BackLowerLeg", type = "revolute", position = [0, -self.weights[9][0], 0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0, 0, -(self.weights[9][4]/2)] , size=[0.2, 0.2, self.weights[9][4]])
            
        #Front Lower Leg
        pyrosim.Send_Joint( name = "FrontLeg_FrontLowerLeg" , parent= "FrontLeg", child = "FrontLowerLeg", type = "revolute", position = [0, self.weights[9][1], 0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0, 0, -(self.weights[9][5]/2)] , size=[0.2, 0.2, self.weights[9][5]])

        #Left Lower Leg
        pyrosim.Send_Joint( name = "LeftLeg_LeftLowerLeg" , parent= "LeftLeg", child = "LeftLowerLeg", type = "revolute", position = [-self.weights[9][2], 0, 0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLowerLeg", pos=[0, 0, -(self.weights[9][6]/2)] , size=[0.2, 0.2, self.weights[9][6]])

        #Right Lower Leg
        pyrosim.Send_Joint( name = "RightLeg_RightLowerLeg", parent= "RightLeg", child = "RightLowerLeg", type = "revolute", position = [self.weights[9][3], 0, 0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0, 0, -(self.weights[9][7]/2)] , size=[0.2, 0.2, self.weights[9][7]])

        pyrosim.End()
        #exit() # uncommenting this allows you to see effects of code on body.urdf

    def Generate_Brain(self):  #ADDED TO ROBOT_BRAIN

        pyrosim.Start_NeuralNetwork("brainFiles/brain" + str(self.myID) + ".nndf") #changed from brain.nndf


# Upper Extremity Sensor Neurons
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "LeftLeg")
        pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "RightLeg")

# Lower Extremity Sensor Neurons
        pyrosim.Send_Sensor_Neuron(name = 5 , linkName = "BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 6 , linkName = "FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 7 , linkName = "LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name = 8 , linkName = "RightLowerLeg")

# Upper Extremity Motor Neurons
        pyrosim.Send_Motor_Neuron( name = 9, jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 10, jointName = "Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron( name = 11, jointName = "Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron( name = 12, jointName = "Torso_RightLeg")

# Lower Extremity Motor Neurons
        pyrosim.Send_Motor_Neuron( name = 13, jointName = "BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 14, jointName = "FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 15, jointName = "LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron( name = 16, jointName = "RightLeg_RightLowerLeg")
   
        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse( sourceNeuronName = currentRow , targetNeuronName = currentColumn+c.numSensorNeurons , weight = self.weights[currentRow][currentColumn] ) #step 7 randomsearch

        pyrosim.End()

    def Mutate(self): #ADDED TO ROBOT_BRAIN
        randomRow = random.randint(0,c.numSensorNeurons - 1) #(0,2) represents 0th, 1st, and 2nd rows
        randomColumn = random.randint(0,c.numMotorNeurons - 1) #(0,1) represents 0th and 1st column
        self.weights[randomRow, randomColumn] = random.random() * 2 - 1

        tempfile = open('WeightsTemp.txt','a')
        tempfile.write(str(self.weights))
        tempfile.write('\n')
        tempfile.write('\n')
        tempfile.close  

    def Mutate_Body(self): #ADDED TO ROBOT_BRAIN
        randomLegPart = random.randint(0,7)
        self.weights[9][randomLegPart] = random.uniform(0.5,1.5)

        tempfile = open('LegSizesTemp.txt','a')
        tempfile.write(str(self.weights[9]))
        tempfile.write('\n')
        tempfile.write('\n')
        tempfile.close   


        # legPartList = ['l1','l2','l3','l4','l5','l6','l7','l8']
        # self.randomIndex2 = random.choice([0,1,2,3,4,5,6,7])
        # if legPartList[self.randomIndex2] == 'l1':
        #     self.weights[9][0] =  np.random.uniform(0,2)
        # if legPartList[self.randomIndex2] == 'l2':
        #     self.weights[9][1] =  np.random.uniform(0,2)
        # if legPartList[self.randomIndex2] == 'l3':
        #     self.weights[9][2] =  np.random.uniform(0,2)
        # if legPartList[self.randomIndex2] == 'l4':
        #     self.weights[9][3] =  np.random.uniform(0,2)
        # if legPartList[self.randomIndex2] == 'l5':
        #     self.weights[9][4] =  np.random.uniform(0,2)
        # if legPartList[self.randomIndex2] == 'l6':
        #     self.weights[9][5] =  np.random.uniform(0,2)
        # if legPartList[self.randomIndex2] == 'l7':
        #     self.weights[9][6] =  np.random.uniform(0,2)
        # if legPartList[self.randomIndex2] == 'l8':
        #     self.weights[9][7] =  np.random.uniform(0,2)

        

    def Set_ID(self): #ADDED TO ROBOT_BRAIN
        self.myID

    def Start_Simulation(self, directOrGUI, botIndex):
        self.Create_World()
        self.Generate_Brain() #ADDED TO ROBOT_BRAIN

        positions = [
            (0,-18),
            (0,-14),
            (0,-10),
            (0,-6),
            (0,-2),
            (0,2),
            (0,6),
            (0,10),
            (0,14),
            (0,18)
        ]

        self.Generate_Body(*positions[botIndex]) #... I just put this in 11-22-2022... will putting this here allow me to evolve the body? 
        os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID)+ ' ' + str(botIndex) + ' '+ str(self.spaceOrC) + ' ' + str(self.emptySwarmIndex) +" &") # changed from "DIRECT" to directOrGUI... added " &"

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("fitness"+ str(self.myID) + ".txt"):
            time.sleep(0.01)

        fitnessFile = open("fitness"+ str(self.myID) + ".txt","r")
        time.sleep(0.1)
        lines = fitnessFile.read()
        time.sleep(0.1)
        self.fitness = float(lines)
        #self.fitness = float(fitnessFile.read()) #Used fitnessFile, they normally use f
        #print("fitness"+str(self.myID)+"=", self.fitness) # commented out for step 75 parallelHC
        fitnessFile.close()
        os.system("rm fitness"+ str(self.myID) + ".txt")
        while os.path.exists("fitness"+str(self.myID)+".txt"):
            os.system("rm fitness"+ str(self.myID) + ".txt")
       
        # allIDFile = open("allIDs.txt", "a") 
        # allIDFile.write(str(self.myID))  
        # allIDFile.write('\n')                              #Write delimiter after brain ID
        # allIDFile.close