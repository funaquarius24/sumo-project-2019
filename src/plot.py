import numpy as np
import math
import matplotlib.pyplot as plt #For plotting graphs
import pandas as pd 
from pylab import figure, axes, pie, title, show

#t = linspace(0, 2*math.pi, 400)
data = pd.read_csv("data/results.csv")
print(type(data))

print(data)
data["period"] = 1 / data["period"]
print(data.mean(axis = 0))

# For all result data
plt.plot(data["period"], data["Adaptive_Time"], 'r', label="Adaptive") # plotting Period, Adaptive
plt.plot(data["period"], data["Static_Time"], 'b', label="Static") # plotting Period, Static

plt.title('Plot: Time to Arrive with Different Vehicle Injection Periods')

plt.legend() # Allows the labels to be added into the graph
plt.savefig('testAllLine.png') #Saving the plot 
plt.show()

# For saturated Data For Line
saturationData = data[4:10] #Cuts data from 0-10
plt.plot(saturationData["period"], saturationData["Adaptive_Time"], 'r', label="Adaptive") # plotting Period, Adaptive 
plt.plot(saturationData["period"], saturationData["Static_Time"], 'b', label="Static") # plotting Period, Static

plt.title('Plot: Time to Arrive with Different Vehicle Injection Periods For Saturated Flow')

plt.legend()
plt.savefig('testSaturatedLine.png')
plt.show()

unsaturatedData = data[10:] ##Cuts data from 10-end
plt.plot(unsaturatedData["period"], unsaturatedData["Adaptive_Time"], 'r', label="Adaptive") 
plt.plot(unsaturatedData["period"], unsaturatedData["Static_Time"], 'b', label="Static") 

plt.title('Plot: Time to Arrive with Different Vehicle Injection Periods For Unsaturated Flow')

plt.legend()
plt.savefig('testUnsaturatedLine.png')
plt.show()

#For Saturated
saturationData = data[4:10]
n_groups = 6 #number of bar groups to be plotted
index = np.arange(n_groups) #creates a list from 0-10 10 exclusive
bar_width = 0.35
opacity = 0.8
rects1 = plt.bar(index, saturationData["Static_Time"], bar_width, alpha=opacity, color='b', label='Static_Time')
rects2 = plt.bar(index + bar_width, saturationData["Adaptive_Time"], bar_width, alpha=opacity, color='r', label='Adaptive_Time')

plt.xlabel('Period')
plt.ylabel('Time')
plt.title('Plot: Time to Arrive with Different Vehicle Injection Periods For Saturated Flows')
plt.xticks(index + bar_width, saturationData["period"])

# yTicks = np.array(range(6000, 12000, 500))
# plt.yticks(yTicks)
plt.legend()
plt.savefig('testSaturatedBar.png')

plt.tight_layout()
plt.show()

# For Unsaturated
unsaturatedData = data[10:]
n_groups = len(unsaturatedData)
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8
rects1 = plt.bar(index, unsaturatedData["Static_Time"], bar_width, alpha=opacity, color='b', label='Static_Time')
rects2 = plt.bar(index + bar_width, unsaturatedData["Adaptive_Time"], bar_width, alpha=opacity, color='r', label='Adaptive_Time')

plt.xlabel('Period')
plt.ylabel('Time')
plt.title('Plot: Time to Arrive with Different Vehicle Injection Periods For Unsaturated Flows')
plt.xticks(index + bar_width, unsaturatedData["period"])

plt.legend()
plt.tight_layout()
plt.savefig('testUnsaturatedBar.png')
plt.show()

sumAdaptive = sum(data["Adaptive_Time"])
sumStatic = sum(data["Static_Time"])
