from solution import SOLUTION
import constants as c
import copy
import os
#------------------------------------
class PARALLEL_HILL_CLIMBER:
    def __init__(self):

        os.system("rm brain*.nndf") # step 82 parallelHC
        os.system("rm fitness*.txt") # step 83 parallelHC
        self.parents = {}
        self.children = {}
        self.nextAvailableID = 0
        #self.child = SOLUTION() #might need to pass in self.nextAvailableID to SOLUTION()
        for i in range(c.populationSize): # why isn't this len(self.nextAvailableID)?
            self.parents[i] = SOLUTION(self.nextAvailableID) 
            self.nextAvailableID = self.nextAvailableID + 1

    def Evolve(self): 
        for i in range(len(self.parents)):
            self.parents[i].Start_Simulation("DIRECT") #step 69 parallelHC -- GUI -> DIRECT
        for i in range(len(self.parents)):            #step 72 parallelHC... uncomment to activate Parallelism, comment to deactivate Parallelism
            self.parents[i].Wait_For_Simulation_To_End()
        for currentGeneration in range(c.numberOfGenerations): # to get just the first gen, set c.numberOfGenerations = 1
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        #self.Mutate()
        #self.child.Evaluate("DIRECT")
        #self.Print()
        #self.Select()

    def Spawn(self):
        self.children = {}
        #self.child = copy.deepcopy(self.parent)
        for i in range(len(self.parents)):
            self.children[i].Set_ID()
            self.children[i] = copy.deepcopy(self.parents[i])
            self.nextAvailableID = self.nextAvailableID + 1

 

    def Mutate(self):
        self.child.Mutate()

    def Print(self):
        print('parent fitness =',self.parent.fitness, 'child fitness=',self.child.fitness)

    def Select(self):
        if self.parent.fitness > self.child.fitness:
            self.parent = self.child
        
    def Show_Best(self):
        pass
        #self.parent.Evaluate("GUI") #why isn't this showing?