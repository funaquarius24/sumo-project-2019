import os
import sys
import utils
import numpy as np

import traci  # noqa
import traci.domain
from sumolib import checkBinary  # noqa

from TlLogic import TlLogic

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:   
    sys.exit("please declare environment variable 'SUMO_HOME'")
    
nsDetectors = ['N0_In_0_9', 'N0_In_1_10', 'N0_In_2_11', 'S0_In_0_5', 'S0_In_1_4', 'S0_In_2_3']
ewDetectors = ['E0_In_0_8', 'E0_In_1_7', 'E0_In_2_6','W0_In_0_5', 'W0_In_1_4', 'W0_In_2_3']

nsDetectorsDict = dict.fromkeys(nsDetectors, 0)
ewDetectorsDict = dict.fromkeys(ewDetectors, 0)

detectorsDictList = [nsDetectorsDict, ewDetectorsDict]
detectorsDict = {"nsDetectors": 0, "ewDetectors": 0}
length = np.array([0, 0])

tl = TlLogic()

phaseTimeList = [42, 3 , 42, 3]
xk = xkInit = np.array([0, 0, 0, 0])  

params = {"ready": False, "steps": 0}


def handleSwitch(steps, ready):
    phase = traci.trafficlight.getPhase("gneJ0")
    cycleLength = sum(tl.getPhaseTimeList())

    if steps == cycleLength:
        logic = tl.controlPhase(getLength())
        phaseTimeList = tl.getPhaseTimeList()
        params["ready"] = True

    if ready:
        switch(logic)
        params["ready"]  = False

    if steps % 5 == 0:
        phase = traci.trafficlight.getPhase("gneJ0")
        getLength()

        # print("phase: {} len0: {} len1: {} steps {}".format(phase, length[0], length[1], steps))
        if not all(v > 0 for v in length):
            
            if length[0] > 0 and phase > 1 and length[1] == 0:
                # print("1 worked")
                traci.trafficlight.setPhase("gneJ0", 0)
            elif length[0] == 0 and phase < 2 and length[1] > 0:
                # print("2 worked")
                traci.trafficlight.setPhase("gneJ0", 2)

def switch(logic):
    
    # phase = traci.trafficlight.getPhase("gneJ0")
    # traci.trafficlight.setPhaseDuration("gneJ0", phaseTimeList[phase] )
    traci.trafficlight.setCompleteRedYellowGreenDefinition("gneJ0", logic) 
    return
        
def getLength():
    for elem in detectorsDictList:
        for key, val in elem.items():
            elem[key] = traci.lanearea.getLastStepVehicleNumber(key)

    detectorsDict['nsDetectors'] = sum(nsDetectorsDict.values())
    detectorsDict['ewDetectors'] = sum(ewDetectorsDict.values())

    length[0] = detectorsDict['nsDetectors']
    length[1] = detectorsDict['ewDetectors']

    return length    
        
def runSumo(gui = True):

    switchTime = 0
    switched = False
    
    steps = 0
    ready = False
    cycleLength = sum(phaseTimeList)
    
    if gui:
        sumoBinary = checkBinary('sumo-gui')
    else:
        sumoBinary = checkBinary('sumo')
    sumoCmd = [sumoBinary, "-c", "conf\mine.sumocfg", "--no-step-log"]

    traci.start(sumoCmd) 
    numCycles = 10
    

    step = 0
    
    while traci.simulation.getMinExpectedNumber() > 0:
        if params["steps"] > sum(tl.getPhaseTimeList()):
            params["steps"] = 0
        
        traci.simulationStep()

        params["steps"] += 1
        handleSwitch(params["steps"], ready)

        # if traci.simulation.getTime() == 2650:
        #     input()


    time = traci.simulation.getTime()
    traci.close()
    return time

if __name__ == "__main__":
    print("Time: ", runSumo())