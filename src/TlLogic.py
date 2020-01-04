import traci

class TlLogic: 
    

    def __init__(self):
        self.phaseTimeList = [42, 3 , 42, 3]
        self.defaultPhaseTimeList = [42, 3 , 42, 3]
    
    def controlPhase(self, xk, phaseTimeList = [42, 3 , 42, 3], shortPhaseTime = 3, cycleLengthLong = 80, cycleLengthShort = 30, xkMin = 30, minDur = 6):
    
        nsLength = xk[0] #queue length in the north edge and the south edge
        ewLength = xk[1] ##queue length in the north edge and the south edge

        allLength = nsLength + ewLength #sum them together


        if allLength <= xkMin:
            cycleLength = cycleLengthShort
        else:
            cycleLength = cycleLengthLong


        if allLength == 0:
            phaseTimeList = [minDur, 3, minDur, 3]
        elif nsLength == 0:
            phaseTimeList[0] = minDur
            phaseTimeList[2] = cycleLength - phaseTimeList[0] - 2 * shortPhaseTime
        elif ewLength == 0:
            phaseTimeList[2] = minDur
            phaseTimeList[0] = cycleLength - phaseTimeList[2] - 2 * shortPhaseTime
        else:
            # print("both have values")
            ratio = nsLength / allLength * ( cycleLength - 2 * shortPhaseTime )
            
            # print("ratio: ", ratio)
            
            if ratio >= 6:
                phaseTimeList[2] = max(( cycleLength - 2 * shortPhaseTime ) - int(ratio), minDur)
                phaseTimeList[0] = ( cycleLength - 2 * shortPhaseTime ) - phaseTimeList[2]
                
            else:
                phaseTimeList[0] = minDur
                phaseTimeList[2] = ( cycleLength - 2 * shortPhaseTime ) - phaseTimeList[0]
                
                
        # print("xk: ", xk, "allLength: ", allLength)
        # print("phasetimelist: ", phaseTimeList)
        phases = []
        
        phases.append(traci.trafficlights.Phase(phaseTimeList[0], "GGGGgrrrrrGGGGgrrrrr"))
        phases.append(traci.trafficlights.Phase(phaseTimeList[1], "yyyyyrrrrryyyyyrrrrr"))
        phases.append(traci.trafficlights.Phase(phaseTimeList[2], "rrrrrGGGGgrrrrrGGGGg"))
        phases.append(traci.trafficlights.Phase(phaseTimeList[3], "rrrrryyyyyrrrrryyyyy"))

        logic = traci.trafficlights.Logic("new-program", 0, 0, phases )
        
        self.phaseTimeList = phaseTimeList
        

        return logic
    
    def getPhaseTimeList(self):
        return self.phaseTimeList
