import os
import sys 

import traci  # noqa
from sumolib import checkBinary  # noqa

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools') 
    sys.path.append(tools)
else:   
    sys.exit("please declare environment variable 'SUMO_HOME'") 

def runSumo(gui = True):
    print("Static")
    #createRoute()
    
    if gui:
        sumoBinary = checkBinary('sumo-gui')
    else:
        sumoBinary = checkBinary('sumo')
    sumoCmd = [sumoBinary, "-c", "conf\mine.sumocfg", "--no-step-log"]

    traci.start(sumoCmd) 
    step = 0

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        

        time = traci.simulation.getTime()
        #if time == 3638:
            #input()

        step += 1

    #print("Time: {}".format(traci.simulation.getTime()))

    time = traci.simulation.getTime()
    traci.close()
    return time

if __name__ == "__main__":
    
    print("Time: ", runSumo(True))
