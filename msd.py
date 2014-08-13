import glob
import os
import math
import numpy as np
import matplotlib.pyplot as plt


#### Instructions:
####Type in name of folder containing tracks; adjust time stamp (default is 0.0168 seconds); adjust time interval range
####If you receive error that list index is out of range for creating xdata list, one of the tracks in the folder may be shorter than the specified number of frames 


def msd():
  # Open a user input file
  with open(file) as myfile:
    raw_data = myfile.read().replace('\n', ' ').replace('\t', ' ')
  
  myfile.close()
  
  # Append each number to a list called 'data'; data = ['x1', 'y1', 'x2', 'y2', ..., 'xn', 'yn']
  rawdata = []
  rawdata = raw_data.split()
  # Convert elements from string to float
  rawdata = [float(i) for i in rawdata]
  #print (data, file = outFile)
  
  # Create list of x-positions only
  xdata = []
  for i in range (0, 1800, 2): #### Limit range to time intervals of ~1 to ~10 seconds; 60th x-position is 121st element in list, 600th x-position is 1201st element in list
    xdata.append(rawdata[i])
  
  # Create list of y-positions only
  #ydata = []
  #for i in range (1, len(rawdata), 2):
  #   ydata.append(rawdata[i])
  
  
  # Create a list of (list of squared differences); [ [squared_differences for interval=1*timestamp], [squared_differences for interval=2*timestamp], ..., [squared_differences for interval = len(dataset)*timestamp]]
  squared_differences = []
  for interval in range (1, len(xdata), 1):
    squared_differences_for_intervalj = []
    for j in range (0, len(xdata)-interval, 1):
      squared_differences_for_intervalj.append((xdata[j] - xdata[j+interval])**2)
    squared_differences.append(squared_differences_for_intervalj)
  
  
  
  global msd_list
  global time_list
  
  # Create list of average msds; avg_msd_list = [avg_msd for interval=1, avg_msd for interval=2, ..., avg_msd for interval=len(dataset)]
  avg_msd_list = []
  for row in squared_differences:
    avg_msd_value = 0
    for item in row:
      avg_msd_value += item
    avg_msd = avg_msd_value/len(row)
    avg_msd_list.append(avg_msd)
  averages.append(avg_msd_list) 
  
  #outFile = open('output.txt' , 'a')
  #outFile.write(str(avg_msd_list))
  #outFile.close()
  
  # Output aggregate msd values to aggregatemsd.txt. Contains average msd across all the tracks at each time interval
  aggregateMsdFile = open('aggregatemsd.txt', 'a')
  aggregateMsdFile.write(str(avg_msd_list))
  aggregateMsdFile.close()
  

  # Create list of standard deviations; std_err = [std err for interval=1, std err for interval=2, ..., std err for interval=len(dataset)]
  std_dev = []
  deviation = 0
  for i in range (0, len(avg_msd_list)):
    row = squared_differences[i]
    for item in row:
      deviation += (item - avg_msd_list[i])**2
    deviation = math.sqrt(deviation/len(row))
    std_dev.append(deviation)
  


 

averages = []  #### List containing one list for each track
for file in glob.iglob(os.path.join('2.0selected', '*.txt')):      ###### Choose folder containing tracks########
  msd()
#msdAcrossTracks = open('msdacrosstracks.txt', 'w')
#msdAcrossTracks.write(str(averages))

####Find the aggregate MSD over all the (good) tracks

Aggregate = []
limit = len(averages[0])
#### Transpose the list; Aggregate = [ [list of average msds at t=1 for all tracks], [list of average msds at t=2 f or all tracks], ...]
for item in range (0, limit, 1):  #### 600 - 60 = 540 data points
  Aggregate.append([row[item] for row in averages])



#### Average the msd for each interval over all tracks
AggregateMSD = [] #### This is the list of aggregate msds, averaged over all the tracks;
for row in Aggregate:
  AggregateMSDvalue = np.mean(row)
  AggregateMSD.append(AggregateMSDvalue)
#msdAcrossTracks.write(str(AggregateMSD))
#msdAcrossTracks.close

#### Calculate standard deviations for aggregate msds

# Create list of standard deviations; std_err = [std err for interval=1, std err for interval=2, ..., std err for interval=len(dataset)]
  aggStdDev = []
  deviation = 0
  for i in range (0, len(AggregateMSD)):
    row = Aggregate[i]
    for item in row:
      deviation += (item - AggregateMSD[i])**2
    deviation = math.sqrt(deviation/len(row))
    aggStdDev.append(deviation)
  
# Now I need to put AggregateMSD in one column and aggStdDev in another column. Or I can just plot them in python. Time stamp is still the same: 0.0168

# Create log-log plot of Aggregate MSD versus time; include errors if possible

  msd = [(10**(-18))*item for item in AggregateMSD]
  
  xerr = [0]*len(msd)
  
  yerr = [(10**(-18))*item for item in aggStdDev]
  
  #time_interval = input('What is the time interval between frames (in seconds)?: ')
  time_interval = .0168 
  time = 0
  time_list = []
  for i in range (0, len(msd), 1):
    time += time_interval
    time_list.append(time)

fig, ax = plt.subplots()
#ax.errorbar(time_list, msd)
ax.set_xscale('log')
ax.set_yscale('log')
plt.errorbar(time_list, msd)
plt.xlabel ('Time (seconds)')
plt.ylabel('MSD (meters $^2$)')
plt.title('2.0 Spacing: log-log Aggregate MSD versus Time')

plt.show()

#### To output aggregate msd and std dev in columns:
print('Current folder path: ', file)
fileName = raw_input('Enter name of file to write data to: ')
AggMSD = open(fileName, 'w')

columns = []
columns.append(time_list)
columns.append(msd)
columns.append(yerr)
for x in zip(*columns):
  AggMSD.write('{0}\t{1}\t{2}\n'.format(*x))



