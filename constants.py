import numpy as np

# Simulation Parameters
gravityConstant = -9.8 * 2.5 
loopLength = 1000 # was evolved for 5000
sleepRate = 1/5000 

# Robot Parameters
amplitude = np.pi /4
phaseOffset = np.pi/2
frequency = 10
legMaxForce = 120 
motorJointRange = 0.8 
numSensorNeurons = 4 
numMotorNeurons = 8
legLengthRange = (0.5, 1.5) # only used for case3

# Evolution Parameters
numberOfGenerations = 2
populationSize = 3

# collection parameters
swarmType = 'case1'  # Choose swarmType: case1, case2, case3
numberOfSwarms = 2
botsPerSwarm = 10
continueEvolution = False  # if continueEvolution = True, add more generations (assuming same number of parents)
# continueCollection = False # currently not implemented completely. Might appear in codebase occasionally.

# playback parameters
botPositions = [
    (0, -18),        
    (0, -14),
    (0, -10),
    (0, -6),
    (0, -2),
    (0, 2),
    (0, 6),
    (0, 10),
    (0, 14),
    (0, 18)
]
playbackView = 'GUI'

# Assertions
assert len(botPositions) == botsPerSwarm    # kind of unecessary


