import os
import ga
import numpy
import Adaptive
import Static
import csv, time

results = [] 



def createRoute(period):
    tee = '''randomtrips.py -n conf\mine.net.xml -a conf\mine.add1.xml -o conf\mine.randout.pRun.xml -b 0 -e 3600 --seed 42 --period {} --binomial 3 --validate'''.format(period)
    ter = '''tesd {}'''.format(89)
    os.system(tee)

def WriteDictToCSV(csv_file,csv_columns,dict_data, append=True):
    if append:
        writeType = 'a'
    else:
        writeType = 'w'
    try:
        with open(csv_file, writeType) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError:
            print("I/O error")    
    return  

def csvwrite(csv_file, data, append=True):
    if append:
        writeType = 'a'
    else:
        writeType = 'w'
    with open(csv_file, writeType) as f:
        writer = csv.writer(f)
        writer.writerow(data)


if __name__ == "__main__":
    currentPath = os.getcwd()
    csv_file = currentPath + "/data/results.csv"
    csv_columns = ['period','Static_Time','Adaptive_Time']
    csvwrite(csv_file ,csv_columns, False)
    teResult = []

    #for i in range(1, 10, 2)
    count = 0
    for i in range(1, 40):
        result = {}
        period = i / 10

        createRoute(period) #defines traffic
        result["period"] = period
        
        result["Static_Time"] = Static.runSumo(False)
        result["Adaptive_Time"] = Adaptive.runSumo(False) 

        print(result)
        teResult.append(result)

        csvwrite(csv_file ,result.values())

        # results.append(result)
        
        print(count)
        
        count += 1
        
    
        
    timestr = time.strftime("%Y%m%d-%H%M%S")

    csv_file = currentPath + "/data/Results{}.csv".format( timestr )
    #csv_file = currentPath + "/data/results.csv"
    csvwrite(csv_file ,csv_columns, False)
    for result in teResult:
        csvwrite(csv_file, list(result.values()))

    #WriteDictToCSV(csv_file ,csv_columns,results, False)
