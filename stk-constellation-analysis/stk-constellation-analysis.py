# --- STK CONSTELLATION ANALYSIS --------------------------------------------------------------------------------------------
# Authors: Alejandro Gonzalez Puerta (ALGP)
# Goal: To post-process the results of STK Basic and yield constellation performance metrics
# ---------------------------------------------------------------------------------------------------------------------------

# IMPORT STATEMENTS
import matplotlib, matplotlib.pyplot as plt, matplotlib.dates as mdates
from numpy import _sanity_check
from numpy.core import numeric
import pandas as pd
import datetime
import os, glob

# FILE OPERATIONS
scriptName = "stk-constellation-analysis.py"
currentPath = __file__.replace(scriptName,'')
folderToSearch = 'Brasilia'

# BOOLEAN ENABLES
enableFigurePrinting = False
enableFigureShowing = False

# COLUMN HEADERS
headerAccess = "Access"
headerStartTime  = "Start Time (UTCG)"
headerEndTime  = "Stop Time (UTCG)"
headerDuration = "Duration (sec)"

# DEFINE SATELLITE VISIBILITY FUNCTION
def isSatelliteInView(currentTime,satelliteDataFrame):
    # By default satellite is NOT in view
    satelliteIsInView = False

    for index in satelliteDataFrame.index:         
        # Identify current access bounds
        accessStart = satelliteDataFrame[headerStartTime][index].to_pydatetime()
        accessEnd = satelliteDataFrame[headerEndTime][index].to_pydatetime()

        if ( (currentTime > accessStart) and (currentTime < accessEnd) ):
            # Satellite is in view
            satelliteIsInView = True
            break

    return satelliteIsInView

# DEFINE CONTACT GAP ANALYSIS FUNCTION
def findContactGaps(listSatelliteAccesses):

    # Determine first satellite contact time
    listOfFirstContacts = []
    for satelliteAccess in listSatelliteAccesses:
        listOfFirstContacts.append(min(satelliteAccess[headerStartTime]).to_pydatetime())

    # Start analysis a few seconds after the first contact
    startTime = min(listOfFirstContacts) + datetime.timedelta(seconds=5.0)

    print("Analysis Start Time: " + str(startTime))
    print("-------------------------------------------------------")

    # Initialize loop variables
    revisitTime = 0.0
    revisitTimeList = []
    stepSize = 10
    numberOfDays = 30
    endTime = 86400*numberOfDays
    atLeastOneSatelliteInView = False

    # Iterate through the STK scenario time.
    for dt in range(0,endTime,stepSize):

        storeRevisitTime = revisitTime

        # Check if there is at least one satellite in view
        for satelliteAccess in listSatelliteAccesses:
            if isSatelliteInView(startTime,satelliteAccess):
                atLeastOneSatelliteInView = True
                break
            else:
                atLeastOneSatelliteInView = False

        if atLeastOneSatelliteInView:
            revisitTime = 0.0
        else:
            revisitTime = revisitTime + stepSize

        # Check if the revisit time has set to zero but on the previous instant it was non-zero
        if storeRevisitTime > revisitTime:
            revisitTimeList.append(storeRevisitTime)

        startTime = startTime + datetime.timedelta(seconds=stepSize)

        print(dt/endTime)

    return revisitTimeList

def findAccessesPerDay(listSatelliteAccesses,startDate,endDate):

    accessesPerDay = []

    while startDate < endDate:
        numberOfContactsToday = 0

        # Check if there is at least one satellite in view
        for satelliteAccess in listSatelliteAccesses:
            for index in satelliteAccess.index:
                if ((satelliteAccess[headerStartTime][index]-startDate).days) == 0:
                    numberOfContactsToday = numberOfContactsToday + 1

        startDate = startDate + datetime.timedelta(days=1)

        accessesPerDay.append(numberOfContactsToday)

    return accessesPerDay

def findAccessDurationStatistics(listSatelliteAcesses):
    listOfDataFrames = []
    for satelliteAccess in listSatelliteAccesses:
        listOfDataFrames.append(satelliteAccess)
    concatenatedFrames = pd.concat(listOfDataFrames)
    print(concatenatedFrames)


# ITERATE THROUGH FOLDER
listSatelliteAccesses = []

os.chdir(currentPath+folderToSearch)

for fileToSearch in glob.glob("*.csv"):

    # Get current dataframe
    df = pd.read_csv(fileToSearch , delimiter=',')

    # Remove miliseconds from datetime string
    df[headerStartTime] = df[headerStartTime].str[:-4]
    df[headerEndTime] = df[headerEndTime].str[:-4]

    # Convert time strings into datetime format
    df[headerStartTime] = df.apply(lambda x: datetime.datetime.strptime(x[headerStartTime], '%d %b %Y %H:%M:%S'),axis=1)
    df[headerEndTime] = df.apply(lambda x: datetime.datetime.strptime(x[headerEndTime], '%d %b %Y %H:%M:%S'),axis=1)

    # Append dataframe to search list
    listSatelliteAccesses.append(df)

findAccessDurationStatistics(listSatelliteAccesses)

# revisitTimeList = findContactGaps(listSatelliteAccesses)

startDate = datetime.datetime(year= 2022, month= 1,day=1,hour=0,minute=0,second=0)
endDate = datetime.datetime(year= 2022, month= 2,day=1,hour=0,minute=0,second=0)

accessesPerDay = findAccessesPerDay(listSatelliteAccesses,startDate,endDate)

print(" ")
print("Revisit time statistics for " + folderToSearch + ":")
print("-------------------------------------------------------")
print(revisitTimeList)
print(" ")
print("MIN: " + str(min(revisitTimeList)))
print("AVG: " + str(round(sum(revisitTimeList)/len(revisitTimeList),2)))
print("MAX: " + str(max(revisitTimeList)))
print(" ")

print(" ")
print("Daily access statistics for " + folderToSearch + ", total of " + str((endDate-startDate).days) + " days:")
print("-------------------------------------------------------")
print(accessesPerDay)
print(" ")
print("MIN: " + str(min(accessesPerDay)))
print("AVG: " + str(round(sum(accessesPerDay)/len(accessesPerDay),2)))
print("MAX: " + str(max(accessesPerDay)))
print(" ")
